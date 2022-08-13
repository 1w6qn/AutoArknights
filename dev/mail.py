import log
def auto_receive_mails(player):
    mails=[i['mailId']for i in player.api.mail.getMetaInfoList()['result']if i['state']]
    
    