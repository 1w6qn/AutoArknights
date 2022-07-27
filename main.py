import server,player,utils,json
def load_from_json(filename):
    j=utils.load_json(filename)[0]
    return login(j['account'],j['password'],j['access_token'])
def login(account,password,access_token):
    aus=server.AuthServer(account,password,access_token)
    uid,token=aus.get_token()
    gs=server.GameServer(uid,token)
    gs.game_login(aus)
    return player.Player(gs)
def play(player):
    p.auto_recruit()
p=load_from_json('./user.json')
play(p)