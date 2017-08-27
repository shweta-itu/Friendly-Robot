import argparse
import almath as m
from naoqi import ALProxy

def main(robotIP, PORT=52742):

    motionNaoProxy  = ALProxy("ALMotion", robotIP, PORT)
    postureNaoProxy = ALProxy("ALRobotPosture", robotIP, PORT)

    # Wake up robot
    motionNaoProxy.wakeUp()

    # Send robot to Stand Init
    postureNaoProxy.goToPosture("StandInit", 0.5)

    # first we defined the goalNao
    goalNao = m.Pose2D(0.0, -0.4, 0.0)

     circleR = 0.04
    dubinAbs = m.getDubinsSolutions(goalNao, circleR)

     # So, we compute dubinsSolution relative form
    dubinRel = []
    dubinRel.append(dubinAbs[0])
    for i in range(len(dubinAbs)-1):
        dubinRel.append(
                dubinAbs[i].inverse() *
                dubinAbs[i+1])

    # create a vector of moveTo with dubins Control Points
    moveTarg = []
    for i in range(len(dubinRel)):
        moveTarg.append(
            [dubinRel[i].x,
             dubinRel[i].y,
             dubinRel[i].theta] )

     motionNaoProxy.moveInit()

    # get robot position before move
    robotNaoPosnBefCommand  = m.Pose2D(motionNaoProxy.getRobotPosition(False))

    motionNaoProxy.moveTo( moveTarg )

    # get robot position after move
    robotNaoPosnAftCommand = m.Pose2D(motionNaoProxy.getRobotPosition(False))

    # compute and print the robot motion
    moveNaoComms = m.pose2DInverse(robotNaoPosnBefCommand)*robotNaoPosnAftCommand
    print "The Robot Move Command: ", moveNaoComms

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
