from api import bind
@bind("/templateShop/getGoodList")
def getGoodList(shopId):
    return {"shopId":shopId}
@bind("templateShop/buyGood")
def buyGood(shopId,goodId,count):
    return {"shopId":shopId,"goodId":goodId,"count":count}