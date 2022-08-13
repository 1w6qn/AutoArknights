import log
import random
from object.activity import Activity
def check_in(player):
    acts=player.data.activity['CHECKIN_ONLY']
    if not acts.keys():
        log.d("无可用签到活动")
        return
    for k,v in acts.items():
        act=Activity(v|{"id":k})
        check_list=[i for i,h in enumerate(v['history'])if h]
        if not check_list:
            log.d(f"{act.name}无可用签到")
            return
        for i in check_list:
            res=player.api.activity.getActivityCheckInReward(player.gs,k,i)
            print(res)
            player.data.update(res['playerDataDelta'])
            log.d(f"{act.name}第{i+1}天签到成功")
def get_login_reward(player):
    acts=player.data.activity['LOGIN_ONLY']
    if not acts.keys():
        log.d("无可用登录活动")
        return
    for k,v in acts.items():
        act=Activity(v|{"id":k})
        if not act.reward:
            log.d(f"{act.name}已领取")
            return
        res=player.api.activity.loginOnly_getReward(player.gs,k)
        print(res)
        player.data.update(res['playerDataDelta'])
        log.d(f"{act.name}领取成功")
def get_pray_reward(player):
    acts=player.data.activity['PRAY_ONLY']
    if not acts.keys():
        log.d("无可用幸运墙活动")
        return
    for k,v in acts.items():
        act=Activity(v|{"id":k})
        count=act.prayDaily
        if act.prayArray:
            log.d(f"{act.name}已签到")
            return
        pray_array=[random.randint(0,11)for i in range(count)]
        res=player.api.activity.prayOnly_getReward(player.gs,k,pray_array)
        print(res)
        player.data.update(res['playerDataDelta'])
        log.d(f"{act.name}签到成功")