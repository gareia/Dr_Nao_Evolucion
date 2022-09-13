# -*- coding: utf-8 -*-
import numpy as np
import time
from collections import Counter 
import urllib 
import json

Lista_Enfermedades = ['apnea del sueno', 'asbestosis', 'asma','aspergilosis','bronquiectasias','bronquiolitis','bronquitis','bronquitis cronica','enfermedad pulmonar obstructiva cronica','hipertension pulmonar','influenza','mesotelioma','neumonia', 'neumotorax','sindrome de distres respiratorio agudo','tos cronica','tuberculosis','virus sincitial respiratorio']
Lista_Sintomas = ['tos','sensacion de opresion en el pecho','sibilancias','dificultad para respirar','fiebre','frio','alergia','tos con mucosidad amarilla o verde todos los dias','dificultad para respirar que empeora durante los brotes','dolor de pecho','nariz que moquea','congestion nasal','perdida de apetito','fiebre de bajo grado','congestion en el pecho','tos amarilla','moco','tos cronica','fatiga','dolor de espalda baja','tos seca','tos verdosa','tos con sangre','transpiracion','sacudida','respiracion rapida','respiracion superficial','nauseas','vomitos','dolor agudo en el pecho','piel azulada','latidos rapidos','fiebre alta','dolor de cabeza','dolores musculares','dolor en las articulaciones','escalofrios','dolor de garganta','diarrea','aliento','mareo','desmayo','palpitaciones del corazon','edema','ronquidos','somnolencia diurna','pausas en la respiracion','dificultades con la memoria y la concentracion','mal humor inusual','irritabilidad','despertarse con frecuencia','dolores de cabeza matutinos','boca seca','tos sibilante','respiracion corta superficial y rapida','sudores nocturnos','falta de aliento','angustioso','latido del corazon mas rapido','dolor','tos seca persistente','perdida de peso por perdida de apetito','un sonido seco y crepitante en los pulmones al inhalar','dedos de manos y pies mas anchos y redondos que lo normal','perdida de peso']

ProbAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)
CntAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)

def Calcula_Enfermedades(output):
  Data_Resultados = output.copy()
  Probabilidades_de_enfermedades = []
  Diagnostico = dict() 
  del Data_Resultados['sintomas']
  del Data_Resultados['edad']
  del Data_Resultados['sexo']
  del Data_Resultados['enfermedad']
  del Data_Resultados['gravedad'] 
  for i in range(len(Lista_Enfermedades)):
    Probabilidades_de_enfermedades.append(Data_Resultados['Scored Probabilities for Class "{}"'.format(Lista_Enfermedades[i])])
  ind = np.argpartition(Probabilidades_de_enfermedades, -5)[-5:] # AMBOS NUMEROS REPRESENTAN CUANTAS ENFERMEDADES VA A ALMACENAR CON CADA PROCESAMIENTO
  for i in range(len(ind)):
    Diagnostico[str(Lista_Enfermedades[ind[i]])] = round(float(Probabilidades_de_enfermedades[ind[i]]),3)
  return Diagnostico

def Analisis_Enfermedades2(tts_service):
  lista_eliminar = []
  for x in ProbAnalisis_Enfermedades:
    if (ProbAnalisis_Enfermedades[x] == None):
      lista_eliminar.append(x)
  for i in lista_eliminar:
    del ProbAnalisis_Enfermedades[i]
  for x in ProbAnalisis_Enfermedades:
    ProbAnalisis_Enfermedades[x] /= CntAnalisis_Enfermedades[x]
  k = Counter(ProbAnalisis_Enfermedades) 
  high = k.most_common(5) # COLOCAR EL NUMERO DE ENFERMEDADES QUE VOY A SUGERIR EN MIS RESULTADOS

  for i in high:
    print("->",i[0]," :",i[1]," ") 
    time.sleep(1)
    tts_service.say(i[0])

def Analisis_Enfermedades(dic):
  for x in dic:
    if(CntAnalisis_Enfermedades[x]==None):
      CntAnalisis_Enfermedades[x] = 1
      ProbAnalisis_Enfermedades[x] = dic[x]
    else:
      CntAnalisis_Enfermedades[x] += 1
      ProbAnalisis_Enfermedades[x] += dic[x]

def alg_mortalidad(Mortalidades,tts_service):
  api_key2='VS+CDolkU07ItaajsgHQlF2s41ATOPc4uRDM16ZQsBV2wdtQQwGD5d7rqZ3Fd4uEjePyBywVFxfT+AMCDuSnlQ=='
  url2='https://ussouthcentral.services.azureml.net/workspaces/4baff35fd4b3430c83395d179d1f6994/services/05f2cf6f65804848ae5611078e09ba2f/execute?api-version=2.0&format=swagger'
  headers2 = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key2)}
  cnt_morts = 0
  for i in Mortalidades:
    req2 = urllib.request.Request(url2, i, headers2)
    try:
        response = urllib.request.urlopen(req2)
        result2 = response.read()
        #print(result)
        json_result = json.loads(result2)
        output = json_result["Results"]["output1"][0]
        if (output['Scored Labels'] == "si"):
          cnt_morts+=1   
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))
        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(json.loads(error.read().decode("utf8", 'ignore')))
  print("Nivel de mortalidad: " + str(cnt_morts))
  if(cnt_morts>1):
    tts_service.say("Te sugiero que visites a un doctor urgentemente, tus síntomas no se ven nada bien.")
  else:
    tts_service.say("Te sugiero que visites a un doctor para obtener más informacion sobre tus sintomas")

#algoritmo
def procesar(Mi_Edad,Mi_Sexo,Mis_Sintomas,Mis_Gravedades,tts_service):
    
    Mortalidades = []

    for i in range(len(Mis_Sintomas)):
      Dict = {'sintomas': Mis_Sintomas[i], 'edad': Mi_Edad,
      'sexo': Mi_Sexo,'enfermedad': "", 'tratamiento': "",
      'gravedad': Mis_Gravedades[i],'mortalidad': ""}
      data = {
        "Inputs": {
            "input1":
                [Dict]
        },
        "GlobalParameters": {
        },
      }
      body = str.encode(json.dumps(data))
      url = 'https://ussouthcentral.services.azureml.net/workspaces/4baff35fd4b3430c83395d179d1f6994/services/cd3d3c5e9cc4438badb1bcfaf9819957/execute?api-version=2.0&format=swagger'
      api_key = '7YlRnExDHxL+p76HbpSr3x8LEZ8ZctFNWnbiccRMOyZaq1PV+50pV6GwHJx6r2fyNClYGq+x2cRVrn/rSO8T8Q==' # Replace this with the API key for the web service
      headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}
      req = urllib.request.Request(url, body, headers) #urllib2.Request(url, body, headers)

      Mortalidades.append(body)

      try:
          response = urllib.urlopen(req)
          result = response.read()

          #print(result)
          json_result = json.loads(result)
          output = json_result["Results"]["output1"][0]
          resultados = Calcula_Enfermedades(output)

          print('Edad: {}\nSexo: {}\nSintomas: {}\nGravedad: {}'.format(output['edad'],output['sexo'],output['sintomas'],output['gravedad']))
          print('Resultados: ' + str(resultados)+ ' \n')

          Analisis_Enfermedades(resultados)

      except urllib.error.HTTPError as error: #urllib2.HTTPError
          print("The request failed with status code: " + str(error.code))
          # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
          print(error.info())
          print(json.loads(error.read().decode("utf8", 'ignore')))

    #Resultados
    print("--------------------------------------\n")
    print("RESULTADOS SUGERIDOS\n")
    
    if(len(Mis_Sintomas) == 0):
      tts_service.say("No tenemos resultados ya que no presenta síntomas")
      print("No tenemos resultados ya que no presenta síntomas")

    tts_service.say("Los resultados son los siguientes")
    Analisis_Enfermedades2(tts_service)

    #Recomendación
    print("--------------------------------------\n")
    print("RECOMENDACION\n")
    
    if(len(Mortalidades) == 0):
      tts_service.say("No tenemos resultados ya que no presenta síntomas")
      print("No tenemos resultados ya que no presenta síntomas")
      
    tts_service.say("La recomendación es la siguiente")
    alg_mortalidad(Mortalidades, tts_service)


#Motion.wakeUp()
#Motion.moveInit()
#Motion.post.moveTo(0.5, 0, 0)
#Speech.say("Hola!!")
#for i in range(3):
    #Motion.angleInterpolation(names, [-3.0, 1.2, -0.7], times, True)
    #Motion.angleInterpolation(names, [-1.0, 1.2, -0.7], times, True)
#Motion.rest()

#urllib2
#from naoqi import ALProxy








