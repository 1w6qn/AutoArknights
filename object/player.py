import object.gameServer,object.playerData
import json
import utils
import api
class Player:
    dump_list=['account','password','access_token','platform','server']
    def init_data(self,data):
        self.data=object.playerData.PlayerData(data)
    def __init__(self,account,password,access_token=""):
        self.gs=object.gameServer.GameServer()
        self.account=account
        self.password=password
        self.access_token=access_token
        self.deviceId=utils.get_random_device_id()
        self.deviceId2=utils.get_random_device_id2()
        self.deviceId3=utils.get_random_device_id3()
        self.platform=1
        self.server="zh_CN"
        api.player=self
        self.api=api
    @classmethod
    def load_from_json(cls,filename):
        with open(filename,'r+') as f:
            j=json.loads(f.read())
        return [cls(**i)for i in j]
    @property
    def attr(self):return self.__dict__
    def dump(self):return dict(filter(lambda x:x[0] in self.dump_list,self.attr.items()))