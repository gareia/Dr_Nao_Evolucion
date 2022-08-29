# -*- coding: utf-8 -*-
import time

def nombre(tts_service, sr_service, memory_service):
    
    sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
    memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador

    sr_service.pause(False) #
    time.sleep(5) #
    
    nombre=memory_service.getData("WordRecognized")[0] #1era opcion d lista descendente | str()?
    print(nombre) #print(aux, "|", aux[0], "|", aux[1])
    
    sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
    memory_service.unsubscribeToEvent('WordRecognized',"nombre_id")#,'wordRecognized')

    tts_service.say("Hola, "+ nombre + " ¿Cómo estás?") #str() ?

def nombrebucle(tts_service, sr_service, memory_service, nombres):
    
    askName = True
    while askName:

        sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador

        sr_service.pause(False) #
        time.sleep(5) #

        nombre=memory_service.getData("WordRecognized")[0] #1era opcion d lista descendente | str()?
        print(nombre)

        sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
        memory_service.unsubscribeToEvent('WordRecognized',"nombre_id")#,'wordRecognized')

        if nombre in nombres:
            tts_service.say("Hola, "+ nombre + " encantado de conocerte") #str() ?
            askName = False
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu nombre?") 


def edad(tts_service, sr_service, memory_service, edad_dict):

    sr_service.subscribe("edad_id") # Genera el evento llamado edad
    memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized') 

    sr_service.pause(False) #
    time.sleep(5) #

    edad=memory_service.getData("WordRecognized")[0] #1era opcion d lista descendente | str()?
    print(edad)
    edad_save = edad_dict[edad] #str() ? 
    print(edad_save)
    
    sr_service.unsubscribe("edad_id")
    memory_service.unsubscribeToEvent('WordRecognized',"edad_id")#,'wordRecognized')

    tts_service.say("Tienes "+ edad + " años") #str() ?

def edadbucle(tts_service, sr_service, memory_service, edades, edad_dict):

    askEdad = True
    while askEdad:

        sr_service.subscribe("edad_id") # Genera el evento llamado edad
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

        sr_service.pause(False) #
        time.sleep(5) #

        edad=memory_service.getData("WordRecognized")[0] #1era opcion d lista descendente | str()?
        print(edad)
        edad_save = edad_dict[edad] #str() ? 
        print(edad_save)

        sr_service.unsubscribe("edad_id")
        memory_service.unsubscribeToEvent('WordRecognized',"edad_id")#,'wordRecognized')

        if edad in edades:
            tts_service.say("Tienes "+edad + " años") #str() ? 
            askEdad = False
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu edad?") 

