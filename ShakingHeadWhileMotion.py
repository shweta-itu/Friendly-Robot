# -*- encoding: UTF-8 -*-

import argparse
import time
import random
from naoqi import ALProxy

def main(robotIP, PORT=25986):

    motionNaoProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureNaoProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Alert robot
    motionNaoProxy.wakeUp()

    # Send robot to Stand Init
    postureNaoProxy.goToPosture("StandInit", 0.5)

    # Initialize the move process.
    motionNaoProxy.moveInit()

    testTime = 10.0 # seconds
    t  = 0.0
    deltat = 0.35

    while t<testTime:
        deltaX         = random.uniform(0.4, 1.0)
        deltaY         = random.uniform(-0.4, 0.4)
        RotZ     = random.uniform(-0.4, 0.4)
        Frequency = random.uniform(0.5, 1.0)
        try:
            motionNaoProxy.moveToward(deltaX, deltaY, RotZ, [["Frequency", Frequency]])
        except Exception, errorMsg:
            print str(errorMsg)
            exit()

        # Sudden Head Movement
        motionNaoProxy.setAngles("HeadYaw", random.uniform(-1.0, 1.0), 0.6)
        motionNaoProxy.setAngles("HeadPitch", random.uniform(-0.5, 0.5), 0.6)

        t = t + dt
        time.sleep(dt)

    motionNaoProxy.stopMove()

    # Rest position
    motionNaoProxy.rest()

if __name__ == "__main__":
    parseFile = argparse.ArgumentParser()
    parseFile.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parseFile.add_argument("--port", type=int, default=52742,
                        help="Robot port number")

    args = parseFile.parse_args()
    main(args.ip, args.port)
