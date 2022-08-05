from api import bind
@bind("/gacha/cancelNormalGacha")
def cancelNormalGacha(slotId:str):->dict
    return {"slotId":slotId}
@bind("/gacha/refreshTags")
def refreshTags(slotId:str):->dict
    return {"slotId":slotId}
@bind("/gacha/syncNormalGacha")
def syncNormalGacha():->dict
    return {}
@bind("/gacha/finishNormalGacha")
def finishNormalGacha(slotId:str):->dict
    return {"slotId":slotId}
@bind("/gacha/normalGacha")
def normalGacha(slotId:str,tagList:list,specialTagId:int,duration:int):->dict
    return {"slotId":slotId,"tagList":tagList,"specialTagId":specialTagId,"duration":duration}
@bind("/gacha/boostNormalGacha")
def boostNormalGacha(slotId:str,buy:int):->dict
    return {"slotId":slotId,"buy"buy}
@bind("/gacha/getPoolDetail")
def getPoolDetail():->dict
    return {}
@bind("/gacha/advancedGacha")
def advancedGacha(poolId:str,useTkt:int):->dict
    return {"poolId":poolId,"useTkt":useTkt}
@bind("/gacha/tenAdvancedGacha")
def tenAdvancedGacha(poolId:str,useTkt:int):->dict
    return {"poolId":poolId,"useTkt":useTkt}