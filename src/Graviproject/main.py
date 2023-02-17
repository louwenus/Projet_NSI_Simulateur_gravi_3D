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
from . import gravilib
from . import affichage3D
from . import affichage #temporaire, à raffiner
# on créé une dimension (classe principale de la librairie)

def launch_app():
    #tests:
    test = gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(1,1,1,0,10,10,20,20))
    test2 = gravilib.PyBaseSphere(gravilib.cppgravilib.CySimpleSphere,(0,0,0,0,10,-10,-10,-10))
    universe = gravilib.cppgravilib.CyBaseDimension()
    universe.add_sphere(test.cy_sphere)
    universe.add_sphere(test2.cy_sphere)
    print(universe.collisions(gravilib.collide))
    universe.move_all(10)
    print(universe.collisions(gravilib.collide))
    
    
    sys.exit(affichage3D.app.exec_())