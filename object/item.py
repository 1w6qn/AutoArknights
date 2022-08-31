from utils import *
#item_table=load_json('./gamedata/zh_CN/gamedata/excel/item_table.json')
class Item:
    def __init__(self,data):
        self.cnt=0
        self.__dict__.update(data)
        self.colored=True
        
    def __str__(self):
        table="{0}*{1} "
        return table.format(f"{self.name}",f"{self.cnt}")
    def __repr__(self):
        return self.__str__()
class ItemDatabase:
    _db=[]
    def _init(self,obj):
        gd=obj.gamedata
        for k,v in gd.item_table['items'].items():
            item=Item({"itemId":k}|v)
            self._db.append(item)
        self.init=True
    def __get__(self,obj,type):
        if not self.init:self._init(obj)
        return self
    def get(self,key,type='itemId'):
        return list(filter(lambda x:x.__dict__[type]==key,self))[0]
    def __set__(self,obj,val):
        if not self.init:self._init(obj)
        for k,v in val.items():self.get(k).cnt=v
        if not self.pdata_init:
            self.pdata_init=True
    def __iter__(self):
        self.i=-1
        self.db=list(filter(lambda x:x.cnt,self._db))
        return self
    def __next__(self):
        if self.i>=len(self.db)-1:
            raise StopIteration
        self.i+=1
        return self.db[self.i]
    def __init__(self):
        self.init=False
        self.pdata_init=False

def items2str(items):
    s=''
    for i in items:
        item=Item(i)
        s+=str(item)
    return s