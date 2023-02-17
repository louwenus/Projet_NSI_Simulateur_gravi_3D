import sys
import PySide6
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from . import gravilib

class MaFenetre(QWidget):
    def __init__(self):
        super().__init__()
        self.creationInterface()
        self.show()
        self.compteur = 0
    
    def addition(self):
        self.compteur+=1
        self.label.setText("{} km à pied".format(self.compteur))

    def creationInterface(self):
        self.setWindowTitle("J'apprends !!!")
        self.resize(1000, 400)
        self.label = QLabel("truc", self)
        self.label.setGeometry(50, 50, 100, 20)
        self.label.setStyleSheet("QLabel {background-color : yellow;}")
        bouton = QPushButton("Cliquez ici", self)
        bouton.setGeometry(50, 70, 100, 20)
        bouton.clicked.connect(self.addition)

app2 = QApplication(sys.argv)
fen = MaFenetre()
sys.exit(app2.exec_())
