import os
import json
import config
import requests
from funtools import partial
path = os.getcwd() + '/api/'
__all__ = [i.replace('.py','')for i in os.listdir(path)]
player=None
def bind(cgi,type='gs'):
    def deco(func):
        def wrapper(*args,**kwargs):
            if not player:raise Exception
            keys=dict(filter(lambda x:x[0] in func.__code__.co_varnames,kwargs.items()))
            data=func(*args,**keys)
            return player.post(type,cgi,data)
        return wrapper
    return deco
from api import *