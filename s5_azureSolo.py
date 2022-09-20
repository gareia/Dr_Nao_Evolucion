# -*- coding: utf-8 -*-
from s5_internet import connect
from Azure_ApiSolo import procesar

#!--------------------------------------INTERMEDIO--------------------------------------

sexo_save = 0 #fem: 0 | masc:1
edad_save = 23
mis_sespecificos = ["tos amarilla", "dificultad para respirar", "dolor de cabeza"]
mis_intensidades = ["medio", "medio", "medio"]

#conectar a wlan
name="Ni te atrevas"
connect(name, name)

resultados, recomendacion = procesar(edad_save,sexo_save,mis_sespecificos,mis_intensidades)

for enfermedad in resultados:
    print(enfermedad)
    #print(type(enfermedad) + "->" + str(enfermedad))

print(recomendacion[0])