# Projet_NSI_Simulateur_gravi_3D

Projet de simulateur de gravitation en 3D, avec une librairie calculatoire en C++ et un frontend en python :<br/>
Utilisation de [Cython](https://github.com/cython/cython).<br/><br/>

Licence GPLV3+ :
Lisez LICENSE ou https://www.gnu.org/licenses/ pour plus de détails.

## Installation :<br/>
- avec pip :<br/>
  - Allez chercher la wheel corespondant a votre platforme [ici](https://mwaserv.hd.free.fr/downloads/graviproject/) puis installez la avec<br/>
  `pip install nom_du_fichier.whl`<br/>
  - vous pouvez lancer le programme avec la commande `Graviproject` si les script généré par pip sont bien dans le path.
- en compilant :<br/>
  - installez le système de build python et les dépendances,<br/>
  `python3 -m pip install build cython setuptools pyside2`<br/>
  - copiez le repo git, et compilez le code Cython et c++<br/>
  `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D`<br/>
  `cd Projet_NSI_Simulateur_gravi_3D`<br/>
  `python3 setup.py build_ext`<br/>
  - lancez le script avec: <br/>
  `python src/launch.py`