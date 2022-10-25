from urllib2 import urlopen
from _internet import connect
from _internet import createNewConnection
from _internet import removeConnection
import time

def main():

    celularRed = "Ni te atrevas 2"
    celularPass = "nfzm1408"
    
    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        print("Error al agregar red")
        return 0

    #if(connect("UPC_ALUMNOS", "UPC_ALUMNOS") != 0):
    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0

    response = urlopen('https://pokeapi.co/api/v2/pokemon/?limit=10').read()
    #data = json.load(response)   
    print(response)

    time.sleep(6)
    removeConnection(celularRed)

main()