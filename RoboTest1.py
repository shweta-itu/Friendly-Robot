import qi
import argparse
import sys


def main(session):
    """
    This example uses the goToPosture method.
    """
    # Get the service ALRobotPosture.

    postNaoProxy = session.service("ALRobotPosture")

    postNaoProxy.goToPosture("StandInit", 1.0)
    postNaoProxy.goToPosture("SitRelax", 1.0)
    postNaoProxy.goToPosture("StandZero", 1.0)
    postNaoProxy.goToPosture("LyingBelly", 1.0)
    postNaoProxy.goToPosture("LyingBack", 1.0)
    postNaoProxy.goToPosture("Stand", 1.0)
    postNaoProxy.goToPosture("Crouch", 1.0)
    postNaoProxy.goToPosture("Sit", 1.0)

    print postNaoProxy.getPostureFamily()


if __name__ == "__main__":
    ParseArgs = argparse.ArgumentParser()
    ParseArgs.add_argument("--ip", type=str, default="127.0.0.1")
    ParseArgs.add_argument("--port", type=int, default=65423")

    args = ParseArgs.parse_args()
    session = qi.Session()
    main(session)
