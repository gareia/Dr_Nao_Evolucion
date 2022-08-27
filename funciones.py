# -*- coding: utf-8 -*-
import time

def nombre(tts_service, sr_service, memory_service, nombres):
    
    sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
    memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador
    sr_service.pause(False) #
    time.sleep(5) #
    #aux = memory_service.getData("WordRecognized")
    #print(aux, "|", aux[0], "|", aux[1])
    nombre=memory_service.getData("WordRecognized")[1] #(value, pair)
    print(nombre)
    
    tts_service.say("Hola, "+ nombre + " ¿Cómo estás?") #str() ?
    sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
    memory_service.unsubscribeToEvent('WordRecognized',"nombre_id",'wordRecognized')


def nombrebucle(tts_service, sr_service, memory_service, nombres):
    
    hasName = False
    while not hasName:

        sr_service.subscribe("nombre_id") #Empieza a escribir en memoria WordRecognized, identificador
        memory_service.subscribeToEvent('WordRecognized',"nombre_id",'wordRecognized') #evento, identificador
        sr_service.pause(False) #
        time.sleep(5) #
        nombre=memory_service.getData("WordRecognized")[1] #(value, pair)
        print(nombre)

        if nombre in nombres:
            tts_service.say("Hola, "+ nombre + " encantado de conocerte") 
            sr_service.unsubscribe("nombre_id") #Deja de escribir en memoria
            memory_service.unsubscribeToEvent('WordRecognized',"nombre_id",'wordRecognized')
            hasName = True
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu nombre?") 

def edad(tts_service, sr_service, memory_service, edades, edad_dict):

    sr_service.subscribe("edad_id") # Genera el evento llamado edad
    memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
    sr_service.pause(False) #
    time.sleep(5) #
    edad=memory_service.getData("WordRecognized")[1]
    print(edad)
    edad_save = edad_dict[edad] #str() ? 
    print(edad_save)

    tts_service.say("Tienes "+edad + " años")
    sr_service.unsubscribe("edad_id")
    memory_service.unsubscribeToEvent('WordRecognized',"edad_id",'wordRecognized')

def edadbucle(tts_service, sr_service, memory_service, edades, edad_dict):

    hasEdad = False
    while not hasEdad:

        sr_service.subscribe("edad_id") # Genera el evento llamado edad
        memory_service.subscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
        sr_service.pause(False) #
        time.sleep(5) #
        edad=memory_service.getData("WordRecognized")[1]
        print(edad)
        edad_save = edad_dict[edad] #str() ? 
        print(edad_save)

        if edad in edades:
            tts_service.say("Tienes "+edad + " años")
            sr_service.unsubscribe("edad_id")
            memory_service.unsubscribeToEvent('WordRecognized',"edad_id",'wordRecognized')
            hasEdad = True
        else:
            tts_service.say("Disculpa, ¿puedes repetirme tu edad?") 

