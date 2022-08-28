import hmac,hashlib,json,random,string
import zipfile,io,base64
HMAC_KEY = '91240f70c09a08a6bc72af1a5c8d4670'
def decrypt_battle_replay(battle_replay):
    data=base64.b64decode(battle_replay)
    with zipfile.ZipFile(io.BytesIO(data), "r") as z_file:
        return z_file.read("default_entry").decode()
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
    sign = hmac.new(HMAC_KEY.encode(), data.encode(), hashlib.sha1)
    return sign.hexdigest()
def load_json(filename):
    with open(filename,'r') as f:
        return json.loads(f.read())
