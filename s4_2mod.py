# -*- coding: utf-8 -*-

#python s4_2parte.py

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
    
    ##tts_service.say("Hola, yo soy NAO")

    #!-----------------------------------VOCABULARIO---------------------------------------
    
    opciones = ["no"]

    sintomas={}
    sintomas["tos"] = ['alergia','tos con mucosidad amarilla o verde todos los dias',\
                    'nariz que moquea','congestion nasal', 'tos amarilla', 'moco', 'tos cronica',\
                    'tos seca', 'tos verdosa', 'tos con sangre','dolor de garganta',\
                    'boca seca','tos sibilante','tos seca persistente']
    sintomas["dificultad para respirar"] = ['sensacion de opresion en el pecho','sibilancias', \
                    'dificultad para respirar que empeora durante los brotes', 'nariz que moquea','congestion nasal'\
                    'congestion en el pecho','respiracion rapida','respiracion superficial',\
                    'dolor agudo en el pecho','latidos rapidos','palpitaciones del corazon','pausas en la respiracion',\
                    'respiracion corta superficial y rapida','falta de aliento','latido del corazon mas rapido',\
                    'un sonido seco y crepitante en los pulmones al inhalar']
    sintomas["dolores"] = ['dolor de pecho','congestion en el pecho', 'dolor de espalda baja', \
                    'dolor agudo en el pecho','dolor de cabeza','dolores musculares','dolor en las articulaciones',\
                    'dolor de garganta','edema','dolores de cabeza matutinos']
    sintomas["perdida de peso"] = ['perdida de apetito', 'nauseas', 'vomitos', 'diarrea', \
                'perdida de peso por perdida de apetito', 'perdida de peso']
    sintomas["fatiga"] = ['fatiga', 'mal humor inusual', 'despertarse con frecuencia', \
                'irritabilidad']
    sintomas["molestias generales"] = ['fiebre', 'frio', 'fiebre de bajo grado', 'transpiracion', 'sacudida', 
                'fiebre alta','piel azulada', 'escalofrios', 'mareo', 'desmayo', 'edema', 'ronquidos', 
                'somnolencia diurna', 'dificultades con la memoria y la concentracion', 'sudores nocturnos', 
                'angustioso', 'dedos de manos y pies mas anchos y redondos que lo normal']

    sgenerales = [sg for sg in sintomas]

    decir_sgenerales = ''
    sespecificos = []

    for sg in sgenerales:
        sespecificos += sintomas[sg]
        decir_sgenerales += sg + ', '
    
    decir_sgenerales = decir_sgenerales[:-2] #sin ultima comita y espacio

    admitir_sgenerales = sgenerales + opciones

    intensidades = ["bajo","medio","alto"]

    vocabulario = sgenerales + opciones #+ intensidades+ sespecificos
    
    scovid = ["fiebre","tos","fatiga","falta de aliento",\
        "dificultad para respirar"] #perdida del gusto o del olfato"?

    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True)
    sr_service.pause(False)
    print("asignado el vocabulario")

    sexo_save = 2 #0 1 2

    #------Asignar cortesía
    if sexo_save == 0:
        cortesia = "Señorita"
    elif sexo_save == 1:
        cortesia = "Señor"
    elif sexo_save == 2:
        cortesia = "Paciente"
        sexo_save = 1 #se considera masculino

    #!----------------------------------SINTOMAS GENERALES------------------------------------

    mis_sespecificos = [] #? set
    mis_intensidades = []
    nummax_scovid = 3
    contar_scovid = 0

    askSGeneral = True
    while askSGeneral:

        #Listar síntomas generales
        print("Sintomas generales: " + decir_sgenerales)
        tts_service.say("Si presenta alguno de los siguientes síntomas generales repítalo")
        ##time.sleep(1)
        print(decir_sgenerales)
        ##tts_service.say(decir_sgenerales)
        ##time.sleep(1)
        ##tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para finalizar el proceso")

        #Escuchar
        sr_service.subscribe("sgeneral_id") 
        memory_service.subscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')
        tts_service.say("ya")
        time.sleep(15)
        tts_service.say("ya")
        sr_service.unsubscribe("sgeneral_id")
        
        #sr_service.removeAllContext()

        #Extraer data
        sgeneral=memory_service.getData("WordRecognized")
        print(sgeneral[0]+"-"+str(sgeneral[1])) #palabra y probabilidad
        sgeneral = sgeneral[0][6:-6] #de la palabra lo necesario
        
        #Si es una palabra admitida
        if sgeneral in admitir_sgenerales:

            if sgeneral == "no":
                askSGeneral = False
                #si no hay ningun especifico para procesar -> adiós
                if len(mis_sespecificos) == 0:
                    tts_service.say("No hay síntomas qué procesar. Hasta pronto, " + cortesia)
                    print("Fin: No se ha registrado ningún síntoma específico para procesar")
                    return
                #si ha mencionado alguno -> pasa al algoritmo
                break 
            
            print("----------------------------")
            tts_service.say("Recibido: Síntoma general: " + sgeneral)
            print("Recibido: Síntoma general " + sgeneral)
            
            decir_sespecificos = ''
            for se in sintomas[sgeneral]: #solo los sintomas especificos de este sintomas general
                decir_sespecificos += se + ', '

            decir_sespecificos = decir_sespecificos[:-2] #sin ultima comita y espacio
            print("Sintomas específicos: " + decir_sespecificos)

            admitir_sespecificos = sintomas[sgeneral] + opciones
           
            #!----------------------------------SINTOMAS ESPECIFICOS------------------------------------
            askSEspecifico = True
            while askSEspecifico:
                
                #!--------------------DESPISTAJE COVID--------------------------------
                for mi_se in mis_sespecificos:
                    if mi_se in scovid:
                        contar_scovid += 1
                
                if contar_scovid >= nummax_scovid:
                    tts_service.say("Usted presenta por lo menos "+ str(nummax_scovid) +" síntomas de Covid")
                    time.sleep(1)
                    tts_service.say("Por favor, realícese una prueba de descarte")
                    time.sleep(1)
                    tts_service.say("Hasta pronto, " + cortesia)
                    #motion_service.rest()
                    print("Fin: Recomendación descarte covid")
                    return
                #!--------------------------------------------------------------------

                #Listar síntomas especificos
                tts_service.say("Si presenta alguno de los siguientes síntomas específicos repítalo")
                ##time.sleep(1)
                ##tts_service.say(decir_sespecificos)
                ##time.sleep(1)
                ##tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para finalizar el proceso")
                
                #Escuchar
                sr_service.subscribe("sespecifico_id")
                memory_service.subscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')
                time.sleep(15)
                sr_service.unsubscribe("sespecifico_id")
                
                ##sr_service.removeAllContext()
                
                #Extraer data
                sespecifico = memory_service.getData("WordRecognized")
                print(sespecifico[0]+"-"+str(sespecifico[1])) #palabra y probabilidad
                sespecifico = sespecifico[0][6:-6] #de la palabra lo necesario

                #Si es una palabra admitida
                if sespecifico in admitir_sespecificos :

                    if sespecifico == "no":
                        askSEspecifico = False
                        #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                        break 

                    mis_sespecificos.append(sespecifico)
                    tts_service.say("Recibido. Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico)
                    print("Recibido. Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico)
             
                    askIntensidad = True
                    while askIntensidad:

                        tts_service.say("¿Qué tan intenso es el síntoma? Bajo, medio o alto")

                        #Escuchar
                        sr_service.subscribe("intensidad_id")
                        memory_service.subscribeToEvent('WordRecognized',"intensidad_id",'wordRecognized')
                        time.sleep(10)
                        sr_service.unsubscribe("intensidad_id")
                        
                        #sr_service.removeAllContext()
                        
                        #Extraer data
                        intensidad =memory_service.getData("WordRecognized")
                        print(intensidad[0]+"-"+str(intensidad[1])) #palabra y probabilidad
                        intensidad = intensidad[0][6:-6] #de la palabra lo necesario

                        if intensidad in intensidades:
                            askIntensidad = False
                            mis_intensidades.append(intensidad)
                            tts_service.say("Anotado")
                            time.sleep(1)
                            tts_service.say("Recibido. Síntoma " + sespecifico + "con intensidad " + sespecifico)
                            print("Recibido. Síntoma " + sespecifico + "con intensidad " + sespecifico)
                        else:
                            tts_service.say("Disculpe, no pude entender")
                    
                else:
                    tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 

            print("----------------------------")

        else:
            tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 
        
    #!----------------------------------DESPEDIRSE------------------------------------
    tts_service.say("Con esta información, le sugiero que contacte a un médico profesional")
    time.sleep(1)
    tts_service.say("Muchas gracias por conversar conmigo")
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
