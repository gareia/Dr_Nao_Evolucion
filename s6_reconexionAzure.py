# -*- coding: utf-8 -*-
from _internet import connect
from _internet import createNewConnection
from _internet import removeConnection
from _azureApi import procesar

import argparse
import qi
import time
import urllib2
import sys

def saludar(session, naoRed):
    
    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    #memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    #motion_service.rest() 

    tts_service.setLanguage('Spanish') 
    #tts_service.say("\\vol=50\\Hola, yo soy NAO")

    sr_service.setLanguage("Spanish") 
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)

    #!--------------------------------------INTERMEDIO--------------------------------------
    sexo_save = 0 #fem: 0 | masc:1
    edad_save = 23
    mis_sespecificos = ["tos amarilla", "dificultad para respirar", "dolor de cabeza"]
    mis_intensidades = ["medio", "medio", "medio"]

    resultados = []
    recomendacion = []
    #!--------------------------RESULTADOS Y RECOMENDACION----------------------------------
    #tts_service.say("A continuación procesaré los síntomas. Espere por favor")
    
    removeConnection(naoRed)

    celularRed = "Ni te atrevas 2" #
    celularPass = "nfzm1408" #3gUbUVsXehf9eztAp39G
    
    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    try:    
        print("Espere por favor.. conectando con internet...\n")
        time.sleep(7)
        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)
        print("resultados: "+ str(len(resultados)))
        removeConnection(celularRed)

    except urllib2.HTTPError as error: #URLError
        removeConnection(celularRed)
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))

    #volver conectar a nao
    naoRed = "DIY_UPC" 
    naoPass = "fablabupc7"

    if(createNewConnection(naoRed, naoRed, naoPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(naoRed, naoRed) != 0):
        removeConnection(naoRed)
        print("Error al conectarse a la red")
        return 0

    print("Espere por favor.. conectando con Nao...\n")
    time.sleep(7)

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
        #sys.exit(1)
        return 0

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    #memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    #motion_service.rest() 

    tts_service.setLanguage('Spanish') 
    #tts_service.say("\\vol=50\\Hola, yo soy NAO")

    sr_service.setLanguage("Spanish") 
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    
    print("--------------------------------------\n")
    for enfermedad in resultados:
        print(enfermedad[0] + " con un " + str(enfermedad[1]))
        tts_service.say(enfermedad[0]+".")
    print("--------------------------------------\n")
    print(recomendacion[0])
    tts_service.say(recomendacion[0])
    print("--------------------------------------\n")

    removeConnection(naoRed)


#!-------------------------------INICIAR PROGRAMAA------------------------------------
def main():

    naoRed = "DIY_UPC" 
    naoPass = "fablabupc7"

    if(createNewConnection(naoRed, naoRed, naoPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(naoRed, naoRed) != 0):
        removeConnection(naoRed)
        print("Error al conectarse a la red")
        return 0

    print("Espere por favor.. conectando con Nao...\n")
    time.sleep(7)

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
        #sys.exit(1)
        return 0

    saludar(session, naoRed)

main()