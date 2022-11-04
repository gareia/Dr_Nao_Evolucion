# -*- coding: utf-8 -*-
from _internet import connect,createNewConnection,removeConnection
from _azureApi import procesar

import sys
import qi #para crear la sesión
import time
import urllib2 #azure api exception
import csv

print("------archivo flujo-------")

naoRed = "" 
internetRed = ""

cel =""
resultados = []
recomendacion = []

def fcelular():
    return cel

def fresultados():
    return resultados

def frecomendacion():
    return recomendacion

def conectarInternet():

    global internetRed
    #Ver archivo _auxRedes.txt
    try:
        pathInternetId = '_redInternetId.txt'
        with open(pathInternetId, 'r') as file:
            internetRed = file.read()
            print("Red internet: "+internetRed)
    except Exception as e:
        raise Exception("Ocurrió un error al leer el archivo "+pathInternetId)

    try:
        pathInternetPass = '_redInternetPass.txt'
        with open(pathInternetPass, 'r') as file:
            celularPass = file.read()
    except Exception as e:
        raise Exception("Ocurrió un error al leer el archivo "+pathInternetPass)
    
    #!--------------------------------------------------------------------

    if(createNewConnection(internetRed, internetRed, celularPass) != 0):
        raise Exception("Error al agregar red " + internetRed)

    time.sleep(3)

    if(connect(internetRed, internetRed) != 0):
        removeConnection(internetRed)
        raise Exception("Error al conectarse a la red " + internetRed)

def conectarNao():
    
    global naoRed
    #Ver archivo _auxRedes.txt
    try:
        pathNaoId = '_redNaoId.txt'
        with open(pathNaoId, 'r') as file:
            naoRed = file.read()
            print("Red Nao: "+naoRed)
    except Exception:
        raise Exception("Ocurrió un error al leer el archivo "+pathNaoId)
    
    try:
        pathNaoPass = '_redNaoPass.txt'
        with open(pathNaoPass, 'r') as file:
            naoPass = file.read()
    except Exception:
        raise Exception("Ocurrió un error al leer el archivo "+pathNaoPass)
    

    if(createNewConnection(naoRed, naoRed, naoPass) != 0):
        raise Exception("Error al agregar red "+naoRed)

    time.sleep(3)

    if(connect(naoRed, naoRed) != 0):
        removeConnection(naoRed)
        raise Exception("Error al conectarse a la red "+naoRed)

    print("Espere por favor.. conectando con Nao...\n")

    time.sleep(7)
    
    try:
        
        session = qi.Session()

        pathNaoIp = '_redNaoIp.txt'
        with open(pathNaoIp, 'r') as file:
            naoIp = file.read()
            print("Ip Nao: "+naoIp)

        pathNaoPort = '_redNaoPort.txt'
        with open(pathNaoPort , 'r') as file:
            naoPort  = file.read()

        tcpStr = "tcp://" + naoIp + ":" + str(naoPort)
        print(tcpStr)
        session.connect(tcpStr)

    except RuntimeError:
        raise Exception("No se puede conectar a Naoqi con ip \"" + naoIp + "\" y puerto" + str(naoPort))
    except Exception:
        raise Exception("Ocurrió un error inesperado al conectar con Nao")

    return session
    
def ejecutar():

    session = conectarNao()

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    #motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    #motion_service.rest() #sentarse 
    sr_service.pause(True)
    tts_service.setLanguage('Spanish') # Lenguaje para hablar

    #!-----------------------------------VOCABULARIO---------------------------------------
    prob_aceptable = 0.4 

    sexos=['femenino','masculino']
    sexo_dict={'femenino':0,'masculino':1}

    confirmacion = ["si", "no"]

    #En minúsculas
    sintomas={}
    sintomas["relacionado a tos"] = ['tos','tos amarilla','tos crónica','tos seca','tos verdosa',\
                    'tos con sangre','tos sibilante','tos seca persistente',\
                    'tos con mucosidad amarilla o verde todos los días','boca seca',\
                    'congestión nasal','nariz que moquea','moco','alergia']
    sintomas["relacionado a respirar"] = ['dificultad para respirar','sensación de opresión en el pecho',\
                    'dificultad para respirar que empeora durante los brotes','dolor de pecho',\
                    'congestión en el pecho','dolor agudo en el pecho','respiración rápida',\
                    'respiración superficial','latidos rápidos','palpitaciones del corazón','pausas en la respiración',\
                    'respiración corta superficial y rápida','falta de aliento','latido del corazón mas rápido',\
                    'un sonido seco y crepitante en los pulmones al inhalar','sibilancias','aliento']
    sintomas["dolores"] = ['dolor de espalda baja', 'dolor de pecho',\
                    'dolor de cabeza','dolores musculares','dolor en las articulaciones',\
                    'dolor de garganta','dolores de cabeza matutinos','dolor']
    sintomas["pérdida de peso"] = ['pérdida de apetito', 'náuseas', 'vómitos', 'diarrea', \
                'pérdida de peso por pérdida de apetito', 'pérdida de peso']
    sintomas["relacionado a fatiga"] = ['fatiga', 'mal humor inusual', 'despertarse con frecuencia', \
                'irritabilidad']
    sintomas["molestias generales"] = ['fiebre', 'frío', 'fiebre de bajo grado', 'transpiración', 'sacudida', \
                'fiebre alta','piel azulada', 'escalofríos', 'mareo', 'desmayo', 'edema', 'ronquidos', \
                'somnolencia diurna', 'dificultades con la memoria y la concentración', 'sudores nocturnos', \
                'angustioso', 'dedos de manos y pies mas anchos y redondos que lo normal']

    sgenerales = [sg for sg in sintomas]

    lista_sgenerales = ''
    sespecificos = []

    for sg in sgenerales:
        sespecificos += sintomas[sg]
        lista_sgenerales += sg + '. '
    lista_sgenerales = lista_sgenerales[:-2] #sin ultima comita y espacio

    
    opciones = ["no", "repetir", "ya no tengo más síntomas"]

    admitir_sgenerales = sgenerales + opciones

    intensidades = ["bajo","medio","alto"]

    limiteEdad = 120
    edades = []
    for d in range(limiteEdad):
        edades.append(str(d))

    digitos = edades + []

    nummax_digito = 10
    for d1 in range(nummax_digito):
        for d2 in range(nummax_digito):
            digitos.append(str(d1)+" "+str(d2))
            #for d3 in range(nummax_digito):
                #digitos.append(str(d1)+" "+str(d2)+" "+str(d3))

    print("len(edades): "+str(len(edades)))
    print("len(digitos): "+str(len(digitos)))

    csvfile = "_nombresComunes.csv" 
    nombres = []
    try:
        
        with open(csvfile) as f:
            names_csv = csv.reader(f)
            for row in names_csv:
                nombres.append(row[0])
            
    except FileNotFoundError:
        raise Exception("No se ha encontrado el archivo llamado " + csvfile)
    except Exception:
        raise Exception("Ha ocurrido un error al cargar los nombres")
    
    #ver archivo _auxSintomasCovid.txt
    scovid = ["fiebre","tos","fatiga","falta de aliento",\
        "dificultad para respirar", "tos seca", "tos seca persistente", "dolor de garganta", "dolor de pecho"] #perdida del gusto o del olfato"?

    #Configuración speech recognition
    sr_service.pause(True)
    sr_service.setLanguage("Spanish")
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    tts_service.setVolume(0.5)#Disminuir el volumen a la mitad \\vol=30\\
    tts_service.setParameter("speed",150) #50-400 default=100

    tts_service.say("Hola, yo soy NAO") 

    #!--------------------------------------NOMBRE--------------------------------------------

    askNombre = True
    while askNombre:
        
        sr_service.pause(True)
        sr_service.setVocabulary(nombres,True)
        sr_service.subscribe("nombre_id") 
        memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized')

        tts_service.say("¿Cuál es su nombre estimado caballero coménteme")
        sr_service.pause(False)
        time.sleep(6)
        sr_service.pause(True)
        sr_service.unsubscribe("nombre_id")

        nombre=memory_service.getData("WordRecognized")
        nombre_pal = nombre[0][6:-6] #de la palabra lo necesario
        nombre_prob = nombre[1] #probabilidad
        print(nombre_pal+"-"+str(nombre_prob))
        
        if (nombre_pal in nombres) and (nombre_prob >= prob_aceptable): 
            nombre_save = nombre_pal
        else:
            nombre_save = "Paciente"
            #tts_service.say("Disculpe, no entendí")
        askNombre = False
        tts_service.say("Hola, "+ nombre_save)
        print("Nombre: "+ nombre_save)
    
    #!--------------------------------------SEXO--------------------------------------------
        
    askSexo = True
    while askSexo:
        
        sr_service.pause(True)
        sr_service.setVocabulary(sexos,True)
        sr_service.subscribe("sexo_id") 
        memory_service.subscribeToEvent('WordRecognized',"sexo_id",'wordRecognized')

        tts_service.say("¿Cuál es su sexo biológico?") 
        tts_service.say("Femenino. O. Masculino.")

        sr_service.pause(False)
        time.sleep(6)
        sr_service.pause(True)
        sr_service.unsubscribe("sexo_id")

        sexo=memory_service.getData("WordRecognized")
        sexo_pal = sexo[0][6:-6] #de la palabra lo necesario
        sexo_prob = sexo[1] #probabilidad
        print(sexo_pal+"-"+str(sexo_prob)) 
        
        if (sexo_pal in sexos) and (sexo_prob >= prob_aceptable): 

            askSexo = False
            tts_service.say("Recibido: sexo "+ sexo_pal)
            sexo_save = sexo_dict[sexo_pal]
            print("Sexo: "+ str(sexo_save) + "( " + sexo_pal + ")")

        else:
            tts_service.say("Disculpe, no pude entender")

    #!--------------------------------------EDAD--------------------------------------------

    askEdad = True 
    while askEdad:
        print("while askEdad")
        sr_service.pause(True)
        sr_service.setVocabulary(edades,True) #TODO:vocabulary clean
        sr_service.subscribe("edad_id")
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

        tts_service.say("¿Cuántos años tiene?")        

        sr_service.pause(False)
        time.sleep(6)
        sr_service.pause(True)
        sr_service.unsubscribe("edad_id")

        edad=memory_service.getData("WordRecognized")
        edad_pal = edad[0][6:-6] #de la palabra lo necesario
        edad_prob = edad[1] #probabilidad
        print(edad_pal+"-"+str(edad_prob))
        
        if (edad_pal in edades) and (edad_prob >= prob_aceptable): 

            askConfirmacion = True
            while askConfirmacion:
                print("while askConfirmacion")
                sr_service.pause(True)
                sr_service.setVocabulary(confirmacion,True)
                sr_service.subscribe("confirmacion_id") 
                memory_service.subscribeToEvent('WordRecognized',"confirmacion_id",'wordRecognized')
                
                print("¿ Ha dicho " + edad_pal + " ?")
                tts_service.say("¿ Ha dicho " + edad_pal + " ?")

                sr_service.pause(False)
                time.sleep(5)
                sr_service.pause(True)
                sr_service.unsubscribe("confirmacion_id")

                confirmado=memory_service.getData("WordRecognized")
                confirmado_pal = confirmado[0][6:-6] #de la palabra lo necesario
                confirmado_prob = confirmado[1] #probabilidad
                print(confirmado_pal+"-"+str(confirmado_prob))

                if (confirmado_pal in confirmacion) and (confirmado_prob >= prob_aceptable):

                    askConfirmacion = False #deja de pedir confirmacion

                    if confirmado_pal == "si":
                        if(int(edad_pal) > limiteEdad):
                            tts_service.say("Debe decir una edad dentro del rango de 0 a "+ str(limiteEdad))
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

    mis_sespecificos = [] 
    mis_intensidades = [] 
    nummax_scovid = 2
    contar_scovid = 0
    decir_sgenerales = True
    decir_sespecificos = True

    askSGeneral = True
    while askSGeneral:
        print("while askSGeneral")
        sr_service.pause(True)
        sr_service.setVocabulary(admitir_sgenerales,True)
        sr_service.subscribe("sgeneral_id") 
        memory_service.subscribeToEvent('WordRecognized',"sgeneral_id",'wordRecognized')

        print("Sintomas generales: " + lista_sgenerales)
        if(decir_sgenerales):
            tts_service.say("Elija alguna de las siguientes categorías")
            tts_service.say(lista_sgenerales)
            decir_sgenerales = False
        else:
            tts_service.say("Mencione una de las categorías.")

        tts_service.say("Diga no para empezar a procesar. Diga repetir para mencionar las categorías nuevamente.")
        
        sr_service.pause(False)
        time.sleep(10)
        sr_service.pause(True)
        sr_service.unsubscribe("sgeneral_id")

        sgeneral=memory_service.getData("WordRecognized")
        sgeneral_pal = sgeneral[0][6:-6] #de la palabra lo necesario
        sgeneral_prob = sgeneral[1] #probabilidad
        print(sgeneral_pal+"-"+str(sgeneral_prob))
        
        if (sgeneral_pal in admitir_sgenerales) and (sgeneral_prob >= prob_aceptable):

            if (sgeneral_pal == "no" or sgeneral_pal == "ya no tengo más síntomas"):
                askSGeneral = False
                #si no hay ningun especifico para procesar -> adiós
                if len(mis_sespecificos) == 0:
                    tts_service.say("No hay síntomas qué procesar. Hasta pronto")
                    sys.exit("Fin: No hay síntomas qué procesar. Hasta pronto")
                
                break #si ha mencionado alguno -> pasa al algoritmo

            if sgeneral_pal == "repetir":
                decir_sgenerales = True
                askSEspecifico = False
                continue #pasa a la sgte iteración

            print("----------------------------")
            tts_service.say("Recibido: Síntoma general " + sgeneral_pal)
            print("Recibido: Síntoma general " + sgeneral_pal)
            
            #!----------------------------------SINTOMAS ESPECIFICOS------------------------------------
              
            lista_sespecificos = ''
            for se in sintomas[sgeneral_pal]: #solo los sintomas especificos de este sintomas general
                lista_sespecificos += se + '. '

            lista_sespecificos = lista_sespecificos[:-2] #sin ultima comita y espacio

            admitir_sespecificos = sintomas[sgeneral_pal] + opciones
           
            askSEspecifico = True
            while askSEspecifico:
                print("while askSEspecifico")
                print(str(askSEspecifico))
                sr_service.pause(True)
                sr_service.setVocabulary(admitir_sespecificos,True)
                sr_service.subscribe("sespecifico_id")
                memory_service.subscribeToEvent('WordRecognized',"sespecifico_id",'wordRecognized')
                
                print("Sintomas específicos: " + lista_sespecificos)
                if(decir_sespecificos):
                    tts_service.say("Repita alguno de los siguientes síntomas")
                    tts_service.say(lista_sespecificos)
                    decir_sespecificos = False
                else:
                    tts_service.say("Mencione uno de los síntomas o")

                tts_service.say("Diga repetir para mencionar los síntomas nuevamente. Diga no para cambiar de categoría.")
                tts_service.say("Diga ya no tengo más síntomas para empezar a procesar.")

                sr_service.pause(False)
                time.sleep(10)
                sr_service.pause(True)
                sr_service.unsubscribe("sespecifico_id")
                
                sespecifico = memory_service.getData("WordRecognized")
                sespecifico_pal = sespecifico[0][6:-6] #de la palabra lo necesario
                sespecifico_prob = sespecifico[1] #probabilidad
                print(sespecifico_pal+"-"+str(sespecifico_prob))

                if (sespecifico_pal in admitir_sespecificos) and (sespecifico_prob >= prob_aceptable):
                    print("sí escuche")
                    askConfirmacion = True

                    if (sespecifico_pal == "no"):
                        askConfirmacion = False
                        askSEspecifico = False
                        #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                        tts_service.say("Okey Volvamos a las categorías")
                        break 
                    
                    if sespecifico_pal == "repetir":
                        decir_sespecificos = True
                        askConfirmacion = False
                        continue #pasa a la sgte iteración

                    if (sespecifico_pal == "ya no tengo más síntomas"):
                        askSGeneral = False
                        break

                    while askConfirmacion:
                        print("while askConfirmacion")
                        sr_service.pause(True)
                        sr_service.setVocabulary(confirmacion,True)
                        sr_service.subscribe("confirmacion_id") 
                        memory_service.subscribeToEvent('WordRecognized',"confirmacion_id",'wordRecognized')
                        
                        print("¿ Ha dicho " + sespecifico_pal + " ?")
                        tts_service.say("¿ Ha dicho " + sespecifico_pal + " ?")

                        sr_service.pause(False)
                        time.sleep(5)
                        sr_service.pause(True)

                        sr_service.unsubscribe("confirmacion_id")

                        confirmado=memory_service.getData("WordRecognized")
                        confirmado_pal = confirmado[0][6:-6] #de la palabra lo necesario
                        confirmado_prob = confirmado[1] #probabilidad
                        print(confirmado_pal+"-"+str(confirmado_prob))

                        if (confirmado_pal in confirmacion) and (confirmado_prob >= prob_aceptable):

                            askConfirmacion = False

                            if confirmado_pal == "si":
                                if sespecifico_pal in mis_sespecificos:
                                    tts_service.say("Este síntoma ya ha sido registrado.")
                                    askPruebaCovid = False
                                    askIntensidad = False
                                    continue #pasa a la sgte iteración (vuelve el sintoma)

                                if sespecifico_pal in scovid:
                                    contar_scovid += 1
                                
                                #!------------------ --DESPISTAJE COVID--------------------------------
                                if contar_scovid >= nummax_scovid: #si supera el límite d síntomas similares de covid
                                    
                                    askPruebaCovid = True
                                    while askPruebaCovid:
                                        print("while askPruebaCovid")
                                        sr_service.pause(True)
                                        sr_service.setVocabulary(confirmacion,True)
                                        sr_service.subscribe("prueba_covid_id")
                                        memory_service.subscribeToEvent('WordRecognized',"prueba_covid_id",'wordRecognized')
                                        
                                        tts_service.say("Usted presenta por lo menos "+ str(nummax_scovid) +" síntomas de Covid")
                                        tts_service.say("¿Se ha realizado la prueba de descarte de Covid?")
                                        
                                        sr_service.pause(False)
                                        time.sleep(6)
                                        sr_service.pause(True)

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
                                                sys.exit("Fin: Recomendación descarte covid")
                                            #else -> continua pidiendo la intensidad del síntoma mencionado
                                        else:
                                            tts_service.say("Disculpe, no pude entender")
                                #!--------------------------------------------------------------------

                                mis_sespecificos.append(sespecifico_pal)
                                
                                tts_service.say("Recibido. Síntoma específico "+ str(len(mis_sespecificos)) + ": " + sespecifico_pal)
                                print("Recibido. Síntoma especifico "+ str(len(mis_sespecificos)) + ": " + sespecifico_pal)
                                         
                                askIntensidad = True
                                while askIntensidad:
                                    print("while askIntensidad")
                                    sr_service.pause(True)
                                    sr_service.setVocabulary(intensidades,True)
                                    sr_service.subscribe("intensidad_id")
                                    memory_service.subscribeToEvent('WordRecognized',"intensidad_id",'wordRecognized')
                                    
                                    tts_service.say("¿Qué tan intenso es el síntoma? Bajo, medio o alto")

                                    sr_service.pause(False)
                                    time.sleep(6)
                                    sr_service.pause(True)

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
                    print("no entendí nada")
                    askConfirmacion = False
                    askSEspecifico = False
                    #deja de preguntar por sintoma especifico, vuelve a preguntar por sintoma general
                    tts_service.say("Okey Volvamos a las categorías")

            print("----------------------------")

        else:
            tts_service.say("Disculpe, hagámoslo de nuevo, no pude entender") 
    """
    sexo_save = 1 #fem: 0 | masc:1
    edad_save = 21
    mis_sespecificos = ['palpitaciones del corazón','náuseas']
    mis_intensidades = ["alto", "medio"]
    """
    #!--------------------------RESULTADOS Y RECOMENDACION------------------------------
    tts_service.say("A continuación procesaré los síntomas. Espere por favor") 
    sr_service.pause(True)
    removeConnection(naoRed)

    conectarInternet()

    try:
        str_sct = ""
        for me in mis_sespecificos:
            str_sct += me + ", "
        print("Con tilde: "+str_sct)

        mis_sespecificos_stilde = []
        for me in mis_sespecificos:
            nuevome = me.replace("á","a")
            nuevome = nuevome.replace("é","e")
            nuevome = nuevome.replace("í","i")
            nuevome = nuevome.replace("ó","o")
            nuevome = nuevome.replace("ú","u")
            mis_sespecificos_stilde.append(nuevome) 

        str_sst = ""
        for me in mis_sespecificos_stilde:
            str_sst += me + " "
        print("Sin tilde: "+str_sst)

        print("Espere por favor.. conectando con internet...\n")
        time.sleep(7)
        global resultados, recomendacion
        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos_stilde,mis_intensidades)
        #resultados= [("enfermedad pulmonar obstructiva cronica",0.949),("neumonia",0.408),("influenza",0.113),("bronquitis",0.102),("hipertension pulmonar",0.06)]
        #recomendacion = ["Te sugiero que visites a un doctor para obtener mas informacion sobre tus sintomas"]
        removeConnection(internetRed)

    except urllib2.HTTPError as error:
        removeConnection(internetRed)
        raise Exception("Http Error con código: " + str(error.code) + " | Info: " + error.info())

    except Exception:
        raise Exception("Ocurrió un error inesperado al procesar los datos")

    session = conectarNao()

    #!--------------------------------INICIAR SERVICIOS------------------------------------
    #motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    sr_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos
    
    sr_service.pause(True)
    sr_service.setLanguage("Spanish")
    sr_service.setAudioExpression(True)
    sr_service.setVisualExpression(True)
    tts_service.setLanguage('Spanish') 
    tts_service.setVolume(0.5)#Disminuir el volumen a la mitad \\vol=30\\
    tts_service.setParameter("speed",150) #50-400 default=100 

    tts_service.say("Ya se procesaron sus datos")
    
    #!------------------------------------CELULAR-------------------------------------
    
    global cel

    print("len(edades): "+str(len(edades)))
    print("len(digitos): "+str(len(digitos)))

    voc_celular = digitos+confirmacion+["me equivoqué","confirmo"]
    sr_service.pause(True)
    sr_service.setVocabulary(voc_celular,True)

    tts_service.say("Por favor, dícteme un número celular de 9 dígitos para enviar los resultados. Diga Me equivoqué para comenzar nuevamente.") 
    
    askCel = True
    while askCel:

        print(askCel, cel, len(cel))

        sr_service.pause(True)
        sr_service.subscribe("numero_id")
        memory_service.subscribeToEvent('WordRecognized',"numero_id",'wordRecognized')
    
        tts_service.say("Lo escucho") #TODO: reiniciar Continue   #ENTENDI mal, qué escucho?
        sr_service.pause(False)
        time.sleep(8)
        sr_service.pause(True)
        sr_service.unsubscribe("numero_id")

        num=memory_service.getData("WordRecognized")
        num_pal = num[0][6:-6] #de la palabra lo necesario
        num_prob = num[1] #probabilidad
        print(num_pal+"-"+str(num_prob))

        if (num_pal in voc_celular) and (num_prob >= prob_aceptable):
            
            if(num_pal == "me equivoqué"):
                cel = "" #volver a empezar
                tts_service.say("Volvamos a empezar") 
                continue

            print(num_pal)
            tts_service.say(num_pal)

            if len(cel) == 0 and num_pal[0] != str(9):
                tts_service.say("El número celular debe comenzar con 9")
                continue #pasa a la sgte iteración (vuelve a pedir el digito)
            
            cel += num_pal.replace(" ","") #concatenamos

            print("cel: "+str(cel))

            time.sleep(2)

            if len(cel) < 9:
                tts_service.say("Continúe") #siga dictando
            if len(cel) == 9:
                #TODO: pedir confirmacion o reiniciar
                askCel = False #terminado, continuar el flujo
            if len(cel) > 9:
                cel = "" #volver a empezar
                tts_service.say("El número celular tiene más de 9 dígitos")
                tts_service.say("Volvamos a empezar") 
        else:
            tts_service.say("Disculpe, no entendí. Nuevamente")
    """            
            askConfirmacion = True
            while askConfirmacion:

                sr_service.subscribe("confirmacion_id") 
                memory_service.subscribeToEvent('WordRecognized',"confirmacion_id",'wordRecognized')
                
                print(num_pal + " ?")
                tts_service.say(num_pal + " ?")
                
                sr_service.pause(False)
                time.sleep(5)
                sr_service.pause(True)
                sr_service.unsubscribe("confirmacion_id")

                confirmado=memory_service.getData("WordRecognized")
                confirmado_pal = confirmado[0][6:-6] #de la palabra lo necesario
                confirmado_prob = confirmado[1] #probabilidad
                print(confirmado_pal+"-"+str(confirmado_prob))


                if (confirmado_pal in confirmacion) and (confirmado_prob >= prob_aceptable):

                    askConfirmacion = False

                    if confirmado_pal == "si": #una vez confirmado el número escuchado
                        
                    else: #no -> volver a pedir numero
                        tts_service.say("Disculpe, entendí mal. Repítame")
                else:
                    tts_service.say("Disculpe, no pude entender")
        """     
        
    tts_service.say("El número al que mandaré los resultados y la recomendación es ") #TODO: recienpedir confirmar Pause+setvoc

    for c in cel:
        tts_service.say(c)

    cel = "+51" + cel

    #!----------------------------------DESPEDIRSE------------------------------------
    tts_service.say("Se le estará enviando un watsap. Muchas gracias por conversar conmigo")
    #motion_service.rest() #sentarse
    removeConnection(naoRed)

#!-------------------------------INICIAR PROGRAMAA------------------------------------
ejecutar()


