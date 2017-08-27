import sys
from naoqi import ALProxy

if (len(sys.argv) < 2):
    sys.exit(1)

IP = "127.0.0.1"
PORT = 46598
if (len(sys.argv) > 2):
    PORT = sys.argv[2]
try:
    ALTextNaoSpeech = ALProxy("ALTextToSpeech", IP, PORT)
except Exception,e:
    print "Error was: ",e
    sys.exit(1)

langs = ALTextNaoSpeech.getAvailableLanguages();
print "Available languages in Nao are: " + str(langs)