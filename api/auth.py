from api import bind
from functools import partial
import json
import config
bind=partial(bind,type='as')
@bind("/user/login")
def login(account,password,deviceId,platform):
    return {"account":account,"password":password,"deviceId":deviceId,"platform":platform}
@bind("/user/auth")
def auth(access_token):
    return {"token":access_token}
#"/pay/createOrderAppstore"; 
#"/pay/confirmOrderAppstore"; 
#"/pay/confirmOrderAppstoreNew"; 
@bind("/user/sendSmsCode")
def sendSmsCode(account,captcha,type):
    return {"account":account,"captcha":captcha,"type":type}
@bind("/u8/user/getToken")
def getToken(deviceId,deviceId2,deviceId3,channel_uid,access_token,platform,appId=config.APP_ID,channelId='1',subChannel='1',worldId='1'):
    return {"appId":appId,"channelId":channelId,"deviceId":deviceId,"deviceId2":deviceId2,"deviceId3":deviceId3,"extension":json.dumps({"uid":channel_uid,"access_token":access_token}),"platform":platform,"subChannel":subChannel,"worldId":worldId}
"""
		"/user/register"; 
		"/user/authenticateUserIdentity"; 
		"/user/checkIdCard"; 
		"/captcha/v1/register"; 
		"/user/v1/guestLogin"; 
		"/user/loginBySmsCode"; 
		"/online/v1/ping"; 
		"/online/v1/loginout"; 
		"/user/updateAgreement"; 
		"/user/changePassword"; 
		"/user/changePhoneCheck"; 
		"/user/changePhone"; 
		"""
		