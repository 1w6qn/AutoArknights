from utils import *

t={'SNIPER':2,'MEDIC':4,'SUPPORT':5,'WARRIOR':1,'TANK':3,'CASTER':6,'PIONEER':8,'SPECIAL':7,'MELEE':9,'RANGED':10,0:28,1:17,2:0,3:0,4:14,5:11}
class Tag:
    def __eq__(self,other):
        if isinstance(other,Tag):return self.id==other.id
        elif isinstance(other,int):return self.id==other
        elif isinstance(other,str):return self.name==other
        return False
    def __getattr__(self,name):
        key="tag"+name[0].upper()+name[1:]
        return self._data[key]
    def __init__(self,data):
        self._data=data
    def __repr__(self):
        return self.name
class Character:
    def update(self,new):
        #old=str(self)
        #self.attr=new
        self.__dict__.update(new)
        #print(f"{old} -> {str(self)}")
    @property
    def maxExp(self):
        if self.level==self.maxLevel:return 0
        return self._expMap[self.evolvePhase][self.level-1]
    @property
    def maxLevel(self):
        return self._maxLevel[self.rarity][self.evolvePhase]
    @property
    def favorPercent(self):
        if self.favorPoint in self._favorLevel:return self.favorLevel.index(self.favorPoint)
        t=sorted(self._favorLevel+[self.favorPoint])
        return t.index(self.favorPoint)-1
    @property
    def isNew(self):
        return '新'if self.__dict__['isNew']else '重复'
    def __init__(self,data,expMap,favorLevel,maxLevel,tag_table):
        self.__dict__.update(data)
        self._expMap=expMap
        self._favorLevel=favorLevel
        self._maxLevel=maxLevel
        self.colored=True
        self.tagList+=[t[self.profession],t[self.position],t[self.rarity]]
        self.tagList= [tag_table.get(i)for i in self.tagList if i]
    def __str__(self):
        table="{0:{3}<10}\t{1:{3}<10}\t{2:{3}<10}\t"
        return table.format(f"{self.name}",f"精{self.evolvePhase} {self.level}级",f"{self.favorPercent}%",chr(12288))
class GachaTagDatabase:
    def get(self,key):
        if isinstance(key,int):return self._db[key]
        if isinstance(key,str):return list(filter(lambda x:x==key,self._db))[0]
    def __set__(self,obj,val):
        pass
    def __get__(self,obj,type):
        self._table=obj.gamedata.gacha_table['gachaTags']
        self._db=[Tag(i)for i in self._table]
        return self
    def __init__(self):
        self._init=False
class CharacterDatabase:
    _db=[]
    def __get__(self,obj,type):
        if not self.init:
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
        return self._db
    def get(self,key,type):
        filter(lambda x:x._d)
    def __set__(self,obj,val):
        
        if not self.pdata_init:
            for i in self._db:
                i.evolve=obj._api.charBuild.evolveChar,char.instId
            self.pdata_init=True
    def __init__(self):
        self.init=False
        self.pdata_init=False
