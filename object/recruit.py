from itertools import combinations as cb
class RecruitPool:
    def _calc_all(self,tags,chars,r={}):
        for i in [1,2,3]:
            for j in cb(tags,i):
                def f(tags,char,c=0):
                    for i in tags:
                        if i in char.tagList:c+=1
                    return c==len(tags)
                if res:=list(filter(lambda x:f(j,x),chars)):
                    r[j]=sorted(res,key=lambda x:x.rarity)
        return r
    def check(self,tags,r=2,result=None):
        if 11 in tags:r=5
        elif 14 in tags:r=4
        else:
            char_=list(filter(lambda x:2<=x.rarity<=4,self._data))
            for k,v in self._calc_all(tags,char_).items():
                if v[0].rarity<=r:continue
                r=v[0].rarity
                result=list(k)
        return 0 if r==2 else r,result
    def __get__(self,obj,type):
        self._data=obj._pool
        return self
    def __set__(self,obj,val):
        pass
class RecruitSlot:
    def __init__(self):
        pass
    def __get__(self,obj,type):
        #self._data=obj.load('gacha_table.json')
        return self
    def __set__(self,obj,val):
        raise AttributeError
    def update(self,data):
        self.__dict__.update(data)
class Recruit:
    pool=RecruitPool()
    slots=[RecruitSlot()for i in range(4)]
    def _pool_init(self,chars):
        def recr_filter(x):
            fix1=fix2=False
            if x.name not in self._detail:return False
            i=self._detail.index(x.name)
            fix1='\u4e00' <= self._detail[i-1] <= '\u9fff'
            fix2='\u4e00' <= self._detail[i+len(x.name)] <= '\u9fff'
            return not(fix1 or fix2)
        self._pool=list(filter(recr_filter,chars))
    def __init__(self):
        self._init=False
    def __get__(self,obj,type):
        if not self._init:
            self._detail=obj.gamedata.gacha_table['recruitDetail']+" "
            self._pool_init(obj.chars)
            self._init=True
        return self
    def __set__(self,obj,val):
        raise AttributeError
