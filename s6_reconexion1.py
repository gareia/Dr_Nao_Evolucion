from Azure_ApiSolo import procesar
from s5_internet import connect
from s5_internet import createNewConnection
from s5_internet import removeConnection
import time
import urllib2
#import json

def main():
    
    print("--------------------------------------\n")
    print("--------- RED CELULAR 1---------------\n")

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
        print("Espere por favor.. conectando...\n")
        time.sleep(7)
        sexo_save = 0 #fem: 0 | masc:1
        edad_save = 23
        mis_sespecificos = ["fiebre", "dificultad para respirar", "dolor de cabeza", "desmayo"]
        mis_intensidades = ["medio", "medio", "medio", "medio"]

        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

        print("--------------------------------------\n")

        for enfermedad in resultados:
            print(enfermedad[0] + " con un " + str(enfermedad[1]))

        print("--------------------------------------\n")

        print(recomendacion[0])

        removeConnection(celularRed)

    except urllib2.HTTPError as error:
        removeConnection(celularRed)
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))

    print("--------------------------------------\n")
    print("--------- RED CELULAR 2---------------\n")

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

    try:
        sexo_save = 1 #fem: 0 | masc:1
        edad_save = 27
        mis_sespecificos = ['tos amarilla','dolor agudo en el pecho', "dificultad para respirar"]
        mis_intensidades = ["medio", "medio", "medio"]

        print("Espere por favor.. reconectando...\n")
        time.sleep(7)
        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

        print("--------------------------------------\n")

        for enfermedad in resultados:
            print(enfermedad[0] + " con un " + str(enfermedad[1]))

        print("--------------------------------------\n")

        print(recomendacion[0])

        print("--------------------------------------\n")
    
        removeConnection(celularRed)

    except urllib2.HTTPError as error:
        removeConnection(celularRed)
        print("The request failed with status code: " + str(error.code))
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))

main()