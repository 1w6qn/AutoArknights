from utils import *
char_table=load_json('./gamedata/zh_CN/gamedata/excel/character_table.json')
favor_table=load_json('./gamedata/zh_CN/gamedata/excel/favor_table.json')
game_const=load_json('./gamedata/zh_CN/gamedata/excel/gamedata_const.json')
favor_level=[]
for i in favor_table['favorFrames']:favor_level.append(i['level'])
class Character:
    class data:
        def __init__(self,name,value):
            self.value=value
            self.name=name
        def __get__(self,inst,owner):
            return self.value
        def __set__(self,inst,value):
            self.value=value
        def __str__(self):
            return f"{self.name}:{self.value}"
    def update(self,new):
        #old=str(self)
        self.attr=new
        #self.__dict__.update(new)
        #print(f"{old} -> {str(self)}")
    def __getattr__(self,item):
        if item not in self.attr:return None
        return self.data(item,self.attr[item])
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
    def calc_exp_mats(self,exp,inventory):
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