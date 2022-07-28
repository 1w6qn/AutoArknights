import config,json,objects,random,time,server
from utils import *
gacha_table=load_json('./zh_CN/gamedata/excel/gacha_table.json')
class Player:
    chars=[]
    items={}
    attr={}
    def sync_data(self):
        self.api_sync_data()
        self.api_sync_status()
        self.api_sync_building()
        report("数据同步成功")
    def auto_recruit(self):
        self.api_sync_normal_gacha()
        for i in range(0,4):
            slot=self.attr['recruit']['normal']['slots'][str(i)]
            if not slot['state']:continue
            if slot['maxFinishTs']>time.time():continue
            if slot['state']==2:
                res=self.api_finish_normal_gacha(i)
                print(res)
                if not res['result']:
                    char_get=objects.Char(res["charGet"])
                    report(f"公招完成 slotId:{i} {char_get.attr['isNew']}获得{char_get.name} 获得{char_get.attr['itemGet']}")
            tag_list,special_tag_id,duration=self.select_tag(slot['tags'])
            self.api_normal_gacha(i,tag_list,special_tag_id,duration)
            report(f"公招成功 slotId:{i} tagList:{tag_list} duration:{duration}")
    def auto_select_tag(self,tag_list):#WIP
        tags=random.choice(tag_list,k=3)
        return tags,0,32400
    def get_tag_str(self,tag_id):
        tag_name=gacha_table['gachaTags'][tag_id-1]['tagName']
        tag_color=color.WHITE
        if tag_id==11 or tag_id==14:tag_color=color.YELLOW
        return f"{tag_id}.{tag_color}{tag_name}{color.RESET}"
    def select_tag(self,tag_list):#手动选tag
        s=""
        for i in tag_list:
            s+=self.get_tag_str(i)
        sp_tag=0
        duration=32400
        tags=[int(i)for i in input(f"{s}\n请选择tag:").split()]
        if 11 in tags:sp_tag=11
        if 14 in tags:sp_tag=14
        if 28 in tags:duration=13800
        return tags,sp_tag,duration
    def check_in(self):
        if self.attr["checkIn"]["canCheckIn"]:
            report("已签到")
            return
        res=self.api_check_in()
        s="获得"
        for i in res['signInReward']:
            item=objects.Item(i)
            s+=f" {item.name} {item.count}"
        report(f"签到成功 {s}")
    def auto_buy_social_good(self):
        good_list=self.api_get_social_good_list()
        a=0
        buy_list=[]
        unavail_list=self.get_unavail_social_good_list()
        for i in range(0,len(good_list)):
            good=good_list[i]
            a+=good['price']
            afford=(a<=self.attr['status']['socialPoint'])
            s=f"{i}. {good['displayName']} "
            if not afford:
                s+=f"{color.RED}{good['price']}{color.RESET}"
            else:
                if good_list[i]['goodId'] not in unavail_list:
                    buy_list.append(i)
                s+=f"{color.WHITE}{good['price']}{color.RESET}"
            if good['discount']:
                s+=f"{color.GREEN}-{good['discount']*100}%{color.RESET}"
            print(s)
        for i in buy_list:
            self.api_buy_social_good(good_list[i]['goodId'])
        report('获取信用商品成功')
    def get_unavail_social_good_list(self):
        unavail_list=[]
        for i in self.attr['shop']['SOCIAL']['info']:
            unavail_list.append(i['id'])
        return unavail_list
    def auto_confirm_missions(self):
        d=self.api_auto_confirm_missions("DAILY")
        w=self.api_auto_confirm_missions("WEEKLY")
    def auto_receive_mail(self):
        mail_list=self.api_get_meta_info_list()['result']
        norm,sys=[],[]
        for i in mail_list:
            if i['state'] or (not i['hasItem']):continue
            if i['type']:sys.append(i['mailId'])
            else:norm.append(i['mailId'])
        if not(norm and sys):
            r=self.api_receive_all_mail(norm,sys)
            report("邮件物品收取成功")
            self.print_items(r['items'])
        else:report("无可收取邮件")
    def update_attr(self,new):
        if new.get("mission"):
            self.update_mission(new['mission'])
        merge_dict(self.attr,new)
        if new.get("troop",{}).get("chars"):
            chars=new['troop']['chars']
            for i in chars:
                self.chars[int(i)-1].update(chars[i])
        with open('player.txt','w') as f:
            f.write(json.dumps(self.attr))
    def update_mission(self,new):
        s=""
        for type,missions in new.items():
            if type=="DAILY":s+="日常任务更新"
            elif type=="WEEKLY":s+="周常任务更新"
            for id,data in missions.items():
                data.update({"id":id})
                mission=objects.Mission(data)
                progress=mission.attr['progress'][0]
                s+=f"\n{mission.attr['description']} {progress['value']}/{progress['target']}"
                if progress['value']==progress['target']:
                    s+='( 已完成 )'
    def print_items(self,items):
        s=""
        for i in items:
            item=objects.Item(i)
            s+=f"{item.name}*{item.count} "
        print(s)
    def init_inventory(self):
        for k,v in self.attr['inventory'].items():
            v.update({"id":k})
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
        elif res.get("playerDataDelta",{}).get("modified"):self.update_attr(res["playerDataDelta"]["modified"])
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
    def api_ten_advanced_gacha(self, pool_id, use_ticket):
        data = f'{{"poolId":"{pool_id}","useTkt":{use_ticket}}}'
        res = self.post('/gacha/tenAdvancedGacha', data)
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
        data = f'{{"from":{int(time.time())}}}'
        res = self.post('/mail/getMetaInfoList', data)
        return res
    def api_receive_mail(self, mail_id, mail_type):
        data = f'{{"type":{mail_type},"mailId":{mail_id} }}'
        res = self.post('/mail/receiveMail', data)
        return res
    def api_receive_all_mail(self, mail_id_list, sys_mail_id_list):
        data = f'{{"mailIdList":{mail_id_list},"sysMailIdList":{sys_mail_id_list}}}'
        res = self.post('/mail/receiveAllMail', data)
        return res
    def api_list_mail_box(self, mail_id_list, sys_mail_id_list):
        data = f'{{"mailIdList":{mail_id_list},"sysMailIdList":{sys_mail_id_list}}}'
        res = self.post('/mail/listMailBox', data)
        return res
    def api_receive_social_point(self):
        res=self.post("/social/receiveSocialPoint",'{}')
        return res
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