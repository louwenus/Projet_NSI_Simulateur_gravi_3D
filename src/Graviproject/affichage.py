#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE
# encoding = utf8

import sys
import os
from sys import stderr
from math import cos, pi, sin
from functools import partial
# import des différentes librairies non-standard avec debug en cas de librairie manquante
try:
    from PySide6.QtCore import *
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from random import *

    Signal()
except ModuleNotFoundError as e:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails", file=stderr)
    raise e

from . import settings
from . import gravilib
from .affichage3D import Renderer3D 
from . import langue

if settings.get("logging") >= 3:
    from time import time #importation de la libraire time

ticktime=1
app: QApplication = QApplication(sys.argv)

warnwin = QScrollArea()
warnwintxt = QLabel(warnwin)
warnwin.setWidget(warnwintxt)
warnwin.setWindowTitle("WARNINGS:")

def warn(warning:str)->None:
    if settings.get("affichage.warn"):
        warnwintxt.setText(warnwintxt.text() + "\n\n" + langue.get("warnings."+warning))
        warnwin.show()
    else:
        if settings.get("logging")>=2:
            print(langue.get("warnings."+warning))

if not gravilib.cppgravilib.is_128_bit:
    warn("64-bits")

class Main_window(QWidget):
    """Cette class définit la fenètre principale du programme, à partir d'un QWidget."""
    changeLangSignal : Signal = Signal()
    
    def __init__(self) -> None:
        super().__init__()
        self.setFocusPolicy(Qt.ClickFocus)
        self.affichage_controles: bool = True

        self.setWindowTitle(langue.get("title"))
        self.changeLangSignal.connect(langue.lazyEval(self.setWindowTitle,"title"))

        self.layout: QLayout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.addSpacing(10)

        # Création des actions utiliseables dans les menus
        self.attach_detachAction: QAction = QAction(langue.get("menu.display.detach"), self)
        self.attach_detachAction.triggered.connect(self.attach_detach_controles)
        self.changeLangSignal.connect(self.attach_detach_texte)
        
        self.langAction: list(QAction) = []
        for speak in (("Français","fr"),("English","en"),("Italiano","it")):
            self.langAction.append(QAction(speak[0], self))
            self.langAction[-1].triggered.connect(partial(self.change_lang,speak[1]))
        
        self.themeAction: list(QAction) = []
        for theme in ("light","dark"):
            self.themeAction.append(QAction(langue.get("menu.settings.theme."+theme), self))
            self.changeLangSignal.connect(langue.lazyEval(self.themeAction[-1].setText,"menu.settings.theme."+theme))
            #self.themeAction[-1].triggered.connect()

        #TODO : ajout de l'action pour le thème 

        self.licenseAction: QAction = QAction(langue.get("menu.help.license"), self)
        self.changeLangSignal.connect(langue.lazyEval(self.licenseAction.setText,"menu.help.license"))
        self.licenseAction.triggered.connect(self.affich_licence)

        # Création des menus
        self.menuBar: QWidget = QMenuBar(self)
        self.menuBar.setFixedWidth(self.size().width())

        self.affichageMenu: QMenu = QMenu(langue.get("menu.display.title"), self.menuBar)
        self.changeLangSignal.connect(langue.lazyEval(self.affichageMenu.setTitle,"menu.display.title"))
        self.menuBar.addMenu(self.affichageMenu)
        self.affichageMenu.addAction(self.attach_detachAction)
        
        self.configMenu : QMenu = QMenu(langue.get("menu.settings.title"), self.menuBar)
        self.changeLangSignal.connect(langue.lazyEval(self.configMenu.setTitle,"menu.settings.title"))
        self.menuBar.addMenu(self.configMenu)
        self.langMenu : QMenu = QMenu(langue.get("menu.settings.speak"), self.configMenu)
        self.changeLangSignal.connect(langue.lazyEval(self.langMenu.setTitle,"menu.settings.speak"))
        self.configMenu.addMenu(self.langMenu)
        self.langMenu.addActions(self.langAction)
        self.themeMenu : QMenu = QMenu(langue.get("menu.settings.theme.title"), self.configMenu)
        self.changeLangSignal.connect(langue.lazyEval(self.themeMenu.setTitle,"menu.settings.theme.title"))
        self.configMenu.addMenu(self.themeMenu)
        self.themeMenu.addActions(self.themeAction)

        self.helpMenu: QMenu = QMenu(langue.get("menu.help.title"), self.menuBar)
        self.changeLangSignal.connect(langue.lazyEval(self.helpMenu.setTitle,"menu.help.title"))
        self.menuBar.addMenu(self.helpMenu)
        self.helpMenu.addAction(self.licenseAction)

        # Fenètre détacheable de controle
        self.affichage_controles: bool = True
        self.controles = Controles()
        self.layout.addWidget(self.controles)
        self.controles.setFixedHeight(self.controles.minimumSizeHint().height())
        self.changeLangSignal.connect(langue.lazyEval(self.controles.boutton1.setText,"control.simple_add.title"))
        self.changeLangSignal.connect(langue.lazyEval(self.controles.boutt_show_aj_sph.setText,"control.add_settings.title"))

        # Widget de rendu3D
        self.widget_3D: Renderer3D = Renderer3D(self.controles)
        self.layout.addWidget(self.widget_3D)

        # Dimension affichée par la fenètre de rendu
        ticktime:float=1/settings.get("simulation.fps")*settings.get("simulation.simspeed")
        self.dimension = gravilib.PyBaseDimension(self.widget_3D,ticktime)
        
        # A raffiner, mais est utilisé pour update la simulation à intervalles réguliers
        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(1/settings.get("simulation.fps")*1000)
        self.timer.timeout.connect(self.update_simulation)
        self.timer.start()
        if settings.get("logging") >= 2:
            print("main windows initialized")

    def closeEvent(self, event) -> None:
        """Permet de fermer toutes les fenêtres lors de la fermeture de la fenêtre principale, et de terminer le programme
        """
        app.exit(0)
    
    def attach_detach_controles(self) -> None: 
        """Permet d'afficher les controles dans une fenètre séparée de la principale."""
        if self.affichage_controles:
            self.controles.hide()
            controles_graphiques.show()
            self.attach_detachAction.setText(langue.get("menu.display.attach"))
            self.affichage_controles = False
            if settings.get("logging") >= 2:
                print("controles déttachés")
        else:
            self.controles.show()
            controles_graphiques.hide()
            self.attach_detachAction.setText(langue.get("menu.display.detach"))
            self.affichage_controles = True
            if settings.get("logging") >= 2:
                print("controles attachés")
                
    def attach_detach_texte(self):
        if self.affichage_controles:
            self.attach_detachAction.setText(langue.get("menu.display.detach"))
        else :
            self.attach_detachAction.setText(langue.get("menu.display.attach"))

    def change_lang(self, lang):
        settings.set("affichage.langue",lang)
        settings.save()
        langue.reload()
        self.changeLangSignal.emit()
        
    def affich_licence(self) -> None:
        """Cette fonction permet d'afficher la licence du projet"""
        self.fenetre_license: QWidget = QScrollArea()
        self.fenetre_license.setWindowTitle(langue.get("file.license"))
        try:
            path: str = os.path.abspath(os.path.dirname(__file__))
            path = os.path.join(path, langue.get("file.license"))
            with open(path, encoding="utf-8") as file:
                self.licenseTextlabel: QWidget = QLabel(file.read())
        except:
            if settings.get("logging") >= 1:
                print("The french licence file was not found at", path, file=stderr)
            self.licenseTextlabel: QWidget = QLabel(
                "Ficher manquant ou chemin cassé.\n\nRendez vous sur :\nhttps://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D/blob/main/LICENCE_FR")
        self.fenetre_license.setWidget(self.licenseTextlabel)
        self.fenetre_license.show()

    def ajouter_sphere(self, sph: gravilib.PyBaseSphere) -> None:
        """Permet d'ajouter une sphère.

        Args:
            sph (gravilib.PyBaseSphere): Sphère venant de gravilib.py
        """
        self.dimension.add_sphere(sph)
        for rendu in sph.get_render_items():
            self.widget_3D.add_to_display(rendu)
    
    if  settings.get("logging")>=3:
        def update_simulation(self) -> None:
            totalstart = time()
            start = time()
            print("starting update")
            self.dimension.gravite_all()
            print("grav time:", time()-start)
            start = time()
            self.dimension.move_all()
            print("move time:", time()-start)
            start = time()
            self.dimension.gerer_colision()
            print("coli time", time()-start)
            start = time()
            self.widget_3D.repaint()
            print("graph time:", time()-start)
            print("total:", time()-totalstart,"on",ticktime,"normaly")
    else:
        def update_simulation(self) -> None:
            self.dimension.gravite_all()
            self.dimension.move_all()
            self.dimension.gerer_colision()
            self.widget_3D.repaint()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Décale la caméra par rapport au milieu de la fenêtre.

        Args:
            event (QResizeEvent): évenement de resize dans le widget.
        """
        self.menuBar.setFixedWidth(self.size().width())


class Controles(QWidget):
    """Classe permettant de gérer et afficher les contrôles des sphères ainsi que leurs effets.

    Args:
        QWidget (class 'Shiboken.ObjectType'): permet l'utilisation de Widgets.
    """
    """Ce QWidget permet de gérer les différents contrôles."""
    fenetre_ajoute: QWidget = QScrollArea()
    fenetre_ajoute.setWindowTitle(langue.get("control.add_settings.title"))
    layout_aj_sph: QLayout = QGridLayout()
    fenetre_ajoute.setLayout(layout_aj_sph)

    amount = QSpinBox(minimum=0, maximum=10000, value=100)
    amountl = QLabel(langue.get("control.add_settings.nb"))
    layout_aj_sph.addWidget(amountl, 0,0)
    layout_aj_sph.addWidget(amount,0,1)

    xmean = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=0,decimals=0)
    xrand = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=20000000,decimals=0)
    xlabel = QLabel(langue.get("control.add_settings.x"))
    for i,widget in enumerate((xlabel, xmean, QLabel('+-'),xrand)):
        layout_aj_sph.addWidget(widget,1,i)

    ymean = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=0,decimals=0)
    yrand = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=20000000,decimals=0)
    ylabel = QLabel(langue.get("control.add_settings.y"))
    for i,widget in enumerate((ylabel, ymean, QLabel('+-'),yrand)):
        layout_aj_sph.addWidget(widget,2,i)
    
    zmean = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=0,decimals=0)
    zrand = QDoubleSpinBox(minimum=-2000000000, maximum=2000000000, value=20000000,decimals=0)
    zlabel = QLabel(langue.get("control.add_settings.z"))
    for i,widget in enumerate((zlabel, zmean, QLabel('+-'),zrand)):
        layout_aj_sph.addWidget(widget,3,i)
    
    massemin = QDoubleSpinBox(minimum=1, maximum=float(10**17), value=3*10**2,decimals=0)
    massemax = QDoubleSpinBox(minimum=1,maximum=float(10**17),value=3*10**8,decimals=0)
    massel = QLabel(langue.get("control.add_settings.m"))
    for i,widget in enumerate((massel, massemin, QLabel("<?<"),massemax)):
        layout_aj_sph.addWidget(widget,4,i)
        
    rayonmin = QDoubleSpinBox(minimum=1,maximum=10**7,value=3*10**4,decimals=0)
    rayonmax = QDoubleSpinBox(minimum=1,maximum=10**7,value=4*10**4,decimals=0)
    rayonl = QLabel(langue.get("control.add_settings.r"))
    for i,widget in enumerate((rayonl, rayonmin, QLabel("<?<"),rayonmax)):
        layout_aj_sph.addWidget(widget,5,i)
    
    def ajouter_spheres(*_) -> None:
        """Permet d'ajouter un nombre définie de sphères dans la plage de coordonnées selectionné.

        Args:
            boo (int): le nombre de sphères à ajouter.
        """
        xmean=Controles.xmean.value()*1000
        xrand=Controles.xrand.value()*1000
        ymean=Controles.ymean.value()*1000
        yrand=Controles.yrand.value()*1000
        zmean=Controles.zmean.value()*1000
        zrand=Controles.zrand.value()*1000
        mmin=Controles.massemin.value()*1000
        mmax=Controles.massemax.value()*1000
        rmin=Controles.rayonmin.value()*1000
        rmax=Controles.rayonmax.value()*1000
        for _ in range(Controles.amount.value()):
            dist:float=random()**(1/3)
            teta=random()*2*pi
            phi=random()*2*pi
            x=xmean+xrand*dist*sin(teta)*cos(phi)
            y=ymean+yrand*dist*sin(teta)*sin(phi)
            z=zmean+zrand*dist*cos(teta)
            #if _ == 1 :
                #var = gravilib.PyBaseSphere(0, 0, 100000000, 2,6*10**62, rmax,0, 0, 0, 10*9, ticktime)
                #Fenetre_principale.ajouter_sphere(var)
            #else :
            var = gravilib.PyBaseSphere(x, y, z, randint(mmin, mmax), randint(rmin, rmax), vx=randint(-1_000_000, 1_000_000), vy=randint(-1_000_000, 1_000_000), vz=randint(-1_000_000, 1_000_000), d=randint(10,1000000))
            Fenetre_principale.ajouter_sphere(var)

    bouton_val_aj: QAbstractButton = QPushButton(langue.get("control.add_settings.valid"))
    layout_aj_sph.addWidget(bouton_val_aj)
    bouton_val_aj.clicked.connect(ajouter_spheres)

    def __init__(self) -> None:
        """Méthode constructeur, permet de créer les boutons cliquables d'ajout de sphères.
        """
        super().__init__()
        self.setWindowTitle(langue.get("control.title"))
        # layout des controles widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.boutton1: QAbstractButton = QPushButton(langue.get("control.simple_add.title"))
        self.boutton1.clicked.connect(Controles.ajouter_spheres)
        self.layout.addWidget(self.boutton1)

        self.boutt_show_aj_sph: QAbstractButton = QPushButton(langue.get("control.add_settings.title"))
        self.layout.addWidget(self.boutt_show_aj_sph)
        self.boutt_show_aj_sph.clicked.connect(self.fenetre_ajoute.show)


controles_graphiques: QWidget = Controles()
Fenetre_principale: QWidget = Main_window()

Fenetre_principale.changeLangSignal.connect(langue.lazyEval(controles_graphiques.bouton_val_aj.setText,"control.add_settings.valid"))
Fenetre_principale.changeLangSignal.connect(langue.lazyEval(controles_graphiques.fenetre_ajoute.setWindowTitle,"control.add_settings.title"))
for label,setloc in ((Controles.amountl,"control.add_settings.nb"),
                     (Controles.xlabel,"control.add_settings.x"),
                     (Controles.ylabel,"control.add_settings.y"),
                     (Controles.zlabel,"control.add_settings.z"),
                     (Controles.rayonl,"control.add_settings.r"),
                     (Controles.massel,"control.add_settings.m")):
    Fenetre_principale.changeLangSignal.connect(langue.lazyEval(label.setText,setloc))
Fenetre_principale.changeLangSignal.connect(langue.lazyEval(controles_graphiques.boutton1.setText,"control.simple_add.title"))
Fenetre_principale.changeLangSignal.connect(langue.lazyEval(controles_graphiques.boutt_show_aj_sph.setText,"control.add_settings.title"))

Fenetre_principale.showMaximized()