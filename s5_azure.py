# -*- coding: utf-8 -*-
import argparse
import sys
import qi
import time
import os

from _internet import connect
from _internet import createNewConnection
from _azureApi import procesar

def main(session):
    
    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    #memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    motion_service.rest() #sentarse

    tts_service.setLanguage('Spanish') # Lenguaje para hablar
    tts_service.say("\\vol=50\\Hola, yo soy NAO")

    sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)

    #!--------------------------------------INTERMEDIO--------------------------------------

    sexo_save = 0 #fem: 0 | masc:1
    edad_save = 23
    mis_sespecificos = ["tos amarilla", "dificultad para respirar", "dolor de cabeza"]
    mis_intensidades = ["medio", "medio", "medio"]

    #!--------------------------RESULTADOS Y RECOMENDACION----------------------------------
    tts_service.say("A continuación procesaré los síntomas. Espere por favor")
    
    os.remove("DIY_UPC.xml")

    #conectar a wlan
    createNewConnection("Ni te atrevas", "Ni te atrevas", "nvth2041")
    connect("Ni te atrevas", "Ni te atrevas")

    time.sleep(10)
    #resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

    os.remove("Ni te atrevas.xml")
    print("antes")
    time.sleep(3)
    createNewConnection("DIY_UPC", "DIY_UPC", "fablabupc7")
    connect("DIY_UPC", "DIY_UPC")
    connect("DIY_UPC", "DIY_UPC")
    time.sleep(5)
    print("despues")

    #tts_service=session.service("ALTextToSpeech")
    tts_service.say("hola")

    """
    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    #memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    motion_service.rest() #sentarse

    tts_service.setLanguage('Spanish') # Lenguaje para hablar
    tts_service.say("\\vol=50\\Hola, yo soy NAO")

    sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    """
    """
    for enfermedad in resultados:
        #tts_service.say(enfermedad[0])
        print(enfermedad)
        #print(type(enfermedad) + "->" + str(enfermedad))

    tts_service.say(recomendacion[0])
    """

    #volver a conectar al robot

#!-------------------------------INICIAR PROGRAMAA------------------------------------
if __name__ == "__main__":

    createNewConnection("DIY_UPC", "DIY_UPC", "fablabupc7")
    connect("DIY_UPC", "DIY_UPC")

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.15",
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
        sys.exit(1)
    main(session)
