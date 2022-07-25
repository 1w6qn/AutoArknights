import requests,json
PLATFORM_ID='Android'
SERVER="CN"
PLATFORM=1
HOST={'PASSPORT':'','AUTH':'','GAME':'','CONFIG':'','VERSION':''}
SERVER_ID='3'
RES_VERSION=''
CLIENT_VERSION=''
NETWORK_VERSION='5'
APP_ID='1'
MODULES=1631
HMAC_KEY = '91240f70c09a08a6bc72af1a5c8d4670'
COMMON_HEADER ={
    'Content-Type': 'application/json',
    'X-Unity-Version': '2017.4.39f1',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; X Build/V417IR)',
    'Connection': 'Keep-Alive'
}
PASSPORT_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 6.0.1; X Build/V417IR)',
    'Connection': 'Keep-Alive'
}
if (SERVER == 'JP'):
    HOST["PASSPORT"]= 'https://passport.arknights.jp'
    HOST["AUTH"] = 'https://as.arknights.jp'
    HOST["GAME"]= 'https://gs.arknights.jp:8443'
    HOST["CONFIG"]= 'https://ak-conf.arknights.jp'
    HOST["VERSION"] = "https://ark-jp-static-online.yo-star.com/assetbundle/official/{}/version".format(PLATFORM_ID)
elif (SERVER == 'US'):
    HOST["PASSPORT"] = 'https://passport.arknights.global'
    HOST["AUTH"]= 'https://as.arknights.global'
    HOST["GAME"]= 'https://gs.arknights.global:8443'
    HOST["CONFIG"]= 'https://ak-conf.arknights.global'
    HOST["VERSION"]= "https://ark-us-static-online.yo-star.com/assetbundle/official/{}/version".format(PLATFORM_ID)
else:
    HOST["AUTH"] = 'https://as.hypergryph.com'
    HOST["GAME"]= 'https://ak-gs-gf.hypergryph.com'
    HOST["CONFIG"]= 'https://ak-conf.hypergryph.com'
    HOST["VERSION"]= "https://ak-conf.hypergryph.com/config/prod/official/{}/version".format(PLATFORM_ID)
def get_from_conf(url):
    return requests.get(url,headers=COMMON_HEADER).json()
def update_config():
    global NETWORK_VERSION,RES_VERSION,CLIENT_VERSION
    res=get_from_conf(HOST['CONFIG']+"/config/prod/official/network_config")
    NETWORK_VERSION=json.loads(res["content"])["configVer"]
    v=get_from_conf(HOST['VERSION'])
    RES_VERSION,CLIENT_VERSION=v['resVersion'],v['clientVersion']
    report(f"资源更新成功 ResVersion:{RES_VERSION} ClientVersion:{CLIENT_VERSION}")
update_config()