# Projet_NSI_Simulateur_gravi_3D

Projet de simulateur de gravitation en 3D, avec une librairie calculatoire en C++ et un frontend en python :<br/>
Utilisation de [Cython](https://github.com/cython/cython).<br/><br/>

Licence GPLV3+ :
Lisez LICENSE ou https://www.gnu.org/licenses/ pour plus de détails.

## Installation :<br/>
- Avec les versions déjà compilées :<br/>
  *NB : Cette méthode peut ne pas marcher en cas de différence trop importante entre le serveur sur lequel les wheel sont build et votre ordinateur.*
  - Installez python3.10 et pip

    - Pour windows:<br/>
      installez [python3.10](https://www.python.org/downloads/windows) *NB: selectionnez bien python3.10 puisque les wheel sont build sous python3.10*

    - Pour linux:<br/>
      installez python3.10 et pip :<br/>
      *NB: au moment d'écrire ce README, python 3.10 et le standard sous linux, donc le python3 par default. Modifiez au besoin*
      - Pour apt (Ubuntu, Debian...) :<br/>
        `sudo apt-get install python3 python3-pip`
      - Pour yum (CentOS, RHEL...) :<br/>
        `sudo yum install python3 python3-pip`
      - Pour dnf (Fedora...) :<br/>
        `sudo dnf install python3 python3-pip`
      - Pour zypper (openSUSE...) :<br/>
        `sudo zypper in python3 python3-pip`
      - Pour apk (Alpine...) :<br/>
        `sudo apk add python3 py3-pip`
      - Pour apt-cyg (Cygwin...) :<br/>
        `apt-cyg install python3 python3-pip`
      - Pour pacman (Arch, Manjaro...) :<br/>
        `pacman -S python python-pip`
    
  - Allez chercher la wheel correspondant à votre platforme [ici](https://mwaserv.hd.free.fr/downloads/graviproject/) *(les wheel linux sont build sur le ubuntu-latest de github)* puis installez la avec,<br/>
  `python3.10 -m pip install nom_du_fichier.whl`<br/>
  - vous pouvez lancer le programme avec la commande `Graviproject` si les scripts générés par pip sont bien dans le path.
- En compilant :<br/>
  - Vous devez compiler du c++ et du cython :
    - Pour Windows :

      Installez [python3](https://www.python.org/downloads/windows/)<br/>
      *NB: normalement, les header python.h et pip sont installés en meme temps*<br/>
      Installez un compilateur c++ de votre choix capable de compiler du C++20, par exemple [msvc](https://aka.ms/vs/17/release/vs_BuildTools.exe).

    - Pour Linux :

      Vous avez besoin de python3, pip d'un compilateur pour le C++20 (par exemple `gcc`), et des headers python (`python.h`), instalables selon votre distribution :
      - Pour apt (Ubuntu, Debian...) :<br/>
        `sudo apt-get install python3 python3-pip g++ python3-dev`
      - Pour yum (CentOS, RHEL...) :<br/>
        `sudo yum install python3 python3-pip gcc-c++ python3-devel`
      - Pour dnf (Fedora...) :<br/>
        `sudo dnf install python3 python3-pip gcc-c++ python3-devel`
      - Pour zypper (openSUSE...) :<br/>
        `sudo zypper in python3 python3-pip gcc-c++ python3-devel`
      - Pour apk (Alpine...) :<br/>
        `sudo apk add python3 py3-pip g++ python3-dev`
      - Pour apt-cyg (Cygwin...) :<br/>
        `apt-cyg install python3 python3-pip gcc-g++ python3-devel`
      - Pour pacman (Arch, Manjaro...) :<br/>
        `pacman -S python python-pip gcc`
      
      *NB : python3-dev couvre seulement l'instalation par default de python, si vous utilisez une version spécifique, par exemple python 3.8, vous devez installer python3.8-dev.*
      
    - Pour MacOS :

      Aucun d'entre nous n'a de mac sous la main pour tester, si quelqu'un peut fournir des instructions, ce sera avec plaisir.<br/>
      Vous avez besoin de python3, pip, d'un compilateur C++20 et peut-être des headers python3 (`Python.h`).
  
  - Installez le système de build python et les dépendances,<br/>
  `python3 -m pip install --upgrade build cython setuptools pyside6`<br/>
  - copiez le repo git<br/>
  `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D`<br/>
  `cd Projet_NSI_Simulateur_gravi_3D`<br/>
  - Si vous voulez compiler pour une utilisation dans ce repertoire:
    - compilez avec: `python3 setup.py build_ext --force`<br/>
    - lancez le programme avec la commande `python3 src/launch.py`
  - si vous voulez installer le paquet pip pour avoir une commande accessible partout et pouvoir retirer tout le repertoire git
    - compilez avec: `python3 -m build -w`
    - installez la wheel: `python3 -m pip install dist/nom_du_fichier.whl`
    - Vous pouvez maintenant lancer `Graviproject`
