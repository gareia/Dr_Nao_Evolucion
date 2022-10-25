# -*- coding: utf-8 -*-
from _internet import connect
from _internet import createNewConnection
from _internet import removeConnection
from _azureApi import procesar

import time
import urllib2

def saludar(celularRed):
    
    print("Hola, yo soy NAO")

    #!--------------------------------------INTERMEDIO--------------------------------------
    sexo_save = 0 #fem: 0 | masc:1
    edad_save = 23
    mis_sespecificos = ["tos amarilla", "dificultad para respirar", "dolor de cabeza"]
    mis_intensidades = ["medio", "medio", "medio"]

    #!--------------------------RESULTADOS Y RECOMENDACION----------------------------------
    
    removeConnection(celularRed)

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

        removeConnection(celularRed)

    except urllib2.HTTPError as error:
        removeConnection(celularRed)
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))


    #volver conectar a nao
    celularRed = "Ni te atrevas"
    celularPass = "nvth2041"

    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    print("Espere por favor.. conectando con Nao...\n")
    time.sleep(7)

    print("--------------------------------------\n")
    for enfermedad in resultados:
        print(enfermedad[0] + " con un " + str(enfermedad[1]))
    print("--------------------------------------\n")
    print(recomendacion[0])
    print("--------------------------------------\n")

    removeConnection(celularRed)


#!-------------------------------INICIAR PROGRAMAA------------------------------------
def main():

    celularRed = "Ni te atrevas"
    celularPass = "nvth2041"

    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    print("Espere por favor.. conectando con Nao...\n")
    time.sleep(7)

    saludar(celularRed)

main()
    