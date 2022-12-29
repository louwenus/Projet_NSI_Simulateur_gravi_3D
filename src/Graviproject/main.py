#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

#   Ceci est le fichier exécutable principal, lancé par l'utilisateur.
#   Comme il est potentiellement réimporté par certaines dépendances, le code exécuté est inclus dans un if __name__ == "__main__"
#   Ce fichier importe et gère la librairie c++, gravilib, et délègue l'affichage à un sous script, lib/affichage.py
import sys

# import des différentes librairies avec debug
try:
    import cython
except ModuleNotFoundError:
    print("le module cython devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")
    exit(1)
try:
    from . import cppgravilib
except ModuleNotFoundError:
    print("cppravilib doit etre compilé pour que ce programme fonctionne, lisez README.md pour plus de détails")
    exit(1)
from .affichage import app #temporaire, à raffiner
# on créé une dimension (classe principale de la librairie)
universe: cppgravilib.PyBaseDimension

def launch_app():
    universe=cppgravilib.PyBaseDimension() # une dimension
    testboule1=cppgravilib.PySimpleSphere(0,0,0,100,2,0,0,0) #4 simple spheres de test
    testboule2=cppgravilib.PySimpleSphere(10,0,0,100,2,0,0,0)
    universe.add_sphere(testboule1) 
    universe.add_sphere(testboule2)
    universe.debug()
    universe.gravite_all(1)
    universe.debug()
    universe.move_all(1)
    universe.debug()

    sys.exit(app.exec_())