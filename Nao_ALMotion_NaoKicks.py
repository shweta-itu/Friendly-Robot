# -*- encoding: UTF-8 -*-

import argparse
import motion
import time
import almath
from naoqi import ALProxy

def computeNaoPath(proxyNao, effectLeg, frame):
    deltaX      = 0.05                 # translation axis X (meters)
    deltaZ      = 0.05                 # translation axis Z (meters)
    rotY     = 5.0*almath.TO_RAD    # rotation axis Y (radian)

    useSensorValues = False

    pathCurve = []
    currTF = []
    try:
        currTF = proxyNao.getTransform(effectLeg, frame, useSensorValues)
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    # 1
    destTf  = almath.Transform(currTF)
    destTf *= almath.Transform(-deltaX, 0.0, deltaZ)
    destTf *= almath.Transform().fromRotY(rotY)
    pathCurve.append(list(destTf.toVector()))

    # 2
    destTf  = almath.Transform(currTF)
    destTf *= almath.Transform(deltaX, 0.0, deltaZ)
    pathCurve.append(list(destTf.toVector()))

    # 3
    pathCurve.append(currTF)

    return pathCurve


def main(robotIP, PORT=9559):
 
    motionNaoProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureNaoProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionNaoProxy.wakeUp()

    # Send robot to Stand Init
    postureNaoProxy.goToPosture("StandInit", 0.5)

    # Activate Whole Body Balancer
    isEnabled  = True
    motionNaoProxy.wbEnable(isEnabled)

    # Legs are constrained fixed
    stateNaoRobot  = "Fixed"
    supportedLeg = "Legs"
    motionNaoProxy.wbFootState(stateNaoRobot, supportedLeg)

    # Constraint Balance motionNao
    isEnable   = True
    supportedLeg = "Legs"
    motionNaoProxy.wbEnableBalanceConstraint(isEnable, supportedLeg)

    # Com go to LLeg
    supportedLeg = "LLeg"
    duration   = 2.0
    motionNaoProxy.wbGoToBalance(supportedLeg, duration)

    # RLeg is free
    stateNaoRobot  = "Free"
    supportedLeg = "RLeg"
    motionNaoProxy.wbFootState(stateNaoRobot, supportedLeg)

    # RLeg is optimized
    effectLeg = "RLeg"
    axisMask = 63
    frame    = motion.FRAME_WORLD

    # Motion of the RLeg
    times   = [2.0, 2.7, 4.5]

    pathCurve = computePath(motionNaoProxy, effectLeg, frame)

    motionNaoProxy.transformInterpolations(effectLeg, frame, pathCurve, axisMask, times)

    # Example showing how to Enable effectLeg Control as an Optimization
    isActive     = False
    motionNaoProxy.wbEnableEffectorOptimization(effectLeg, isActive)

    # Com go to LLeg
    supportedLeg = "RLeg"
    duration   = 2.0
    motionNaoProxy.wbGoToBalance(supportedLeg, duration)

    # RLeg is free
    stateNaoRobot  = "Free"
    supportedLeg = "LLeg"
    motionNaoProxy.wbFootState(stateNaoRobot, supportedLeg)

    effectLeg = "LLeg"
    pathCurve = computePath(motionNaoProxy, effectLeg, frame)
    motionNaoProxy.transformInterpolations(effectLeg, frame, pathCurve, axisMask, times)

    time.sleep(1.0)

    # Deactivate Head tracking
    isEnabled = False
    motionNaoProxy.wbEnable(isEnabled)

    # send robot to Pose Init
    postureNaoProxy.goToPosture("StandInit", 0.3)

    # Go to rest position
    motionNaoProxy.rest()

if __name__ == "__main__":
    parseFile = argparse.ArgumentParser()
    parseFile.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parseFile.add_argument("--port", type=int, default=52742,
                        help="Robot port number")

    args = parseFile.parse_args()
    main(args.ip, args.port)
