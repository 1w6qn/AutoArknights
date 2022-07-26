import log
import time
from object.item import items2str
from utils import *
def finish_recruit(player,id):
    r=player.api.gacha.finishNormalGacha(player.gs,id)
    char_get=player.data.chars.get(r['charGet']['id'])
    item_get=r['charGet']['itemGet']
    player.data.update(r['playerDataDelta'])
    log.d(f"公招#{int(id)+1}完成 {char_get.isNew}获得{char_get.name} 获得 {items2str(item_get)}")
def auto_recruit(player):
    for id,slot in player.data.recruit['normal']['slots'].items():
        if not slot['state']==1:continue
        if not player.data.status['recruitLicense']:
            continue
        duration=27600
        rget,tags=player.data.recruit.pool.check(slot['tags'])
        if tags==None and rget>3:
            log.d('发现稀有 tag请自行选择')
            continue
        if rget:duration=32400
        if tags==None and rget==0:tags=[]
        res=recruit(player,id,tags,sp_tag,duration)
        print(res)
def recruit(player,id,tags,sp_tag,duration):
    r=player.api.gacha.normalGacha(player.gs,id,tags,sp_tag,duration)
    if 'error' in r:log.e(r['msg']);return
    player.data.update(r['playerDataDelta'])
    log.d(f"公招#{int(id)+1} 成功, 选中{tags}, 时长{duration}")
    return r
def advanced_gacha(player,pool_id):#0no 1normal 3free
    if pool_id[0:7]=='LIMITED' and player.data.gacha['limit'][pool_id]['leastFree']:tkt=3
    elif player.data.status['gachaTicket']:tkt=1
    else:tkt=0
    r= player.api.gacha.advancedGacha(player.gs,pool_id,tkt)
    char_get=player.data.chars.get(r['charGet']['id'])
    item_get=r['charGet']['itemGet']
    print(f"{pool_id}单抽成功 {char_get.isNew}获得{char_get.name} 获得 {items2str(item_get)}")
    player.data.update(r['playerDataDelta'])