from _internet import connect,createNewConnection,removeConnection
import time

print("------archivo wsp-------")

def main():
    
    #!--------------------------------------------------------------------

    try:
        pathInternetId = '_redInternetId.txt'
        with open(pathInternetId, 'r') as file:
            celularRed = file.read()
            print("Red internet: "+celularRed)
    
    except Exception as e:
        print("Ocurrió un error al leer el archivo "+pathInternetId)
        return 0

    try:
        pathInternetPass = '_redInternetPass.txt'
        with open(pathInternetPass, 'r') as file:
            celularPass = file.read()
    
    except Exception as e:
        print("Ocurrió un error al leer el archivo "+pathInternetPass)
        return 0    
    
    #!--------------------------------------------------------------------

    if(createNewConnection(celularRed, celularRed, celularPass) != 0):
        removeConnection(celularRed)
        print("Error al agregar red")
        return 0

    time.sleep(3)

    if(connect(celularRed, celularRed) != 0):
        removeConnection(celularRed)
        print("Error al conectarse a la red")
        return 0
    
    time.sleep(6)

    #!--------------------------------------------------------------------

    import pywhatkit
    import argparse

    try:
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--celular", type=str)
        parser.add_argument("-rc", "--recomendacion", nargs='*', type=str)
        parser.add_argument('-rs', '--resultados', nargs='*', type=str)
        args = parser.parse_args()

        mensaje = "Paciente, a continuación listo los resultados de su última visita:\n"

        cel = args.celular
        print(cel)

        res = args.resultados
        print(type(res))
        for r in res:
            r = r.replace("+", " ")
            r = r.replace(":", " al ")
            mensaje += "*" + r + "%\n"
            print(r)

        rec = args.recomendacion
        print(type(rec))
        for r in rec:
            r = r.replace("+", " ")
            mensaje += "\n" + r + "\n"
            print(r)

        mensaje += "Gracias."
        
        pywhatkit.sendwhatmsg_instantly(args.celular, mensaje, 10)
        print("Mensaje enviado")
        removeConnection(celularRed)

    except pywhatkit.InternetException:
        print("Error conectando a internet para enviar el mensaje de whatsapp")
        removeConnection(celularRed)
        return 0

    except Exception as e:
        print("Ocurrió un error inesperado en el archivo wsp: "+ e.message)
        return 0
    
main()