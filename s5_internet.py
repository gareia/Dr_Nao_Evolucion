import os

# function to establish a new connection
def createNewConnection(name, SSID, password):
    config = """<?xml version=\"1.0\"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>"""+name+"""</name>
    <SSIDConfig>
        <SSID>
            <name>"""+SSID+"""</name>
        </SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <connectionMode>auto</connectionMode>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>"""+password+"""</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>"""
    command = "netsh wlan add profile filename=\""+name+".xml\""+" interface=Wi-Fi"
    with open(name+".xml", 'w') as file:
        file.write(config)
    os.system(command)
 
# function to connect to a network   
def connect(name, SSID):
    command = "netsh wlan connect name=\""+name+"\" ssid=\""+SSID+"\" interface=Wi-Fi"
    os.system(command)
 
# function to display avavilabe Wifi networks   
def displayAvailableNetworks():
    command = "netsh wlan show networks interface=Wi-Fi"
    os.system(command)


# display available netwroks
#displayAvailableNetworks()

# input wifi name and password
#name = "DIY_UPC" #"Ni te atrevas" #input("Name of Wi-Fi: ")
#password = "fablabupc7"
#password = #"nvth2041" #input("Password: ")

# establish new connection
#createNewConnection("DIY_UPC", "DIY_UPC", "fablabupc7")

# connect to the wifi network
#connect(name, name)
#print("If you aren't connected to this network, try connecting with the correct password!")



#command = "netsh wlan show networks interface=Wi-Fi"
#command = "netsh wlan show profiles"
#command = "netsh wlan show interfaces"
#command = "ipconfig"
#os.system(command)

#https://www.youtube.com/watch?v=J2tmjOXrvWY

"""
name = "Ni te atrevas"
command = "netsh wlan connect name=\""+name+"\" ssid=\""+name+"\" interface=Wi-Fi"
os.system(command)
"""
"""
from wireless import Wireless
wireless = Wireless()
#wireless.interface()
wireless.connect(ssid='Ni te atrevas', password='nvth2041')
#wireless.interface()
"""
"""
from pythonwifi.iwlibs import Wireless
wifi = Wireless('Ni te atrevas')
print(wifi.getEssid())
print(wifi.getMode())
"""