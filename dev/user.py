import log
def check_in(player):
    can_check_in=player.data.checkIn['canCheckIn']
    if can_check_in:
        player.api.user.checkin()
        log.d(f"每日签到成功")
    else:log.d("已签到")