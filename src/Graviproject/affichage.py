# encoding=utf8

print("Importation de affichage.py")


try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ModuleNotFoundError:
    print("le module PySide6 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")

import sys
import random


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.hello = ["Hallo Welt", "Hei maailma", "Hola Mundo", "Привет мир"]

        self.button = QtWidgets.QPushButton("Click me!")
        self.text = QtWidgets.QLabel("Hello World",alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.button.clicked.connect(self.magic)

    @QtCore.Slot()
    def magic(self):
        self.text.setText(random.choice(self.hello))


app = QtWidgets.QApplication(sys.argv)

widget = MyWidget()  
try:
    widget.showMaximized() #Pour faire en sorte que la fenêtre prenne tout l'écran 
except:
    widget.show() #Si votre gestionnaire de fenêtre ne conçoit pas qu'une fenêtre puisse se définir elle même