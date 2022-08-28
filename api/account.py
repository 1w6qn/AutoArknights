from api import bind
import config
@bind("/account/login")
def login(uid,token,deviceId,deviceId2,deviceId3,platform,configVer,resVersion,clientVersion):
    return {"networkVersion":configVer,"uid":uid,"token":token,"assetsVersion":resVersion,"clientVersion":clientVersion,"platform":platform,"deviceId":deviceId,"deviceId2":deviceId2,"deviceId3":deviceId3}
@bind("/account/syncData")
def syncData(platform):
    return {"platform":platform}
@bind("/account/syncStatus")
def syncStatus(modules,params):
    return {"modules":modules,"params":params}