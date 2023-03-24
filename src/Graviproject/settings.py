import json
from typing import Iterable

settings: dict={}
defaults: dict={}
try:
    with open('default_settings.json','r') as setfile:
        defaults=json.load(setfile)
except Exception as e:
    print("no default_settings.json file, package should be réinstalled or permission checked, aborting")
    raise FileNotFoundError('default_settings.json')
try:
    with open('settings.json','r') as setfile:
        settings=json.load(setfile)
except:
    print("inexistant or ill-formated settings.json file, using defaults settings only")

def get(setloc : str):
    try:
        temp=settings
        for key in setloc.split('.'):
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

def set(setloc : str,value) -> bool:
    """set settings 'setloc' at value

    Args:
        setloc (str): setting to update, a . permit to separate per group, ..is not permited
        value (any): the new value of the setting

    Returns:
        bool: _description_
    """
    temp=settings
    for key in setloc.split('.')[:-1]:
        if type(temp) is not dict:
            print("setting path to non dict, abborting")
            return False
        if key not in temp:
            temp[key]={}
        temp=temp[key]
    temp[setloc.split('.')[-1]]=value
    return True



def save()->bool:
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


if get("logging") >=2:
    print("INFO: settings initialized")