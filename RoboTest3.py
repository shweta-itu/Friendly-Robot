from naoqi import ALProxy
NaoTTS = ALProxy("ALTextToSpeech", "127.0.0.1", 59438)
NaoTTS.say("Hello, ITU!")
NaoTTS.say("Hello, Welcome to Capstone!")