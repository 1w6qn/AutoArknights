import json
from utils import *
from object.character import *
from object.item import *
from object.shop import Shop
from object.recruit import Recruit
class GameData:
    def _load(self,filename):
        if filename[:-5] in self.__dict__:
            print(f"{filename} already loaded")
        with open(self.path+filename,'r')as f:
            self.__dict__[filename[:-5]]=json.load(f)
            print(f"Loaded {filename}")
    def __get__(self,obj,type):
        return self
    def __set__(self,obj,val):
        self.path=f"gamedata/{obj.server}/gamedata/excel/"
        if isinstance(val,str):self._load(val)
        if isinstance(val,list):
            for i in val:self._load(i)
    def __str__(self):
        return f"Loaded {str(self.__dict__.keys())}"
    def __repr__(self):
        return self.__str__
class PlayerData:
    recruit=Recruit()
    gamedata=GameData()
    chars=CharacterDatabase()
    inventory=ItemDatabase()
    gachaTags=GachaTagDatabase()
    def _init(self,obj):
        self.server=obj.server
        self.gamedata=[
        "character_table.json",
        "gacha_table.json",
        "favor_table.json",
        "gamedata_const.json",
        "item_table.json",
        "stage_table.json"
        ]
        self.gamedata_init=True
    def __get__(self,obj,type):
        if not self.gamedata_init:self._init(obj)
        return self
    def __set__(self,obj,data):
        self.server=obj.server
        if not self.gamedata_init:self._init(obj)
        if not self.init:
            
            self._api=obj.api
            self.mod(data)
            self.sort_list={"key":"rarity","reverse":True}
            self.item_filter={"key":"sortId"}
            self.inventory= data['inventory']
            self.init_shops()
            self.init=True
        else:self.mod(data['modified'])
    @property
    def items(self):
        return list(filter(lambda x:x.__dict__[item_filter["key"]],__items))
    def __init__(self):
        self.init=False
        self.gamedata_init=False
    def init_shops(self):
        pass
    def mod(self,new):
        
        if c:=new.get('troop',{}).get('chars'):self.chars=c
        merge_dict(self.__dict__,new)
