from api import bind
@bind("/account/login")
def login(networkVersion,uid,token,assetsVersion,clientVersion,platform,device_id,device_id2,device_id3):
    return {"networkVersion":networkVersion,"uid":uid,"token":token,"assetsVersion":assetsVersion,"clientVersion":clientVersion,"platform":platform,"deviceId":deviceId,"deviceId2":deviceId2,"deviceId3":deviceId3}
@bind("/account/syncData")
def syncData():
    return {}
@bind("/account/syncStatus")
def syncStatus(modules,params):
    return {"modules":modules,"params":params}