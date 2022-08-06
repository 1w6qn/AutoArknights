from api import bind
@bind("/charBuild/evolveChar")
def evolveChar(charInstId):
    return {"charInstId":charInstId}
@bind("/charBuild/upgradeChar")
def evolveChar(charInstId,expMats):
    return {"charInstId":charInstId,"expMats":expMats}
@bind("/charBuild/setDefaultSkill")
def setDefaultSkill(charInstId,defaultSkillIndex):
    return {"charInstId":charInstId,"defaultSkillIndex":defaultSkillIndex}
@bind("/charBuild/boostPotential")
def boostPotential(charInstId,itemId,targetRank):
    return {"charInstId":charInstId,"itemId":itemId,"targetRank":targetRank}
@bind("/charBuild/upgradeSkill")
def upgradeSkill(charInstId,targetLevel):
    return {"charInstId":charInstId,"targetLevel":targetLevel}
@bind("/charBuild/changeCharSkin")
def changeCharSkin(charInstId,skinId):
    return {"charInstId":charInstId,"skinId":skinId}
@bind("/charBuild/changeCharTemplate")
def changeCharTemplate(charInstId,templateId):
    return {"charInstId":charInstId,"templateId":templateId}
@bind("/charBuild/changeCharSkin")
def changeCharSkin(charInstId,skinId):
    return {"charInstId":charInstId,"skinId":skinId}
@bind("/charBuild/getSpCharMissionReward")
def getSpCharMissionReward(charId,missionId):
    return {"charId":charId,"missionId":missionId}
@bind("/charBuild/evolveCharUseItem")
def evolveCharUseItem(charInstId,itemId,instId):
    return {"charInstId":charInstId,"itemId":itemId,"instId":instId}
@bind("/charBuild/setEquipment")
def setEquipment(charInstId,templateId,equipId):
    return {"charInstId":charInstId,"templateId":templateId,"equipId":equipId}
@bind("/charBuild/unlockEquipment")
def unlockEquipment(charInstId,templateId,equipId):
    return {"charInstId":charInstId,"templateId":templateId,"equipId":equipId}
@bind("/charBuild/addonStory/unlock")
def addonStory_unlock(charId,storyId):
    return {"charId":charId,"storyId":storyId}
@bind("/charBuild/addonStage/battleStart")
def addonStage_battleStart():return {}
@bind("/charBuild/addonStage/battleFinish")
def addonStage_battleFinish():return {}
@bind("/charBuild/batchSetCharVoiceLan")
def batchSetCharVoiceLan(voiceLan):
    return {"voiceLan":voiceLan}
@bind("/charBuild/setCharVoiceLan")
def setCharVoiceLan(charList,voiceLan):
    return {"charList":charList,"voiceLan":voiceLan}