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
    import cppgravilib
except ModuleNotFoundError:
    print("PyGravilib doit etre compilé ou téléchargé pour votre distribution pour que ce programme fonctionne, lisez README.md pour plus de détails")
    exit(1)
from .affichage import app #temporaire, à raffiner
# on créé une dimension (classe principale de la librairie)
universe: cppgravilib.PyBaseDimension

def launch_app():
    universe=cppgravilib.PyBaseDimension()
    universe.print_hello_world()
    sys.exit(app.exec_())