# -*- coding: utf-8 -*-

#python s5_celular.py

import qi
import argparse
import sys
import time

def main(session): 

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    motion_service.rest() #sentarse

    tts_service.setLanguage('Spanish') # Lenguaje para hablar

    sr_service.setLanguage("Spanish")
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)

    #!-----------------------------------VOCABULARIO---------------------------------------
    prob_aceptable = 0.4

    digitos = []
    for d in range(1000):
        digitos.append(str(d))

    confirmacion = ["si", "no"]

    vocabulario = digitos + confirmacion
    #print(vocabulario)
    
    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True) #False
    sr_service.pause(False)
    print(">Vocabulario asignado")

    cel = ""
    tts_service.say("Por favor, dícteme un número celular de 9 dígitos")
    
    askCel = True
    while askCel:

        print(askCel, cel, len(cel))
        tts_service.say("Lo escucho") 

        sr_service.subscribe("digito_id")
        memory_service.subscribeToEvent('WordRecognized',"digito_id",'wordRecognized')
        time.sleep(4)
        sr_service.unsubscribe("digito_id")

        dig=memory_service.getData("WordRecognized")
        dig_pal = dig[0][6:-6] #de la palabra lo necesario
        dig_prob = dig[1] #probabilidad
        print(dig_pal+"-"+str(dig_prob))
        
        if (dig_pal in digitos) and (dig_prob >= prob_aceptable):
            
            askConfirmacion = True
            while askConfirmacion:

                print("¿ Ha dicho " + dig_pal + " ?")
                tts_service.say("¿ Ha dicho " + dig_pal + " ?")

                sr_service.subscribe("confirmacion_id") 
                memory_service.subscribeToEvent('WordRecognized',"confirmacion_id",'wordRecognized')
                time.sleep(5)
                sr_service.unsubscribe("confirmacion_id")

                confirmado=memory_service.getData("WordRecognized")
                confirmado_pal = confirmado[0][6:-6] #de la palabra lo necesario
                confirmado_prob = confirmado[1] #probabilidad
                print(confirmado_pal+"-"+str(confirmado_prob))
                
                if (confirmado_pal in confirmacion) and (confirmado_prob >= prob_aceptable):

                    askConfirmacion = False

                    if confirmado_pal == "si":
                        cel += dig_pal 

                        if len(cel) == 9:
                            askCel = False #terminado, continuar el flujo
                        if len(cel) > 9:
                            cel = ""
                            tts_service.say("El número celular tiene más de 9 dígitos")
                            tts_service.say("Volvamos a empezar")

                    else: #no -> volver a pedir digito
                        tts_service.say("Disculpe, entendí mal. Repítame")
                else:
                    tts_service.say("Disculpe, no pude entender")
        else:
            tts_service.say("Disculpe, no entendí. Nuevamente")


    tts_service.say("El número al que mandaré los resultados y la recomendación es ")

    for c in cel:
        tts_service.say(c)

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