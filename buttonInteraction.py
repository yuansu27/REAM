#-*- coding: UTF-8 -*-
import RobotApi

def setLED(pcColor='white',pcMode='On'):    
    pcType = "button"
    #pcColor = ['white','red','green','blue','yellow','purple','cyan']
    #pcMode =  ['On','blink','breath','alternation','off']
    ret = RobotApi.ubtSetRobotLED(pcType,pcColor,pcMode)
    if ret != 0:
        print("Can not set color for robot! Error code: %d" % ret)
    else:
        print "Set button to color "+pcColor+" with mode "+pcMode
