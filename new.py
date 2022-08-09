import api
import api.auth,api.account
from object import *
api.player=player.Player.load_from_json('user.json')[0]
p=api.player
p.channel_uid="0"
t=api.auth.getToken(**p.attr)
p.gs.uid=t['uid']
p.token=t['token']
p.gs.secret=api.account.login(**(p.attr|p.gs.attr))['secret']
r=api.account.syncData(**p.attr)
p.init_data(r['user'])
p.data.update(r['playerDataDelta'])