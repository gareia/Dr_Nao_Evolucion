# -*- coding: utf-8 -*-
from s5_internet import connect
from s5_internet import createNewConnection
from s5_internet import removeConnection
from Azure_ApiSolo import procesar

import qi
import argparse
import sys
import time
#import pywhatkit
import urllib2

naoRed = "DIY_UPC" 

def conectarNao():
    
    naoPass = "fablabupc7"

    if(createNewConnection(naoRed, naoRed, naoPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(naoRed, naoRed) != 0):
        removeConnection(naoRed)
        print("Error al conectarse a la red")
        return 0

    print("Espere por favor.. conectando con Nao...\n")
    time.sleep(7)

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.1.15",help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,help="Naoqi port number")
    args = parser.parse_args()
    session = qi.Session()
    try:
        print("tcp://" + args.ip + ":" + str(args.port))
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        return 0

    return session
    
def ejecutar():

    session = conectarNao()
    if session == 0: return 0

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    motion_service.rest() #sentarse

    tts_service.setLanguage('Spanish') # Lenguaje para hablar

    sr_service.setLanguage("Spanish") # Lenguaje para reconocer voces o sonidos
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)

    #!-----------------------------------VOCABULARIO---------------------------------------

    tts_service.say("\\vol=50\\Hola, yo soy NAO")

    prob_aceptable = 0.4 

    sexos=['femenino','masculino']
    sexo_dict={'femenino':0,'masculino':1}

    escape = ["no"]
    confirmacion = ["si", "no"]

    sintomas={}
    sintomas["tos"] = ['tos','tos amarilla','tos crónica','tos seca','tos verdosa',\
                    'tos con sangre','tos sibilante','tos seca persistente',\
                    'tos con mucosidad amarilla o verde todos los días','boca seca',
                    'congestión nasal','naríz que moquea','moco','alergia']
    sintomas["relacionado a respirar"] = ['dificultad para respirar','sensación de opresión en el pecho',\
                    'dificultad para respirar que empeora durante los brotes','dolor de pecho',\
                    'congestión en el pecho','dolor agudo en el pecho','respiración rápida',\
                    'respiración superficial','latidos rápidos','palpitaciones del corazón','pausas en la respiración',\
                    'respiración corta superficial y rápida','falta de aliento','latido del corazón mas rápido',\
                    'un sonido seco y crepitante en los pulmones al inhalar','sibilancias','aliento']
    sintomas["dolores"] = ['dolor de espalda baja', 'dolor de pecho'\
                    'dolor de cabeza','dolores musculares','dolor en las articulaciones',\
                    'dolor de garganta','dolores de cabeza matutinos','dolor']
    sintomas["pérdida de peso"] = ['pérdida de apetito', 'nauseas', 'vómitos', 'diarrea', \
                'pérdida de peso por pérdida de apetito', 'pérdida de peso']
    sintomas["relacionado a fatiga"] = ['fatiga', 'mal humor inusual', 'despertarse con frecuencia', \
                'irritabilidad']
    sintomas["molestias generales"] = ['fiebre', 'frío', 'fiebre de bajo grado', 'transpiración', 'sacudida', 
                'fiebre alta','piel azulada', 'escalofríos', 'mareo', 'desmayo', 'edema', 'ronquidos', 
                'somnolencia diurna', 'dificultades con la memoria y la concentración', 'sudores nocturnos', 
                'angustioso', 'dedos de manos y pies mas anchos y redondos que lo normal']

    sgenerales = [sg for sg in sintomas]


    decir_sgenerales = ''
    sespecificos = []

    for sg in sgenerales:
        sespecificos += sintomas[sg]
        decir_sgenerales += sg + '. '
    decir_sgenerales = decir_sgenerales[:-2] #sin ultima comita y espacio

    admitir_sgenerales = sgenerales + escape

    intensidades = ["bajo","medio","alto"]

    digitos = []
    for d in range(1000):
        digitos.append(str(d))

    vocabulario = sexos + sgenerales + sespecificos + escape + intensidades + digitos + confirmacion

    sr_service.pause(True)
    sr_service.setVocabulary(vocabulario,True)
    sr_service.pause(False)
    print(">Vocabulario asignado")

    #molestias generales #relacionado a respirar #relacionado a fatiga #relacionado a respirar
    scovid = ["fiebre","tos","fatiga","falta de aliento",\
        "dificultad para respirar"] #perdida del gusto o del olfato"?

    #!--------------------------------------SEXO--------------------------------------------
    askSexo = True
    while askSexo:
        
        tts_service.say("¿Cuál es su sexo biológico?") 
        tts_service.say("Femenino. O. Masculino.")

        sr_service.subscribe("sexo_id") 
        memory_service.subscribeToEvent('WordRecognized',"sexo_id",'wordRecognized')
        time.sleep(6)
        sr_service.unsubscribe("sexo_id")

        sexo=memory_service.getData("WordRecognized")
        sexo_pal = sexo[0][6:-6] #de la palabra lo necesario
        sexo_prob = sexo[1] #probabilidad
        print(sexo_pal+"-"+str(sexo_prob)) 
        
        if (sexo_pal in sexos) and (sexo_prob >= prob_aceptable): 

            askConfirmacion = True
            while askConfirmacion:

                print("¿ Ha dicho " + sexo_pal + " ?")
                tts_service.say("¿ Ha dicho " + sexo_pal + " ?")

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
                        askSexo = False
                        tts_service.say("Recibido: sexo "+ sexo_pal)
                        sexo_save = sexo_dict[sexo_pal]
                        print("Sexo: "+ str(sexo_save) + "( " + sexo_pal + ")")

                    else: #no -> volver a pedir sexo
                        tts_service.say("Disculpe, entendí mal. Repítame")

                else:
                    tts_service.say("Disculpe, no pude entender")
        
        else:
            tts_service.say("Disculpe, no pude entender")

    #!--------------------------------------EDAD--------------------------------------------
    askEdad = True 
    while askEdad:

        tts_service.say("¿Cuántos años tiene?")

        sr_service.subscribe("edad_id")
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
        time.sleep(6)
        sr_service.unsubscribe("edad_id")

        edad=memory_service.getData("WordRecognized")
        edad_pal = edad[0][6:-6] #de la palabra lo necesario
        edad_prob = edad[1] #probabilidad
        print(edad_pal+"-"+str(edad_prob))
        
        if (edad_pal in digitos) and (edad_prob >= prob_aceptable): 

            askConfirmacion = True
            while askConfirmacion:

                print("¿ Ha dicho " + edad_pal + " ?")
                tts_service.say("¿ Ha dicho " + edad_pal + " ?")

                sr_service.subscribe("confirmacion_id") 
                memory_service.subscribeToEvent('WordRecognized',"confirmacion_id",'wordRecognized')
                time.sleep(5)
                sr_service.unsubscribe("confirmacion_id")

                confirmado=memory_service.getData("WordRecognized")
                confirmado_pal = confirmado[0][6:-6] #de la palabra lo necesario
                confirmado_prob = confirmado[1] #probabilidad
                print(confirmado_pal+"-"+str(confirmado_prob))

                if (confirmado_pal in confirmacion) and (confirmado_prob >= prob_aceptable):

                    askConfirmacion = False #deja de pedir confirmacion

                    if confirmado_pal == "si":
                        if(int(edad_pal) > 120):
                            tts_service.say("Debe decir una edad dentro del rango de 0 a 120")
                            continue #pasa a la sgte iteración (vuelve a pedir la edad)
                        askEdad = False
                        tts_service.say("Recibido: edad "+ edad_pal + " años")
                        edad_save = int(edad_pal)#edad_dict[edad_pal]
                        print("Edad: "+ edad_pal)
                    else: #no -> volver a pedir edad
                        tts_service.say("Disculpe, entendí mal. Repítame")
                else:
                    tts_service.say("Disculpe, no pude entender")

        else:
            tts_service.say("Disculpe, no pude entender")

    #!----------------------------------SINTOMAS GENERALES------------------------------------

    mis_sespecificos = [] #setish
    mis_intensidades = [] #setish
    nummax_scovid = 2
    contar_scovid = 0

    askSGeneral = True
    while askSGeneral:

        print("Sintomas generales: " + decir_sgenerales)
        tts_service.say("Si presenta alguno de los siguientes síntomas generales repítalo")
        ##time.sleep(1)
        ##tts_service.say(decir_sgenerales)
        ##time.sleep(1)
        tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para continuar")

        sr_service.subscribe("sgeneral_id") 
        memory_service.subscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')
        time.sleep(10)
        sr_service.unsubscribe("sgeneral_id")

        sgeneral=memory_service.getData("WordRecognized")
        sgeneral_pal = sgeneral[0][6:-6] #de la palabra lo necesario
        sgeneral_prob = sgeneral[1] #probabilidad
        print(sgeneral_pal+"-"+str(sgeneral_prob))
        
        if (sgeneral_pal in admitir_sgenerales) and (sgeneral_prob >= prob_aceptable):

            if sgeneral_pal == "no":
                askSGeneral = False
                #si no hay ningun especifico para procesar -> adiós
                if len(mis_sespecificos) == 0:
                    tts_service.say("No hay síntomas qué procesar. Hasta pronto")
                    print("Fin: No hay síntomas qué procesar. Hasta pronto")
                    return
                #si ha mencionado alguno -> pasa al algoritmo
                break 
            
            print("----------------------------")
            tts_service.say("Recibido: Síntoma general " + sgeneral_pal)
            print("Recibido: Síntoma general " + sgeneral_pal)
            
            decir_sespecificos = ''
            for se in sintomas[sgeneral_pal]: #solo los sintomas especificos de este sintomas general
                decir_sespecificos += se + '. '

            decir_sespecificos = decir_sespecificos[:-2] #sin ultima comita y espacio
            print("Sintomas específicos: " + decir_sespecificos)

            admitir_sespecificos = sintomas[sgeneral_pal] + escape
           
            #!----------------------------------SINTOMAS ESPECIFICOS------------------------------------
            askSEspecifico = True
            while askSEspecifico:
                
                tts_service.say("Si presenta alguno de los siguientes síntomas específicos repítalo")
                ##time.sleep(1)
                ##tts_service.say(decir_sespecificos)
                ##time.sleep(1)
                tts_service.say("Si no presenta ninguno de estos síntomas diga la palabra no para continuar")
                
                sr_service.subscribe("sespecifico_id")
                memory_service.subscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')
                time.sleep(10)
                sr_service.unsubscribe("sespecifico_id")
                
                sespecifico = memory_service.getData("WordRecognized")
                sespecifico_pal = sespecifico[0][6:-6] #de la palabra lo necesario
                sespecifico_prob = sespecifico[1] #probabilidad
                print(sespecifico_pal+"-"+str(sespecifico_prob))

                if (sespecifico_pal in admitir_sespecificos) and (sespecifico_prob >= prob_aceptable):

                    askConfirmacion = True

                    if sespecifico_pal == "no":
                        askConfirmacion = False
                        askSEspecifico = False
                        #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                        tts_service.say("Okey Volvamos a los síntomas generales")
                        break 

                    while askConfirmacion:

                        print("¿ Ha dicho " + sespecifico_pal + " ?")
                        tts_service.say("¿ Ha dicho " + sespecifico_pal + " ?")

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
                                """
                                if sespecifico_pal == "no":
                                    askSEspecifico = False
                                    #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                                    tts_service.say("Okey Volvamos a los síntomas generales")
                                    break 
                                """
                                if sespecifico_pal in mis_sespecificos:
                                    tts_service.say("Este síntoma ya ha sido registrado.")
                                    continue

                                if sespecifico_pal in scovid:
                                    contar_scovid += 1
                                
                                #!--------------------DESPISTAJE COVID--------------------------------
                                if contar_scovid >= nummax_scovid: #si supera el límite d síntomas similares de covid
                                    
                                    askPruebaCovid = True
                                    while askPruebaCovid:
                                        tts_service.say("Usted presenta por lo menos "+ str(nummax_scovid) +" síntomas de Covid")
                                        tts_service.say("¿Se ha realizado la prueba de descarte de Covid?")
                                        
                                        sr_service.subscribe("prueba_covid_id")
                                        memory_service.subscribeToEvent('WordRecognized',"prueba_covid_id",'wordRecognized')
                                        time.sleep(6)
                                        sr_service.unsubscribe("prueba_covid_id")
                                        
                                        pruebaCovid = memory_service.getData("WordRecognized")
                                        pruebaCovid_pal = pruebaCovid[0][6:-6] #de la palabra lo necesario
                                        pruebaCovid_prob = pruebaCovid[1] #probabilidad
                                        print(pruebaCovid_pal+"-"+str(pruebaCovid_prob))

                                        if (pruebaCovid_pal in confirmacion) and (pruebaCovid_prob >= prob_aceptable):
                                            
                                            askPruebaCovid = False

                                            if pruebaCovid_pal == "no":
                                                tts_service.say("Por favor, realícese una prueba de descarte")
                                                tts_service.say("Hasta pronto")
                                                print("Fin: Recomendación descarte covid")
                                                return 1 #termina todo el proceso
                                            #else -> continua pidiendo la intensidad del síntoma mencionado
                                        else:
                                            tts_service.say("Disculpe, no pude entender")
                                #!--------------------------------------------------------------------

                                mis_sespecificos.append(sespecifico_pal)
                                
                                tts_service.say("Recibido. Síntoma específico "+ str(len(mis_sespecificos)) + ": " + sespecifico_pal)
                                print("Recibido. Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico_pal)
                        
                                askIntensidad = True
                                while askIntensidad:

                                    tts_service.say("¿Qué tan intenso es el síntoma? Bajo, medio o alto")

                                    sr_service.subscribe("intensidad_id")
                                    memory_service.subscribeToEvent('WordRecognized',"intensidad_id",'wordRecognized')
                                    time.sleep(6)
                                    sr_service.unsubscribe("intensidad_id")
                                    
                                    intensidad = memory_service.getData("WordRecognized")
                                    intensidad_pal = intensidad[0][6:-6] #de la palabra lo necesario
                                    intensidad_prob = intensidad[1] #probabilidad
                                    print(intensidad_pal+"-"+str(intensidad_prob))

                                    if (intensidad_pal in intensidades) and (intensidad_prob >= prob_aceptable):
                                        askIntensidad = False
                                        mis_intensidades.append(intensidad_pal)
                                        tts_service.say("Recibido. Síntoma " + sespecifico_pal + " con intensidad " + intensidad_pal)
                                        print("Recibido. Síntoma " + sespecifico_pal + " con intensidad " + intensidad_pal)
                                    else:
                                        tts_service.say("Disculpe, no pude entender")
                    
                            else: #no -> volver a pedir sintoma especifico
                                tts_service.say("Disculpe, entendí mal. Repítame")

                        else:
                            tts_service.say("Disculpe, no pude entender")

                else:
                    tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 

            print("----------------------------")

        else:
            tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 
        
    #!--------------------------RESULTADOS Y RECOMENDACION------------------------------
    tts_service.say("A continuación procesaré los síntomas. Espere por favor")

    removeConnection(naoRed)

    celularRed = "Ni te atrevas 2" #
    celularPass = "nfzm1408" #3gUbUVsXehf9eztAp39G
    
    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    try:    
        print("Espere por favor.. conectando con internet...\n")
        time.sleep(7)
        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)
        print("resultados: "+ str(len(resultados)))
        removeConnection(celularRed)

    except urllib2.HTTPError as error:
        removeConnection(celularRed)
        print("Http Error con código: " + str(error.code))
        print(error.info())
        return 0

    except urllib2.URLError as error:
        removeConnection(celularRed)
        print("Url Error")
        return 0

    session = conectarNao()
    if session == 0: return 0

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #!-----------------------------------PRESENTARSE---------------------------------------
    #motion_service.rest() 

    tts_service.setLanguage('Spanish') 
    #tts_service.say("\\vol=50\\Hola, yo soy NAO")

    sr_service.setLanguage("Spanish") 
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    
    print("--------------------------------------\n")
    for enfermedad in resultados:
        print(enfermedad[0] + " con un " + str(enfermedad[1]))
        tts_service.say(enfermedad[0]+".")
    print("--------------------------------------\n")
    print(recomendacion[0])
    tts_service.say(recomendacion[0])
    print("--------------------------------------\n")

    removeConnection(naoRed)

    #!------------------------------------CELULAR-------------------------------------
    cel = ""
    tts_service.say("Por favor, dícteme un número celular de 9 dígitos") 

    askCel = True
    while askCel:

        print(askCel, cel, len(cel))
        tts_service.say("Lo escucho") 

        sr_service.subscribe("numero_id")
        memory_service.subscribeToEvent('WordRecognized',"numero_id",'wordRecognized')
        time.sleep(10)
        sr_service.unsubscribe("numero_id")

        num=memory_service.getData("WordRecognized")
        num_pal = num[0][6:-6] #de la palabra lo necesario
        num_prob = num[1] #probabilidad
        print(num_pal+"-"+str(num_prob))

        if (num_pal in digitos) and (num_prob >= prob_aceptable):
            
            askConfirmacion = True
            while askConfirmacion:

                print("¿ Ha dicho " + num_pal + " ?")
                tts_service.say("¿ Ha dicho " + num_pal + " ?")

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

                    if confirmado_pal == "si": #una vez confirmado el número escuchado
                        cel += num_pal #concatenamos

                        if len(cel) < 9: 
                            tts_service.say("Continúe") #siga dictando
                        if len(cel) == 9:
                            askCel = False #terminado, continuar el flujo
                        if len(cel) > 9:
                            cel = "" #volver a empezar
                            tts_service.say("El número celular tiene más de 9 dígitos")
                            tts_service.say("Volvamos a empezar") 

                    else: #no -> volver a pedir numero
                        tts_service.say("Disculpe, entendí mal. Repítame")
                else:
                    tts_service.say("Disculpe, no pude entender")
        else:
            tts_service.say("Disculpe, no entendí. Nuevamente")

    tts_service.say("El número al que mandaré los resultados y la recomendación es ")

    for c in cel:
        tts_service.say(c)

    cel = "+51" + cel

    #time.sleep(7)
    #pywhatkit.sendwhatmsg_instantly(cel, "Mensaje a enviaaaar", 20) #Python3

    #!----------------------------------DESPEDIRSE------------------------------------
    tts_service.say("Con esta información, le sugiero que contacte a un médico profesional")
    tts_service.say("Muchas gracias por conversar conmigo")
    #motion_service.rest() #sentarse


#!-------------------------------INICIAR PROGRAMAA------------------------------------
ejecutar()


