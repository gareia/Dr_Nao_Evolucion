# -*- coding: utf-8 -*-

#python s4_0anterior.py

import qi
import argparse
import sys
import time

#TODO arreglar consola | emitir sonido

def main(session): 

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")
    motion_service.rest() #sentarse

    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------VOCABULARIO---------------------------------------
    #TODO cambié | las comillas
    nombres = ["fernando","paolo","roberto","rafael","jireh","grecia"] #"fernando","paolo","roberto","grecia"
    edades = ['cinco','seis','siete','ocho',\
        'nueve','diez','once','doce','trece','catorce','quince',\
        'dieciseis','diecisiete','dieciocho','diecinueve','veinte']
    vocabulario = nombres + edades
    print(vocabulario)
    
    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True) #False
    sr_service.pause(False)
    print("asignado el vocabulario")

    #!--------------------------------------EDAD--------------------------------------------
    askEdad = True
    while askEdad:

        tts_service.say("Dime tu edad") 

        sr_service.subscribe("edad_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized') #evento, identificador

        time.sleep(10)

        sr_service.unsubscribe("edad_id") #Deja de escribir en memoria
        #memory_service.unsubscribeToEvent('WordRecognized',"edad_id")

        edad=memory_service.getData("WordRecognized")
        print(edad[0]+"-"+str(edad[1])) #palabra y probabilidad
        edad = edad[0][6:-6] #TODO: cambié | de la palabra lo necesario
        
        if edad in edades:
            askEdad = False
            tts_service.say("Edad "+ edad)
            print("Edad: "+ edad)
        else:
            tts_service.say("Disculpa, ¿puedes repetir tu edad?")

    #!--------------------------------------NOMBRE--------------------------------------------
    askName = True
    while askName:

        tts_service.say("Dime tu nombre por favor")#Pedir nombre de usuario

        sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador

        #memory_service.subscribeToEvent('SpeechDetected',"escuchando_id",'wordRecognized')
        time.sleep(10)
        
        sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
        #memory_service.unsubscribeToEvent('WordRecognized',"nombre_id")#,'wordRecognized')

        nombre=memory_service.getData("WordRecognized")
        print(nombre[0]+"-"+str(nombre[1])) #palabra y probabilidad
        nombre = nombre[0][6:-6] #de la palabra lo necesario #nombre = nombre[6:-6]

        if nombre in nombres:
            askName = False
            tts_service.say("Hola, "+ nombre + " encantado de conocerte") 
            print("Nombre: "+ nombre)            
        else:
            tts_service.say("Disculpa, ¿puedes repetir tu nombre?")


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
