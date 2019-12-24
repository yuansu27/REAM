#!/usr/bin/python
# _*_ coding: utf-8 -*-

import time
import RobotApi
import action
import audition
import buttonInteraction
import stateMachine
import vision
import jieba
import userInfo
import mood

RobotApi.ubtRobotInitialize()
#------------------------------Connect----------------------------------------
gIPAddr = ""

robotinfo = RobotApi.UBTEDU_ROBOTINFO_T()
#The robot name you want to connect
robotinfo.acName="Yanshee_8F83"
ret = RobotApi.ubtRobotDiscovery("SDK", 15, robotinfo)
if (0 != ret):
	print ("Return value: %d" % ret)
	exit(1)

gIPAddr = robotinfo.acIPAddr
ret = RobotApi.ubtRobotConnect("SDK", "1", gIPAddr)
if (0 != ret):
	print ("Can not connect to robot %s" % robotinfo.acName)
	exit(1)

#---------------------------Program Start---------------------------
jieba.load_userdict("myDictionary.txt")
user = userInfo.UserInfo()
depression = mood.Depression()

fsm = stateMachine.StateMachine()
fsm.addState("start",stateMachine.startTransitions)
fsm.addState("detectUser",stateMachine.detectUserTransitions)
fsm.addState("detectExpression",stateMachine.detectExpressionTransitions)
fsm.addState("evaluationState",stateMachine.evaluationStateTransitions)
fsm.addState("depressionDiagnosis",stateMachine.depressionDiagnosisTransitions)
fsm.addState("depressionTreatment",stateMachine.depressionTreatmentTransitions)
fsm.addState("anxietyDiagnosis",stateMachine.anxietyDiagnosisTransitions)
#fsm.addState("",stateMachine.Transitions)
#fsm.addState("",stateMachine.Transitions)
#fsm.addState("",stateMachine.Transitions)
fsm.addState("dance",stateMachine.danceTransitions)
fsm.addState("summary",stateMachine.summaryTransitions)
fsm.addState("goodbye",stateMachine.goodbyeTransitions)
fsm.addState("end", None, endState=1)  

fsm.setStart("start") 
fsm.run("")

#--------------------------DisConnect--------------------------------- 
RobotApi.ubtRobotDisconnect("SDK","1",gIPAddr)
RobotApi.ubtRobotDeinitialize()
#---------------------------------------------------------------------
class StateMachine:
    def __init__(self): 
        self.handlers = {}       
        self.startState = None    
        self.endStates = []       
    
    def addState(self, name, handler, endState=0):
        name = name.upper()
        self.handlers[name] = handler
        if endState:
            self.endStates.append(name)

    def setStart(self, name):
        self.startState = name.upper()

    def run(self):
        try:
            handler = self.handlers[self.startState]
        except:
            raise InitializationError("must call .setStart() before .run()")
        if not self.endStates:
            raise  InitializationError("at least one state must be an endState")
       
        while True: 
            newState = handler()    
            if newState.upper() in self.endStates: 
                print("reached ", newState)
                break 
            else:                        
                handler = self.handlers[newState.upper()]   
                
def startTransitions():
    audition.tts("我准备好了") 
    newState = "detectUser"
    return newState
    
def detectUserTransitions():
    if vision.detectFace()==True:
        user.gender = vision.detectGender() 
        audition.tts("你好，我是小优。请问你叫什么名字？") 
        # to do: add 挥手
        name = audition.asr()
        user.name = name
        audition.tts(name+"？真是一个好听的名字。最近在忙什么啊？学习，工作，还是减肥？") 
        ans = audition.asr()
        if audition.searchKeyWord(text,["学习"]): 
            audition.tts("你的努力一定会有回报，祝你学业有成！")
        elif audition.searchKeyWord(text,["工作"]):
            if user.isMale == True:
                audition.tts("敬业的男人最帅了。祝你事业蒸蒸日上，日进斗金")
            else:
                audition.tts("明明可以靠颜值，偏要靠事业，真是令人钦佩的姐姐。不要让自己太累哦！")
        elif audition.searchKeyWord(text,["减肥"])
            if user.isMale == True:
                audition.tts("有人说，自律使人自由。祝你早日拥有六块腹肌！")
            else:
                audition.tts("有人说，自律使人自由。祝你瘦出性感好身材！")
        newState = "detectExpression"
    else:
        newState = "detectUser"  
    return newState      
           
def detectExpressionTransitions():
    if vision.detectExpression()==True:
        audition.tts("你看起来不是很开心，可以跟我讲讲吗？") 
        text = audition.asr()
        if audition.searchKeyWord(text,["好","好的","可以","是","是的","嗯"]): 
            newState = "evaluationState"
        elif audition.searchKeyWord(text,["不","不好","不可以","不要"])::
            newState = "dance"
    else:
        newState = "detectExpression"
    return newState
    
def evaluationStateTransitions():
    audition.tts("用一个词形容一下你现在的心情，比如难受、烦、焦虑、担心、害怕")
    user.mood = audition.asr()
    audition.tts(user.name+",下面我将问你几个问题，请回答是或者否。") 
    depressionScore = 0.0;
    audition.tts("你是否时常觉得难以找到有价值的事情？")
    ans = audition.asr()
    if audition.searchYes(ans):
        depressionScore +=1
    audition.tts("你是否时常觉得很多事情都很糟糕？")
    ans = audition.asr()
    if audition.searchYes(ans):
        depressionScore +=1
    audition.tts("你是否对自己满意？")
    ans = audition.asr()
    if audition.searchNo(ans):
        depressionScore +=1
    audition.tts("你是否最近饭量变少？")
    ans = audition.asr()
    if audition.searchYes(ans):
        depressionScore +=1
    
    anxietyScore = 0.0
    audition.tts("你是否时常担心发生某些不好的事情？")
    ans = audition.asr()
    if audition.searchYes(ans):
        anxietyScore +=1
    audition.tts("你是否时常有过度出汗、心悸或头晕的现象？")
    ans = audition.asr()
    if audition.searchYes(ans):
        anxietyScore +=1
    audition.tts("你脑海是否时常浮现一些令你担心或恐惧的画面或后果？")
    ans = audition.asr()
    if audition.searchYes(ans):
        anxietyScore +=1
    
    depressionScore /=4.0
    anxietyScore /= 3.0
    if depressionScore>=anxietyScore:
        user.illnessType = "抑郁"
        newState = "depressionDiagnosis"
    else:
        user.illnessType = "焦虑"
        newState = "anxietyDiagnosis"
    return newState


def depressionDiagnosisTransitions():
    audition.tts("你觉得你有"+user.mood+"的心情多久了?")
    depression.lastTime = audition.asr()
    audition.tts("主要是什么事情发生后你产生了这种情绪？")
    depression.reason = audition.asr()
    audition.tts("此前你用什么方式来放松或者娱乐呢？")
    depression.entertainment = audition.asr()
    audition.tts("所以你其实是热爱生活的，只是暂时的情绪让你失去一部分快乐对吗")
    audition.tts("你觉得有把握解决"+depression.reason+"吗？")
    ans = audition.asr()
    if searchKeyWord(ans,["有","有把握"]):
        depression.confidence2Solve = True
    audition.tts("你觉得生活里别人眼中的你是怎么样的？")
    depression.opinionFromOthers = audition.asr()
    audition.tts("你觉得自己的未来是否是光明有希望的？")
    ans = audition.asr()
    if searchYes(ans):
        depression.hope4Future = True
    audition.tts("你觉得这个世界是值得欣赏和享受的吗？")
    ans = audition.asr()
    if searchYes(ans):
        depression.enjoyWorld = True
    audition.tts("你觉得身体有什么不舒服吗？")
    depression.physicalDiscomfort = audition.asr()
    audition.tts("谢谢你如此信任地告诉我你的难处，让我们看看怎么改变这个现状吧！")
    newState = "depressionTreatment"
    return newState

def depressionTreatmentTransitions():
    string = ""
    if depression.hope4Future == False:
        string +=",对自己的未来没有希望"
    if depression.enjoyWorld == False:
        string +=",认为人间不值得"
    audition.tts("你知道吗，任何情绪不是凭空而来的，而是与你的想法有关。每个人的想法、情绪、行为和身体互相之间都是时时影响着的。对于你目前的情况，我认为是这样的，由于"+depression.reason+"等的事情，你自然地产生了"+user.mood+"情绪。在此情绪下，你产生了消极的想法和症状，比如你觉得别人认为你"+opinionFromOthers+string+"这会使你解决问题的能力下降，因此更难改变现状。同时，在消极想法下，你减少了"+depression.entertainment+"等令人愉快的活动，因此会更加沉溺于"+user.mood+"的情绪之中。这是一种维持过程，既然现在找到了情绪产生的方式，我们就可以入手来打破这个模式了。")
    audition.tts("其实,情绪都是短暂的体验，而不是唯一的存在，每个人都有积极、消极的观念，而你的情绪只是因为一些你自己的想法产生的。如果你赞同我，并能体会到自己那些想法，那么恭喜你已经超越原先的自己啦！")
    audition.tts("回顾一下你对自己、他人、世界以及未来的看法，你可以试着找出证明它的证据吗？有没有反例？如果没有证据，这说明那只是你的臆断，何不去看看世界的真相。")
    audition.tts("此外，我建议你一点点增加自己的"+depression.entertainment+"等活动，哪怕身心上可能有抗拒，但着有助于你打破心情的维持过程，不妨去试试吧！")
    newState = "summary"
    return newState

def anxietyDiagnosisTransitions():
    
    return newState

def danceTransitions():
    newState = "end"
    return newState
def summaryTransitions():
    
    newState = "goodbye"
    return newState

def goodbyeTransitions():
    
    newState = "end"
    return newState
