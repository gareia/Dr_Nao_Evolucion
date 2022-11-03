# -*- coding: utf-8 -*-
import qi
import argparse
import sys
import time

def main(session):

    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general

    motion_service.rest()

    #tts_service.setLanguage('Spanish')
    #tts_service.say("Hola") #, yo soy NAO. A continuación haremos algunas pruebas")#Pedir nombre de usuario
    #sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    
    #tts_service.say("Hola, yo soy NAO") 

    #sr_service.pause(True)
    #sr_service.setVocabulary(["rafael","mateo","lucas"],True)
    #tts_service.setVolume(0.3)#Disminuir el volumen a la mitad \\vol=30\\
    #tts_service.setParameter("speed",150) #50-400 default=100
    #sr_service.setAudioExpression(True)
    #sr_service.setVisualExpression(True)
    #sr_service.pause(False)
    #print("vocabulario asignado")

    #tts_service.say("Hola, yo soy NAO") 

    #motion_service.wakeUp()
    #motion_service.moveInit()
    #motion_service.post.moveTo(0.5, 0, 0)
    #for i in range(3):
        #motion_service.angleInterpolation(names, [-3.0, 1.2, -0.7], times, True)
        #motion_service.angleInterpolation(names, [-1.0, 1.2, -0.7], times, True)


try:
    session = qi.Session()

    pathNaoIp = '_redNaoIp.txt'
    with open(pathNaoIp, 'r') as file:
        naoIp = file.read()
        print("Ip Nao: "+naoIp)

    pathNaoPort = '_redNaoPort.txt'
    with open(pathNaoPort , 'r') as file:
        naoPort  = file.read()

    tcpStr = "tcp://" + naoIp + ":" + str(naoPort)
    print(tcpStr)
    session.connect(tcpStr)
    main(session)

except RuntimeError:
    raise Exception("No se puede conectar a Naoqi con ip \"" + naoIp + "\" y puerto" + str(naoPort))
except Exception:
    raise Exception("Ocurrió un error inesperado al conectar con Nao")

sys.exit()