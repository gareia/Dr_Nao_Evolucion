# -*- coding: utf-8 -*-
from _internet import connect
from _internet import createNewConnection
from _azureApi import procesar
import time
import os

#!--------------------------------------INTERMEDIO--------------------------------------

#conectar a wlan2
#os.remove("*.xml")
time.sleep(5)
createNewConnection("Ni te atrevas 2", "Ni te atrevas 2", "nfzm1408")
connect("Ni te atrevas 2", "Ni te atrevas 2")

sexo_save = 0 #fem: 0 | masc:1
edad_save = 23
mis_sespecificos = ["tos amarilla", "dificultad para respirar", "dolor de cabeza"]
mis_intensidades = ["medio", "medio", "medio"]

#conectar a wlan1
os.remove("Ni te atrevas 2.xml")
time.sleep(5)
createNewConnection("Ni te atrevas", "Ni te atrevas", "nvth2041")
connect("Ni te atrevas", "Ni te atrevas")

resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

for enfermedad in resultados:
    print(enfermedad)
    #print(type(enfermedad) + "->" + str(enfermedad))

print(recomendacion[0])

#conectar a wlan2
os.remove("Ni te atrevas.xml")
time.sleep(5)
createNewConnection("Ni te atrevas 2", "Ni te atrevas 2", "nfzm1408")
connect("Ni te atrevas 2", "Ni te atrevas 2")