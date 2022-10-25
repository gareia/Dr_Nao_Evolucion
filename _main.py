# -*- coding: utf-8 -*-
import os
import time
import sys
from _internet import connect,createNewConnection,removeConnection

try:
    pathInternetId = '_redInternetId.txt'
    with open(pathInternetId, 'r') as file:
        internetRed = file.read()
        print("Red internet: "+internetRed)

    pathInternetPass = '_redInternetPass.txt'
    with open(pathInternetPass, 'r') as file:
        celularPass = file.read()

    if(createNewConnection(internetRed, internetRed, celularPass) != 0):
        raise Exception("Error al agregar red " + internetRed)

    time.sleep(3)

    if(connect(internetRed, internetRed) != 0):
        removeConnection(internetRed)
        raise Exception("Error al conectarse a la red " + internetRed)
    
    time.sleep(1)
    os.system("python3 -m pip install --upgrade pip")
    
    time.sleep(1)
    os.system("python3 -m pip install glob2")

    import glob
    for f in glob.glob("*.xml"):
        os.remove(f)

except Exception as e:
    sys.exit("Ocurrió un error inesperado al eliminar los archivos .xml")

try:
    
    #Entorno CON NAO
    #from _flujo import fcelular, fresultados, frecomendacion

    #Entorno SIN NAO
    from _simulacionNao import fcelular, fresultados, frecomendacion

    print("------archivo main-------")

    time.sleep(2)
    cel = fcelular()
    print("cel: "+cel)
    if(len(cel) == 0): raise Exception("El campo celular no ha sido registrado")

    res_list = fresultados()
    print("len(resultados): "+str(len(res_list)))
    if(len(res_list) == 0): raise Exception("No hay resultados registrados")
    res_str = ""
    for rs in res_list:
        res_sin = rs[0].replace(" ", "+")
        res_str += res_sin+":"+str(round(rs[1],3))+" "
    print(res_str)

    rec = frecomendacion()
    print("len(rec): "+str(len(rec)))
    if(len(rec) == 0): raise Exception("No hay recomendación registrada")
    rec_str = rec[0].replace(" ","+")
    print(rec_str)
    
except Exception as e:
    sys.exit("Ocurrió un error inesperado con los datos de entrada: "+ e.message)

try:
    pathInternetId = '_redInternetId.txt'
    with open(pathInternetId, 'r') as file:
        internetRed = file.read()
        print("Red internet: "+internetRed)

    pathInternetPass = '_redInternetPass.txt'
    with open(pathInternetPass, 'r') as file:
        celularPass = file.read()

    if(createNewConnection(internetRed, internetRed, celularPass) != 0):
        raise Exception("Error al agregar red " + internetRed)

    time.sleep(3)

    if(connect(internetRed, internetRed) != 0):
        removeConnection(internetRed)
        raise Exception("Error al conectarse a la red " + internetRed)
    
    time.sleep(1)
    os.system("python3 -m pip install selenium")
    time.sleep(1)
    os.system("python3 -m pip install packaging")
    time.sleep(1)
    os.system("python3 -m pip install webdriver_manager")
    time.sleep(1)
    os.system("python3 _wsp.py --celular="+cel+ " -rc "+rec_str+" -rs "+res_str)

    removeConnection(internetRed)

except Exception as e:
    sys.exit("Ocurrió un error inesperado al enviar mensaje a whatsapp")

sys.exit()
