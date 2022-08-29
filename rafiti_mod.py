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
    sexos=['femenino','masculino','otro']
    sexo_dict={'femenino':0,'masculino':1,'otro':2} #solo para la cortesia

    sr_service.setVocabulary(sexos,True)

    askSexo = True
    while askSexo:
        
        tts_service.say("Por favor dígame ¿Cuál es su sexo: femenino, masculino u otro?")

        sr_service.subscribe("sexo_id")
        memory_service.subscribeToEvent('WordRecognized',"sexo_id",'wordRecognized')

        sr_service.pause(False)
        time.sleep(5)

        sexo=memory_service.getData("WordRecognized")[1] #? (value,pair)

        sr_service.unsubscribe("sexo_id")
        memory_service.unsubscribeToEvent('WordRecognized',"sexo_id")

        if sexo in sexos: 
            sexo_save = sexo_dict[sexo]
            askSexo = False
        else:
            tts_service.say("Disculpe, no pude entender")

    #Asignar cortesía
    print(sexo_save)
    if sexo_save == 0:
        cortesia = "Señorita"
    elif sexo_save == 1:
        cortesia = "Señor"
    elif sexo_save == 2:
        cortesia = "Paciente"
        sexo_save = 1 #se considera masculino

    #Edad
    edades=["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis",\
        "diecisiete","dieciocho","diecinueve","veinte"]
    edad_dict = {edad: i+5 for i, edad in enumerate(edades)} #diccionario cadena:numero

    sr_service.setVocabulary(edades,True) 

    askEdad = True
    while askEdad:

        tts_service.say(cortesia + "¿Cuántos años tiene? ")

        sr_service.subscribe("edad_id")
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

        sr_service.pause(False)
        time.sleep(5)

        edad=memory_service.getData("WordRecognized")[1] #? (value,pair)

        sr_service.unsubscribe("edad_id")
        memory_service.unsubscribeToEvent('WordRecognized',"edad_id")

        if edad in edades: 
            edad_save = edad_dict[edad]
            askEdad = False
        else:
            tts_service.say("Disculpe, no pude entender")

    #Sintomas generales
    sgenerales=["tos","dificultad para respirar","dolores","perdida de peso","fatiga",\
    "molestias generales"]

    for sg in sgenerales:
        decir_sgenerales += sg + ', '

    decir_sgenerales = decir_sgenerales[:-2] #sin ultima comita y espacio
    sgenerales += ["no"] #opcion no
    
    intensidades = ["bajo","medio","alto"]
    #intensidad_dict={"baja":0,"bajo":0,"media":1,"medio":1,"alta":2,"alto":2}
    #opcionesContinuar = ["si", "no"]
    
    mis_sgenerales = [] #? set 
    mis_sespecificos = [] #? set
    mis_intensidades = []
    
    askSGeneral = True
    while askSGeneral:

        #Despistaje covid   
        if len(mis_sgenerales) >= 3:
            tts_service.say("Usted presenta por lo menos 3 síntomas de Covid")
            time.sleep(1)
            tts_service.say("Por favor, realícese una prueba de descarte")
            time.sleep(1)
            tts_service.say("Hasta pronto, " + cortesia)
            motion_service.rest()
            return

        #Listar síntomas generales
        tts_service.say("Si presenta alguno de los siguientes síntomas generales repítalo")
        time.sleep(1)
        tts_service.say(decir_sgenerales) #TODO Mostrar en pantalla sintomas
        time.sleep(1)
        tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para finalizar el proceso")

        #asignar vocabulario de sintomas generales
        sr_service.setVocabulary(sgenerales,True)

        sr_service.subscribe("sgeneral_id") 
        memory_service.subscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')

        sr_service.pause(False) #?
        time.sleep(7)

        sgeneral=memory_service.getData("WordRecognized")[1] #? str()
        print(sgeneral)

        sr_service.unsubscribe("sgeneral_id")
        memory_service.unsubscribeToEvent('WordRecognized',"sgeneral_id")

        if sgeneral in sgenerales:

            if sgeneral == "no":
                #deja de pedir sintomas generales
                askSGeneral = False
                #se procesan los especificos
                if len(mis_sespecificos) == 0: #si no ha mencionado ningun sintoma esp -> se despide
                    tts_service.say("No hay síntomas qué procesar. Hasta pronto, " + cortesia)
                    motion_service.rest()
                    return
                #si ha mencionado alguno -> pasa al algoritmo
                break 
            
            #Para el despistaje de covid
            mis_sgenerales.append(sgeneral)
            tts_service.say("Síntoma general "+ str(len(mis_sgenerales)) + ": " + sgeneral)
            
            #Declarar síntomas específicos para el síntoma general
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
                
                sespecificos=['perdida de apetito', 'nauseas', 'vomitos', 'diarrea', \
                'perdida de peso por perdida de apetito', 'perdida de peso']
     
            elif sgeneral =='fatiga o cansancio':
                
                sespecificos=['fatiga', 'mal humor inusual', 'despertarse con frecuencia', \
                'irritabilidad']

            elif sgeneral =='molestias generales':

                sespecificos=['fiebre', 'frio', 'fiebre de bajo grado', 'transpiracion', 'sacudida', 
                'fiebre alta','piel azulada', 'escalofrios', 'mareo', 'desmayo', 'edema', 'ronquidos', 
                'somnolencia diurna', 'dificultades con la memoria y la concentracion', 'sudores nocturnos', 
                'angustioso', 'dedos de manos y pies mas anchos y redondos que lo normal']
                
            for se in sespecificos:
                decir_sespecificos += se + ', '

            decir_sespecificos = decir_sespecificos[:-2]
            sespecificos += ["no"] #opcion no
            
            askSEspecifico = True
            while askSEspecifico:

                #Listar síntomas especificos
                tts_service.say("Si presenta alguno de los siguientes síntomas específicos repítalo")
                time.sleep(1)
                tts_service.say(decir_sespecificos) #TODO Mostrar en pantalla sintomas
                time.sleep(1)
                tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para finalizar el proceso")

                #asignar vocabulario de sintomas especificos
                sr_service.setVocabulary(sespecificos,True)

                sr_service.subscribe("sespecifico_id")
                memory_service.subscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')
                
                sr_service.pause(False) #?
                time.sleep(7)

                sespecifico = memory_service.getData("WordRecognized")[1]
                print(sespecifico)

                sr_service.unsubscribe("sespecifico_id")
                memory_service.unsubscribeToEvent('WordRecognized',"sespecifico_id")

                if sespecifico in sespecificos :

                    if sespecifico == "no":
                        askSEspecifico = False
                        #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                        break 

                    mis_sespecificos.append(sespecifico) #TODO solo con especificos se procesa?
                    tts_service.say("Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico)
             
                    askIntensidad = True
                    while askIntensidad:

                        tts_service.say("¿Qué tan intenso es el síntoma? Bajo, medio o alto")

                        #asignar vocabulario de intesidades
                        sr_service.setVocabulary(intensidades,True)

                        sr_service.subscribe("intensidad_id")
                        memory_service.subscribeToEvent('WordRecognized',"intensidad_id",'wordRecognized')
                        
                        sr_service.pause(False) #?
                        time.sleep(5)

                        intensidad =memory_service.getData("WordRecognized")[1]

                        sr_service.unsubscribe("intensidad_id")
                        memory_service.unsubscribeToEvent('WordRecognized',"intensidad_id")

                        if intensidad in intensidades:

                            mis_intensidades.append(intensidad)
                            
                            tts_service.say("Anotado")
                            time.sleep(1)
                            tts_service.say("Síntoma " + sespecifico + "con intensidad " + sespecifico)

                            askIntensidad = False

                        else:
                            tts_service.say("Disculpe, no pude entender")
                    
                else:
                    tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 

        else:
            tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 
        
    #Procesar síntomas #TODO Mortalidad
    tts_service.say("A continuación procesaré los síntomas. Espere por favor")
    algoritmo(edad_save,sexo_save, mis_sespecificos, mis_intensidades)

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
