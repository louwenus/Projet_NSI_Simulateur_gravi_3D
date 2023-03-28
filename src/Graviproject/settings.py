import json
import os
from typing import Iterable
from sys import stderr

settings: dict={}
defaults: dict={}
try:
    path: str=os.path.abspath(os.path.dirname(__file__))
    path=os.path.join(path, "default_settings.json")
    with open(path,'r') as setfile:
        defaults=json.load(setfile)
except Exception as e:
    print("no default_settings.json file, package should be réinstalled or permission checked, aborting",file=stderr)
    raise FileNotFoundError('default_settings.json')
path: str=os.path.abspath(os.path.dirname(__file__))
path=os.path.join(path, "settings.json")
try:
    with open(path,'r') as setfile:
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
            for key in setloc.split('.'):
                temp=temp[key]
            return temp
        except:
            if get("logging")>=1:
                print("No setting found for ",setloc,file=stderr)
            return None

def set(setloc : str,value) -> bool:
    """set settings 'setloc' at value

    Args:
        setloc (str): setting to update, a . permit to separate per group (eg "group.sub.setting")
        value (any): the new value of the setting, must be representable in json

    Returns:
        bool: if the update was sucessful
    """
    temp=settings
    for key in setloc.split('.')[:-1]:
        if type(temp) is not dict:
            if get("logging") >= 1:
                print("setting path to non dict, abborting",file=stderr)
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
        with open(path,'w') as setfile:
            json.dump(settings, setfile, indent = 2)
            return True
    except Exception as e:
        if get("logging") >= 1:
            print("Illegal setting for json representation or no write acess:",e,file=stderr)
        return False


if get("logging") >=2:
    print("settings initialized")