import utils
class Level:
    def __init__(self,id):
        self.id=id.lower()
        data=utils.load_json('gamedata/zh_CN/gamedata/levels/'+self.id+'.json')
        self.__dict__.update(data)