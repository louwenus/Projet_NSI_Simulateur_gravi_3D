#!python3

#   <one line to give the program's name and a brief idea of what it does.>
#   Copyright (C) <year>  <name of author>
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


#ceci est le fichier executable principal, lancé par l'utilisateur.
#Comme il est potentiellement réimporté par certaine dépendance, le code executé est inclus dans un if __name__ == "__main__"
#Ce fichier importe et gere la librairie c++,gravilib , et delegue l'affichage a un sous script, lib/affichage.py
import sys
if __name__ == "__main__":
    pass
    #todo: check sys.argv
    #si --lisence, --show,-lisence,-show /lisence ou /show est présent, afficher la lisence et exit
    #de meme avec les bonnes partie de lisence pour --no-warranty et --redistribute
    #si -h -help ou --help est présent, afficher l'aide et exit
    #si gravilib, cython, ... n'est pas présent, afficher les instruction de build
import cython
import pygravilib
universe=pygravilib.PyDimension()

if __name__ == "__main__":
    print("program_name  Copyright (C) 2022 louwenus,Artefact42,kalyklos,Bjctrhtg,g-aled",
    "This program comes with ABSOLUTELY NO WARRANTY; for details type `"+sys.argv[0]+" --no-warranty'.",
    "This is free software, and you are welcome to redistribute it",
    "under certain conditions; type `"+sys.argv[0]+" --redistribute' for details.",sep="\n")
    universe.print_hello_world()
    universe.hello_text="\nHello World from python\n"
    universe.print_hello_world()