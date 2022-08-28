import requests,json,log,utils
COMMON_HEADER ={
    'Content-Type': 'application/json',
    'X-Unity-Version': '2017.4.39f1',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; X Build/V417IR)',
    'Connection': 'Keep-Alive'
}
HOST={
    'zh_CN':'https://ak-conf.hypergryph.com',
    'ja_JP':'https://ak-conf.arknights.jp',
    'en_US':'https://ak-conf.arknights.global'
}
class AuthServer:
    def post(self,cgi,data):
        url=self.url+cgi
        headers=COMMON_HEADER
        signstr="&".join(["=".join((k,str(v)))for k,v in data.items()])
        data.update({"sign":utils.u8_sign(signstr)})
        res= requests.post(url,data=json.dumps(data),headers=headers).json()
        return res
    def __init__(self):
        self.url=""
    def __set__(self,obj,val):
        raise AttributeError
    def __get__(self,obj,type):
        if not self.url:self.url=obj.nc['as']
        return self.post
class GameServer:
    def post(self,cgi,data):
        url=self.url+cgi
        headers=COMMON_HEADER|{'uid':self.uid,'secret':self.secret,'seqnum':str(self.seqnum)}
        res= requests.post(url,data=json.dumps(data),headers=headers)
        if 'secret' in res.json():self.secret=res.json()['secret']
        seq=res.headers.get('seqnum')
        if seq and seq.isdigit():self.seqnum=int(seq)
        else:self.seqnum+=1
        return res.json()
    def __init__(self):
        self.uid=""
        self.secret=""
        self.url=""
        self.seqnum=0
    def __set__(self,obj,val):
        self.uid=val
    def __get__(self,obj,type):
        if not self.url:self.url=obj.nc['gs']
        return self.post
class NetworkConfig:
    def __init__(self):
        self.isupd=False
    @staticmethod
    def get_from_conf(url):
        return requests.get(url,headers=COMMON_HEADER).json()
    def update(self):
        res=NetworkConfig.get_from_conf(self.config+"/config/prod/official/network_config")
        content=json.loads(res["content"])
        self.__dict__.update(content)
        self.__dict__.update(self.configs[self.funcVer]['network'])
        del self.configs
        v=NetworkConfig.get_from_conf(self.hv.format(self.platform_id))
        self.__dict__.update(v)
        log.d(f"资源更新成功 ResVersion:{self.resVersion} ClientVersion:{self.clientVersion}")
        self.isupd=True
    def __set__(self,obj,val):
        raise AttributeError
    def __get__(self,obj,type):
        if not self.isupd:
            self.server=obj.server
            self.platform_id=obj.platform_id
            self.config=HOST[self.server]
            self.update()
        return self.__dict__