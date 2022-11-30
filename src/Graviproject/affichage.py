print("Importation de affichage.py")


try:
    from PySide2.QtWidgets import QApplication, QLabel
except ModuleNotFoundError:
    print("le module PySide2 devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")

import sys


app = QApplication(sys.argv)
label = QLabel("<font color=red size=40>Hello World !</font>")
label.show()