import json
from typing import Iterable

settings={}
defaults={}
print("initializing settings")
try:
    with open('default_settings.json','r') as setfile:
        defaults=json.load(setfile)
except Exception as e:
    print("no default_settings.json file, aborting")
    raise
try:
    with open('settings.json','r') as setfile:
        settings=json.load(setfile)
except:
    print("inexistant or ill-formated settings.json file, using defaults settings")

def access(setloc : Iterable[str]):
    try:
        temp=settings
        for key in setloc:
            temp=temp[key]
        return temp
    except KeyError:
        try:
            temp=defaults
            for key in setloc:
                temp=temp[key]
            return temp
        except:
            print("No setting found for ",setloc)
            return None

def set_setting(setloc : Iterable[str],value) -> bool:
    """set settings 'setloc' at value

    Args:
        setloc (Iterable[str]): iterable of the setting path (eg ("setting_group","seting_name"))
        value (any): the new value of the setting

    Returns:
        bool: _description_
    """
    temp=settings
    for key in setloc[:-1]:
        if type(temp) is not dict:
            print("setting path to non dict, abborting")
            return False
        if key not in temp:
            temp[key]={}
        temp=temp[key]
    temp[setloc[-1]]=value
    return True



def save_settings()->bool:
    """save settings to settings.json

    Returns:
        bool: if save was sucessful 
    """
    try:
        with open('settings.json','w') as setfile:
            json.dump(settings, setfile, indent = 2)
            return True
    except Exception as e:
        print("Illegal setting for json representation or no write acess:",e)
        return False