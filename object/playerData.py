from utils import *
from object.character import Character
class PlayerData:
    __chars=[]
    @property
    def chars(self):
        key=self.sort_list|{"key":lambda x:x.__dict__[self.sort_list['key']]}
        return sorted(self.__chars,**key)
    def list_box(self):
        for i in self.chars:print(i)
    def __init__(self,data):
        self.__dict__.update(data)
        #self.__chars=list(range(1,data['troop']['curCharInstId']))
        self.sort_list={"key":"rarity","reverse":True}
        self.__chars=[Character(v)for k,v in data['troop']['chars'].items()]
    def update(self,new):
        modified=new['modified']
        merge_dict(self.__dict__,modified)
        if c:=modified.get('troop',{}).get('chars'):
            for k,v in c.items():self.__chars[int(k)-1].update(v)
