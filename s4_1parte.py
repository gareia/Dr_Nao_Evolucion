# -*- coding: utf-8 -*-

#python s4_1parte.py

import qi
import argparse
import sys
import time
#from Azure_Api import procesar

def main(session): #TODO session

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    motion_service.rest() #sentarse
    tts_service.setLanguage('Spanish') # Lenguaje para hablar
    sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    
    tts_service.say("Hola, yo soy NAO")

    #!-----------------------------------VOCABULARIO---------------------------------------
    sexos=['femenino','masculino','otro']
    sexo_dict={'femenino':0,'masculino':1,'otro':2} #solo para la cortesia

    edades=["cinco","seis","siete","ocho","nueve","diez",\
        "once","doce","trece","catorce","quince",\
        "dieciseis","diecisiete","dieciocho","diecinueve","veinte",\
        "veintiuno","veintidos","veintitres","veinticuatro","veinticinco",\
        "veintiseis","veintisiete","veintiocho","veintinueve","treinta"]
    edad_dict = {edad: i+5 for i, edad in enumerate(edades)} #diccionario cadena:numero

    vocabulario = sexos + edades 

    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True)
    sr_service.pause(False)
    print("asignado el vocabulario")
    
    #!--------------------------------------SEXO--------------------------------------------
    askSexo = True
    while askSexo:
        
        tts_service.say("Por favor dígame ¿Cuál es su sexo: femenino, masculino u otro?") #TODO

        sr_service.subscribe("sexo_id") 
        memory_service.subscribeToEvent('WordRecognized',"sexo_id",'wordRecognized') #TODO parameters

        time.sleep(10)

        sr_service.unsubscribe("sexo_id")
        #memory_service.unsubscribeToEvent('WordRecognized',"sexo_id") #TODO

        sexo=memory_service.getData("WordRecognized")
        print(sexo[0]+"-"+str(sexo[1])) #palabra y probabilidad
        sexo = sexo[0][6:-6] #de la palabra lo necesario
        
        if sexo in sexos: 
            askSexo = False
            tts_service.say("Recibido: sexo "+ sexo)
            sexo_save = sexo_dict[sexo]
            print("Sexo: "+ str(sexo_save) + "( " + sexo + ")")
        else:
            tts_service.say("Disculpe, no pude entender")

    #------Asignar cortesía
    if sexo_save == 0:
        cortesia = "Señorita"
    elif sexo_save == 1:
        cortesia = "Señor"
    elif sexo_save == 2:
        cortesia = "Paciente"
        sexo_save = 1

    #!--------------------------------------EDAD--------------------------------------------
    askEdad = True
    while askEdad:

        tts_service.say(cortesia + "¿Cuántos años tiene? ")

        sr_service.subscribe("edad_id")
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

        time.sleep(10)

        sr_service.unsubscribe("edad_id")
        #memory_service.unsubscribeToEvent('WordRecognized',"edad_id")

        edad=memory_service.getData("WordRecognized")
        print(edad[0]+"-"+str(edad[1])) #palabra y probabilidad
        edad = edad[0][6:-6] #de la palabra lo necesario
        
        if edad in edades: 
            askEdad = False
            tts_service.say("Recibido: edad "+ edad + " años")
            edad_save = edad_dict[edad]
            print("Edad: "+ str(edad_save) + " (" + edad + ")")
        else:
            tts_service.say("Disculpe, no pude entender")

    #!----------------------------------DESPEDIRSE------------------------------------
    ##tts_service.say("Con esta información, le sugiero que contacte a un médico profesional")
    ##time.sleep(1)
    ##tts_service.say("Muchas gracias por conversar conmigo")
    #motion_service.rest() #sentarse


#!-------------------------------INICIAR PROGRAMAA------------------------------------
if __name__ == "__main__":
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
