import log
from object.item import items2str
def check_in(player):
    res=player.api.user.checkIn(player.gs)
    print(res)
    player.data.update(res['playerDataDelta'])
    items_get=res['signInRewards']
    log.d(f"每日签到成功 获得 {items2str(items_get)}")