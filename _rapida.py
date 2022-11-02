# -*- coding: utf-8 -*-

#print(round(0.56789,3))
import os

dir = os.path.dirname(os.path.realpath(__file__))
print("Directorio actual: " + dir)
for f in os.listdir(dir):
    if(f[-4:] == ".xml"): 
        os.remove(os.path.join(dir, f))

mensaje = "*holaa%0aahaa"
#print(mensaje)

def prueba():
    lis = [("uno",0.10),("dos",0.2),("tres",3.4)]
    r = "holaa yo había pensado que tenías un perro"
    return lis,r

#a, b = prueba()

#res_nombres = [i[0] for i in a]
#res_porcentajes = [round(i[1],3) for i in a]

#for i in res_nombres:
#    print(i)

#for i in res_porcentajes:
#    print(i)

#print(type(a))
#print(type(b))

"""
myset = {5, 6, 7}
myset.add(5)
myset.add(8)
myset.add(3)
#for i in myset:
#    print(i)
print(len(myset))
"""

"""
for i in range(5):
    if(i == 3):
        continue
    print(i)
"""

"""
a = 2
print(type(a))
b = "2"
print(type(b))

covid = ["a","c","f"]
mias = ["a","b","c","d","e"]

print(covid[a])
print(covid[a])
"""

"""
count = 0
for mia in mias:
    if mia in covid: 
        count+=1
print(count)
"""
"""
sintomas={}
sintomas["tos"] = ['alergia','tos con mucosidad amarilla o verde todos los dias',\
                'nariz que moquea','congestion nasal', 'tos amarilla', 'moco', 'tos cronica',\
                'tos seca', 'tos verdosa', 'tos con sangre','dolor de garganta',\
                'boca seca','tos sibilante','tos seca persistente']
sintomas["perdida de peso"] = ['perdida de apetito', 'nauseas', 'vomitos', 'diarrea', \
            'perdida de peso por perdida de apetito', 'perdida de peso']
sintomas["fatiga"] = ['fatiga', 'mal humor inusual', 'despertarse con frecuencia', \
            'irritabilidad']

sgenerales = [sg for sg in sintomas]
print(type(sgenerales))

decir_sgenerales = ''
sespecificos = []
for sg in sgenerales:
    sespecificos += sintomas[sg]
    decir_sgenerales += sg + ', '
decir_sgenerales = decir_sgenerales[:-2] #sin ultima comita y espacio
print(decir_sgenerales)

#decir_sespecificos = sintomas[0][1][1]
#for k,v in sintomas:
#    decir_sespecificos += ','+k
#print(decir_sespecificos)

#print(sintomas["tos"])
"""
"""
nombres = ["fernando","paolo","roberto","grecia"]
edades = ["cinco","seis","siete","ocho",\
    "nueve","diez","once","doce","trece","catorce","quince","dieciseis","diecisiete",\
        "dieciocho","diecinueve","veinte"]

voc = nombres + edades
print(voc)
"""

"""
prueba = ("Word","masculino")
#print(prueba["Word"])
print(prueba[1])

cod = ["hola", "que", "tal"]
cod += ["no"]

for c in cod:
    print(c)
"""
"""
seguir = True
ok=True
i=2
while(ok):
    while(seguir):
        if(i > 2):
            print("holii")
            if(i == 5):
                seguir = False
                ok = False
                break #salir del bucle
            print("que onda")
        print("nonoooo")
        i += 1
    print("sisisi")
"""
"""
for i in range(5):
    if(i > 2):
        print("holii")
        if(i == 5):
            break
        print("que onda")
    print("nonoooo")
"""

#print("tengo"+str(5)+"años")

"""
edades=["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis",\
        "diecisiete","dieciocho","diecinueve","veinte"]
print(len(edades))
edades_dict = {edad: i+5 for i, edad in enumerate(edades)}
for i, edad in edades_dict:
    print(str(i)+"->"+edad)
"""

"""
digitos = ['cero','uno','dos','tres','cuatro','cinco','seis','siete','ocho','nueve']

digs_dict = {dig:i for i, dig in enumerate(digitos)}
for dig in digs_dict:
    print(dig+"->"+str(digs_dict[dig]))
"""

#print(edades_dict["ocho"])
