from api import bind
@bind("/gacha/cancelNormalGacha")
def cancelNormalGacha(slotId):
    return {"slotId":slotId}
@bind("/gacha/refreshTags")
def refreshTags(slotId):
    return {"slotId":slotId}
@bind("/gacha/syncNormalGacha")
def syncNormalGacha():
    return {}
@bind("/gacha/finishNormalGacha")
def finishNormalGacha(slotId):
    return {"slotId":slotId}
@bind("/gacha/normalGacha")
def normalGacha(slotId,tagList,specialTagId,duration):
    return {"slotId":slotId,"tagList":tagList,"specialTagId":specialTagId,"duration":duration}
@bind("/gacha/boostNormalGacha")
def boostNormalGacha(slotId,buy):
    return {"slotId":slotId,"buy":buy}
@bind("/gacha/getPoolDetail")
def getPoolDetail(poolId):
    return {"poolId":poolId}
@bind("/gacha/advancedGacha")
def advancedGacha(poolId,useTkt):
    return {"poolId":poolId,"useTkt":useTkt}
@bind("/gacha/tenAdvancedGacha")
def tenAdvancedGacha(poolId,useTkt):
    return {"poolId":poolId,"useTkt":useTkt}