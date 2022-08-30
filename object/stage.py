import utils
from object.level import Level
db=utils.load_json('gamedata/zh_CN/gamedata/excel/stage_table.json')
class Stage:
    def __init__(self,id):
        self.__dict__.update(db['stages'][id])
        self.level=Level(self.levelId)