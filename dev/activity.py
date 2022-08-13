import log
import random
from object.activity import Activity
def check_in(player,act):
    act=Activity(act[1]|{"id":act[0]})
    if 1 not in act.history:
        log.d(f"{act.name}无可用签到")
        return
    check_list=[i for i,h in enumerate(act.history)if h]
    for i in check_list:
        res=player.api.activity.getActivityCheckInReward(player.gs,act.id,i)
        print(res)
        player.data.update(res['playerDataDelta'])
        log.d(f"{act.name}第{i+1}天签到成功")
def get_login_reward(player,act):
    act=Activity(act[1]|{"id":act[0]})
    if not act.reward:
        log.d(f"{act.name}已领取")
        return
    res=player.api.activity.loginOnly_getReward(player.gs,act.id)
    print(res)
    player.data.update(res['playerDataDelta'])
    log.d(f"{act.name}领取成功")
def get_pray_reward(player,act):
    act=Activity(act[1]|{"id":act[0]})
    count=act.prayDaily
    if act.prayArray:
        log.d(f"{act.name}已签到")
        return
    pray_array=[random.randint(0,11)for i in range(count)]
    res=player.api.activity.prayOnly_getReward(player.gs,act.id,pray_array)
    print(res)
    player.data.update(res['playerDataDelta'])
    log.d(f"{act.name}签到成功")