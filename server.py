import json
import requests
import config
import utils
class AuthServer:
    device_id=""
    device_id2=""
    device_id3=""
    def __init__(self,account,password,access_token):
        self.account=account
        self.password=password
        self.access_token=access_token
        self.device_id=utils.get_random_device_id()
        self.device_id2=utils.get_random_device_id2()
        self.device_id3=utils.get_random_device_id3()
        if access_token:self.auth_login()
        else:self.user_login()
    def post(self,cgi,data):
        sign_str=''
        for i in data:
            sign_str.join('{}={}&'.format(i,data[i]))
        sign=utils.u8_sign(sign_str[:-1])
        data.update({"sign":sign})
        return requests.post(config.HOST['AUTH']+cgi,data=json.dumps(data),headers=config.COMMON_HEADER).json()
    def user_login(self):
        data ={"account":self.account,"password":self.password,"deviceId":self.device_id,"platform":config.PLATFORM}
        j=self.post('/user/login',data)
        self.channel_uid=j['uid']
        self.access_token=j['token']
        utils.report(f"登录成功 channel_uid:{self.channel_uid} access_token:{self.access_token}")
    def auth_login(self):
        data={"token":self.access_token}
        j=self.post("/user/auth",data)
        self.channel_uid=j['uid']
        utils.report(f"登录成功 channel_uid:{self.channel_uid} access_token:{self.access_token}")
    def get_token(self,channel_id='1',sub_channel='1',world_id='1'):
        data={"appId":config.APP_ID,"channelId":channel_id,"deviceId":self.device_id,"deviceId2":self.device_id2,"deviceId3":self.device_id3,"extension":json.dumps({"uid":self.channel_uid,"access_token":self.access_token}),"platform":config.PLATFORM,"subChannel":sub_channel,"worldId":world_id}
        j=self.post("/u8/user/getToken",data)
        utils.report(f"登录成功 uid:{j['uid']} token:{j['token']}")
        return j['uid'],j['token']
class GameServer:
    def __init__(self,uid,token):
        self.uid=uid
        self.token=token
        self.seqnum=0
        self.secret=''
    def post(self,cgi,data):
        header={"uid":self.uid,"secret":self.secret,"seqnum":str(self.seqnum)}
        header.update(config.COMMON_HEADER)
        res=requests.post(config.HOST['GAME']+cgi,data=data,headers=header)
        if 'seqnum' in res.headers.keys() and res.headers['seqnum'].isdigit():
            self.seqnum=int(res.headers['seqnum'])
        else:
            self.seqnum+=1
        return res.json()
    def game_login(self,aus):
        data='''{{"networkVersion":"{}","uid":"{}","token":"{}","assetsVersion":"{}","clientVersion":"{}","platform":{},"deviceId":"{}","deviceId2":"{}","deviceId3":"{}"}}'''.format(config.NETWORK_VERSION, self.uid, self.token, config.RES_VERSION, config.CLIENT_VERSION, config.PLATFORM, aus.device_id,aus.device_id2, aus.device_id3)
        j=self.post("/account/login",data)
        self.secret=j["secret"]
        utils.report("游戏登录成功 uid:{} secret:{}".format(self.uid,self.secret))
