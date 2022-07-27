import config,json,objects,random,time,server
from utils import *
gacha_table=load_json('./zh_CN/gamedata/excel/gacha_table.json')
class Player:
    chars=[]
    items={}
    attr={}
    def update_attr(self,new):
        merge_dict(self.attr,new)
        if new.get("troop",{}).get("chars"):
            chars=new['troop']['chars']
            for i in chars:
                self.chars[int(i)-1].update(chars[i])
        with open('player.txt','w') as f:
            f.write(json.dumps(self.attr))
    def init_inventory(self):
        for k,v in self.attr['inventory'].items():
            v.update({"itemId":k})
            self.items.update({k:objects.Item(v)})
    def get_inventory(self):
        return self.items
    def init_chars(self):
        for k,v in self.attr['troop']['chars'].items():
            self.chars.append(objects.Char(v))
    def get_chars(self):
        return self.chars
    def __str__(self):
        return "uid:{}\n昵称:{}#{}\n等级:{}\n经验:{}".format(self.uid,self.attr['status']["nickName"],self.attr['status']['nickNumber'],self.attr['status']['level'],self.attr['status']['exp'])
    def __init__(self,gs,attr={}):
        self.gs=gs
        self.uid=gs.uid
        if attr:self.attr=attr
        else:self.sync_data()
        self.init_chars()
    def post(self,cgi,data):
        res=self.gs.post(cgi,data)
        if res.get("user"):self.update_attr(res["user"])
        elif res.get("playerDataDelta").get("modified"):self.update_attr(res["playerDataDelta"]["modified"])
        return res
    def api_sync_data(self):
        data=f'{{"platform":{config.PLATFORM}}}'
        res=self.gs.post("/account/syncData",data)
        merge_dict(self.attr,res['user'])
        return res
    def api_sync_status(self):
        data =f'{{"modules":{config.MODULES},"params":{{"16":{{"goodIdMap":{{"LS":[],"HS":[],"ES":[],"CASH":[],"GP":["GP_Once_1"],"SOCIAL":[]}}}}}}}}'
        res=self.post('/account/syncStatus', data)
        return res
    def api_sync_building(self):
        res=self.post('/building/sync','{}')
        return res
    def sync_data(self):
        self.api_sync_data()
        self.api_sync_status()
        self.api_sync_building()
        report("数据同步成功")
    def api_sync_normal_gacha(self):
        res=self.post('/gacha/syncNormalGacha','{}')
        return res
    def api_normal_gacha(self,slot_id,tag_list,special_tag_id,duration):
        data=f'{{"slotId":{slot_id},"tagList":{tag_list},"specialTagId":{special_tag_id},"duration":{duration}}}'
        res=self.post('/gacha/normalGacha',data)
        return res
    def api_finish_normal_gacha(self,slot_id):
        data='{{"slotId":{}}}'.format(slot_id)
        res=self.post('/gacha/finishNormalGacha',data)
        return res
    def auto_recruit(self):
        self.api_sync_normal_gacha()
        for i in range(0,4):
            slot=self.attr['recruit']['normal']['slots'][str(i)]
            if not slot['state']:continue
            if slot['state']==2 and slot['maxFinishTs']<=time.time():
                res=self.api_finish_normal_gacha(i)
                if not res['result']:
                    char_get=objects.char(res["charGet"]["charId"],"0")
                    report(f"公招完成 slotId:{i} {res['charGet']['isNew']}获得{char_get.name}")
            tag_list,special_tag_id,duration=self.select_tag(slot['tags'])
            self.api_normal_gacha(i,tag_list,special_tag_id,duration)
    def auto_select_tag(self,tag_list):#WIP
        tags=random.choice(tag_list,k=3)
        return tags,0,32400
    def select_tag(self,tag_list):#手动选tag
        for i in tag_list:
            tag_name=gacha_table['gachaTags'][i-1]['tagName']
            tag_color=color.WHITE
            if i==11 or i==14:tag_color=color.YELLOW
            print(f"{i}.{tag_color}{tag_name}{color.RESET}",end=' ')
        print('')
        sp_tag=0
        duration=32400
        tags=[int(i)for i in input("请选择tag:").split()]
        if 11 in tags:sp_tag=11
        if 14 in tags:sp_tag=14
        if 28 in tags:duration=13800
        return tags,sp_tag,duration
    def api_get_unconfirmed_order_id_list(self):
        res=self.post('/pay/getUnconfirmedOrderIdList','{}')
        return res
    def api_check_in(self):
        res=self.post('/user/checkIn','{}')
        return res
    def api_advanced_gacha(self, pool_id, use_ticket):
        data = f'{{"poolId":"{pool_id}","useTkt":{use_ticket}}}'
        res = self.post('/gacha/advancedGacha', data)
        return res
    def api_squad_formation(self, squad_id, slots, change_skill = 0):
        data = f'{{"squadId":"{squad_id}","slots":{json.dumps(slots, ensure_ascii = False)},"changeSkill":{change_skill}}}'
        res = self.post('/quest/squadFormation', data, player)
        return res
    def api_confirm_mission(self, mission_id):
        data = f'{{"missionId":"{mission_id}"}}'
        res = self.post('/mission/confirmMission', data)
        return res
    def api_auto_confirm_mission(self, type):
        data = f'{{"type":"{type}"}}'
        res = self.post('/mission/autoConfirmMissions', data)
        return res
    def api_activity_checkin(self, activity_id, index):
        data = f'{{"index":{index},"activityId":"{activity_id}"}}'
        res = self.post('/activity/getActivityCheckInReward', data)
        return res
    def api_get_meta_info_list(self):
        data = f'{{"from":{time.localtime()}}}'
        res = self.post('/mail/getMetaInfoList', data)
        return res
    def api_recieve_mail(self, mail_id, mail_type):
        data = '{{"type":{mail_type},"mailId":{mail_id}}}'
        res = self.post('/mail/receiveMail', data)
        return res
    def api_receive_social_point(self):
        res=self.post("/social/receiveSocialPoint",'{}')
        return res
    def auto_get_social_good(self):
        good_list=self.api_get_social_good_list()
        a=0
        buy_list=[]
        unavail_list=self.get_unavail_social_good_list()
        for i in range(0,len(good_list)):
            good=good_list[i]
            a+=good['price']
            afford=(a<=self.attr['status']['socialPoint'])
            s="{}. {} ".format(i,good['displayName'])
            if not afford:
                s+="{}{}{}".format(color.RED,good['price'],color.RESET)
            else:
                if good_list[i]['goodId'] not in unavail_list:
                    buy_list.append(i)
                s+="{}{}{}".format(color.WHITE,good['price'],color.RESET)
            if good['discount']:
                s+="{}-{}%{}".format(color.GREEN,good['discount']*100,color.RESET)
            print(s)
        for i in buy_list:
            self.api_buy_social_good(good_list[i]['goodId'])
        report('获取信用商品成功: uid:{}'.format(self.uid))
    def get_unavail_social_good_list(self):
        unavail_list=[]
        for i in self.attr['shop']['SOCIAL']['info']:
            unavail_list.append(i['id'])
        return unavail_list
    def api_get_social_good_list(self):
        res=self.post('/shop/getSocialGoodList','{}')
        return res['goodList']
    def api_buy_social_good(self,good_id):
        data=f'{{"goodId":"{good_id}","count":1}}'
        res=self.post("/shop/buySocialGood",data)
        return res
    def api_gain_all_intimacy(self):
        res=self.post("/building/gainAllIntimacy",'{}')
        return res
    def api_use_item(self, inst_id, item_id, cnt):
        data = f'{{"instId":{inst_id},"itemId":"{item_id}","cnt":{cnt}}}'
        res = self.post('/user/useItem', data)
        return res
    def api_upgrade_char(self,char_inst_id,exp_mats):
        data=f'{{"charInstId":{char_inst_id},"expMats":{json.dumps(exp_mats)}}}'
        res = self.post('/charBuild/upgradeChar',data)
        return res
    def api_evolve_char(self,char_inst_id):
        data=f'{{"charInstId":{char_inst_id}}}'
        res = self.gs.post('/charBuild/evolveChar',data)
        return res