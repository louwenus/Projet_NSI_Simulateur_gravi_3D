#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8
#from . import settings
import sys
if {"--license","-license","/license","--show","-show","/show"}.intersection(sys.argv):  # Disclaimer & parsing des options passées à l'appel
    with open("LICENSE_FR") as license:
        print(license.read())
        exit(0)
print("program_name  Copyright (C) 2022 louwenus, Artefact42, kalyklos, Bjctrhtg, g-aled",
"This program comes with ABSOLUTELY NO WARRANTY;",
"This is free software, and you are welcome to redistribute it under certain conditions;",
"type `"+sys.argv[0]+" --license' for details.",sep="\n")