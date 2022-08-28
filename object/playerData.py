import json
from utils import *
from object.character import Character
from object.item import Item
from object.shop import Shop
from object.recruit import Recruit
class PlayerData:
    recruit=Recruit()
    def __get__(self,obj,type):
        self.server=obj.server
        return self
    def __set__(self,obj,data):
        if not self.init:
            self.__dict__.update(data)
            self.sort_list={"key":"rarity","reverse":True}
            self.item_filter={"key":"sortId"}
            self.__chars=[Character(v)for k,v in data['troop']['chars'].items()]
            self.__items=[Item({"id":k,"cnt":v})for k,v in data['inventory'].items()]
            self.init_shops()
            self.init=True
        else:self.update(data)
    def load(self,filename):
        with open(f"gamedata/{self.server}/gamedata/excel/{filename}",'r')as f:
            return json.load(f)
    @property
    def items(self):
        return list(filter(lambda x:x.__dict__[item_filter["key"]],__items))
    @property
    def chars(self):
        key=self.sort_list|{"key":lambda x:x.__dict__[self.sort_list['key']]}
        return sorted(self.__chars,**key)
    def list_box(self):
        for i in self.chars:print(i)
    def __getattr__(self,k):
        return None
    def __init__(self):
        self.init=False
    def init_shops(self):
        pass
    def update(self,new):
        modified=new['modified']
        merge_dict(self.__dict__,modified)
        if c:=modified.get('troop',{}).get('chars'):
            for k,v in c.items():
                if len(self.__chars)<int(k):self.__chars.append(Character(v))
                else:self.__chars[int(k)-1].update(v)
