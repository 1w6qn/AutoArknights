from api import bind
@bind("/quest/changeSquadName")
def changeSquadName(squadId,name):
    return {"squadId":squadId,"name":name}
@bind("/quest/getAssistList")
def getAssistList(profession,askRefresh,currSquadId):
    return {"profession":profession,"askRefresh":askRefresh,"currSquadId":currSquadId}
@bind("/quest/battleStart")
def battleStart(stageId,usePracticeTicket):
    return{"stageId":stageId,"usePracticeTicket":usePracticeTicket}
#		"/quest/battleFinish"; 
@bind("/quest/saveBattleReplay")
def saveBattleReplay(battleReplay,battleId):
    return {"battleReplay":battleReplay,"battleId":battleId}
@bind("/quest/getBattleReplay")
def getBattleReplay(stageId):
    return {"stageId":stageId}
@bind("/quest/finishStoryStage")
def finishStoryStage(stageId):
    return {"stageId":stageId}
@bind("/quest/unlockStageFog")
def unlockStageFog(stageId):
    return {"stageId":stageId}
@bind("/quest/getCowLevelReward")
def getCowLevelReward(stageId):
    return {"stageId":stageId}
@bind("/quest/squadFormation")
def squadFormation(squadId,slots,changeSkill):
    return {"squadId":squadId,"slots":slots,"changeSkill":changeSkill}