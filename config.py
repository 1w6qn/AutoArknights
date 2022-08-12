
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
NETWORK_CONFIG={}
if (SERVER == 'JP'):HOST["CONFIG"]= 'https://ak-conf.arknights.jp'
elif (SERVER == 'US'):HOST["CONFIG"]= 'https://ak-conf.arknights.global'
else:HOST["CONFIG"]= 'https://ak-conf.hypergryph.com'
