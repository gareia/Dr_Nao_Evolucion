#from naoqi import ALProxy
import numpy as np
from collections import Counter 
import urllib2
import json
import time


Lista_Enfermedades = ['apnea del sueno', 'asbestosis', 'asma','aspergilosis','bronquiectasias','bronquiolitis','bronquitis','bronquitis cronica','enfermedad pulmonar obstructiva cronica','hipertension pulmonar','influenza','mesotelioma','neumonia', 'neumotorax','sindrome de distres respiratorio agudo','tos cronica','tuberculosis','virus sincitial respiratorio']
Lista_Sintomas = ['tos','sensacion de opresion en el pecho','sibilancias','dificultad para respirar','fiebre','frio','alergia','tos con mucosidad amarilla o verde todos los dias','dificultad para respirar que empeora durante los brotes','dolor de pecho','nariz que moquea','congestion nasal','perdida de apetito','fiebre de bajo grado','congestion en el pecho','tos amarilla','moco','tos cronica','fatiga','dolor de espalda baja','tos seca','tos verdosa','tos con sangre','transpiracion','sacudida','respiracion rapida','respiracion superficial','nauseas','vomitos','dolor agudo en el pecho','piel azulada','latidos rapidos','fiebre alta','dolor de cabeza','dolores musculares','dolor en las articulaciones','escalofrios','dolor de garganta','diarrea','aliento','mareo','desmayo','palpitaciones del corazon','edema','ronquidos','somnolencia diurna','pausas en la respiracion','dificultades con la memoria y la concentracion','mal humor inusual','irritabilidad','despertarse con frecuencia','dolores de cabeza matutinos','boca seca','tos sibilante','respiracion corta superficial y rapida','sudores nocturnos','falta de aliento','angustioso','latido del corazon mas rapido','dolor','tos seca persistente','perdida de peso por perdida de apetito','un sonido seco y crepitante en los pulmones al inhalar','dedos de manos y pies mas anchos y redondos que lo normal','perdida de peso']

Mis_Sintomas = [] # ENFERMEDADES DETECTADAS DE LA LISTA DE SINTOMAS
#Mi_Edad = -1 # EDAD
#Mi_Sexo = -1 # 0 mujer, 1 hombre
Mi_Gravedad = [] # alto,medio,bajo

ProbAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)
CntAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)

def Analisis_Enfermedades2():
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
    print("-> " + str(i[0]) +": " + str(i[1])) 

def Analisis_Enfermedades(dic):
  for x in dic:
    if(CntAnalisis_Enfermedades[x]==None):
      CntAnalisis_Enfermedades[x] = 1
      ProbAnalisis_Enfermedades[x] = dic[x]
    else:
      CntAnalisis_Enfermedades[x] += 1
      ProbAnalisis_Enfermedades[x] += dic[x]
      

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

def algoritmo(Mi_Edad,Mi_Sexo,Mis_Sintomas):
    ProbAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)
    CntAnalisis_Enfermedades = dict.fromkeys(Lista_Enfermedades)
    for i in range(len(Mis_Sintomas)):
      Dict = {'sintomas': Lista_Sintomas[Mis_Sintomas[i]], 'edad': Mi_Edad, 'sexo': Mi_Sexo,'enfermedad': "", 'tratamiento': "", 'gravedad': Mi_Gravedad[i]}
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
      req = urllib2.Request(url, body, headers)

      try:
          response = urllib2.urlopen(req)
          result = response.read()
          #print(result)
          json_result = json.loads(result)
          output = json_result["Results"]["output1"][0]
          resultados = Calcula_Enfermedades(output)
          # ENVIAR RESULTADOS A ANALISIS_ENFERMEDADES

          #print(output)
          print('Edad: {}\nSexo: {}\nSintomas: {}\nGravedad: {}'.format(output['edad'],output['sexo'],output['sintomas'],output['gravedad']))
          print('Resultados: ' + str(resultados)+ ' \n')
          Analisis_Enfermedades(resultados)

      except urllib2.HTTPError as error:
          print("The request failed with status code: " + str(error.code))
          # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
          print(error.info())
          print(json.loads(error.read().decode("utf8", 'ignore')))

    print("--------------------------------------\n")
    print("RESULTADOS SUGERIDOS\n")
    if(len(Mis_Sintomas) == 0):
      print("No tenemos resultados ya que no tienes sintomas")
    Analisis_Enfermedades2()

def check_int(string):
  try:
    int(string)
  except ValueError:
      return False
  else:
    if(string[0] == '-' or string[0] == '+'):
      return False
    else:
      return True


def main():

    """
    Mi_Nombre = ""
    print("- Hola, soy el robot NAO")
    time.sleep(2)
    print("- Mi funcion es informarte sobre las posibles enfermedades que puedas padecer; pero no te alarmes. Yo no diagnostico.")
    time.sleep(5)
    Mi_Nombre = raw_input("- Cual es tu nombre?\n")
    time.sleep(2)
    print("- Hola, "+ str(Mi_Nombre))
    time.sleep(2)
    Mi_Edad = raw_input("- Por favor, ingresa tu edad\n")
    while(not check_int(Mi_Edad) or not(int(Mi_Edad)>0 and int(Mi_Edad)<150)):
      Mi_Edad = raw_input("- Ingresa tu edad real\n")
    Mi_Edad = int(Mi_Edad)
    time.sleep(2)
    print("- Entiendo, tienes " + str(Mi_Edad) + " anio(s)")
    time.sleep(2)

    Mi_Sexo = raw_input("- Por favor, ingresa tu sexo (0 = Mujer, 1 = Hombre)\n")
    while(not check_int(Mi_Sexo) or (int(Mi_Sexo)!=0 and int(Mi_Sexo)!=1)):
      Mi_Sexo = raw_input("- Ingresa un dato real (0 o 1)\n")
    Mi_Sexo = int(Mi_Sexo)
    time.sleep(2)
    if(Mi_Sexo):
      print("- Ya veo, eres un hombre")
    else:
      print("- Ya veo, eres una mujer")
    time.sleep(2)
    
    print("- Ahora te voy a mostrar una lista de sintomas")
    time.sleep(2)
    print("- Quiero que me digas cuales de ellos tienes segun su indice")
    time.sleep(2)
    print("- Cuando hayas colocado todos tus sintomas, ingresa 0")
    time.sleep(5)
    """
    #print("--------------------------------")
    #for i in range(len(Lista_Sintomas)):
    #  print(str(i+1) + " " + str(Lista_Sintomas[i]))
    #print("--------------------------------")
    """
    time.sleep(2)
    aux = -1
    grav = -1
    while(aux != 0):
      aux = raw_input("- Te escucho...\n")
      while(not check_int(aux) or not(int(aux)>-1 and int(aux)<len(Lista_Sintomas)+1) or Mis_Sintomas.__contains__(int(aux)-1)):
        aux = raw_input("- Ingresa un dato numerico real y que no haya sido registrado\n")
      aux = int(aux)
      if(aux > 0):
        Mis_Sintomas.append(aux-1)
        time.sleep(2)
        print("- Entiendo, tienes el sintoma: " + Lista_Sintomas[aux-1])
        time.sleep(2)
        grav = raw_input("- Dime que tan fuerte es (0 - bajo, 1 - medio, 2 - alto)\n")
        while(not check_int(grav) or (int(grav)!=0 and int(grav)!=1 and int(grav)!=2)):
          grav =  raw_input("- Ingresa un dato real: 0 - bajo, 1 - medio, 2 - alto\n")
        grav = int(grav)
        if(grav == 0):
          time.sleep(2)
          print("- Entiendo, el sintoma es bajo")
          Mi_Gravedad.append("bajo")
        else:
          if(grav == 1):
            time.sleep(2)
            print("- Entiendo, el sintoma es medio")
            Mi_Gravedad.append("medio")
          else:
            time.sleep(2)
            print("- Entiendo, el sintoma es alto")
            Mi_Gravedad.append("alto")
        aux = -1
        time.sleep(2)
        print("- Ok, continua...")
    time.sleep(3)
    print("- Listo, esos serian todos tus sintomas\n")
    time.sleep(2)
    print("--- PROCESANDO ---")
    print("")
    time.sleep(3)
    algoritmo(Mi_Edad,Mi_Sexo,Mis_Sintomas)
    print("")
    if(len(Mis_Sintomas) != 0):
      time.sleep(2)
      print("- Con esta informacion, te sugiero que contactes a un medico profesional para que te haga una revision exhaustiva y mas exacta.\n")
    time.sleep(3)
    print("- Muchas gracias por conversar conmigo\n")
    """

main()

#Motion.wakeUp()
# Motion.moveInit()
# Motion.post.moveTo(0.5, 0, 0)
#Speech.say("Hola a todos!!")
#for i in range(3):
    #Motion.angleInterpolation(names, [-3.0, 1.2, -0.7], times, True)
    #Motion.angleInterpolation(names, [-1.0, 1.2, -0.7], times, True)
#Motion.rest()








