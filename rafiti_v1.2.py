import qi
import argparse
import sys
import time
from Azure_Api import algoritmo

def main(session):

    motion_service = session.service("ALMotion")# Permite el movimiento del robot
    tts_service=session.service("ALTextToSpeech") # Permite hablar al robot
    tts_recognition_service=session.service("ALSpeechRecognition") # Reconocer sonidos en general
    memory_service=session.service("ALMemory") # Guardar en memoria los datos reconocidos

    # Wake up robot
    motion_service.wakeUp()
    # Send robot to Stand Init

    #Changue the language
    tts_service.setLanguage('Spanish') # Lenguaje con el cual hablara el robot

    tts_recognition_service.setLanguage("Spanish") # Lenguaje con el cual reconocera las voces o sonidos.
    
    #Say Hello to user
#!------------------------------------------------------------------------------------
    tts_service.say("Hola, yo soy NAO y tu como te llamas?")
#!------------------------------------------------------------------------------------
    #The robot talk to ask the user about her/his age
    tts_service.say("Y cuantos anios tienes?")
    vocabulary1=["cinco","seis","siete","ocho","nueve","diez","once","doce","trece","catorce","quince","dieciseis",\
        "diecisiete","dieciocho","diecinueve","veinte"]
    edad_dict={'cinco':5,'seis':6,'siete':7,'ocho':8,'nueve':9,'diez':10,'once':11,'doce':12,'trece':13,'catorce':14,\
        'quince':15,'dieciseis':16,'diecisiete':17,'dieciocho':18,'diecinueve':19,'veinte':20}
    

    tts_recognition_service.setVocabulary(vocabulary1,False) # Falso : se refiere a que debes indicarle o hablar tal y cual es la palabra  // True : obviar palabras o frases ejemplo: <Tengo> cinco <anios> , obviara los que contengan <>
    tts_recognition_service.subscribe("edad") # Genera el evento llamado edad
    memory_service.subscribeToEvent('WordRecognized',"edad",'wordRecognized')
    time.sleep(10) 
    boolean=False

    while boolean==False:

        edad=memory_service.getData("WordRecognized")
        if str(edad[0]) in vocabulary1 :
            tts_service.say("Entiendo tienes"+str(edad[0])+"anios")
            print("edad: %s" % edad[0])
            edad_save=edad_dict[str(edad[0])]
            tts_recognition_service.unsubscribe("edad")
            memory_service.unsubscribeToEvent('WordRecognized',"edad",'wordRecognized')

            tts_recognition_service.pause(False) #reinicia el servicio de reconocimiento de voz
            boolean=True
        else:
            tts_service.say("No he entendido tu edad puedes repetirlo")


#!-------------------------------------------33[]33[]-----------------------------------------
    #The robot ask the user about her/his sex.
    tts_service.say("Dime cual es tu sexo: masculino o femenino ?")
    vocabulary2=['masculino','femenino','otro']
    sexo_dict={'masculino':1,'femenino':0,'otro':1}


    tts_recognition_service.setVocabulary(vocabulary2,False)
    tts_recognition_service.subscribe("sexo")
    memory_service.subscribeToEvent('WordRecognized',"sexo",'wordRecognized')
    time.sleep(10)
    boolean=False

    while boolean==False:
        sexo=memory_service.getData("WordRecognized")
        if str(sexo[0]) in vocabulary2 :
            tts_service.say("Entiendo tu sexo es:" +str(sexo[0]))
            print("sexo: %s" % sexo[0])
            sexo_save=sexo_dict[str(sexo[0])]
            tts_recognition_service.unsubscribe("sexo")
            memory_service.unsubscribeToEvent('WordRecognized',"sexo",'wordRecognized')

            tts_recognition_service.pause(False) #reinicia el servicio de reconocimiento de voz
            boolean=True
        else:
            tts_service.say("No he entendido tu sexo puedes repetirlo")
#!------------------------------------------------------------------------------------
    #The robot says some symptoms to the user
    #Condicional COVID else continue
    #Start of While

    covid_sintomas=[]
    while len(covid_sintomas) < 3:
        tts_service.say("\\style=joyfull\\Entonces cuentame?\\pau=1000\\ \\style=didactic\\como te encuentras el dia de hoy?")
        tts_service.say("Te mostraremos una lista de sintomas para descartar el COVID 19")
        tts_service.say("Dime tienes algunos de estos sintomas: Tos, Dificultad para respirar, Dolores, Fatiga , \
            Diarrea, Congestion Nasal, Nauseas, Fiebre, Vomitos ")
        vocabulary4=["tos","dificultad","respirar","dolores","fatiga","diarrea","congestion", "nasal","nauseas",\
            "fiebre","vomitos", "no"]

  
        tts_recognition_service.setVocabulary(vocabulary4,True) 
        tts_recognition_service.subscribe("sintoma_covid") 
        memory_service.subscribeToEvent('WordRecognized',"sintoma_covid",'wordRecognized')
        time.sleep(10)
        boolean=False
        while boolean==False:
            sintoma_voi=memory_service.getData("WordRecognized")
            if str(sintoma_voi[0]) in vocabulary4 :
                tts_service.say("Entiendo tu sintoma es:" +str(sintoma_voi[0]))
                print("sintoma: %s" % sintoma_voi[0])
                covid_sintomas.append(str(sintoma_voi[0]))
                tts_recognition_service.unsubscribe("sintoma_covid")
                memory_service.unsubscribeToEvent('WordRecognized',"sintoma_covid",'wordRecognized')

                tts_recognition_service.pause(False) #reinicia el servicio de reconocimiento de voz
                boolean=True
            else:
                tts_service.say("No he entendido tu sintoma puedes repetirlo")

        if sintoma_voi[0]=='no' :
            break
        if len(covid_sintomas) == 3:
            tts_service.say("Por favor, realice una prueba del COVID 19, nos vemos")
            motion_service.rest()

    
    if sintoma_voi[0] == 'no':

        tts_service.say("\\style=joyfull\\Entonces cuentame?\\pau=1000\\ \\style=didactic\\como te encuentras el dia de hoy?")
        tts_service.say("Dime tienes algunos de estos sintomas: tos, dificultad para respirar, dolores, \
        perdida de peso, fatiga , molestias generales ")
        vocabulary3=["tos","dificultad para respirar","dolores","perdida de peso","fatiga","molestias generales"]


        tts_recognition_service.setVocabulary(vocabulary3,True) 
        tts_recognition_service.subscribe("sintoma") 
        memory_service.subscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
        time.sleep(10)
        boolean=False
        while boolean==False:
            sintoma_recog=memory_service.getData("WordRecognized")
            if str(sintoma_recog[0]) in vocabulary3:
                tts_service.say("Entiendo tu sintoma es:" +str(sintoma_recog[0]))
                print("sintoma_1: %s" % sintoma_voi[0])
                tts_recognition_service.unsubscribe("sintoma")
                memory_service.unsubscribeToEvent('WordRecognized',"sintoma",'wordRecognized')

                tts_recognition_service.pause(False)
                boolean=True
            else:
                tts_service.say("No he entendido tu sintoma puedes repetirlo")
                time.sleep(5)
        
        sintomas=[]
        gravedad=[]
       
        if str(sintoma_recog[0])=='tos':
            #sintomas.append(str(sintoma_recog[0]))
            tts_service.say("Te mencionare otros posibles sintomas: alergia,tos con mucosidad amarilla o verde todos los dias,\
                nariz que moquea,congestion nasal, tos amarilla, moco, tos cronica,tos seca, tos verdosa, tos con sangre,dolor de garganta,\
                      boca seca,tos sibilante,tos seca persistente")

            vocabulary=['alergia','tos con mucosidad amarilla o verde todos los dias',\
                'nariz que moquea','congestion nasal', 'tos amarilla', 'moco', 'tos cronica','tos seca', 'tos verdosa', 'tos con sangre','dolor de garganta',\
                      'boca seca','tos sibilante','tos seca persistente','si','no','repetir','bajo','medio','alto']
            
            tts_recognition_service.setVocabulary(vocabulary,True)
            tts_recognition_service.subscribe("sintoma")
            memory_service.subscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
            time.sleep(10)
            boolean=False
            while boolean==False:
                sintomas_recog=memory_service.getData("WordRecognized")
                if str(sintomas_recog[0]) in vocabulary :
                    tts_service.say("Entiendo tu sintoma es:" +str(sintomas_recog[0]))
                    sintomas.append(str(sintomas_recog[0]))
                    print("sintoma_1: %s" % sintomas_recog[0])
                    
                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                    time.sleep(5)
                    gravedad_recog=memory_service.getData("WordRecognized")
                    gravedad.append(gravedad_recog[0])

                    bool_answer=False
                    while bool_answer==False:
                        tts_service.say("Tienes mas sintomas?")
                        tts_recognition_service.pause(False)
                        time.sleep(5)
                        if str(sintomas_recog[0])=='si' :
                            tts_service.say("Te gustaria escuchar denuevo los sintomas?")
                            tts_recognition_service.pause(False)
                            time.sleep(5)
                            if str(sintomas_recog[0])=='si' :
                                tts_service.say("Los sintomas son los siguientes: alergia,tos con mucosidad amarilla o verde todos los dias,\
                                            nariz que moquea,congestion nasal, tos amarilla, moco, tos cronica,tos seca, tos verdosa, tos con sangre,dolor de garganta,\
                                            boca seca,tos sibilante,tos seca persistente")
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0]) in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])                                    

                            elif str(sintomas_recog[0])=='no':
                                tts_service.say('Dime tu sintoma, porfavor')
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0])in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                        elif str(sintomas_recog[0])=='no' :
                            tts_recognition_service.pause(False)
                            tts_recognition_service.unsubscribe("sintoma")
                            memory_service.unsubscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
                            bool_answer=True
                            boolean=True
                        
                else:
                    tts_service.say("No he entendido tu sintoma puedes repetirlo")
                    time.sleep(5)

        elif sintoma_recog[0]=='dificultad para respirar':
            #sintomas.append(str(sintoma_recog[0]))
            tts_service.say("Te mencionare otros posibles sintomas:sensacion de opresion en el pecho,sibilancias,dificultad para respirar que empeora durante los brotes,\
                nariz que moquea,congestion nasal,congestion en el pecho,respiracion rapida,respiracion superficial,dolor agudo en el pecho,latidos rapidos,palpitaciones del corazon,\
                    pausas en la respiracion,respiracion corta superficial y rapida,falta de aliento,latido del corazon mas rapido,un sonido seco y crepitante en los pulmones al inhalar")
            vocabulary=['sensacion de opresion en el pecho','sibilancias', 'dificultad para respirar que empeora durante los brotes', 'nariz que moquea','congestion nasal'\
                 'congestion en el pecho','respiracion rapida','respiracion superficial','dolor agudo en el pecho','latidos rapidos','palpitaciones del corazon','pausas en la respiracion',\
                    'respiracion corta superficial y rapida','falta de aliento','latido del corazon mas rapido','un sonido seco y crepitante en los pulmones al inhalar','si','no']
            
            tts_recognition_service.setVocabulary(vocabulary,True)
            tts_recognition_service.subcribe("sintoma")
            memory_service.subscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
            time.sleep(10)
            boolean=False
            while boolean==False:
                sintomas_recog=memory_service.getData("WordRecognized")
                if str(sintomas_recog[0]) in vocabulary :
                    tts_service.say("Entiendo tu sintoma es:" +str(sintomas_recog[0]))
                    sintomas.append(str(sintomas_recog[0]))
                    print("sintoma_2: %s" % sintomas_recog[0])
                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                    time.sleep(5)
                    gravedad_recog=memory_service.getData("WordRecognized")
                    gravedad.append(gravedad_recog[0])

                    bool_answer=False
                    while bool_answer==False:
                        tts_service.say("Tienes mas sintomas?")
                        tts_recognition_service.pause(False)
                        time.sleep(5)
                        if str(sintomas_recog[0])=='si':
                            tts_service.say("Te gustaria escuchar denuevo los sintomas?")
                            tts_recognition_service.pause(False)
                            time.sleep(5)
                            if str(sintomas_recog[0])=='si':
                                tts_service.say("Los sintomas son los siguientes:sensacion de opresion en el pecho,sibilancias,dificultad para respirar que empeora durante los brotes,\
                nariz que moquea,congestion nasal,congestion en el pecho,respiracion rapida,respiracion superficial,dolor agudo en el pecho,latidos rapidos,palpitaciones del corazon,\
                    pausas en la respiracion,respiracion corta superficial y rapida,falta de aliento,latido del corazon mas rapido,un sonido seco y crepitante en los pulmones al inhalar")
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0]) in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                            elif str(sintomas_recog[0])=='no':
                                tts_service.say('Dime tu sintoma, porfavor')
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0])in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                        elif str(sintomas_recog[0])=='no':
                            tts_recognition_service.pause(False)
                            tts_recognition_service.unsubscribe("sintoma")
                            memory_service.unsubscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
                            bool_answer=True
                            boolean=True
                        
                else:
                    tts_service.say("No he entendido tu sintoma puedes repetirlo")
                    time.sleep(5)

        elif sintoma_recog[0]=='dolores':
            tts_recognition_service.pause(False)
            tts_service.say("Te mencionare otros posibles sintomas:dolor de pecho,congestion en el pecho,dolor de espalda baja,dolor agudo en el pecho,dolor de cabeza,\
                dolores musculares,dolor en las articulaciones,dolor de garganta,edema,dolores de cabeza matutinos")
            vocabulary=['dolor de pecho','congestion en el pecho', 'dolor de espalda baja', 'dolor agudo en el pecho','dolor de cabeza','dolores musculares','dolor en las articulaciones',\
                'dolor de garganta','edema','dolores de cabeza matutinos','si','no']

            tts_recognition_service.setVocabulary(vocabulary,True)
            tts_recognition_service.subcribe("sintoma")
            memory_service.subscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
            time.sleep(5)

            #sintomas.append(str(sintoma_recog[0]))
            boolean=False
            while boolean==False:
                sintomas_recog=memory_service.getData("WordRecognized")
                if str(sintomas_recog[0]) in vocabulary :
                    tts_service.say("Entiendo tu sintoma es:" +str(sintomas_recog[0]))
                    sintomas.append(str(sintomas_recog[0]))
                    print("sintoma_3: %s" % sintomas_recog[0])
                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                    time.sleep(5)
                    gravedad_recog=memory_service.getData("WordRecognized")
                    gravedad.append(gravedad_recog[0])

                    bool_answer=False
                    while bool_answer==False:
                        tts_service.say("Tienes mas sintomas?")
                        tts_recognition_service.pause(False)
                        time.sleep(5)

                        if str(sintomas_recog[0])=='si' :
                            tts_service.say("Te gustaria escuchar denuevo los sintomas?")
                            tts_recognition_service.pause(False)
                            time.sleep(5)

                            if str(sintomas_recog[0])=='si':
                                tts_service.say("Los sintomas son los siguientes:dolor de pecho,congestion en el pecho,dolor de espalda baja,dolor agudo en el pecho,dolor de cabeza,\
                dolores musculares,dolor en las articulaciones,dolor de garganta,edema,dolores de cabeza matutinos")
                                time.sleep(5)

                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0]) in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                            elif str(sintomas_recog[0])=='no':
                                tts_service.say('Dime tu sintoma, porfavor')
                                time.sleep(5)
                                sintomas_recog=memory_service.getData("WordRecognized")
                                if str(sintomas_recog[0])in vocabulary :
                                    sintomas.append(str(sintomas_recog[0]))
                                    tts_service.say("Y dime cual es tu gravedad: bajo,medio,alto")
                                    time.sleep(5)
                                    gravedad_recog=memory_service.getData("WordRecognized")
                                    gravedad.append(gravedad_recog[0])

                        elif str(sintomas_recog[0])=='no' :
                            tts_recognition_service.pause(False)
                            tts_recognition_service.unsubscribe("sintoma")
                            memory_service.unsubscribeToEvent('WordRecognized',"sintoma",'wordRecognized')
                            bool_answer=True
                            boolean=True 
                else:
                    tts_service.say("No he entendido tu sintoma puedes repetirlo")
                    time.sleep(5)                   
        else:
            pass
    algoritmo(edad_save,sexo_save,sintomas)
    if(len(sintomas) != 0):
        time.sleep(2)
        print("- Con esta informacion, te sugiero que contactes a un medico profesional para que te haga una revision exhaustiva y mas exacta.\n")
        time.sleep(3)
        print("- Muchas gracias por conversar conmigo\n")
    #End While
 #!------------------------------------------------------------------------------------   
    # Go to rest position
    motion_service.rest()




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="127.0.0.1",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        print("tcp://" + args.ip + ":" + str(args.port))
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)
