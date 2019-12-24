#-*- coding: UTF-8 -*-
import RobotApi
import pygame

def action(pcName="Hit left",iRepeat=1):#pcName = ['Forward','Hit left','Hit right','Left slide tackle','reset','Right']
    ret = RobotApi.ubtStartRobotAction(pcName,iRepeat)
    if ret != 0:
        print("Can not start robot action! Error Code: %d" % ret)
    else:
        print "Do action "+pcName

def stopAction()
    ret = RobotApi.ubtStopRobotAction()
    if ret != 0:
        print("Can not stop robot action. Error code: %d" % ret)
    else:
        print("Stop action")
        
def dance(music="haicaowu"):
    pygame.mixer.init()
    pygame.mixer.music.load(r"./music/"+music+".mp3")
    pygame.mixer.music.play(0,0)
    RobotApi.ubtSetRobotVolume(60)
    ret = RobotApi.ubtStartRobotAction("dance",0)
    if ret != 0:
        print("Can not start robot action! Error Code: %d" % ret)
        return 
    else:
        print "Dance "+music
    time.sleep(35)
    stopAction()
    pygame.mixer.music.stop()

def motion(pcType="bow",pcDirect="front",iSpeed=3,iRepeat=1)
    ret = RobotApi.ubtSetRobotMotion(pcType,pcDirect,iSpeed,iRepeat)
    if ret != 0:
        print("Can not set motion for robot! Error Code: %d" % ret)
    else:
        print "Set motion "+pcType+" to "+pcDirect 
