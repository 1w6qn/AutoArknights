from api import bind
@bind("/activity/gridGacha/gacha")
def gridGacha_gacha(activityId):
    return{"activityId":activityId}
@bind("/activity/gridGachaV2/doTodayGacha")
def gridGachaV2_doTodayGacha(activityId):
    return{"activityId":activityId}
@bind("/activity/tryGetCharmFirstReward")
def tryGetCharmFirstReward(activityId):
    return{"activityId":activityId}
@bind("/activity/recycleCharms")
def recycleCharms(activityId):
    return{"activityId":activityId}
@bind("/activity/getActivityCheckInReward")
def getActivityCheckInReward(activityId,index):
    return {"activityId":activityId,"index":index}