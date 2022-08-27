# -*- coding: utf-8 -*-
from naoqi import ALProxy
import time

ip = "127.0.0.1"
port = 9559
tts = ALProxy("ALTextToSpeech", ip, port)
#motion = ALProxy("ALMotion", ip, port)
#motion.wakeUp()
tts.say("Hello, world!")


time.sleep(2)
tts.say("Había un tío")
tts.setLanguage('Spanish')
time.sleep(2)
tts.say("Había un tío")
#motion.rest()