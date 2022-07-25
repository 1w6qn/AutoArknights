import json,utils
with open('/root/AutoArknights/zh_CN/gamedata/excel/item_table.json','r') as f:
    item_info=json.loads(f.read())
with open('/root/AutoArknights/zh_CN/gamedata/excel/character_table.json','r') as f:
    char_info=json.loads(f.read())
with open('/root/AutoArknights/zh_CN/gamedata/excel/gamedata_const.json','r') as f:
    game_const=json.loads(f.read())
class Char:
    def update(self,new):
        print(f"{self.name} 精{self.get_evolve_phase()} {self.get_level()}/{self.get_max_level()}级 {self.get_exp()}/{self.get_max_exp()} -> 精{self.get_evolve_phase()} {self.get_level()}/{self.get_max_level()}级 {self.get_exp()}/{self.get_max_exp()}")
        self.attr.update(new)
    def get_max_exp(self):
        if self.get_level()==self.get_max_level():
            return 0
        return game_const["characterExpMap"][self.get_level()-1]
    def get_max_level(self):
        return game_const["maxLevel"][self.get_rarity()][self.get_evolve_phase()]
    def get_rarity(self):
        return self.attr["rarity"]
    def get_level(self):
        return self.attr["level"]
    def get_exp(self):
        return self.attr["exp"]
    def get_evolve_phase(self):
        return self.attr["evolvePhase"]
    def get_inst_id(self):
        return self.attr["instId"]
    def __init__(self,id,data):
        self.attr=char_info[id]
        self.id=id
        self.attr.update(data)
        self.name=self.attr["name"]
class Item:
    def __init__(self,id,count):
        self.attr=item_info['items'][id]
        self.count=count
    def __str__(self):
        return "{}{}{}:{}".format(utils.rcolor[self.attr['rarity']],self.attr["name"],utils.color.RESET,self.count)