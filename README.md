# Le GraviProject !


Projet de simulateur de gravitation en 3D, avec une librairie calculatoire en C++ et un frontend en python.


Table des matières :
 1. [Installation](#installation)
 2. [Crédits](#crédits)


## Installation :

Il est possible d'installer le GraviProject de 2 manières différentes :
- ### En utilisant une version pré-compilée, selon votre plateforme :
  - [Windows x86_64 et python3.11](#windows)
  - [Linux x86_64 ou aarch64 et python3.10](#Linux)

  Si votre plateforme ou que votre version de python ne correspond pas (et que vous ne désirez pas le mettre a jour), [vous devez compiler le projet](#en-compilant).


  - Avec les versions déjà compilées :

    *NB : La plateforme et la version de python doivent correspondre exactement.*
    - ### Windows
      - Si vous ne l'avez pas déja fait, installez ou mettez à jour python, [disponible ici](https://www.python.org/downloads/windows).
      **Séléctionnez bien la version 3.11** *(La dernière en date au moment de la rédaction de cette documentation).*
      - Allez chercher [la dernière wheel disponible ici](https://mwaserv.fr.to/downloads/graviproject/windows_wheel_x86_64/) puis installez la avec pip : `pip install nom_du_fichier.whl`

    - ### Linux
      - Si vous ne l'avez pas déjà fait, installez ou mettez à jour python3.10 ou 3.11 et pip :<br/>
      *NB : seul le build 3.10 et disponible pour aarch64*
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
        `sudo apt-cyg install python3 python3-pip`
        - Pour pacman (Arch, Manjaro...) :<br/>
        `sudo pacman -S python python-pip`
        
      - Allez chercher la wheel correspondant à votre plateforme [ici](https://mwaserv.fr.to/downloads/graviproject/) *(prenez bien la dernière en date)* puis installez la avec :<br/>
      `python3 -m pip install nom_du_fichier.whl`

      - Vous pouvez lancer le programme avec la commande `Graviproject` si les scripts générés par pip sont bien dans le path, sinon :
        ```
        python3
        from Graviproject.main import launch_app
        launch_app()
        ```
- ### En compilant
  - [Windows](#windows-1)
  - [Linux](#linux-1)
  - [Autres systèmes](#autres-systèmes)
  - ### Windows
    - Installez [python3](https://www.python.org/downloads/windows/).
    *NB : Normalement, les header python.h et pip sont installés en meme temps.*

    - Installez le compilateur c++ de votre choix capable de compiler du C++20, par exemple [msvc](https://aka.ms/vs/17/release/vs_BuildTools.exe).

    - Installez le système de build python et les dépendances :

      `python.exe -m pip install --upgrade build "cython @ git+https://github.com/cython/cython" setuptools pyside6`<br/>
    - Copiez le repo git :

      `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D.git`<br/>
    *NB : La version git de cython et requise jusqu'à ce q'une version post 31 mars 2023 soit disponible autrement (post version 3.0.0b2).*
    - Compilez:

      Entrez dans le répertoire du repo git :<br/>
      `cd Projet_NSI_Simulateur_gravi_3D`

      - Pour une utilisation locale :<br/>
        `python.exe setup.py build_ext`

        Lancez ensuite le programme avec le fichier launch.py (dans le répertoire src) :<br/>
        `python.exe src\launch.py`

      - Pour créer une wheel et pouvoir installer le programme :<br/>
        `python.exe -m build -nx -w`

        La wheel est disponible dans le dossier dist, vous pouvez l'installer avec :<br/>
        `pip install dist\nom_du_fichier.whl` *NB: vous pouvez autocompléter les noms de fichier avec la touche Tab.*

        Il est désormais possible de lancer le programme sous le nom `Graviproject` (si les scripts de pip sont bien dans le PATH) ou de la manière suivante :
        ```
        python.exe
        from Graviproject.main import launch_app
        launch_app()
        ```

  - ### Linux

    - Installez python3, pip, un compilateur pour le C++20 (par exemple `gcc`), et des headers python (`python.h`). Les commandes suivantes fonctionent selon votre distribution :

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
      
      *NB : python3-dev couvre seulement l'installation par default de python, si vous utilisez une version spécifique, par exemple python 3.8, vous devez installer python3.8-dev.*
      
    - Installez le système de build python et les dépendances :

      `python3 -m pip install --upgrade build "cython @ git+https://github.com/cython/cython" setuptools pyside6`<br/>
    *NB : La version git de cython et réquise jusqu'à ce q'une version post 31 mars 2023 soit disponible autrement (post version 3.0.0b2).*
    - Copiez le repo git :

      `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D.git`
    
    - Compilez :

      Entrez dans le répertoire du repo git :<br/>
      `cd Projet_NSI_Simulateur_gravi_3D`
      - Pour une utilisation locale :<br/>
        `python3 setup.py build_ext`

        Lancez ensuite le programme avec le fichier launch.py (dans le répertoire src) :<br/>
        `python3 src\launch.py`

      - pour créer une wheel et pouvoir installer le programme :<br/>
        `python3 -m build -nx -w`

        La wheel est disponible dans le dossier dist, vous pouvez l'installer avec :<br/>
        `python3 -m pip install dist\nom_du_fichier.whl` *NB: vous pouvez autocompléter les noms de fichier avec la touche Tab.*

        Il est désormais possible de lancer le programme sous le nom `Graviproject` (si les scripts de pip sont bien dans le PATH) ou de la manière suivante :
        ```
        python3
        from Graviproject.main import launch_app
        launch_app()
        ```

    
      
  - ### Autres systèmes:

    Si vous avez des instructions plus spécifiques pour un système donné après une installation réussie, dites-le nous, nous les ajouterons avec plaisir !

    Installez python3, pip, un compilateur C++20 (si possible supportant gnu++20) et peut-être les headers python3 (`Python.h`) si ils ne sont pas installés par défaults avec python.
  
    - Installez le système de build python et les dépendances :<br/>
    `python -m pip install --upgrade build "cython @ git+https://github.com/cython/cython" setuptools pyside6`

    *NB : La version git de cython et réquise jusqu'a ce q'une version post 31 mars 2023 soit disponible autrement (post version 3.0.0b2).*

    - Copiez le repo git:

      `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D.git`
    
    - Compilez:

      Entrez dans le répertoire du repo git :<br/>
      `cd Projet_NSI_Simulateur_gravi_3D`

      - Pour une utilisation locale:<br/>
        `python3 setup.py build_ext`

        Lancez ensuite le programme avec le fichier launch.py (dans le répertoire src) :<br/>
        `python3 src\launch.py`
      - pour créer une wheel et pouvoir installer le programme :<br/>
        `python3 -m build -nx -w`

        La wheel est disponible dans le dossier dist, vous pouvez l'installer avec :<br/>
        `python3 -m pip install dist\nom_du_fichier.whl` *NB: vous pouvez autocompléter les noms de fichier avec la touche Tab.*

        Il est désormais possible de lancer le programme sous le nom `Graviproject` (si les scripts de pip sont bien dans le PATH) ou de la manière suivante :
        ```
        python3
        from Graviproject.main import launch_app
        launch_app()
        ```
## Crédits:

Afin de faire une librairie C++ accessible en python, nous utilisons [Cython](https://github.com/cython/cython).

Pour de hautes performances de multithreading, nous utilisons [BS::thread_pool](https://github.com/bshoshany/thread-pool) : A C++17 Thread Pool for High-Performance Scientific Computing.

Pour gérer nos fenêtres et l'affichage en général, nous utilisons [PySide6](https://pypi.org/project/PySide6/) (wrapper python autour de Qt6).

## Licence
Ce programme et son code source sont disponibles sous les termes de la licence GNU General Public License version 3 or later (GPLV3+), 
lisez le fichier LICENSE (en anglais), sa traduction francaise dans le fichier LICENSE_FR ou référez-vous à https://www.gnu.org/licenses/ pour plus de détails.

Les textes de présentations et de documentation (tel que ce README.md) sont disponibles sous la licence [Creative Common Attribution-ShareAlike (CC-BY-SA)](https://creativecommons.org/licenses/by-sa/4.0/legalcode).