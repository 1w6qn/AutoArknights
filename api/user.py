from api import bind
@bind("/user/bindNickName")
def bindNickName(nickName):
    return {"nickName":nickName}
@bind("/user/buyAp")
def buyAp():return {}
@bind("/user/exchangeDiamondShard")
def exchangeDiamondShard(count):
    return{"count":count}
@bind("user/changeResume")
def changeResume(resume):
    return {"resume":resume}
@bind("/user/useItem")
def useItem(instId,itemId,cnt):
    return {"instId":instId,"itemId":itemId,"cnt":cnt}
@bind("/user/useItems")
def useItems(items):
    return {"items":items}
@bind("/user/useRenameCard")
def useRenameCard(instId,itemId,nickName):
    return {"instId":instId,"itemId":itemId,"nickName":nickName}
@bind("/user/checkIn")
def checkIn():return {}
@bind("/user/changeSecretary")
def changeSecretary(charInstId,skinId):
    return {"charInstId":charInstId,"skinId":skinId}
@bind("/user/receiveTeamCollectionReward")
def receiveTeamCollectionReward(rewardId):
    return {"rewardId":rewardId}
@bind("/user/changeAvatar")
def changeAvatar(type,id):
    return{"type":type,"id":id}