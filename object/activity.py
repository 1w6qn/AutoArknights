import log
from utils import *
activity_table=load_json('./gamedata/zh_CN/gamedata/excel/activity_table.json')
class Activity:
    def __init__(self,data):
        self.__dict__.update(data)
        self.__dict__.update(activity_table['basicInfo'][self.id])
class ActivityDatabase:
    _db=[]
    def _init(self,obj):
        gd=obj.gamedata
        self.exp_map=gd.gamedata_const["characterExpMap"]
        self.max_level=gd.gamedata_const["maxLevel"]
        self.favor_level=[i['level']for i in gd.favor_table['favorFrames']]
        tag_table=obj.gachaTags
        for k,v in gd.character_table.items():
            if v['profession']not in t:continue
            char=Character({"charId":k}|v,self.exp_map,self.favor_level,self.max_level,tag_table)
            
            self._db.append(char)
        self.init=True
    def __get__(self,obj,type):
        if not self.init:self._init(obj)
        return self
    def get(self,key,type='charId'):
        return list(filter(lambda x:x.__dict__[type]==key,self))[0]
    def __set__(self,obj,val):
        if not self.init:self._init(obj)
        for k,v in val.items():
            char=self.get(v['charId'])
            char.update(v)
            if char.obtained:continue
            char.evolve=partial(obj._api.charBuild.evolveChar,k)
            char.upgrade=partial(obj._api.charBuild.upgradeChar,k)
            char.obtained=True
        if not self.pdata_init:
            self.pdata_init=True
    def __iter__(self):
        self.i=-1
        return self
    def __next__(self):
        if self.i>=len(self._db)-1:
            raise StopIteration
        self.i+=1
        return self._db[self.i]
    def __init__(self):
        self.init=False
        self.pdata_init=False
