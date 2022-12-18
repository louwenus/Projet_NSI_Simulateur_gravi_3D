# Projet_NSI_Simulateur_gravi_3D

Projet de simulateur de gravitation en 3D, avec une librairie calculatoire en C++ et un frontend en python :<br/>
Utilisation de [Cython](https://github.com/cython/cython).<br/><br/>

Licence GPLV3+ :
Lisez LICENSE ou https://www.gnu.org/licenses/ pour plus de détails.

## Installation :<br/>
Dans tous les cas vous avez besoin d'avoir python3 et pip préinstallés.
- Avec les versions déjà compilées :<br/>
  *NB : Cette méthode n'est pas recommandée puisque les wheel ne sont pas build et uploadées régulièrement, elles ne seront donc probablement pas à jour.*
  - Allez chercher la wheel correspondant à votre platforme [ici](https://mwaserv.hd.free.fr/downloads/graviproject/) puis installez la avec,<br/>
  `python3 -m pip install nom_du_fichier.whl`<br/>
  - vous pouvez lancer le programme avec la commande `Graviproject` si les scripts générés par pip sont bien dans le path.
- En compilant :<br/>
  - Vous devez compiler du c++ et du cython:
    - Pour Windows:
      Installez un compilateur c++ de votre choix capable de compiler du C++20, par exemple [a completer par Kaly](exemple.com)
    - Pour Linux:
      Vous avez besoin d'un compilateur pour le C++20 (par exemple `gcc`),et des header python (`python.h`), instalable selon votre distribution:
      - Pour apt (Ubuntu, Debian...):<br/>
        `sudo apt-get install python3-dev`
      - Pour yum (CentOS, RHEL...):<br/>
        `sudo yum install python3-devel`
      - Pour dnf (Fedora...):<br/>
        `sudo dnf install python3-devel`
      - Pour zypper (openSUSE...):<br/>
        `sudo zypper in python3-devel`
      - Pour apk (Alpine...):<br/>
        `sudo apk add python3-dev`
      - Pour apt-cyg (Cygwin...):<br/>
        `apt-cyg install python3-devel`
      - Pour pacman (Arch, Manjaro...):<br/>
        Vous avez deja les header instalés par default avec le paquet python3

      Note: python3-dev couvre seulement l'instalation par default de python, si vous utilisez une version spécifique, par exemple python 3.8, vous devez installer python3.8-dev
    - Pour MacOS:
      Aucun d'entre nous n'a de mac sous la main pour tester, si quelqu'un peut fournir des instruction, ce sera avec plaisir.<br/>
      Vous avez besoin d'un compilateur C++20 et peut etre des header python3 (`Python.h`)
  - Installez le système de build python et les dépendances,<br/>
  `python3 -m pip install --upgrade build cython setuptools pyside6`<br/>
  - copiez le repo git, et compilez le code Cython et c++,<br/>
  `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D`<br/>
  `cd Projet_NSI_Simulateur_gravi_3D`<br/>
  `python3 setup.py build_ext`<br/>
  - lancez le script avec : <br/>
  `python3 src/launch.py`