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
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    sr_service.pause(True)
    sr_service.setVocabulary(["rafael","mateo","lucas"],True)
    sr_service.pause(False)
    print("vocabulario asignado")

    #motion_service.wakeUp()
    #motion_service.moveInit()
    #motion_service.post.moveTo(0.5, 0, 0)
    #for i in range(3):
        #motion_service.angleInterpolation(names, [-3.0, 1.2, -0.7], times, True)
        #motion_service.angleInterpolation(names, [-1.0, 1.2, -0.7], times, True)

    
    sys.exit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.13",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        print("tcp://" + args.ip + ":" + str(args.port))
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit()
    main(session)