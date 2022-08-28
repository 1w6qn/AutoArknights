from api import bind
@bind("/shop/getFurniGoodList")
def getFurniGoodList():
    return {}
"""		"shop/buyFurniGood"""
@bind("/shop/getSkinGoodList")
def getSkinGoodList(charIdList):
    return {"charIdList":charIdList}
@bind("/shop/getCashGoodList")
def getCashGoodList():
    return {}
@bind("/shop/getHighGoodList")
def getHighGoodList():
    return {}
@bind("/shop/getLowGoodList")
def getLowGoodList():
    return {}
@bind("/shop/getExtraGoodList")
def getExtraGoodList():
    return {}
@bind("/shop/getLMTGSGoodList")
def getLMTGSGoodList():
    return {}
@bind("/shop/getEPGSGoodList")
def getEPGSGoodList():
    return {}
@bind("/shop/getRepGoodList")
def getRepGoodList():
    return {}
@bind("/shop/getGPGoodList")
def getGPGoodList():
    return {}
@bind("/shop/getSocialGoodList")
def getSocialGoodList():
    return {}
@bind("/shop/getGoodPurchaseState")
def getGoodPurchaseState(goodIdMap):
    return {"goodIdMap":goodIdMap}
@bind("/shop/decomposePotentialItem")
def decomposePotentialItem(CharInstIdList):
    return {"charInstIdList":charInstIdList} 
"""		"shop/buyHighGood"; 
		"shop/buyExtraGood"; 
		"shop/buyLowGood"; 
		"shop/buyGPGood"; 
		"shop/buySkinGood"; 
		"/shop/buyFurniGroup"; 
		"shop/buyCashGood"; 
		"shop/buySocialGood"; 
		"shop/getCashGoodPurchaseResult"; 
		"shop/buyLMTGSGood"; 
		"shop/buyEPGSGood"; 
		"shop/buyRepGood"; 
		"shop/getVoucherSkinGoodList"; 
		"shop/useVoucherSkin"; 
"""