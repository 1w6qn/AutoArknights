from api import bind
import time
@bind("/mail/listMailBox")
def listMailBox(mailList,sysMailList):
    return {"mailList":mailList,"sysMailList":sysMailList}
@bind("/mail/receiveMail")
def receiveMail(type,mailId):
    return {"type":type,"mailId":mailId}
@bind("/mail/getMetaInfoList")
def getMetaInfoList():
    return {"from":int(time.time())}
@bind("/mail/receiveAllMail")
def receiveAllMail(mailList,sysMailList):
    return {"mailList":mailList,"sysMailList":sysMailList}
@bind("/mail/removeAllReceivedMail")
def removeAllReceivedMail():
    return {}