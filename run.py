
import eel
import socket
import json
from dataclasses import dataclass
from threading import Thread
import time

# filename = askopenfilename()

eel.init('gui')

_SERVER_IP      =   socket.gethostbyname(socket.gethostname()) 
_SERVER_PORT    =   42697

_UID = json.load(open("uid.json"),)["uid"]

print(f"{_UID}")
@dataclass
class Settings:
    """Class for keeping track of the user settings"""
    username                :       str
    status                  :       str
    avatar                  :       str
    colorScheme             :       list
    internalServerPort      :       int
    _settingsFile           :       dict

    def __init__(self) -> None:
        self.loadSettings()

    def loadSettings(self) -> None:
        try:
            with open("settings.json",) as s:
                self._settingsFile     =   json.load(s)

            self.username              =   self._settingsFile.get("username")
            self.status                =   self._settingsFile.get("status")
            self.avatar                =   self._settingsFile.get("avatar")
            self.colorScheme           =   self._settingsFile.get("colorScheme")
            self.internalServerPort    =   self._settingsFile.get("internalServerPort")

        except:
            print("Settings file not found.")
            exit()

    def saveSettings(self) -> None:

        self._settingsFile = {
            "username"              :       self.username,
            "status"                :       self.status,
            "avatar"                :       self.avatar,
            "internalServerPort"    :       self.internalServerPort,
            "colorScheme"           :       self.colorScheme
        }

        try:
            with open("settings.json","w") as s:
                s.write(json.dumps(self._settingsFile))
        except: 
            print("Could not save settings.")
            exit()

        self.loadSettings()

    def returnJSON(self) -> None:
        eel.loadSettings(json.dumps(self._settingsFile))

@eel.expose()
def updateSettings(misc:list, colors:list) -> None:

    _SETTINGS.username = misc[0]
    _SETTINGS.status = misc[1]
    _SETTINGS.internalServerPort = misc[2]

    _SETTINGS.colorScheme["color1"]     =    colors[0]
    _SETTINGS.colorScheme["color2"]     =    colors[1]
    _SETTINGS.colorScheme["color3"]     =    colors[2]
    _SETTINGS.colorScheme["color4"]     =    colors[3]
    _SETTINGS.colorScheme["color5"]     =    colors[4]
    _SETTINGS.colorScheme["color6"]     =    colors[5]
    _SETTINGS.colorScheme["color7"]     =    colors[6]
    _SETTINGS.colorScheme["color8"]     =    colors[7]
    _SETTINGS.colorScheme["color9"]     =    colors[8]
    _SETTINGS.colorScheme["color10"]    =    colors[9]
    _SETTINGS.colorScheme["color11"]    =    colors[10]


    _SETTINGS.saveSettings()
    _SETTINGS.returnJSON()

@dataclass
class Connections:
    """Class for keeping track of contacts and incoming connections"""

    accepted      :       dict 
    pending       :       dict 
    clients       :       list
    active        :       dict 

    def addPending(self, UID:str, clientFile:dict) -> None:
        self.pending[UID] = {
            "username"          :   clientFile["username"],
            "profilePhoto"      :   clientFile["profilePhoto"],
            "status"            :   clientFile["status"],
        }

    def moveToAccepted(self, UID:str) -> None:
        self.accepted[UID] = self.pending[UID]
        self.pending.pop(UID)

    def remove(self, UID:str) -> None:
        try:
            self.accepted.pop(UID)
        except:
            self.pending.pop(UID)
        finally:
            print("The contract you're trying to remove does not exist")

class Client:
    def __init__(self) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    def connect(self) -> None:
        
        self.socket.connect((_SERVER_IP, _SERVER_PORT))
        
        clientFile = self.generatePacket(
            "newConnection",
            {"username":_SETTINGS.username,"avatar":_SETTINGS.avatar,"status":_SETTINGS.status}
            )

        if clientFile != None:
            
            clientFile = json.dumps(clientFile)
            self.socket.send(clientFile.encode("utf-8"))
        
        
    def generatePacket(self, packetType:str, content:dict, toWhom:str = "") -> dict:
        if packetType == "newConnection":
            packet = {
                "type":packetType,
                "uid":_UID,
                "content":content
            }
        elif packetType == "messagePacket":
            packet = {
                "type":packetType,
                "uid":_UID,
                "destination":toWhom,
                "time":time.time()*1000,
                "content":content
            }
        else:
            print("Invalid packet")
            return None
        
        return packet


# Create the contact dictionary
_CONTACTS = Connections({},{},[],{})

#Load the settings and send the JSON file to JS
_SETTINGS = Settings()
_SETTINGS.returnJSON()

# Create the client object
_CLIENT = Client()
_CLIENT.connect()


#Start the app
eel.start('index.html', size=("1152","640"))
