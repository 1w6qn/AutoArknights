import hmac,hashlib,json,random,string
import time
import config
class color:
    RED="\033[31m"
    WHITE="\033[37m"
    GREEN="\033[32m"
    YELLOW="\033[33m"
    BLUE="\033[34m"
    MAGENTA="\033[35m"
    RESET="\033[0m"
rcolor=[color.WHITE,color.GREEN,color.BLUE,color.MAGENTA,color.YELLOW,color.RED]
def merge_dict(old, new):
    for k in new:
        if k in old:
            if not isinstance(new[k], dict):
                old[k] = new[k]
                continue
            merge_dict(old[k], new[k])
        else:
            old[k] = new[k]
    return
# md5
def GetMd5(src):
    m1 = hashlib.md5()
    m1.update(src.encode('utf-8'))
    return m1.hexdigest()
# 生成随机device_id
def get_random_device_id():
    return GetMd5(''.join(random.choices(string.ascii_letters + string.digits, k = 12)))
# 生成随机device_id2
def get_random_device_id2():
    return '86' + ''.join(random.choices(string.digits, k = 13))
# 生成随机device_id3
def get_random_device_id3():
    return GetMd5(''.join(random.choices(string.ascii_letters + string.digits, k = 12)))
def u8_sign(data):
    sign = hmac.new(config.HMAC_KEY.encode(), data.encode(), hashlib.sha1)
    return sign.hexdigest()
def report(data):
    msg=time.strftime("[%H:%M:%S]", time.localtime())+" "+data
    print(msg)
def load_json(filename):
    with open(filename,'r') as f:
        return json.loads(f.read())