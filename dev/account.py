import log
def login(player):
    r=player.api.account.login(**player.attr)
    player.gs.secret=r['secret']
    log.d(f"游戏登录成功: secret:{player.gs.secret}")
def sync_data(player):
    r=player.api.account.syncData(**player.attr)
    if 'user' in r:player.init_data(r['user'])
    player.data.update(r['playerDataDelta'])
    log.d(f"游戏数据同步成功")