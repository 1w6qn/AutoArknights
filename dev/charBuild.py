def evolve(player,char):
    player.api.charBuild.evolveChar(char.instId)
def upgrade(player,char,target):
    delta=char.calc_exp_cost(target)
    exp_mats=[{"id":"2004","count":0},{"id":"2003","count":0},{"id":"2002","count":0},{"id":"2001","count":0}]
    for i in exp_mats:
        if delta<=200:
            exp_mats["2001"]["count"]+=1
            break
        cur=player.data["inventory"][i]
        id=exp_mats[i]['id']
        weight=2000 if id=="2004" else 1000 if id=="2003" else 400 if id=="2002" else 200
        cnt=min(delta//weight,cur)
        delta-=cnt*weight
        exp_mats[i]["count"]+=cnt
    player.api.charBuild.upgradeChar(char.instId,exp_mats)
