# -*- coding: utf-8 -*-

#python 3InteraccionNombre.py

import qi
import argparse
import sys
import time
#from funciones import nombre
#from funciones import nombrebucle

from naoqi import ALProxy

def main(session):

    """
    ip = "192.168.1.15" #"127.0.0.1"
    port = 9559

    tts_service = ALProxy("ALTextToSpeech", ip, port)
    sr_service = ALProxy("ALSpeechRecognition", ip, port)
    memory_service = ALProxy("ALMemory", ip, port)
    
    """
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos
    motion_service = session.service("ALMotion")

    nombres = ['fernando','paolo','roberto','rafael', 'grecia'] #"fernando","paolo","roberto","grecia"
    edades = ['cinco','seis','siete','ocho',\
        'nueve','diez','once','doce','trece','catorce','quince','dieciseis','diecisiete',\
            'dieciocho','diecinueve','veinte']
    voc = nombres + edades
    print(voc)
    
    sr_service.pause(True)
    sr_service.setVocabulary(voc,True) #False
    sr_service.pause(False)
    print("vocabulario")

    #edad
    tts_service.say("Dime tu edad") #str() ?

    sr_service.subscribe("edad_id") #Empieza a escribir en memoria WordRecognized, identificador
    memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized') #evento, identificador

    #sr_service.pause(False)
    time.sleep(10)

    sr_service.unsubscribe("edad_id") #Deja de escribir en memoria
    #memory_service.unsubscribeToEvent('WordRecognized',"edad_id")#,'wordRecognized')

    edad=memory_service.getData("WordRecognized")#1era opcion d lista descendente | str()?
    print(edad[0]+"-"+str(edad[1]))
    edad = edad[0]

    edad = edad[6:]
    edad = edad[:-6]
    
    tts_service.say("Edad "+ edad) #str() ?

    askName = True
    while askName:

        tts_service.say("Dime tu nombre por favor")#Pedir nombre de usuario

        sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador

        #memory_service.subscribeToEvent('SpeechDetected',"escuchando_id",'wordRecognized')
        
        #sr_service.pause(False)
        time.sleep(10)
        
        sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
        #memory_service.unsubscribeToEvent('WordRecognized',"nombre_id")#,'wordRecognized')

        nombre=memory_service.getData("WordRecognized")
        print(nombre[0]+"-"+str(nombre[1]))
        nombre = nombre[0]

        nombre = nombre[6:]
        nombre = nombre[:-6]

        if nombre in nombres:
            tts_service.say("Hola, "+ nombre + " encantado de conocerte") #str() ?
            askName = False
            print(nombre) #print(aux, "|", aux[0], "|", aux[1])
            #print(type(nombre))
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu nombre?")


    """
        if nombre in nombres:
            tts_service.say("Hola, "+ nombre + " encantado de conocerte") #str() ?
            askName = False
            print(nombre) #print(aux, "|", aux[0], "|", aux[1])
            print(type(nombre))
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu nombre?") 

        memory_service.removeData("WordRecognized")
        print("remove2")
    """



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
