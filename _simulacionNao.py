# -*- coding: utf-8 -*-
import time

cel =""
resultados = []
recomendacion = []

def fcelular():
    return cel

def fresultados():
    return resultados

def frecomendacion():
    return recomendacion

def main(): 

    global resultados
    resultados = [("bronquitis",0.682), ("neumonia",0.678333333333), ("asma",0.091), ("mesotelioma",0.023),\
    ("enfermedad pulmonar obstructiva cronica",0.02)]
    global recomendacion
    recomendacion = ["Te sugiero que visites a un doctor para obtener mas informacion sobre tus sintomas"]
    global cel
    cel = "+51949252410"
    
main()
