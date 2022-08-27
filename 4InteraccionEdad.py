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

    tts_service.say("¿Cuántos años tienes?")

    edades = ["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis",\
        "diecisiete","dieciocho","diecinueve","veinte"]
    edad_dict = {edad: i+5 for i, edad in enumerate(edades)} #diccionario cadena-numero
    
    sr_service.setVocabulary(edades,True) # False: Busca palabra exacta True : obviar palabras o frases ejemplo: <Tengo> cinco <anios> , obviara los que contengan <>

    edad(tts_service, sr_service, memory_service, edades, edad_dict)
    #edadbucle(tts_service, sr_service, memory_service, edades, edad_dict)

    sr_service.pause(False)
    time.sleep(2)
    tts_service.say("Pasemos a la siguiente pregunta") 


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