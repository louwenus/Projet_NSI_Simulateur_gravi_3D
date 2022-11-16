# Projet_NSI_Simulateur_gravi_3D

Projet de simulateur de gravitation en 3D, avec une librairie calculatoire en C++ et un frontend en python :<br/>
Utilisation de [Cython](https://github.com/cython/cython)<br/><br/>

Lisence GPLV3+ :
Lisez LICENSE ou https://www.gnu.org/licenses/ pour plus de détails.

## Installation :<br/>
- avec pip :<br/>
pas encore distribué...<br/>
- en compilant :<br/>
  - installez le système de build python et les dépendances<br/>
  `python3 -m pip install build cython setuptools`<br/>
  - copiez le repo git<br/>
  `git clone https://github.com/louwenus/Projet_NSI_Simulateur_gravi_3D`<br/>
  - allez dans le répertoire nouvellement créé<br/>
  `cd Projet_NSI_Simulateur_gravi_3D`<br/>
  - compilez le code c++ avec cython<br/>
  `python3 setup.py build_ext`<br/>
