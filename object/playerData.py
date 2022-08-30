import json
from utils import *
from object.character import *
from object.item import Item
from object.shop import Shop
from object.recruit import Recruit
class GameData:
    def __get__(self,obj,type):
        return self
    def __set__(self,obj,val):
        path=f"gamedata/{obj.server}/gamedata/excel/{val}"
        with open(path,'r')as f:
            self.__dict__[val[:-5]]=json.load(f)
            print(f"Loaded {val}")
    def __str__(self):
        return f"Loaded {str(self.__dict__.keys())}"
    def __repr__(self):
        return self.__str__
class PlayerData:
    recruit=Recruit()
    gamedata=GameData()
    chars=CharacterDatabase()
    gachaTags=GachaTagDatabase()
    def __get__(self,obj,type):
        self.server=obj.server
        if not self.gamedata_init:
            self.gamedata="character_table.json"
            self.gamedata="gacha_table.json"
            self.gamedata="favor_table.json"
            self.gamedata="gamedata_const.json"
            self.gamedata="item_table.json"
            self.gamedata="stage_table.json"
            self.gamedata_init=True
        return self
    def __set__(self,obj,data):
        if not self.init:
            self.__dict__.update(data)
            self._api=obj.api
            self.sort_list={"key":"rarity","reverse":True}
            self.item_filter={"key":"sortId"}
            self.__chars=[Character(v)for k,v in data['troop']['chars'].items()]
            self.__items=[Item({"id":k,"cnt":v})for k,v in data['inventory'].items()]
            self.init_shops()
            self.init=True
        else:self.update(data)
    @property
    def items(self):
        return list(filter(lambda x:x.__dict__[item_filter["key"]],__items))
    def __init__(self):
        self.init=False
        self.gamedata_init=False
    def init_shops(self):
        pass
    def update(self,new):
        modified=new['modified']
        merge_dict(self.__dict__,modified)
        if c:=modified.get('troop',{}).get('chars'):
            for k,v in c.items():
                if len(self.__chars)<int(k):self.__chars.append(Character(v))
                else:self.__chars[int(k)-1].update(v)
