from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--celular", type=str)
parser.add_argument("-rc", "--recomendacion", nargs='*', type=str)
parser.add_argument('-rs', '--resultados', nargs='*', type=str)
args = parser.parse_args()

mensaje = "Paciente, a continuación listo los resultados de su última visita:%0a"

cel = args.celular
print(cel)

res = args.resultados
print(type(res))
for r in res:
    r = r.replace("+", " ")
    r = r.replace(":", " al ")
    mensaje += "*" + r + "%"+"%0a"
    print(r)

rec = args.recomendacion
print(type(rec))
for r in rec:
    r = r.replace("+", " ")
    mensaje += "%0a" + r + "%0a"
    print(r)

mensaje += "Gracias."

print(mensaje)

options = Options()
options.add_argument("start-maximized")
try:
    pathChromeUserData = '_chromeUserData.txt'
    with open(pathChromeUserData, 'r') as file:
        path = file.read()
except Exception:
    raise Exception("Ocurrió un error al leer el archivo "+pathChromeUserData)

options.add_argument(f"user-data-dir={path}")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
url = f"https://web.whatsapp.com/send?phone={cel}&text={mensaje}"
driver.get(url)

try:
    wait = WebDriverWait(driver,100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Enviar']"))).send_keys(Keys.RETURN)#
    print("Mensaje enviado")
    time.sleep(15)
except Exception:
    driver.quit()
    raise Exception("No se pudo enviar el mensaje")
    
driver.quit()