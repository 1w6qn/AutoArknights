from api import bind
import config
@bind("/account/login")
def login(uid,token,deviceId,deviceId2,deviceId3,platform=config.PLATFORM,networkVersion=config.NETWORK_VERSION,assetsVersion=config.RES_VERSION,clientVersion=config.CLIENT_VERSION):
    return {"networkVersion":networkVersion,"uid":uid,"token":token,"assetsVersion":assetsVersion,"clientVersion":clientVersion,"platform":platform,"deviceId":deviceId,"deviceId2":deviceId2,"deviceId3":deviceId3}
@bind("/account/syncData")
def syncData(platform=config.PLATFORM):
    return {"platform":platform}
@bind("/account/syncStatus")
def syncStatus(modules,params):
    return {"modules":modules,"params":params}