import log
from object.item import items2str
def auto_receive_mails(player):
    mail_list,sys_mail_list=[],[]
    for i in player.api.mail.getMetaInfoList(player.gs)['result']:
        if i['state']:continue
        if not i['hasItem']:continue
        if i['type']:sys_mail_list+=[i['mailId']]
        else:mail_list+=[i['mailId']]
    r=player.api.mail.receiveAllMail(player.gs,mail_list,sys_mail_list)
    print(r)
    log.d(f"邮件收取成功")