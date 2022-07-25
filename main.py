import server,player,utils,json
def load_from_json(filename):
    j=utils.load_json(filename)[0]
    aus=server.AuthServer(j['account'],j['password'],j['access_token'])
    uid,token=aus.get_token()
    gs=server.GameServer(uid,token)
    return player.Player(gs)
def play(player):
    p.sync_data()
p=load_from_json('default.json')
play(p)