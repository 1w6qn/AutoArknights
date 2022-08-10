from utils import *
item_table=load_json('./zh_CN/gamedata/excel/item_table.json')
class Item:
    @property
    def name(self):
        name=self.__dict__['name']
        if self.colored:return rcolor[self.rarity]+name+color.RESET
        return name
    def __init__(self,data):
        self.__dict__.update(data)
        if 'id' in data:self.itemId=self.id
        self.__dict__.update(item_table['items'][self.itemId])
        self.colored=True
    def __str__(self):
        table="{0}*{1} "
        return table.format(f"{self.name}",f"{self.count}")
