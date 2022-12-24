#!/usr/bin/env python3
#  Code sous liscence GPL3+. Plus de détail a <https://www.gnu.org/licenses/> ou dans le fichier LICENCE

# encoding=utf8

#Fichier utilisé pour lancer le code depuis une compilation du code source
import Graviproject.main
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
Graviproject.main.launch_app()

