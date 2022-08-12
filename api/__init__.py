import os
import json
import config
import requests
from utils import u8_sign
path = os.getcwd() + '/api/'
files = os.listdir(path)
__all__ = []
for i in files:
    __all__.append(i.replace('.py', ''))
def post(cgi,data,auth,server):
    if auth:
        signstr=""
        for k,v in data.items():signstr+=f"{k}={v}&"
        data.update({"sign":u8_sign(signstr[:-1])})
        url=config.NETWORK_CONFIG['as']+cgi
        headers=config.COMMON_HEADER
    else:
        url=config.NETWORK_CONFIG['gs']+cgi
        headers=config.COMMON_HEADER|server.attr
    res= requests.post(url,data=json.dumps(data),headers=headers)
    j=res.json()
    if auth:return j
    if 'secret' in j:server.secret=j['secret']
    if 'seqnum' in res.headers.keys() and res.headers['seqnum'].isdigit():server.seqnum=str(int(res.headers['seqnum']))
    else:server.seqnum=str(int(server.seqnum)+1)
    return j
def bind(cgi,auth=False):
    def deco(func):
        def wrapper(gs=None,*args,**kwargs):
            keys=dict(filter(lambda x:x[0] in func.__code__.co_varnames,kwargs.items()))
            res=post(cgi,func(*args,**keys),auth,None if not gs else gs)
            return res
        return wrapper
    return deco
from api import *