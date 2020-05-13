#Christina, Cam and Nikesh
#Feb 2, 2020

import libpyAI as ai
import math
import sys
from random import *

frames = 0
totalframes = 0

ai.headlessMode()

def AI_loop():
    
    try:

        global frames
        global totalframes
        #Release keys
        ai.thrust(0)
        ai.turnLeft(0)
        ai.turnRight(0)

        #Setting environment variables
        ai.setTurnSpeedDeg(20)
        ai.setPower(35)

        #direction values
        upRight, upLeft = 67, 112
        leftUp, leftDown = 157, 202
        downLeft, downRight = 247, 292
        rightDown, rightUp = 337, 22
        up, down, left, right = 90, 270, 180, 0

        #Global variables
        #Speed limit
        speedLim = 6

        #Reaction distance
        reactDist = 250
        thrustDist = 150

        #Set variables
        #degree values
        heading = int(ai.selfHeadingDeg())
        backing = (heading + 180) % 360
        tracking = int(ai.selfTrackingDeg())
        reversing = (tracking + 180) % 360

        #Static Feelers
        #Front feelers
        upRightFeel = ai.wallFeeler(500, upRight)
        upLeftFeel = ai.wallFeeler(500, upLeft)

        #Side feelers
        leftUpFeel = ai.wallFeeler(500, leftUp)
        leftDownFeel = ai.wallFeeler(500, leftDown)

        #Back feelers
        downLeftFeel = ai.wallFeeler(500, downLeft)
        downRightFeel = ai.wallFeeler(500, downRight)

        #Right feelers
        rightDownFeel = ai.wallFeeler(500, rightDown)
        rightUpFeel = ai.wallFeeler(500, rightUp)

        #Tracking feelers
        trackFeel = ai.wallFeeler(500,tracking)
        reverseFeel = ai.wallFeeler(500, reversing)

        #Dynamic Feelers - ship
        #Back Feelers

        sLeftBackFeel = ai.wallFeeler(500, backing)
        sRightBackFeel = ai.wallFeeler(500, backing)


        #List of all feelers
        feelList = [upRightFeel, upLeftFeel, leftUpFeel, leftDownFeel, downLeftFeel, downRightFeel,\
            rightDownFeel, rightUpFeel]

        #Flags
        speedFlag = False
        conflictFlag = False
        upFlag = -1 
        downFlag  = -1 
        leftFlag = -1 
        rightFlag = -1 

        #Flag List
        flagList = [speedFlag, upFlag, downFlag, leftFlag, rightFlag]

        #Rules

        #Rule 1 - Speed Limit
        if ai.selfSpeed() < speedLim:
            speedFlag = True
            ai.thrust(1)
        else:
            ai.thrust(0)
        
        #Rule 2 - Up
        if upLeftFeel < reactDist or upRightFeel < reactDist and not ((leftDownFeel < reactDist or leftUpFeel < reactDist) or (rightDownFeel < reactDist or rightUpFeel < reactDist)) :
            upFlag = down
            ai.turnToDeg(down)
            if sLeftBackFeel < thrustDist or sRightBackFeel < thrustDist:
                ai.thrust(1)

        #Rule 3 - Down
        if downLeftFeel < reactDist or downRightFeel < reactDist and not ((leftDownFeel < reactDist or leftUpFeel < reactDist) or (rightDownFeel < reactDist or rightUpFeel < reactDist)):
            downFlag = up
            ai.turnToDeg(up)
            if sLeftBackFeel < thrustDist or sRightBackFeel < thrustDist:
                ai.thrust(1)

        #Rule 4 - Left
        if leftDownFeel < reactDist or leftUpFeel < reactDist and ((upFlag or downFlag) == -1):
            leftFlag = right
            ai.turnToDeg(right)
            if sLeftBackFeel < thrustDist or sRightBackFeel < thrustDist:
                ai.thrust(1)
                
        #Rule 5 - Right
        if rightUpFeel < reactDist or rightDownFeel < reactDist and ((upFlag or downFlag) == -1):
            rightFlag = left
            ai.turnToDeg(left)
            if sLeftBackFeel < thrustDist or sRightBackFeel < thrustDist:
                ai.thrust(1)

        # if sLeftBackFeel < thrustDist or sRightBackFeel < thrustDist:
        #     ai.thrust(1)

        #Variables List
        dirList = [upFlag, downFlag, leftFlag, rightFlag]
        avgList = []

        #Going through the list
        for element in dirList:
            if element != -1:
                avgList.append(element)

        #Rule 6 - Conflict Resolution

        if len(avgList) > 1:
            conflictFlag = True
            ai.turnToDeg(avgAngle(avgList))

        #Rule 7 - Aiming
        if len(avgList) == 0:
            ai.lockClose()
            ai.turnToDeg(int(ai.lockHeadingDeg()))
            x = randrange(0, 100)
            if x < 10:
                ai.thrust(1)
            else:
                ai.thrust(0)

    except Exception as e:
        print(e)

#Average Degree calculator
def avgAngle(angles):
    x = y = 0
    weights = [1] * len(angles)
    for angle, weight in zip(angles, weights):
        x += math.cos(math.radians(angle)) * weight
        y += math.sin(math.radians(angle)) * weight

    mean = math.degrees(math.atan2(y, x))
    return int(mean)


if __name__ == '__main__':
    port = sys.argv[2]
    global limit
    limit = sys.argv[3]
    limit = eval(limit)
    ai.start(AI_loop,["-name","no_shoot","-join","localhost", "-port", str(port)])