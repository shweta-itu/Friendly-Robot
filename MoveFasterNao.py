import argparse
import time
from naoqi import ALProxy

def main(robotIP, PORT=56945):

    motionNaoProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureNaoProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionNaoProxy.wakeUp()

    # Send robot to Stand Init
    postureNaoProxy.goToPosture("StandInit", 0.5)

    # Initialize the walk process.
    motionNaoProxy.moveInit()

 
    motionX         = 2.0
    motionY         = 0.0
    Theta     = 0.0
    Frequency = 3.0


    try:
        motionNaoProxy.moveToward(motionX, motionY, Theta, [["Frequency", Frequency]])
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    time.sleep(3.0)
    print "walk Speed motionX :",motionNaoProxy.getRobotVelocity()[0]," m/s"


    try:
        motionNaoProxy.moveToward(motionX, motionY, Theta, [["Frequency", Frequency],
                                             ["MaxStepX", 0.06]])
    except Exception, errorMsg:
        print str(errorMsg)
        exit()

    time.sleep(4.0)
    print "walk Speed motionX :",motionNaoProxy.getRobotVelocity()[0]," m/s"

    # stop walk on the next double support
    motionNaoProxy.stopMove()

    # Go to rest position
    motionNaoProxy.rest()

if __name__ == "__main__":
    parseArgs = argparse.ArgumentParser()
    parseArgs.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot ip address")
    parseArgs.add_argument("--port", type=int, default=52742,
                        help="Robot port number")

    args = parseArgs.parse_args()
    main(args.ip, args.port)
