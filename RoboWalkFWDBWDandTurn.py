import argparse
import motion
import time
import almath
from naoqi import ALProxy

def armMotionXY(motionNaoProxy):
    affectedArm   = ["LArm", "RArm"]
    frameNao      = motion.FRAME_TORSO
    usvals = False

    # just control position
    axmsk   = [motion.AXIS_MASK_VEL, motion.AXIS_MASK_VEL]

    # LArm path
    armLPath = []
    initialTf   = almath.Transform(motionNaoProxy.getTransform("LArm", frameNao, usvals))
    destTf = almath.Transform(motionNaoProxy.getTransform("LArm", frameNao, usvals))
    destTf.r1_c4 += 0.04 # x
    destTf.r2_c4 -= 0.10 # y
    destTf.r3_c4 += 0.10 # z
    armLPath.append(list(destTf.toVector()))
    armLPath.append(list(initialTf.toVector()))
    armLPath.append(list(destTf.toVector()))
    armLPath.append(list(initialTf.toVector()))

    # RArm path
    armRPath = []
    initialTf   = almath.Transform(motionNaoProxy.getTransform("RArm", frameNao, usvals))
    destTf = almath.Transform(motionNaoProxy.getTransform("RArm", frameNao, usvals))
    destTf.r1_c4 += 0.04 # x
    destTf.r2_c4 += 0.10 # y
    destTf.r3_c4 += 0.10 # z
    armRPath.append(list(destTf.toVector()))
    armRPath.append(list(initialTf.toVector()))
    armRPath.append(list(destTf.toVector()))
    armRPath.append(list(initialTf.toVector()))

    addPaths = []
    addPaths.append(armLPath)
    addPaths.append(armRPath)

    # Go to the target and back again
    timesList = [[1.0, 2.0, 3.0, 4.0],
                 [1.0, 2.0, 3.0, 4.0]] # seconds

    motionNaoProxy.transformInterpolations(affectedArm, frameNao, addPaths,
                                       axmsk, timesList)


def armMotion(motionNaoProxy):
    jointsNames = ["LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll"]
    armN1 = [-40,  25, 0, -40]
    armN1 = [ x * motion.TO_RAD for x in armN1]

    armN2 = [-40,  50, 0, -80]
    armN2 = [ x * motion.TO_RAD for x in armN2]

    pfMSpeed = 0.6

    motionNaoProxy.angleInterpolationWithSpeed(jointsNames, armN1, pfMSpeed)
    motionNaoProxy.angleInterpolationWithSpeed(jointsNames, armN2, pfMSpeed)
    motionNaoProxy.angleInterpolationWithSpeed(jointsNames, armN1, pfMSpeed)


def main(robotIP, PORT=9559):

    motionNaoProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureNaoProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    motionNaoProxy.wakeUp()

    postureNaoProxy.goToPosture("StandInit", 0.5)
    motionNaoProxy.setMoveArmsEnabled(True, True)
    motionNaoProxy.setMotionConfig([["ENABLE_FOOT_CONTACT_PROTECTION", True]])

    #TARGET VELOCITY
    motionX = -0.5  # backward
    motionY = 0.0
    RotZ = 0.0
    Frequency =0.0 # low speed
    try:
        motionNaoProxy.moveToward(motionX, motionY, RotZ, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    armMotionXY(motionNaoProxy)

    #TARGET VELOCITY
    motionX = 0.8
    motionY = 0.0
    RotZ = 0.0
    Frequency =1.0 # max speed
    try:
        motionNaoProxy.moveToward(motionX, motionY, RotZ, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    time.sleep(4.0)

    #TARGET VELOCITY
    motionX = 0.2
    motionY = -0.5
    RotZ = 0.2
    Frequency = 1.0

    try:
        motionNaoProxy.moveToward(motionX, motionY, RotZ, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    time.sleep(2.0)
    armMotion(motionNaoProxy)
    time.sleep(2.0)
	#Walk Ends now
    motionX = 0.0
    motionY = 0.0
    RotZ = 0.0
    motionNaoProxy.moveToward(motionX, motionY, RotZ)

    motionNaoProxy.waitUntilMoveIsFinished()

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
