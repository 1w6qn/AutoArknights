import os
import json
import config
import requests
path = os.getcwd() + '/api/'
__all__ = [i.replace('.py','')for i in os.listdir(path)]
player=None
def post(cgi,data,server):
    res= server(cgi,data)
    return res
def bind(cgi,auth=False):
    def deco(func):
        def wrapper(*args,**kwargs):
            if not player:raise Exception
            keys=dict(filter(lambda x:x[0] in func.__code__.co_varnames,kwargs.items()))
            data=func(*args,**keys)
            res=post(cgi,data,player.as_post if auth else player.gs_post)
            return res
        return wrapper
    return deco
from api import *