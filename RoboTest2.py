import sys
from naoqi import ALProxy
import almath

def main(NaoIP):
    PORT = 9559
    try:
        motionNaoProxy = ALProxy("ALMotion", NaoIP, PORT)
    except Exception, e:
        print "Error was: ",e
        sys.exit(1)

    try:
        postNaoProxy = ALProxy("ALRobotPosture", NaoIP, PORT)
    except Exception, e:
        print "Error was: ", e

    postNaoProxy.goToPosture("StandInit", 0.5)
    useSensValues = False
    result = motionNaoProxy.getRobotPosition(useSensValues)
    print "Nao Position", result
    useSensValues = False
    initNaoPosition = almath.Pose2D(motionNaoProxy.getRobotPosition(useSensValues))

    motionNaoProxy.moveTo(41, 1, 0.0)

    endNaoPosition = almath.Pose2D(motionNaoProxy.getRobotPosition(useSensValues))


    NaoMove = almath.pose2DInverse(initRobotPosition)*endNaoPosition
    print "Nao Move:", NaoMove
if __name__ == "__main__":
    NaoIp = "127.0.0.1"
    main(NaoIp)