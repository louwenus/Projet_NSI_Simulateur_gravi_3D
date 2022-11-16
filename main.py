#!/usr/bin/env python3

#   Simulateur_gravi_3D : Un simulateur de gravité simple avec rendu 3D
#   Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.


#   Ceci est le fichier exécutable principal, lancé par l'utilisateur.
#   Comme il est potentiellement réimporté par certaines dépendances, le code exécuté est inclus dans un if __name__ == "__main__"
#   Ce fichier importe et gère la librairie c++, gravilib, et délègue l'affichage à un sous script, lib/affichage.py
import sys

if __name__ == "__main__": # Disclaimer & parsing des options passées à l'appel
    if {"--license","-license","/license","--show","-show","/show"}.intersection(sys.argv):
        with open("LICENSE") as license:
            print(license.read())
            exit(0)
    print("program_name  Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled",
    "This program comes with ABSOLUTELY NO WARRANTY;",
    "This is free software, and you are welcome to redistribute it under certain conditions;",
    "type `"+sys.argv[0]+" --license' for details.",sep="\n")

# import des différentes librairies avec debug
try:
    import cython
except ModuleNotFoundError:
    print("le module cython devrait être installé pour que ce programme puisse fonctionner, lisez README.md pour plus de détails")
    exit(1)
try:
    import pygravilib
except ModuleNotFoundError:
    print("PyGravilib doit etre compilé ou téléchargé pour votre distribution pour que ce programme fonctionne, lisez README.md pour plus de détails")
    exit(1)

# on crée une dimension (classe principale de la librairie)
universe: pygravilib.PyDimension

if __name__ == "__main__":
    universe=pygravilib.PyDimension()
    universe.print_hello_world()
    universe.hello_text="\nHello World from python\n"
    universe.print_hello_world()