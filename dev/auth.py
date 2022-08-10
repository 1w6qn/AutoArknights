def auth_login(player):
    r=player.api.auth.auth(**player.attr)
    player.channel_uid=r['uid']
def user_login(player):
    r=player.api.auth.login(**player.attr)
    player.access_token=r['token']
    player.channel_uid=r['uid']
def get_token(player):
    r=player.api.auth.getToken(**player.attr)
    player.gs.uid=r['uid']
    player.uid=player.gs.uid
    player.token=r['token']