import json
from utils import *
item_table=load_json('./zh_CN/gamedata/excel/item_table.json')
char_table=load_json('./zh_CN/gamedata/excel/character_table.json')
game_const=load_json('./zh_CN/gamedata/excel/gamedata_const.json')
class Char:
    attr={}
    def update(self,new):
        print(f"{self.name} 精{self.get_evolve_phase()} {self.get_level()}/{self.get_max_level()}级 {self.get_exp()}/{self.get_max_exp()} -> 精{self.get_evolve_phase()} {self.get_level()}/{self.get_max_level()}级 {self.get_exp()}/{self.get_max_exp()}")
        self.attr.update(new)
    def get_max_exp(self):
        if self.get_level()==self.get_max_level():
            return 0
        return game_const["characterExpMap"][self.get_level()-1]
    def get_max_level(self):
        return game_const["maxLevel"][self.get_rarity()][self.get_evolve_phase()]
    def get_rarity(self):
        return self.attr["rarity"]
    def get_level(self):
        return self.attr["level"]
    def get_exp(self):
        return self.attr["exp"]
    def get_evolve_phase(self):
        return self.attr["evolvePhase"]
    def get_inst_id(self):
        return self.attr["instId"]
    def __init__(self,data):
        self.attr.update(data)
        self.id=self.attr["charId"]
        self.attr.update(char_table[self.id])
        self.name=self.attr["name"]
class Item:
    attr={}
    def __init__(self,data):
        self.attr.update(data)
        self.id=self.attr['itemId']
        self.attr.update(item_table['items'][self.id])
        self.count=self.attr['count']
    def __str__(self):
        return "{}{}{}:{}".format(utils.rcolor[self.attr['rarity']],self.attr["name"],utils.color.RESET,self.count)