#-*- coding: UTF-8 -*-
import RobotApi
import jieba

def tts(text,isInterrputed=1):
    ret = RobotApi.ubtVoiceTTS(isInterrputed,text)
    if ret != 0:
        print("Can not play TTS voice. Error code: %d" % ret)
    else:
        print("Robot: "+text)
        
def startVoiceRecognition():
    ret = RobotApi.ubtVoiceStart()
    if ret != 0:
        print("Can not start start voice recognition. Error Code: %d" % ret)
    else:
        print("Voice recognition service start!")
    
def stopVoiceRecognition():
    ret = RobotApi.ubtVoiceStop()
    if ret != 0:
        print("Can not close voice recognition service. Error code: %d" % ret)
    else:
        print("Voice recognition service is stopped")
        
def detectMsg(text):
    ret = RobotApi.ubtDetectVoiceMsg(text,20)
    if ret != 0:
        print("Can not detect voice message. Error code: %d" % ret)
    else:
        print("Detect msg from user: "+text)

def asr():
    text = 
    
    return text
    
def searchKeyWord(text,keyWordList):
    cutList = jieba.cut(ans, cut_all=True)
    find = False
    for word in cutList:
        for keyWord in keyWordList:
            if word == keyWord:
                find = True
                return find
    return find
def searchYes(text):
    keyWordList =["是","是的","对","对的"]
    cutList = jieba.cut(ans, cut_all=True)
    find = False
    for word in cutList:
        for keyWord in keyWordList:
            if word == keyWord:
                find = True
                return find
    return find
def searchNo(text):
    keyWordList =["否","不是","不对","不"]
    cutList = jieba.cut(ans, cut_all=True)
    find = False
    for word in cutList:
        for keyWord in keyWordList:
            if word == keyWord:
                find = True
                return find
    return find
def asrAndSearchKeyWord(keyWordList):
    text = asr()
    return searchKeyWord(text,keyWordList)
