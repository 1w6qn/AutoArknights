from api import bind
import time
@bind("/mail/listMailBox")
def listMailBox(mailList:list,sysMailList):->dict
    return {"mailList":mailList,"sysMailList":sysMailList}
@bind("/mail/receiveMail")
def receiveMail(type:str,mailId:str):->dict
    return {"type":type,"mailId":mailId}
@bind("/mail/getMetaInfoList")
def getMetaInfoList():->dict
    return {"from":int(time.time())}
@bind("/mail/receiveAllMail")
def receiveAllMail(mailList:list,sysMailList):->dict
    return {"mailList":mailList,"sysMailList":sysMailList}
@bind("/mail/removeAllReceivedMail")
def removeAllReceivedMail():->dict
    return {}