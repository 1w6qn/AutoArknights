
class RecruitPool:
    def __init__(self):
        self.init=False
    def __get__(self,obj,type):
        self._data=obj._pool
class RecruitSlot:
    def __init__(self):
        pass
    def __get__(self,obj,type):
        #self._data=obj.load('gacha_table.json')
        return self
    def __set__(self,obj,val):
        raise AttributeError
    def finish(self):
        r=self.api.gacha.finishNormalGacha(self.gs,self.slotId)
        self.update(r['playerDataDelta']['recruit'][self.slotId])
        return r
    def update(self,data):
        self.__dict__.update(data)
class Recruit:
    pool=RecruitPool()
    slots=[RecruitSlot()for i in range(4)]
    def __get__(self,obj,type):
        self._pool=obj.load('gacha_table.json')
        return self
    def __set__(self,obj,val):
        raise AttributeError