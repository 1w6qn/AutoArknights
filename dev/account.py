import log
def login(player):
    r=player.api.account.login(**(player.attr|player.nc))
    log.d(f"游戏登录成功")
def sync_data(player):
    r=player.api.account.syncData(**player.attr)
    if 'user' in r:player.data=r['user']
    player.data=r['playerDataDelta']
    log.d(f"游戏数据同步成功")