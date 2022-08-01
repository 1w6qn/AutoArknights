import server,player,utils,json
def load_from_json(filename):
    j=utils.load_json(filename)[1]
    return login(j['account'],j['password'],j['access_token'])
def login(account,password,access_token):
    aus=server.AuthServer(account,password,access_token)
    uid,token=aus.get_token()
    gs=server.GameServer(uid,token)
    gs.game_login(aus)
    return player.Player(gs)
def play(player):
    p.check_in()
    p.auto_receive_mail()
    p.auto_recruit()
    p.buy_social_good()
p=load_from_json('./user.json')
play(p)