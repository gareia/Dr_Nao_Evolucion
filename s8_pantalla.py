from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import time

options = Options() #options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument("user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data")
path = "E:/Descargas/chromedriver_win32/chromedriver.exe"
#driver = webdriver.Chrome(executable_path=r"E:/Descargas/chromedriver_win32/chromedriver.exe")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)#path,chrome_options=options)
url = f"https://web.whatsapp.com/send?phone={}&text=ProbandoEnv%C3%ADoAutom%C3%A1tico2ConPython"
driver.get("https://web.whatsapp.com/")
time.sleep(30)
#driver.maximize_window()
#time.sleep(2)
driver.quit()