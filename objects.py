import json
from utils import *
item_table=load_json('./zh_CN/gamedata/excel/item_table.json')
char_table=load_json('./zh_CN/gamedata/excel/character_table.json')
mission_table=load_json('./zh_CN/gamedata/excel/mission_table.json')
favor_table=load_json('./zh_CN/gamedata/excel/favor_table.json')
game_const=load_json('./zh_CN/gamedata/excel/gamedata_const.json')
favor_level=[]
for i in favor_table['favorFrames']:favor_level.append(i['level'])
class Char:
    def update(self,new):
        old=str(self)
        self.__dict__.update(new)
        print(f"{old} -> {str(self)}")
    @property
    def maxExp(self):
        if self.level==self.maxLevel:return 0
        return game_const["characterExpMap"][self.evolvePhase][self.level-1]
    @property
    def maxLevel(self):
        return game_const["maxLevel"][self.rarity][self.evolvePhase]
    @property
    def favorPercent(self):
        if self.favorPoint in favor_level:return favor_level.index(self.favorPoint)
        t=sorted(favor_level+[self.favorPoint])
        return t.index(self.favorPoint)-1
    @property
    def name(self,colored=True):
        name=self.__dict__['name']
        if colored:return rcolor[self.rarity]+name+color.RESET
        return name
    def calc_exp_cost(self,target_level):
        s=sum(game_const["characterExpMap"][self.evolvePhase][self.level-1:target_level])-self.exp
        return s
    def __init__(self,data):
        self.__dict__.update(data)
        self.id=self.charId
        self.__dict__.update(char_table[self.id])
    def __str__(self):
        return f"{self.name.center(16)}{('精'+self.evolvePhase).center(4)}{(self.level+'/'+self.maxLevel+'级').center(8)}\t信赖{self.favorPercent}%/200%"
class Item:
    attr={}
    def __init__(self,data):
        self.attr.update(data)
        self.id=self.attr['id']
        self.attr.update(item_table['items'][self.id])
        self.name=self.attr['name']
        self.count=self.attr['count']
    def __str__(self):
        return "{}{}{}:{}".format(utils.rcolor[self.attr['rarity']],self.attr["name"],utils.color.RESET,self.count)
class Mission:
    attr={}
    def __init__(self,data):
        self.attr.update(data)
        self.id=self.attr['id']
        self.attr.update(mission_table['missions'][self.id])