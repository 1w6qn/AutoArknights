from api import bind
@bind("/charBuild/evolveChar")
def evolveChar(charInstId:str)->dict :
    return {"charInstId":charInstId}
@bind("/charBuild/upgradeChar")
def evolveChar(charInstId:str,expMats:list)->dict :
    return {"charInstId":charInstId,"expMats":expMats}
@bind("/charBuild/setDefaultSkill")
def setDefaultSkill(charInstId:str,defaultSkillIndex:int)->dict :
    return {"charInstId":charInstId,"defaultSkillIndex:int":defaultSkillIndex}
@bind("/charBuild/boostPotential")
def boostPotential(charInstId:str,itemId:str,targetRank:int)->dict :
    return {"charInstId":charInstId,"itemId":itemId,"targetRank":targetRank}
@bind("/charBuild/upgradeSkill")
def upgradeSkill(charInstId:str,targetLevel:int)->dict :
    return {"charInstId":charInstId,"targetLevel":targetLevel}
@bind("/charBuild/changeCharSkin")
def changeCharSkin(charInstId:str,skinId:str)->dict :
    return {"charInstId":charInstId,"skinId":skinId}
@bind("/charBuild/changeCharTemplate")
def changeCharTemplate(charInstId:str,templateId:str)->dict :
    return {"charInstId":charInstId,"templateId":templateId}
@bind("/charBuild/changeCharSkin")
def changeCharSkin(charInstId:str,skinId:str)->dict :
    return {"charInstId":charInstId,"skinId":skinId}
@bind("/charBuild/getSpCharMissionReward")
def getSpCharMissionReward(charId:str,missionId:str)->dict :
    return {"charId":charId,"missionId":missionId}
@bind("/charBuild/evolveCharUseItem")
def evolveCharUseItem(charInstId:str,itemId:str,instId:str)->dict :
    return {"charInstId":charInstId,"itemId":itemId,"instId":instId}
@bind("/charBuild/setEquipment")
def setEquipment(charInstId:str,templateId:str,equipId:str)->dict :
    return {"charInstId":charInstId,"templateId":templateId,"equipId":equipId}
@bind("/charBuild/unlockEquipment")
def unlockEquipment(charInstId:str,templateId:str,equipId:str)->dict :
    return {"charInstId":charInstId,"templateId":templateId,"equipId":equipId}
@bind("/charBuild/addonStory/unlock")
def addonStory_unlock(charId:str,storyId:str)->dict :
    return {"charId":charId,"storyId":storyId}
@bind("/charBuild/addonStage/battleStart")
def addonStage_battleStart():return {}
@bind("/charBuild/addonStage/battleFinish")
def addonStage_battleFinish():return {}
@bind("/charBuild/batchSetCharVoiceLan")
def batchSetCharVoiceLan(voiceLan:str):
    return {"voiceLan":voiceLan}
@bind("/charBuild/setCharVoiceLan")
def setCharVoiceLan(charList:list,voiceLan:str):
    return {"charList":charList,"voiceLan":voiceLan}