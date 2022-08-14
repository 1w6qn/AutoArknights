from api import bind
@bind("/mission/exchangeMissionRewards")
def exchangeMissionRewards(targetRewardsId):
    return {"targetRewardsId":targetRewardsId}
@bind("/mission/confirmMission")
def confirmMission(missionId):
    return {"missionId":missionId}
@bind("/mission/confirmMissionGroup")
def confirmMissionGroup(missionGroupId):
    return {"missionGroupId":missionGroupId}
@bind("/mission/autoConfirmMissions")
def autoConfirmMissions(type):
    return {"type":type}