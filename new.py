import api
import api.auth,api.account
from object import *
api.player=player.Player.load_from_json('user.json')[0]
p=api.player
p.uid="0"
t=api.auth.getToken(**p.attr)
p.gs.uid=t['uid']
p.uid=t['uid']
p.token=t['token']
p.gs.secret=api.account.login(**p.attr)['secret']
p.data.update(api.account.syncData())