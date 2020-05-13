import libpyAI as ai
import sys
from random import randrange
from bin2num import *
import math 
import keyboard
from math import *

#RUN THIS TO TEST BEST NN ADVISORY BOARD
#MAKE SURE YOU HAVE A SERVER RUNNING WITH -maxrobots 3 on simple.xp map before running code

# ai.headlessMode()

weights = [[[6.614121342532178,
   6.324362426722006,
   5.98565729150397,
   1.4979731988367488,
   -0.39824029314420195,
   4.555713537812613],
  [5.918449768877174,
   5.851477740923497,
   3.8310020515553114,
   1.650850466372311,
   -1.554112403683075,
   4.723949866461494],
  [5.9673265150721715,
   6.414678343604476,
   5.681917190283525,
   0.13070573493489557,
   -0.03782741351369707,
   4.131353234815062],
  [6.942866989818756,
   6.4581331144231875,
   5.941573961759422,
   5.309729172493651,
   -3.9207400483847556,
   3.108914131607069]],
 [[3.9708591746805997,
   4.22200387651361,
   4.720474652887747,
   4.383876072362592,
   4.0485799218849134]]]

def neuNet(inputs):
    layers = [5,4,1]
    global weights
    prediction = []
    
    answer = inputs
    # calculates output for all layers but the first
    for l in range(len(layers)-1):
        tempAnswer = []
        # caluclates output for each perceptron in next layer which will be the input for next round
        for w in range(len(weights[l])):
            length = len(answer)
            a = sum(x*y for x,y in zip(answer,weights[l][w][0:length])) - weights[l][w][length]
            a = (1/(1+(exp(-a))))
            tempAnswer.append(a)
        answer = tempAnswer
    for a in answer:
        prediction.append(a)    
    return prediction[0]


def setUp(gene1, gene2, gene3):
  
    try:
        #Bit breakdown
        powerBits = gene1[0:6]
        global power
        power = round((50/63)*bin2num(powerBits)) + 5

        speedLimMoveBits = gene1[6:10]
        global speedLimMove 
        speedLimMove = bin2num(speedLimMoveBits)

        reactDistBits = gene1[10:19]
        global reactDist
        reactDist = bin2num(reactDistBits)

        thrustDistBits = gene1[19:28]
        global thrustDist 
        thrustDist = bin2num(thrustDistBits)
            
        speedLimBits = gene2[0:4]
        global speedLim
        speedLim = bin2num(speedLimBits)

        shiftBits = gene2[4:9]
        global shift
        shift = bin2num(shiftBits)

        tolerBits = gene2[9:13]
        global toler
        toler = bin2num(tolerBits)

        global tempDeg
        tempDeg = 0
        
            
        numBulletsBits = gene3[0:4]
        global numBullets
        numBullets = bin2num(numBulletsBits)

        repelBits = gene3[4:14]
        global repel
        repel = bin2num(repelBits)

        distKamiBits = gene3[14:21]
        global distKami
        distKami = bin2num(distKamiBits)

        minBDistBits = gene3[21:28]
        global minBDist
        minBDist = bin2num(minBDistBits) + distKami
        
        stopSpeedBits = gene3[28:30]
        global stopSpeed
        stopSpeed = bin2num(stopSpeedBits)
        
        velScareBits = gene3[30:33]
        global velScare
        velScare = bin2num(velScareBits)

        kamiTolerBits = gene3[33:37]
        global kamiToler
        kamiToler = bin2num(kamiTolerBits)

        dodgeAngleBits = gene3[37:43]
        global dodgeAngle
        dodgeAngle = bin2num(dodgeAngleBits)

        global braking
        braking = False


        global frames
        frames = 0
        global totalFrames
        totalFrames = 0
        global oldScore 
        oldScore = 0 
        global kill
        kill = 0
        global deaths
        deaths = 0
        global SDs
        SDs = 0
        global speedList
        speedList = []

        global infoList
        infoList = [0,0,0,0,0]
        
    except Exception as e:
        print(e)

def AI_loop():
    
    global typ
    
    mList = ["AI_move", "AI_atk", "AI_def"]
    ai.switchLoop(eval(mList[typ - 1]))

def AI_atk():

    global shift
    
    global tempDeg

    global speedLim

    global toler
    
    global frames
    global totalFrames
    global speedLim
    global oldScore
    global kill
    global deaths
    global SDs
    global final
    global limit

    global infoList

    try:
        ai.setTurnSpeed(64)

        #direction values
        upRight, upLeft = 67, 112
        leftUp, leftDown = 157, 202
        downLeft, downRight = 247, 292
        rightDown, rightUp = 337, 22
        up, down, left, right = 90, 270, 180, 0

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

        #Heading feelers
        headFeel = ai.wallFeeler(500, heading)
        backFeel = ai.wallFeeler(500, backing)

        #Dynamic Feelers - ship
        #Back Feelers

        sLeftBackFeel = ai.wallFeeler(500, backing)
        sRightBackFeel = ai.wallFeeler(500, backing)

        #Moving
        
        if ai.selfSpeed() < speedLim:
            ai.thrust(1)
        else:
            ai.thrust(0)

        #Aiming
        try:
            ai.lockClose()
            enemyMoveDir = ai.enemyTrackingDegId(ai.closestShipId())
            enemySpeed = ai.enemySpeedId(ai.closestShipId())
            relVelocityX = enemySpeed * math.cos(enemyMoveDir) - ai.selfSpeed() * math.cos(tracking)
            relVelocityY = enemySpeed * math.sin(enemyMoveDir) - ai.selfSpeed() * math.sin(tracking)
            relVelocityDir = (math.atan(relVelocityX / relVelocityY + 0.0001) * 180/math.pi) % 360
            shootDir = int((ai.lockHeadingDeg() + shift * (ai.lockHeadingDeg() - tempDeg)) % 360)
            for i in range(3):
                ai.turnToDeg(shootDir)
            if shootDir >  heading - toler and shootDir < heading + toler:
                ai.fireShot()
        
            tempDeg = ai.lockHeadingDeg()
        except:
            pass
        
        if oldScore > ai.selfScore():
          if oldScore - ai.selfScore() < 5:
            SDs = SDs + 1
            limit = limit - 280
          else:
            deaths = deaths + 1
          oldScore = ai.selfScore()
      
        #Alive or not
        if not ai.selfAlive():
            if oldScore < ai.selfScore():
                kill = kill + 1
                oldScore = ai.selfScore()
            elif oldScore > ai.selfScore():
                if oldScore - ai.selfScore() < 5:
                    SDs = SDs + 1
                else:
                    deaths = deaths + 1
                oldScore = ai.selfScore()
        elif totalFrames > limit - 1:
            final = [frames, kill, deaths, SDs]
        else:
            frames = frames + 1
        totalFrames = totalFrames + 1

        
        #Output Code
        nBullet = 8
        bList = []
        enemyDist = 1000
        bulletDist = 1000

        for i in range(nBullet):
            if ai.shotDist(i) != -1:
                bList.append([i, ai.shotDist(i)])
        
        bList.sort(key = lambda x:x[1])

        if bList != []:
            bulletDist = bList[0][1]
        if ai.enemyDistanceId(ai.closestShipId()) != 9999:
            enemyDist = ai.enemyDistanceId(ai.closestShipId())

        trackWall = int(trackFeel <= 250)
        frontWall = int(headFeel <= 250)
        backWall = int(backFeel <= 75)
        enemyBullet = int(bulletDist <= 100)
        enemyShip = int(enemyDist <= 100)

        infoList = [trackWall, frontWall, backWall, enemyBullet, enemyShip]

        mode = neuNet(infoList)
        mode = round(mode*2)/2

        if mode == 1:
            ai.switchLoop(AI_move) 
            ai.talk("MOVE")
            # print("MOVE")
        elif mode == 0.5:
            ai.switchLoop(AI_def)
            ai.talk("DEFEND")
            # print("DEFEND")

    except Exception as e:
        print(e)

def AI_def():

    try:

        global numBullets
        global minBDist
        global stopSpeed
        global velScare
        global kamiToler
        global distKami
        global repel
        global dodgeAngle

        global frames
        global totalFrames
        global speedLimDef
        global oldScore
        global kill
        global deaths
        global SDs
        global final
        global limit

        global brake
        global running

        global infoList

        #direction values
        upRight, upLeft = 67, 112
        leftUp, leftDown = 157, 202
        downLeft, downRight = 247, 292
        rightDown, rightUp = 337, 22
        up, down, left, right = 90, 270, 180, 0

        #Global variables

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

        #Heading feelers
        headFeel = ai.wallFeeler(500, heading)
        backFeel = ai.wallFeeler(500, backing)

        #Dynamic Feelers - ship
        #Back Feelers

        sLeftBackFeel = ai.wallFeeler(500, backing)
        sRightBackFeel = ai.wallFeeler(500, backing)

        try:

            rotLoop = 5

            dataList = []

            for i in range(numBullets):
                if ai.shotDist(i) != -1:
                    dataList.append([i, ai.shotDist(i)])
            
            dataList.sort(key = lambda x:x[1])

            angList = []
            wList = []

            if dataList != []:
                for i in dataList:
                    angBullet = doArctan(ai.shotX(i[0]) - ai.selfX(), ai.shotY(i[0]) - ai.selfY())
                    angList.append(int((angBullet - 180) % 360))
                    wList.append(1000 - ai.shotDist(i[0]) + velScare * ai.shotVel(i[0]))
                
                rAng = int(wAvgAngle(wList, angList)) % 360
                
                if dataList[0][1] < minBDist:
                    
                    if ((tracking - ai.shotVelDir(dataList[0][0]) - 180) % 180 <= kamiToler) or ai.shotDist(dataList[0][0]) < distKami:
                    
                        power = 800 * repel / (ai.shotDist(dataList[0][0]) * ((heading - angList[0] + 180) % 360 + 0.1))
        
                        if power >= 55:
                            power = 55
                        elif power < 5:
                            power = 5
                        else:
                            power = int(power)
                        ai.setPower(power)
                        ai.thrust(1)
                        for i in range(rotLoop):
                            ai.turnToDeg((angList[0] + (dodgeAngle + 58)) % 360)
                    else:

                        power = 100 * repel / ai.shotDist(dataList[0][0])

                        if power >= 55:
                            power = 55
                        elif power < 5:
                            power = 5
                        else:
                            power = int(power)
                        ai.setPower(power)
                        ai.thrust(1)
                        for i in range(rotLoop):
                            ai.turnToDeg((angList[0] + 180) % 360) 
                elif dataList[0][1] < minBDist + 50:

                    ai.setPower(10)
                    ai.thrust(1)
                    for i in range(rotLoop):
                        ai.turnToDeg(rAng)
                else:
                    ai.thrust(0)
                    braking = True
                    selfBrake(heading, tracking, braking, stopSpeed)
            else:
                ai.thrust(0)
                braking = True
                selfBrake(heading, tracking, braking, stopSpeed)

        except Exception as e:
            print(e)

        if oldScore > ai.selfScore():
            if oldScore - ai.selfScore() < 5:
                SDs = SDs + 1
            else:
                deaths = deaths + 1
                limit = limit - 280
            oldScore = ai.selfScore()
        
            #Alive or not
        if not ai.selfAlive():
            if oldScore < ai.selfScore():
                kill = kill + 1
                oldScore = ai.selfScore()
            elif oldScore > ai.selfScore():
                if oldScore - ai.selfScore() < 5:
                    SDs = SDs + 1
                else:
                    deaths = deaths + 1
                oldScore = ai.selfScore()
        elif totalFrames > limit - 1:
            final = [frames, kill, deaths, SDs]
        else:
            frames = frames + 1
        totalFrames = totalFrames + 1
        
        #Output Code
        nBullet = 8
        bList = []
        enemyDist = 1000
        bulletDist = 1000

        for i in range(nBullet):
            if ai.shotDist(i) != -1:
                bList.append([i, ai.shotDist(i)])
        
        bList.sort(key = lambda x:x[1])

        if bList != []:
            bulletDist = bList[0][1]
        if ai.enemyDistanceId(ai.closestShipId()) != 9999:
            enemyDist = ai.enemyDistanceId(ai.closestShipId())

        trackWall = int(trackFeel <= 250)
        frontWall = int(headFeel <= 250)
        backWall = int(backFeel <= 75)
        enemyBullet = int(bulletDist <= 100)
        enemyShip = int(enemyDist <= 100)

        infoList = [trackWall, frontWall, backWall, enemyBullet, enemyShip]

        mode = neuNet(infoList)
        mode = round(mode*2)/2
        
        if mode == 1:
            ai.switchLoop(AI_move)
            ai.talk("MOVE") 
            # print("MOVE")
        elif mode == 0:
            ai.switchLoop(AI_atk)
            ai.talk("ATTACK")
            # print("ATTACK")
    
    except Exception as e:
        print(e)

def AI_move():
  
  global frames
  global totalFrames
  global power 
  global speedLimMove
  global reactDist
  global thrustDist
  global oldScore
  global kill
  global deaths
  global SDs
  global final
  global speedList
  global limit

  global infoList

  try:

      ai.setTurnSpeedDeg(20)
      ai.setPower(power)

      #direction values
      upRight, upLeft = 67, 112
      leftUp, leftDown = 157, 202
      downLeft, downRight = 247, 292
      rightDown, rightUp = 337, 22
      up, down, left, right = 90, 270, 180, 0

      #Global variables

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

      #Heading feelers
      headFeel = ai.wallFeeler(500, heading)
      backFeel = ai.wallFeeler(500, backing)

      #Dynamic Feelers - ship
      #Back Feelers

      sLeftBackFeel = ai.wallFeeler(500, backing)
      sRightBackFeel = ai.wallFeeler(500, backing)

      #Flags
      speedFlag = False
      conflictFlag = False
      upFlag = -1 
      downFlag  = -1 
      leftFlag = -1 
      rightFlag = -1 

      #Flag List - used to print and debug
      flagList = [speedFlag, upFlag, downFlag, leftFlag, rightFlag]

      #Rules

      #Thrust Rules
      if ai.selfSpeed() < speedLimMove:
          speedFlag = True
          ai.thrust(1)
      else:
          ai.thrust(0)
      if sLeftBackFeel < thrustDist:
          ai.thrust(1)
      if sRightBackFeel < thrustDist:
          ai.thrust(1)
      
      #Turn Rules
      #North direction

      if upLeftFeel < reactDist and not leftDownFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      elif upLeftFeel < reactDist and not leftUpFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      if upLeftFeel < reactDist and not rightDownFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      elif upLeftFeel < reactDist and not rightUpFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down

      if upRightFeel < reactDist and not leftDownFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      elif upRightFeel < reactDist and not leftUpFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      if upRightFeel < reactDist and not rightDownFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down
      elif upRightFeel < reactDist and not rightUpFeel < reactDist:
          ai.turnToDeg(down)
          upFlag = down

      #South direction

      if downLeftFeel < reactDist and not leftDownFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      elif downLeftFeel < reactDist and not leftUpFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      if downLeftFeel < reactDist and not rightDownFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      elif downLeftFeel < reactDist and not rightUpFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up

      if downRightFeel < reactDist and not leftDownFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      elif downRightFeel < reactDist and not leftUpFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      if downRightFeel < reactDist and not rightDownFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up
      elif downRightFeel < reactDist and not rightUpFeel < reactDist:
          ai.turnToDeg(up)
          downFlag = up

      #West direction

      if leftDownFeel < reactDist:
          ai.turnToDeg(right)
          leftFlag = right
      if leftUpFeel < reactDist:
          ai.turnToDeg(right)
          leftFlag = right

      #East direction

      if rightUpFeel < reactDist:
          ai.turnToDeg(left)
          rightFlag = left
      if rightDownFeel < reactDist:
          ai.turnToDeg(left)
          rightFlag = left

      #close List
      dirList = [upFlag, downFlag, leftFlag, rightFlag]
      avgList = []

      #Going through close list list
      for element in dirList:
          if element != -1:
              avgList.append(element)

      speedList.append(ai.selfSpeed())

      if oldScore > ai.selfScore():
          if oldScore - ai.selfScore() < 5:
            SDs = SDs + 1
            limit = limit - 280
          else:
            deaths = deaths + 1
          oldScore = ai.selfScore()
      
      #Alive or not
      if not ai.selfAlive():
          if oldScore < ai.selfScore():
              kill = kill + 1
              oldScore = ai.selfScore()
          elif oldScore > ai.selfScore():
              if oldScore - ai.selfScore() < 5:
                  SDs = SDs + 1
              else:
                  deaths = deaths + 1
              oldScore = ai.selfScore()
      elif totalFrames > limit - 1:
          final = [frames, kill, deaths, SDs, speedList]
      else:
          frames = frames + 1
      totalFrames = totalFrames + 1
      
      #Output Code
      nBullet = 8
      bList = []
      enemyDist = 1000
      bulletDist = 1000

      for i in range(nBullet):
          if ai.shotDist(i) != -1:
              bList.append([i, ai.shotDist(i)])
    
      bList.sort(key = lambda x:x[1])

      if bList != []:
          bulletDist = bList[0][1]
      if ai.enemyDistanceId(ai.closestShipId()) != 9999:
          enemyDist = ai.enemyDistanceId(ai.closestShipId())

      trackWall = int(trackFeel <= 250)
      frontWall = int(headFeel <= 250)
      backWall = int(backFeel <= 75)
      enemyBullet = int(bulletDist <= 100)
      enemyShip = int(enemyDist <= 100)

      infoList = [trackWall, frontWall, backWall, enemyBullet, enemyShip]

      mode = neuNet(infoList)
      mode = round(mode*2)/2
            
      if mode == 0.5:
          ai.switchLoop(AI_def) 
        #   print("DEFEND")
          ai.talk("DEFEND")
      elif mode == 0:
          ai.switchLoop(AI_atk)
          ai.talk("ATTACK")
        #   print("ATTACK")

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

def wAvgAngle(weights, angles):
    x = y = 0.
    for angle, weight in zip(angles, weights):
        x += math.cos(math.radians(angle)) * weight
        y += math.sin(math.radians(angle)) * weight

    mean = math.degrees(math.atan2(y, x))
    return mean

def doArctan(x, y):
    if x >= 0 and y >= 0:
        return (math.atan(y / (x + 0.0001)) * 180/math.pi) % 360
    elif x < 0 and y > 0:
        return (180 + math.atan(y / (x + 0.0001)) * 180/math.pi) % 360
    elif x <= 0 and y <= 0:
        return (180 + math.atan(y / (x + 0.0001)) * 180/math.pi) % 360
    elif x > 0 and y < 0:
        return (math.atan(y / (x + 0.0001)) * 180/math.pi) % 360
    else:
        return 0

def runBot(gene, num, port, typ):
    ai.start(AI_loop,["-name", "NN_KCN_final", "-join", "localhost"])

def selfBrake(heading, tracking, braking, slowSpeed):
    if ai.selfSpeed() != 0 and braking == True:
        if abs(heading - (tracking + 180) % 360) > 2:
            ai.thrust(0)
            for i in range(3):
                ai.turnToDeg((tracking + 180) % 360)
        else:
            ai.setPower(int(55))
            ai.thrust(1)
    elif ai.selfSpeed() == slowSpeed:
        ai.thrust(0)
        braking = False

def runAway(heading, tracking, x, y, power, reactDist, running, dodgeAngle):
    if running == True and (x**2 + y**2)**0.5 < reactDist:
        if abs(heading - (doArctan(x, y) + 180) % 360) > 15:
            ai.thrust(0)
            for i in range(3):
                ai.turnToDeg(int(doArctan(x, y) + dodgeAngle) % 360)
        elif abs(heading - (doArctan(x, y) + dodgeAngle) % 360) > 1 and abs(heading - (doArctan(x, y) + dodgeAngle) % 360) <= 15:
            for i in range(3):
                ai.turnToDeg(int(doArctan(x, y) + dodgeAngle) % 360)
            ai.setPower(power)
            ai.thrust(1)
        else:
            ai.setPower(power)
            ai.thrust(1)
    else:
        ai.thrust(0)
        running = False

if __name__ == '__main__':

    gene1 = [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0]
    # gene1 = [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 1, 1]
    
    gene2 = [0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1]
    # gene2 = [0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0]
    
    gene3 = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]
    # gene3 = [1, 0, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0]

    num = 1
    port = 15350
    typ = 3
    limit = 5000
    setUp(gene1, gene2, gene3)
    runBot(gene1, num, port, typ)

