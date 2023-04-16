#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

import sys #Importation de la librairie sys

if "--license" in sys.argv:  # Disclaimer & parsing des options passées à l'appel
    with open("LICENCE_FR") as license:
        print(license.read())
        exit(0)
if "--help" in sys.argv or "-h" in sys.argv:
    print("""Graviproject [OPTIONS]

    OPTIONS:
        --help   -h   Print this help
        --license     Print the (french) license
        --no-settings Use only default settings
    """)
print("program_name  Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, GargantuaArgell",
      "This program comes with ABSOLUTELY NO WARRANTY;",
      "This is free software, and you are welcome to redistribute it under certain conditions;",
      "type `"+sys.argv[0]+" --license' for details.", sep="\n")
