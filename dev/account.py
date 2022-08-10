def login(player):
    r=player.api.account.login(**player.attr)
    player.gs.secret=r['secret']
def sync_data(player):
    r=player.api.account.syncData(**player.attr)
    if 'user' in r:player.init_data(r['user'])
    player.data.update(r['playerDataDelta'])