
REQUISITOS: (Guiarse de _ejemploPath.png)
1.Instalar python2.7 y añadir al path (Ubicacion\Scripts y Ubicacion\)
2.Instalar python3 y añadir al path (Ubicacion\Scripts y Ubicacion\)
3.Asegurarse que python2.7 esté primero para que sea el predeterminado (python archivo.py)
4.Asegurarse que python3 pueda llamar por comandos (python3 archivo.py)
5.Instalar naoqi y añadir al path (Ubicacion\lib)
6.Instalar Google Chrome
7.Mantener una sesión abierta de Whatsapp web 

FUNCIONAMIENTO:
1.Cambiar credenciales de internet en _redInternetId.txt y _redInternetPass.txt
2.Cambiar credenciales de la red del laboratorio en _redNaoId.txt y _redNaoPass.txt
3.Cambiar credenciales del robot en _redNaoIp.txt y _redInternetPort.txt
4.Cambiar urls de azure api en _azureApi.py
5.Cambiar path a la carpeta user data de Chrome en _chromeUserData.txt
6.Asegurarse que las redes estén disponibles
7.Asegurarse que la sesión de Whatsapp web esté abierta
8.En el archivo _main.py
 | Con Nao: Solo descomentar comentario debajo de "Entorno CON NAO"
 | Sin Nao: Solo descomentar comentario debajo de "Entorno SIN NAO"
9.Correr el archivo _main.py con Python 2.7 (python _main.py)

ATENCIÓN:
1.Tareas programadas pueden impedir el envío a Whatsapp por el cambio de focus