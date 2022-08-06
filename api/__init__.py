import os
import json
import config
import requests
from utils import u8_sign
path = os.getcwd() + '/api/'
files = os.listdir(path)
__all__ = []
player=None
for i in files:
    __all__.append(i.replace('.py', ''))
def post(cgi,data,auth,server):
    if auth:
        signstr=""
        for k,v in data.items():signstr+=f"{k}={v}&"
        data.update({"sign":u8_sign(signstr[:-1])})
        url=config.HOST['AUTH']+cgi
        headers=config.COMMON_HEADER
    else:
        url=config.HOST['GAME']+cgi
        headers=config.COMMON_HEADER|server.__dict__
    res= requests.post(url,data=json.dumps(data),headers=headers)
    if auth:return res.json()
    if 'seqnum' in res.headers.keys() and res.headers['seqnum'].isdigit():server.seqnum=str(int(res.headers['seqnum']))
    else:server.seqnum=str(int(server.seqnum)+1)
    return res.json()
def bind(cgi,auth=False):
    def deco(func):
        def wrapper(*args,**kwargs):
            res=post(cgi,func(*args,**kwargs),auth,None if not player else player.gs)
            return res
        return wrapper
    return deco
