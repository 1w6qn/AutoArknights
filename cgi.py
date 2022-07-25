#模拟客户端
import server,player,utils,json
utils.update_config()
aus= server.AuthServer('13105612936','zhu159637','Jvk9w1N8ls8d0McB5gTt2Jcj')
aus.auth_login()
uid,token=aus.get_token()
gs=server.GameServer(uid,token)
gs.game_login(aus)
p=player.Player(gs)
p.sync_data()
commands={"login":"p.login()"}
while True:
    s=input()
    if(s[0]=='/'):
        if s[1:] in commands.keys():
            eval(commands[s[1:]])