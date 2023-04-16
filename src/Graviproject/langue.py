import json
import os
from . import settings

lang: dict = {}

path: str = os.path.abspath(os.path.dirname(__file__))
path = os.path.join(path, "Langues/"+settings.get("affichage.langue")+".json")  
with open(path, 'r') as setfile:
    lang = json.load(setfile)


def get(setloc: str) -> str:
    path: list[str]=setloc.split('.')
    
    try:
        temp = lang
        for key in path:
            temp = temp[key]
        return temp
    except (KeyError):
        if settings.get("logging") >= 1:
            print("Il semblerait que cette clef n'existe pas dans le json",settings.get("affichage.langue"),"vous allez devoir la rajouter ou requérir l'assistance d'Artefact42 (ou de toute autre personne compétente).")
        return lang["404"]