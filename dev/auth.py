import log
def auth_login(player):
    r=player.api.auth.auth(**player.attr)
    player.channel_uid=r['uid']
    log.d(f"auth登录成功:access_token:{player.access_token}, channel_uid:{player.channel_uid}")
def user_login(player):
    r=player.api.auth.login(**player.attr)
    player.access_token=r['token']
    player.channel_uid=r['uid']
    log.d(f"auth登录成功:access_token:{player.access_token}, channel_uid:{player.channel_uid}")
def get_token(player):
    r=player.api.auth.getToken(**player.attr)
    player.uid=r['uid']
    player._gs_post=r['uid']
    player.token=r['token']
    log.d(f"token获取成功:token:{player.token}, uid:{player.uid}")