from _azureApi import procesar
from _internet import connect
from _internet import createNewConnection
from _internet import removeConnection
import time
import urllib2
import json

def main():
    
    celularRed = "Ni te atrevas 2" #"Ni te atrevas"
    celularPass = "nfzm1408" #"nvth2041"
    
    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    #if(connect("UPC_ALUMNOS", "UPC_ALUMNOS") != 0):
    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    try:
        sexo_save = 0 #fem: 0 | masc:1
        edad_save = 23
        mis_sespecificos = ["fiebre", "dificultad para respirar", "dolor de cabeza", "desmayo"]
        mis_intensidades = ["medio", "medio", "medio", "medio"]

        resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

        print("--------------------------------------\n")

        for enfermedad in resultados:
            print(enfermedad[0])
            #print(type(enfermedad) + "->" + str(enfermedad))

        print("--------------------------------------\n")

        print(recomendacion[0])

        print("--------------------------------------\n")

    except urllib2.HTTPError as error: #urllib2.HTTPError
        removeConnection(celularRed)
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        #print(json.loads(error.read().decode("utf8", 'ignore')))

    time.sleep(6)
    removeConnection(celularRed)

main()