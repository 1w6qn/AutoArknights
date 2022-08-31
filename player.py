import config,json,objects,random,time,server
from utils import *
gacha_table=load_json('/root/AutoArknights/gamedata/zh_CN/gamedata/excel/gacha_table.json')
class Player:
    __chars={}
    __items={}
    __missions={}
    __rooms={}
    def sync_data(self):
        self.api_sync_data()
        self.api_sync_status()
        self.api_sync_building()
        report("数据同步成功")
    def auto_recruit(self):
        self.api_sync_normal_gacha()
        for i in range(0,4):
            slot=self.recruit['normal']['slots'][str(i)]
            if not slot['state']:continue
            if slot['maxFinishTs']>self.time:continue
            if self.status['recruitLicense']==0:return
            if slot['state']==2:
                res=self.api_finish_normal_gacha(i)
                if not res['result']:
                    char_get=objects.Char(res["charGet"])
                    report(f"公招完成 slotId:{i} {char_get.isNew}获得{char_get.name} 获得{self.print_items(char_get.itemGet)}")
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
        if not self.checkIn["canCheckIn"]:
            report("已签到")
            return
        res=self.api_check_in()
        print(res)
        s="获得"
        for i in res['signInRewards']:
            item=objects.Item(i)
            s+=str(item)
        report(f"签到成功 {s}")
    def auto_buy_social_good(self):
        good_list=self.api_get_social_good_list()
        a=0
        buy_list=[]
        unavail_list=self.get_unavail_social_good_list()
        for i in range(0,len(good_list)):
            good=good_list[i]
            a+=good['price']
            afford=(a<=self.__dict__['status']['socialPoint'])
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
    def buy_social_good(self):
        print(f"当前信用点:{self.__dict__['status']['socialPoint']}")
        good_list=self.api_get_social_good_list()
        unavail_list=self.get_unavail_social_good_list()
        afford_list=[]
        for i in range(0,len(good_list)):
            good=good_list[i]
            if good['goodId'] in unavail_list:continue
            s=f"{i}. {good['displayName']}*{good['item']['count']} "
            if not (good['price']<=self.status['socialPoint']):
                s+=f"{color.RED}{good['price']}{color.RESET}"
            else:
                s+=f"{color.WHITE}{good['price']}{color.RESET}"
                afford_list.append(i)
            if good['discount']:
                s+=f"{color.GREEN}-{good['discount']*100}%{color.RESET}"
            print(s)
        if not afford_list :return
        buy_list=[int(i)for i in input("请选择:").split()]
        s=""
        for i in buy_list:
            s+=self.print_items(self.api_buy_social_good(good_list[i]['goodId'])['items'])
        report(f'获取信用商品成功 获得{s}')
    def get_unavail_social_good_list(self):
        unavail_list=[]
        for i in self.shop['SOCIAL']['info']:
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
            print(self.print_items(r['items']))
        else:report("无可收取邮件")
    def get_meeting_room_reward(self):
        res=self.api_get_meeting_room_reward([0,1])
        count=0
        for i in res['rewards']:
            count+=i['count']
        print(f"获得信用点*{count}")
    def settle_manufacture(self):
        room_slot_id_list=self.building['rooms']['MANUFACTURE']
        self.api_settle_manufacture(room_slot_id_list,1)
    def update_attr(self,new):
        if new.get("mission"):
            self.update_mission(new['mission'])
        merge_dict(self.__dict__,new)
        if new.get("troop",{}).get("chars"):
            for k,v in new['troop']['chars'].items():
                self.__chars[k].update(v)
    def update_mission(self,new):
        s=""
        for type,missions in new['missions'].items():
            if type=="DAILY":s+="日常任务更新"
            elif type=="WEEKLY":s+="周常任务更新"
            for id,data in missions.items():
                mission=self.__missions[type][id]
                mission.update(data)
                progress=mission.progress[0]
                s+=f"\n{mission.description} {progress['value']}/{progress['target']}"
                if progress['value']==progress['target']:
                    s+='( 已完成 )'
    def print_items(self,items):
        s=""
        for i in items:
            item=objects.Item(i)
            s+=str(item)
        return s
    @property
    def time(self):
        return int(time.time())
    def sort(self,l,type):
        return sorted(chars,key=lambda x:x.__dict__[self.sort[type]['type']],reverse=self.sort[type]['reverse'])
    @property
    def chars(self):
        chars=self.__chars.values()
        return self.sort(chars,'char')
    def init_chars(self):
        self.__chars={k:objects.Char(v)for k,v in self.troop['chars'].items()}
    def list_box(self):
        for i in self.chars:
            print(i)
    @property
    def rooms(self):return self.__rooms
    def init_rooms(self):
        for slotId,data in self.building['roomSlots'].items():
            room=objects.Room({'slotId':slotId}|data)
            room.update(self.building['rooms'][room.roomId][slotId])
            self.__rooms.update({slotId:room})
    @property
    def missions(self):return self.__missions
    def init_missions(self):
        for type,missions in self.mission['missions'].items():
            self.__missions.update({type:{}})
            for id,data in missions.items():
                data.update({"type":type,"id":id})
                mission=objects.Mission(data)
                self.__missions[type].update({id:mission})
    def __str__(self):
        return "uid:{}\n昵称:{}#{}\n等级:{}\n经验:{}".format(self.uid,self.status["nickName"],self.status['nickNumber'],self.status['level'],self.status['exp'])
    def __init__(self,gs,attr={}):
        self.gs=gs
        self.uid=gs.uid
        sort_config={'char':{'type':'rarity','reverse':True},'item':{'type':'sortId','reverse':True}}
        if attr:self.__dict__=attr
        else:self.sync_data()
        self.init_chars()
        self.init_missions()
    def post(self,cgi,data):
        res=self.gs.post(cgi,data)
        if res.get("user"):self.update_attr(res["user"])
        elif res.get("playerDataDelta",{}).get("modified"):self.update_attr(res["playerDataDelta"]["modified"])
        return res
    def api_sync_data(self):
        data=f'{{"platform":{config.PLATFORM}}}'
        res=self.gs.post("/account/syncData",data)
        if 'user' in res:merge_dict(self.__dict__,res['user'])
        else:self.update_attr(res)
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
        data=f'{{"slotId":{slot_id}}}'
        res=self.post('/gacha/finishNormalGacha',data)
        return res
    def api_cancle_normal_gacha(self,slot_id):
        data=f'{{"slotId":{slot_id}}}'
        res=self.post('/gacha/cancleNormalGacha',data)
        return res
    def api_boost_normal_gacha(self,slot_id,buy):
        data=f'{{"slotId":{slot_id},"buy":{buy}}}'
        res=self.post('/gacha/boostNormalGacha',data)
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
    def api_auto_confirm_missions(self, type):
        data = f'{{"type":"{type}"}}'
        res = self.post('/mission/autoConfirmMissions', data)
        return res
    def api_activity_checkin(self, activity_id, index):
        data = f'{{"index":{index},"activityId":"{activity_id}"}}'
        res = self.post('/activity/getActivityCheckInReward', data)
        return res
    def api_get_meta_info_list(self):
        data = f'{{"from":{self.time}}}'
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
        res = self.post('/charBuild/evolveChar',data)
        return res
    def api_boost_potential(self,char_inst_id,item_id,target_rank):
        data=f'{{"charInstId":{char_inst_id},"itemId":{item_id},"targetRank":{target_rank}}}'
        res=self.post('/charBuild/boostPotential',data)
        return res
    def api_upgrade_skill(self,char_inst_id,target_level):
        data=f'{{"charInstId":{char_inst_id},"targetLevel":{target_level}}}'
        res=self.post('/charBuild/upgradeSkill',data)
        return res
    def api_settle_manufacture(self,room_slot_id_list,supplement):
        data=f'{{"roomSlotIdList":{room_slot_id_list},"supplement":{supplement}}}'
        res=self.post('/building/settleManufacture',data)
        return res
    def api_get_meeting_room_reward(self,type):
        data=f'{{"type":{type}}}'
        res=self.post('/building/getMeetingroomReward',data)
        return res
    def api_recycle_charms(self,activity_id):
        data=f'{{"activityId":"{activity_id}"}}'
        res=self.post('/activity/recycleCharms',data)
        return res
    def api_template_shop_get_good_list(self,activity_id):
        data=f'{{"activityId":"{activity_id}"}}'
        res=self.post('/templateShop/getGoodList',data)
        return res