import utils
db=utils.load_json('gamedata/zh_CN/gamedata/levels/enemydata/enemy_database.json')
class Enemy:
    def _load(self,data,f=''):
        for k,v in data.items():
            if not v:continue
            if k=='attributes':self._load(v,f='attr_')
            elif v.get('m_defined'):self.__dict__[f+k]=v['m_value']
    def __init__(self,id,level):
        self.id=id
        self.level=level
        data=list(filter(lambda x:x['Key']==self.id,db['enemies']))[0]['Value'][self.level]['enemyData']
        self._load(data)