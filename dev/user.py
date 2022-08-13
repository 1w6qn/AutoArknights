import log
def check_in(player):
    can_check_in=player.data.checkIn['canCheckIn']
    if can_check_in:
        res=player.api.user.checkIn(player.gs)
        print(res)
        player.data.update(res['playerDataDelta'])
        log.d(f"每日签到成功")
    else:log.d("已签到")