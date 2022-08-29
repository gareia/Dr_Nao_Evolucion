# -*- coding: utf-8 -*-
import qi
import argparse
import sys
import time
from Azure_Api import algoritmo

def main(session):

    #Iniciar servicios
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #Despertar al robot
    motion_service.wakeUp() #se levanta
    
    tts_service.setLanguage('Spanish') # Lenguaje para hablar
    sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    
    #Presentarse
    tts_service.say("Hola, yo soy NAO")

    #Sexo
    tts_service.say("Por favor dígame ¿Cuál es su sexo: femenino, masculino u otro?")
    
    sexos=['femenino','masculino','otro']
    sexo_dict={'femenino':0,'masculino':1,'otro':2}

    sr_service.setVocabulary(sexos,True)

    hasSexo = False
    while not hasSexo:

        sr_service.subscribe("sexo_id")
        memory_service.subscribeToEvent('WordRecognized',"sexo_id",'wordRecognized')

        sr_service.pause(False)
        time.sleep(10)

        sexo=memory_service.getData("WordRecognized")[1] #? (value,pair)

        if sexo in sexos: 
            sexo_save = sexo_dict[sexo]
            sr_service.unsubscribe("edad_id")
            memory_service.unsubscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
            hasSexo = True
        else:
            tts_service.say("Por favor repítame ¿Cuál es su sexo: femenino, masculino u otro?")

    #Asignar cortesía
    print(sexo_save)
    if sexo_save == 0:
        cortesia = "Señorita"
    elif sexo_save == 1:
        cortesia = "Señor"
    elif sexo_save == 2:
        cortesia = "Paciente"
        sexo_save = 1

    #Edad
    tts_service.say(cortesia + "¿Cuántos años tiene? ")

    edades=["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis",\
        "diecisiete","dieciocho","diecinueve","veinte"]
    edad_dict = {edad: i+5 for i, edad in enumerate(edades)} #diccionario cadena:numero

    sr_service.setVocabulary(edades,True) 

    hasEdad = False
    while not hasEdad:

        sr_service.subscribe("edad_id")
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

        sr_service.pause(False)
        time.sleep(10)

        edad=memory_service.getData("WordRecognized")[1] #? (value,pair)

        if edad in edades: 
            edad_save = edad_dict[edad]
            sr_service.unsubscribe("edad_id")
            memory_service.unsubscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
            hasEdad = True
        else:
            tts_service.say("Disculpe, repítame ¿Cuántos años tiene?")

    #Sintomas generales
    sgenerales=["tos","dificultad para respirar","dolores","perdida de peso","fatiga","molestias generales", "no"]
    sr_service.setVocabulary(sgenerales,True)

    for sg in sgenerales:
        decir_sgenerales += sg + ', '

    decir_sgenerales = decir_sgenerales[:-2] #sin ultima comita y espacio
    
    opcionesContinuar = ["si", "no"]
    nuevoSintoma = True
    mis_sgenerales = [] #? set 
    mis_sespecificos = [] #? set

    while nuevoSintoma:

        #Despistaje covid   
        if len(mis_sgenerales) >= 3:
            tts_service.say("Usted presenta por lo menos 3 síntomas de Covid")
            time.sleep(1)
            tts_service.say("Por favor, realícese una prueba de descarte")
            time.sleep(1)
            tts_service.say("Nos vemos")
            motion_service.rest()
            return

        #Pedir síntomas
        tts_service.say("Si presenta alguno de los siguientes síntomas repítalo")
        time.sleep(1)
        tts_service.say(decir_sgenerales) #TODO Mostrar en pantalla sintomas
        time.sleep(1)
        tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para finalizar el proceso")

        sr_service.subscribe("sgeneral_id") 
        memory_service.subscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')

        sr_service.pause(False) #?
        time.sleep(7)

        sgeneral=memory_service.getData("WordRecognized")[1] #? str()
        print(sgeneral)

        if sgeneral in sgenerales:

            sr_service.unsubscribe("sgeneral_id")
            memory_service.unsubscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')

            #Terminar todos los procesos
            if sgeneral == "no":
                tts_service.say("Hasta pronto, " + cortesia)
                motion_service.rest()
                nuevoSintoma = False
                return 

            mis_sgenerales.append(sgeneral)
            tts_service.say("Síntoma general "+ str(len(mis_sgenerales)) + ": " + sgeneral)
            
            decir_sespecificos = "Si presentas alguno de estos síntomas específicos repítelo, por favor: "

            #declarar sintomas especificos para el sintoma general
            if sgeneral =='tos':

                sespecificos=['alergia','tos con mucosidad amarilla o verde todos los dias',\
                    'nariz que moquea','congestion nasal', 'tos amarilla', 'moco', 'tos cronica',\
                    'tos seca', 'tos verdosa', 'tos con sangre','dolor de garganta',\
                    'boca seca','tos sibilante','tos seca persistente']
                
            elif sgeneral =='dificultad para respirar':
                
                sespecificos=['sensacion de opresion en el pecho','sibilancias', \
                    'dificultad para respirar que empeora durante los brotes', 'nariz que moquea','congestion nasal'\
                    'congestion en el pecho','respiracion rapida','respiracion superficial',\
                    'dolor agudo en el pecho','latidos rapidos','palpitaciones del corazon','pausas en la respiracion',\
                    'respiracion corta superficial y rapida','falta de aliento','latido del corazon mas rapido',\
                    'un sonido seco y crepitante en los pulmones al inhalar']
               
            elif sgeneral =='dolores':
                
                sespecificos=['dolor de pecho','congestion en el pecho', 'dolor de espalda baja', \
                    'dolor agudo en el pecho','dolor de cabeza','dolores musculares','dolor en las articulaciones',\
                    'dolor de garganta','edema','dolores de cabeza matutinos']

            elif sgeneral =='perdida peso':
                
                sespecificos=['perdida de apetito', 'nauseas', 'vomitos', 'diarrea', 'perdida de peso por perdida de apetito', 'perdida de peso']
     
            elif sgeneral =='fatiga o cansancio':
                
                sespecificos=['fatiga', 'mal humor inusual', 'despertarse con frecuencia', 'irritabilidad']

            elif sgeneral =='molestias generales':

                sespecificos=['fiebre', 'frio', 'fiebre de bajo grado', 'transpiracion', 'sacudida', 
                'fiebre alta','piel azulada', 'escalofrios', 'mareo', 'desmayo', 'edema', 'ronquidos', 
                'somnolencia diurna', 'dificultades con la memoria y la concentracion', 'sudores nocturnos', 
                'angustioso', 'dedos de manos y pies mas anchos y redondos que lo normal']
                
            #asignar sintomas especificos
            sr_service.setVocabulary(sespecificos,True)

            for se in sespecificos:
                decir_sespecificos += se + ', '

            decir_sespecificos = decir_sespecificos[:-2]
            
            hasSEspecifico=False
            while not hasSEspecifico:

                tts_service.say(decir_sespecificos)

                sr_service.subscribe("sespecifico_id")
                memory_service.subscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')
                
                sr_service.pause(False) #?
                time.sleep(10)

                sespecifico = memory_service.getData("WordRecognized")[1]
                print(sespecifico)

                if sespecifico in sespecificos :

                    sr_service.unsubscribe("sespecifico_id")
                    memory_service.unsubscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')

                    mis_sespecificos.append(sespecifico)
                    tts_service.say("Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico)
                    
                    intensidades = ["baja", "bajo", "media", "medio", "alta", "alto"]
                    mis_intensidades = []

                    hasIntensidad = False
                    while not hasIntensidad:

                        tts_service.say("¿Con qué intensidad? Baja, alta o media")

                        sr_service.subscribe("sintensidad_id")
                        memory_service.subscribeToEvent('WordRecognized',"sintensidad_id",'wordRecognized')
                        
                        sr_service.pause(False) #?
                        time.sleep(5)

                        intensidad =memory_service.getData("WordRecognized")[1]

                        if intensidad in intensidades:
                            sr_service.unsubscribe("sintensidad_id")
                            memory_service.unsubscribeToEvent('WordRecognized',"sintensidad_id",'wordRecognized')

                            mis_intensidades.append(intensidad)
                            
                            tts_service.say("Anotado")
                            tts_service.say("Síntoma " + sespecifico + "con intensidad " + sespecifico)
                            hasIntensidad = True

                        else:
                            tts_service.say("Por favor, repíteme") 

                    """
                    bool_answer=False
                    while bool_answer==False:
                        tts_service.say("Tienes mas sintomas?")
                        tts_recognition_service.pause(False)
                        time.sleep(5)
                        if str(sintomas_recog[0])=='si' :
                            tts_service.say("Te gustaria escuchar denuevo los sintomas?")
                            tts_recognition_service.pause(False)
                            time.sleep(5)
                            if str(sintomas_recog[0])=='si' :
                                tts_service.say("Los sintomas son los siguientes: alergia,tos con mucosidad amarilla o verde todos los dias,\
                                            nariz que moquea,congestion nasal, tos amarilla, moco, tos cronica,tos seca, tos verdosa, tos con sangre,dolor de garganta,\
                                            boca seca,tos sibilante,tos seca persistente")
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0]) in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])                                    

                            elif str(sintomas_recog[0])=='no':
                                tts_service.say('Dime tu sintoma, porfavor')
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0])in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                        elif str(sintomas_recog[0])=='no' :
                            tts_recognition_service.pause(False)
                            tts_recognition_service.unsubscribe("sintoma")
                            memory_service.unsubscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
                            bool_answer=True
                            boolean=True
                    """
                    hasSEspecifico = True
                else:
                    tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 

            #Continuar escuchando?
            tts_service.say("¿Presenta algún síntoma adicional?")
            hasContinuar = False

            #mientras no escuche la respuesta
            while not hasContinuar:
                sr_service.subscribe("continuar_id") 
                memory_service.subscribeToEvent('WordRecognized',"continuar_id",'wordRecognized')

                sr_service.pause(False) #
                time.sleep(5) #

                continuar=memory_service.getData("WordRecognized")[1] #str() ?
                print(continuar)

                if continuar in opcionesContinuar:

                    #dejar de preguntar si continuar
                    hasContinuar = True

                    #Dejar de pedir sintomas generales
                    if continuar == "no":
                        tts_service.say("Hasta pronto, " + cortesia)
                        nuevoSintoma = False
                        break
                    
                else:
                    tts_service.say("Repítame ¿Presenta algún síntoma adicional?")

        else:
            tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 

    #Procesar síntomas #TODO
    algoritmo(edad_save,sexo_save, sespecificos) 

    #Despedirse
    tts_service.say("Con esta información, le sugiero que contacte a un médico profesional")
    time.sleep(1)
    tts_service.say("Muchas gracias por conversar conmigo")
    motion_service.rest() #se apaga


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
