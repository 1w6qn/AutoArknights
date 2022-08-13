import log
from utils import *
activity_table=load_json('./gamedata/zh_CN/gamedata/excel/activity_table.json')
class Activity:
    def __init__(self,data):
        self.__dict__.update(data)
        self.__dict__.update(activity_table['basicInfo'][self.id])