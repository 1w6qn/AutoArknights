from utils import *
char_table=load_json('./gamedata/zh_CN/gamedata/excel/character_table.json')
tag_table=load_json('./gamedata/zh_CN/gamedata/excel/gacha_table.json')['gachaTags']
favor_table=load_json('./gamedata/zh_CN/gamedata/excel/favor_table.json')
game_const=load_json('./gamedata/zh_CN/gamedata/excel/gamedata_const.json')

t={'SNIPER':2,'MEDIC':4,'SUPPORT':5,'WARRIOR':1,'TANK':3,'CASTER':6,'PIONEER':8,'SPECIAL':7,'MELEE':9,'RANGED':10,0:28,1:17,2:0,3:0,4:14,5:11}

favor_level=[]
for i in favor_table['favorFrames']:favor_level.append(i['level'])

class Tag:
    def __eq__(self,other):
        return self.id==other.id
    def __getattr__(self,name):
        key="tag"+name[0].upper()+name[1:]
        return self._data[key]
    def __init__(self,key):
        if isinstance(key,str):st="tagName"
        elif isinstance(key,int):st="tagId"
        self._data=filter(lambda x:key==x[st],tag_table)
class Character:
    def update(self,new):
        #old=str(self)
        self.attr=new
        #self.__dict__.update(new)
        #print(f"{old} -> {str(self)}")
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
    @property
    def isNew(self):
        return '新'if self.__dict__['isNew']else '重复'
    def calc_exp_cost(self,target_level):
        s=sum(game_const["characterExpMap"][self.evolvePhase][self.level-1:target_level])-self.exp
        return s
    def calc_exp_mats(self,exp,inventory):
        exp_mats={}
        exp_mats['2001']=exp/200
        return s
    def __init__(self,data):
        self.__dict__.update(data)
        if 'id' in data:self.charId=self.id
        self.__dict__.update(char_table[self.charId])
        self.colored=True
        self.tagList+=[t[self.profession],t[self.position],t[self.rarity]]
        self.tagList= [Tag(i)for i in self.tagList]
    def __str__(self):
        table="{0:{3}<10}\t{1:{3}<10}\t{2:{3}<10}\t"
        return table.format(f"{self.name}",f"精{self.evolvePhase} {self.level}级",f"{self.favorPercent}%",chr(12288))
