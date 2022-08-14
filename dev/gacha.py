import log
import time
import object.character as ch
from object.item import items2str
from utils import *
from itertools import combinations as cb
recruit_pool={}
prof={'SNIPER':'狙击干员','MEDIC':'医疗干员','SUPPORT':'辅助干员','WARRIOR':'近卫干员','TANK':'重装干员','CASTER':'术师干员','PIONEER':'先锋干员','SPECIAL':'特种干员'}
#prof={'SNIPER':2,'MEDIC':4,'SUPPORT':5,'WARRIOR':1,'TANK':3,'CASTER':6,'PIONEER':8,'SPECIAL':7}
pos={'MELEE':'近战位','RANGED':'远程位'}
#pos={'MELEE':9,'RANGED':10}
rari={0:'支援机械',1:'新手',2:'',3:'',4:'资深干员',5:'高级资深干员'}
#rari={0:28,1:17,2:0,3:0,4:14,5:11}
gacha_table=load_json('./gamedata/zh_CN/gamedata/excel/gacha_table.json')
name_tags={i['tagName']:i['tagId'] for i in gacha_table['gachaTags']}
recruit_detail=gacha_table['recruitDetail']+" "
def recr_filter(x):
    name=x[1]['name']
    fix1,fix2=False,False
    if name not in recruit_detail:return False
    i=recruit_detail.index(name)
    fix1='\u4e00' <= recruit_detail[i-1] <= '\u9fff'
    fix2='\u4e00' <= recruit_detail[i+len(name)] <= '\u9fff'
    return not(fix1 or fix2)
for i in filter(recr_filter,ch.char_table.items()):
    name=i[1]['name']
    rarity=i[1]['rarity']
    profession=prof[i[1]['profession']]
    position=pos[i[1]['position']]
    r=rari[i[1]['rarity']]
    tag_list=i[1]['tagList']+[profession,position]
    if r:tag_list+=[r]
    recruit_pool.update({name:{'tagList':tag_list,'rarity':rarity}})
log.d("公招初始化成功")
def auto_finish_recruit(player):
    for id,slot in player.data.recruit['normal']['slots'].items():
        if not slot['state']:continue
        if slot['state']==2 and time.time()>=slot['maxFinishTs']:
            r=player.api.gacha.finishNormalGacha(player.gs,id)
            log.d(f"公招#{int(id)+1}完成")
            player.data.update(r['playerDataDelta']) 
def auto_recruit(player):
    for id,slot in player.data.recruit['normal']['slots'].items():
        if not slot['state']:continue
        if slot['state']==2 and time.time()>=slot['maxFinishTs']:
            r=player.api.gacha.finishNormalGacha(player.gs,id)
            char_get=ch.Character(r['charGet'])
            item_get=r['charGet']['itemGet']
            log.d(f"公招#{int(id)+1}完成 {char_get.isNew}获得{char_get.name} 获得 {items2str(item_get)}")
            player.data.update(r['playerDataDelta'])
        if not player.data.status['recruitLicense']:
            log.d("调用凭证不足")
            return
        tags,sp_tag,duration=auto_select_tags(slot['tags'])
        res=player.api.gacha.normalGacha(player.gs,id,tags,sp_tag,duration)
        player.data.update(res['playerDataDelta'])
        log.d(f"公招#{int(id)+1} 成功, 选中{tags}, 时长{duration}")
def calc_all(tags,chars):
    r={}
    for i in range(1,4):
        for j in cb(tags,i):
            def f(tags,char):
                c=0
                for i in tags:
                    if i in char[1]['tagList']:c+=1
                if c==len(tags):return True
                else:return False
            if res:=list(filter(lambda x:f(j,x),chars.items())):
                if j in r:r[j]+=res[0]
                else:r[j]=res[0]
    return r
def char_filter(tags,char):
    tag_list=char[1]['tagList']
    rarity=char[1]['rarity']
    max_rarity=4
    min_rarity=2
    if '高级资深干员' in tags:max_rarity=5
    if rarity>max_rarity or rarity<min_rarity:return 0
    return 1
def auto_select_tags(tags):
    if 14 in tags:sp_tag=14
    elif 11 in tags:sp_tag=11
    else:sp_tag=0
    tags=[gacha_table['gachaTags'][i-1]['tagName']for i in tags]
    char_=dict(filter(lambda x:char_filter(tags,x),recruit_pool.items()))
    r,duration=2,27600
    result=[]
    for k,v in calc_all(tags,char_).items():
        if char_[v[0]]['rarity']<=r:continue
        r=char_[v[0]]['rarity']
        result=list(k)
    print(f"选中{result}")
    res=[name_tags[i]for i in result]
    if r>2:duration=32400
    return res,sp_tag,duration
def advanced_gacha(player,pool_id):#0no 1normal 3free
    if pool_id[0:7]=='LIMITED' and player.data.gacha['limit'][pool_id]['leastFree']:tkt=3
    elif player.status['gachaTicket']:tkt=1
    else:tkt=0
    r= player.api.gacha.advancedGacha(player.gs,pool_id,tkt)
    char_get=ch.Character(r['charGet'])
    item_get=r['charGet']['itemGet']
    print(f"{pool_id}单抽成功 {char_get.isNew}获得{char_get.name} 获得 {items2str(item_get)}")
    player.data.update(r['playerDataDelta'])