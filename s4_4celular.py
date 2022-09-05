# -*- coding: utf-8 -*-

#python s4_4celular.py

import qi
import argparse
import sys
import time

def main(session): 

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")
    motion_service.rest() #sentarse
    
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------VOCABULARIO---------------------------------------
    digitos = ['cero','uno','dos','tres','cuatro','cinco','seis','siete','ocho','nueve']
    digs_dict = {dig: i for i, dig in enumerate(digitos)} #diccionario cadena:numero

    vocabulario = digitos
    print(vocabulario)
    
    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True) #False
    sr_service.pause(False)
    print("asignado el vocabulario")

    cel = ''
    tts_service.say("Procederé a guardar su número de celular dígito por dígito") 

    #!------------------------------------CELULAR------------------------------------------
    askCel = True
    while askCel:

        tts_service.say("Dígame el dígito") 

        #Escuchar
        sr_service.subscribe("digito_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"digito_id",'wordRecognized') #evento, identificador
        time.sleep(7)
        sr_service.unsubscribe("digito_id") #Deja de escribir en memoria

        #Extraer data
        dig=memory_service.getData("WordRecognized")
        print(dig[0]+"-"+str(dig[1])) #palabra y probabilidad
        dig = dig[0][6:-6] #de la palabra lo necesario
        
        if dig in digitos:
            tts_service.say(dig)
            print(dig)
            cel += str(digs_dict[dig])

            if(len(cel)) == 9:
                askCel = False
        else:
            tts_service.say("Disculpe, no entendí")

    tts_service.say("El número al que mandaré los resultados y la recomendación es ")

    for c in cel:
        tts_service.say(c) #TODO: digitos[c]