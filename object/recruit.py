class RecruitPool:
    def __init__(self,data):
        self.x=1
class RecruitSlot:
    def __init__(self,gs,data):
        self.gs=gs
        self.__dict__.update(data)
    def finish(self):
        r=self.api.gacha.finishNormalGacha(self.gs,self.slotId)
        self.update(r['playerDataDelta']['recruit'][self.slotId])
        return r
    def update(self,data):
        self.__dict__.update(data)