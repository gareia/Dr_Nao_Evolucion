# -*- coding: utf-8 -*-
import qi
import argparse
import sys
import time
from funciones import edad
from funciones import edadbucle

def main(session):

    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    print("edad")

    tts_service.say("Dime tu edad") #str() ?
    #edades=["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince"]
    edades = ["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis","diecisiete","dieciocho","diecinueve","veinte"]
    
    sr_service.pause(True)
    sr_service.setVocabulary(edades,True) #False
    print("asignacion")

    sr_service.subscribe("edad_id") #Empieza a escribir en memoria WordRecognized, identificador
    memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized') #evento, identificador

    sr_service.pause(False)
    time.sleep(5)

    edad=memory_service.getData("WordRecognized")[0] #1era opcion d lista descendente | str()?
    print(edad) #print(aux, "|", aux[0], "|", aux[1])
    
    sr_service.unsubscribe("edad_id") #Deja de escribir en memoria
    #memory_service.unsubscribeToEvent('WordRecognized',"edad_id")#,'wordRecognized')

    tts_service.say("Edad "+ edad) #str() ?




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
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