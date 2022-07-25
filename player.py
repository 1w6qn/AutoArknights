import config,json,objects,random,time,server
from utils import *
gacha_table=load_json('zh_CN/gamedata/excel/gacha_table.json')
class Player:
    chars=[]
    def update_attr(self,new,print=True):
        if new.get("troop",default=[]).get("chars"):
            chars=new['troop']['chars']
            for i in chars:
                self.chars[int(i)-1].update(chars[i])
        utils.merge_dict(self.attr,new)
        with open('player.txt','w') as f:
            f.write(json.dumps(self.attr))
    def init_inventory(self):
        for i in self.attr['inventory']:
            self.items.append(objects.Item(i,self.attr['inventory'][i]))
    def get_inventory(self):
        return self.items
    def init_chars(self):
        for i in self.attr['troop']['chars']:
            self.chars.append(objects.Char(self.attr['troop']['chars'][i],i))
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
        else:self.update_attr(res["playerDataDelta"]["modified"])
        return res
    def api_sync_data(self):
        data=f'{{"platform":{config.PLATFORM}}}'
        res=self.gs.post("/account/syncData",data)
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
        res=self.gs.post('/gacha/finishNormalGacha',data)
        return res
    def auto_recruit(self):
        for i in range(0,4):
            slot=self.attr['recruit']['normal']['slots'][str(i)]
            if not slot['state']:continue
            if slot['state']==2 and slot['maxFinishTs']<=time.time():
                res=self.api_finish_normal_gacha(i)
                if not res['result']:
                    char_get=objects.char(res["charGet"]["charId"],"0")
                    utils.report(f"公招完成 slotId:{i} {res['charGet']['isNew']}获得{char_get.name}")
            tag_list,special_tag_id,duration=self.select_tag(slot['tags'])
            self.normal_gacha(i,tag_list,special_tag_id,duration)
    def auto_select_tag(self,tag_list):#WIP
        tags=random.choice(tag_list,k=3)
        return tags,0,32400
    def select_tag(self,tag_list):#手动选tag
        for i in tag_list:
            tag_name=gacha_info['gachaTags'][i-1]['tagName']
            tag_color=utils.color.WHITE
            if i==11 or i==14:tag_color=utils.color.YELLOW
            print(f"{i}.{tag_color}{tag_name}{utils.color.RESET}",end=' ')
        print('')
        sp_tag=0
        duration=32400
        tags=[int(i)for i in input("请选择tag:").split()]
        if 11 in tags:sp_tag=11
        if 14 in tags:sp_tag=11
        if 28 in tags:duration=13800
        return tags,sp_tag,duration
    def get_unconfirmed_order_id_list(self):
        res=self.gs.post('/pay/getUnconfirmedOrderIdList','{}')
        self.update_attr(res['playerDataDelta']['modified'])
    def check_in(self):
        res=self.gs.post('/user/checkIn','{}',player)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report("签到成功 uid:{} 同步时间:{}".format(self.uid,res['ts']))
    def advancedGacha(self, pool_id, use_ticket):
        data = '{{"poolId":"{}","useTkt":{}}}'.format(pool_id, use_ticket)
        res = self.gs.post('/gacha/advancedGacha', data)
    # 游戏数据差量更新
        self.update_attr(res['playerDataDelta']['modified'])
        is_new = '新' if res['charGet']['isNew'] else '重复'
        utils.report('单抽成功: uid:{}, 获得{}卡牌: {}'.format(self.uid, is_new, res['charGet']['charId']))
    def squad_formation(self, squad_id, slots, change_skill = 0):
        data = '{{"squadId":"{}","slots":{},"changeSkill":{}}}'.format(squad_id, json.dumps(slots, ensure_ascii = False), change_skill)
        res = self.gs.post('/quest/squadFormation', data, player)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('编队更新成功: uid:{}'.format(self.uid))
    def confirm_mission(self, mission_id):
        data = '{{"missionId":"{}"}}'.format(mission_id)
        res = self.gs.post('/mission/confirmMission', data)
        self.update_attr(res['playerDataDelta']['modified'])
        report('完成任务: uid:{}, mission_id:{}'.format(self.uid, mission_id))
    def auto_confirm_mission(self, type):
        data = '{{"type":"{}"}}'.format(type)
        res = self.gs.post('/mission/autoConfirmMissions', data)
        self.update_attr(res['playerDataDelta']['modified'])
        report('自动领取任务奖励: uid:{},'.format(self.uid, mission_id))
    def activity_checkin(self, activity_id, index):
        data = '{{"index":{},"activityId":"{}"}}'.format(index, activity_id)
        res = self.gs.post('/activity/getActivityCheckInReward', data)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('活动签到完成: uid:{}, 活动id:{}, 当前签到次数:{}'.format(self.uid, activity_id, index))
    def get_meta_info_list(self):
        data = '{{"from":{}}}'.format(time.localtime())
        res = self.gs.post('/mail/getMetaInfoList', data)
    # 游戏数据差量更新
        self.update_attr(res['playerDataDelta']['modified'])
        unread_mail_list = []
        has_item = False
        for mail in res['result']:
            if 0 == mail['state']:
                unread_mail_list.append({'mailId': mail['mailId'], 'type': mail['type']})
                if mail['hasItem']:
                    has_item = True
        utils.report('成功获取邮件列表: uid:{}, 未读邮件数:{}, 是否有物品:{}'.format(self.uid, len(unread_mail_list), has_item))
        return unread_mail_list
    def recieve_mail(self, mail_id, mail_type):
        data = '{{"type":{},"mailId":{}}}'.format(mail_type, mail_id)
        res = self.gs.post('/mail/receiveMail', data)
    # 游戏数据差量更新
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('邮件收取成功: uid:{}, 邮件id:{}'.format(self.uid, mail_id))
    def receive_social_point(self):
        res=self.gs.post("/social/receiveSocialPoint",'{}')
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('收取信用成功: uid:{}'.format(self.uid ))
    def auto_get_social_good(self):
        good_list=self.get_social_good_list()
        a=0
        buy_list=[]
        unavail_list=self.get_unavail_social_good_list()
        for i in range(0,len(good_list)):
            good=good_list[i]
            a+=good['price']
            afford=(a<=self.attr['status']['socialPoint'])
            s="{}. {} ".format(i,good['displayName'])
            if not afford:
                s+="{}{}{}".format(utils.color.RED,good['price'],utils.color.RESET)
            else:
                if good_list[i]['goodId'] not in unavail_list:
                    buy_list.append(i)
                s+="{}{}{}".format(utils.color.WHITE,good['price'],utils.color.RESET)
            if good['discount']:
                s+="{}-{}%{}".format(utils.color.GREEN,good['discount']*100,utils.color.RESET)
            print(s)
        for i in buy_list:
            self.buy_social_good(good_list[i]['goodId'])
        utils.report('获取信用商品成功: uid:{}'.format(self.uid))
    def get_unavail_social_good_list(self):
        unavail_list=[]
        for i in self.attr['shop']['SOCIAL']['info']:
            unavail_list.append(i['id'])
        return unavail_list
    def get_social_good_list(self):
        res=self.gs.post('/shop/getSocialGoodList','{}')
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('同步信用商品成功: uid:{}'.format(self.uid))
        return res['goodList']
    def buy_social_good(self,good_id):
        data='{{"goodId":"{}","count":1}}'.format(good_id)
        res=self.gs.post("/shop/buySocialGood",data)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('购买信用商品成功: uid:{}'.format(self.uid))
    def gain_all_intimacy(self):
        res=self.gs.post("/building/gainAllIntimacy",'{}')
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('收取信赖成功: uid:{}'.format(self.uid ))
    def use_item(self, inst_id, item_id, cnt):
        data = '{{"instId":{},"itemId":"{}","cnt":{}}}'.format(inst_id, item_id, cnt)
        res = self.gs.post('/user/useItem', data)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('道具使用成功: uid:{}, 道具id:{}, 道具剩余数量:{}'.format(self.uid, item_id, self.attr['consumable'][item_id][inst_id]['count']))
    def upgrade_char(self,char_inst_id,exp_mats):
        data='{{"charInstId":{},"expMats":{}}}'.format(inst_id, json.dumps(exp_mats))
        res = self.gs.post('/charBuild/upgradeChar',data)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report(f'干员升级成功: uid:{self.uid}')
    def evolve_char(self,char_inst_id):
        data='{{"charInstId":{}}}'.format(inst_id)
        res = self.gs.post('/charBuild/evolveChar',data)
        self.update_attr(res['playerDataDelta']['modified'])
        utils.report('干员精英化成功: uid:{}'.format(self.uid))