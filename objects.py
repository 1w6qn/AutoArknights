import json
from utils import *
item_table=load_json('./zh_CN/gamedata/excel/item_table.json')
mission_table=load_json('./zh_CN/gamedata/excel/mission_table.json')
char_table=load_json('./zh_CN/gamedata/excel/character_table.json')
favor_table=load_json('./zh_CN/gamedata/excel/favor_table.json')
game_const=load_json('./zh_CN/gamedata/excel/gamedata_const.json')
activity_table=load_json('./zh_CN/gamedata/excel/activity_table.json')
building_data=load_json('./zh_CN/gamedata/excel/building_data.json')
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
    def name(self):
        name=self.__dict__['name']
        if self.colored:return rcolor[self.rarity]+name+color.RESET
        return name
    def calc_exp_cost(self,target_level):
        s=sum(game_const["characterExpMap"][self.evolvePhase][self.level-1:target_level])-self.exp
        return s
    def calc_exp_mats(self,exp):
        exp_mats={}
        exp_mats['2001']=exp/200
        return s
    def __init__(self,data):
        self.__dict__.update(data)
        if 'id' in data:self.charId=self.id
        self.__dict__.update(char_table[self.charId])
        self.colored=True
    def __str__(self):
        table="{0:{3}<10}\t{1:{3}<10}\t{2:{3}<10}\t"
        return table.format(f"{self.name}",f"精{self.evolvePhase} {self.level}级",f"{self.favorPercent}%",chr(12288))
class Item:
    @property
    def name(self):
        name=self.__dict__['name']
        if self.colored:return rcolor[self.rarity]+name+color.RESET
        return name
    def __init__(self,data):
        self.__dict__.update(data)
        if 'id' in data:self.itemId=self.id
        self.__dict__.update(item_table['items'][self.itemId])
        self.colored=True
    def __str__(self):
        table="{0}*{1} "
        return table.format(f"{self.name}",f"{self.count}")
class Mission:
    def update(self,new):
        self.__dict__.update(new)
    def __init__(self,data):
        self.__dict__.update(data)
        if self.type=='ACTIVITY':self.__dict__.update({})
        elif self.type=='OPENSERVER':self.__dict__.update({})
        else:self.__dict__.update(mission_table['missions'][self.id])
class Room:
    def update(self,new):
        self.__dict__.update(new)
    def __init__(self,data):
        self.__dict__.update(data)
        self.__dict__.update(building_data['rooms'][self.roomId])