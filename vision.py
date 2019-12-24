#-*- coding: UTF-8 -*-
import RobotApi

def detectFace():
    pcVisionType = str("face")
    iTimeout = 30
    pcValue = "0"
    findFace = False
    ret = RobotApi.ubtVisionDetect(pcVisionType,pcValue,iTimeout)
    if ret != 0:
        print("Can not detect vision. Error code: %d" % ret)
    else:
        print(" find : %s face in camera" % pcValue[0])
        if pcValue[0]>0:
            findFace = True
    return findFace

def detectExpression():
    print "Start detech face expression"
    hasDepression = False
    faceinfo = RobotApi.UBTEDU_FACEEXPRE_T()  
    ret = RobotApi.ubtFaceExpression(20,faceinfo)
    if ret !=0:
	    print "faceinfo error %d" %(ret)
    else:
	    print "face Happiness = %0.3f" %(faceinfo.fHappinessValue)
	    print "face Surprise = %0.3f" %(faceinfo.fSurpriseValue)
	    print "face Anger = %0.3f" %(faceinfo.fAngerValue)
	    print "face Sadness = %0.3f" %(faceinfo.fSadnessValue)
	    print "face Neutral = %0.3f" %(faceinfo.fNeutralValue)
	    print "face Disgust = %0.3f" %(faceinfo.fDisgustValue)
	    print "face Fear = %0.3f" %(faceinfo.fFearValue)
        maxValue = max(faceinfo.fHappinessValue, faceinfo.fSurpriseValue, faceinfo.fAngerValue, faceinfo.fSadnessValue, faceinfo.fNeutralValue, faceinfo.fDisgustValue, faceinfo.fFearValue)
        if maxValue == faceinfo.fSadnessValue or maxValue == faceinfo.fFearValue:
            hasDepression = True
            print("The user is upset")
    return hasDepression

def detectGender():
    iTimeout = 20
    pcGender = str("9")
    pcAge = str("8")
    isMale = True
    ret = RobotApi.ubtFaceAgeGender(iTimeout,pcGender,pcAge)
    if ret != 0:
        print("Can not detect vision error : %d" % ret)
    else:
        print(" pcGender : %s , pcAge : %s \n" % (pcGender,pcAge))
    if pcGender!="0":
        isMale = False
    return isMale
