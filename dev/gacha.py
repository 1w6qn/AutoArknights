import log
import time
import object.character as ch
from utils import *
recruit_pool={}
prof={'SNIPER':'狙击干员','MEDIC':'医疗干员','SUPPORT':'辅助干员','WARRIOR':'近卫干员','TANK':'重装干员','CASTER':'术师干员','PIONEER':'先锋干员','SPECIAL':'特种干员'}
gacha_table=load_json('./gamedata/zh_CN/gamedata/excel/gacha_table.json')
def recr_filter(x):
    return x[1]['name'] in gacha_table['recruitDetail']
for i in filter(recr_filter,ch.char_table.items()):
    name=i[1]['name']
    rarity=i[1]['rarity']
    profession=prof[i[1]['profession']]
    tag_list=i[1]['tagList']+[profession]
    recruit_pool.update({name:{'tagList':tag_list,'rarity':rarity}})
def auto_normal_gacha(player):
    for id,slot in player.data.recruit['normal']['slots'].items():
        if slot['state']==3:continue
        if slot['state']==2 and time.time()>=slot['maxFinishTs']:
            r=player.api.gacha.finishNormalGacha(id)
            log.d("公招#{int(id)+1}完成")
            player.data.update(r['playerDataDelta'])
        tags,sp_tag,duration=auto_select_tags(slot['tags'])
def calc_sort(tags,char):
    if 11 in char['tagList']:id=0
    if 14 in char['tagList']:id=50
    else:id=char['rarity']*100
    for i in tags:
        if i in char['tagList']:id+=1
    return id
def auto_select_tags(tags):
    tags=[gacha_table[i-1]for i in tags]
    char_=sorted(recruit_pool.keys(),key=lambda x:calc_sort(tags,x))
    return char_