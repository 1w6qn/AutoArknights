import object.server,object.playerData
import json
import utils
import api
class Player:
    dump_list=['account','password','access_token','platform','server']
    _as_post=object.server.AuthServer()
    _gs_post=object.server.GameServer()
    nc=object.server.NetworkConfig()
    data=object.playerData.PlayerData()
    def __init__(self,account,password,access_token="",platform=1,server="zh_CN"):
        self.account=account
        self.password=password
        self.access_token=access_token
        self.deviceId=utils.get_random_device_id()
        self.deviceId2=utils.get_random_device_id2()
        self.deviceId3=utils.get_random_device_id3()
        self.platform=platform
        self.platform_id='Android'
        self.server=server
        api.player=self
        self.api=api
    def post(self,type,cgi,data):
        if type=='as':server=self._as_post
        elif type=='gs':server=self._gs_post
        return server(cgi,data)
    @classmethod
    def load_from_json(cls,filename):
        with open(filename,'r') as f:
            j=json.load(f)
        return [cls(**i)for i in j]
    @property
    def attr(self):return self.__dict__
    def dump(self):return dict(filter(lambda x:x[0] in self.dump_list,self.attr.items()))