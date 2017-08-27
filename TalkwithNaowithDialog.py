import sys
from naoqi import ALProxy

# Change port as seen on choreographe
port = 57818
dialog_p = ALProxy("ALDialog","127.0.0.1",port)
dialog_p.setLanguage("English")

# Add complete path to topic file
toppath = "/Users/shwetasahu/Dropbox/ITU/Spring 2017/Capstone Project SWE 690 1/final_capstone_project/demo/topic_final.txt"
toppath = toppath.decode('utf-8')
dialog_p.subscribe("mymodule")
topic = dialog_p.loadTopic(toppath.encode('utf-8'))
dialog_p.activateTopic(topic)
