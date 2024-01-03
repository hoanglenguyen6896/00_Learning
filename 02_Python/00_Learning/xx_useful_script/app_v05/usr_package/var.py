from colorama import Fore

bot = "bots"
botId = "id"
botName = "botName"
status = "status"
isLifted = "isLifted"
podName = "podName"
chargerLevel = "chargeLevel"
chargerId = "chargerId"
location = "location"
path = "path"
dateUpdated = "dateUpdated"
isPaused = "isPaused"
botIp = "botIp"
taskStatus = "taskStatus"

connected = "connectedBots"

botStatus_dict = {
    1:"Available",
    2:"Reserved",
    3:"Busy",
    4:"Charging",
    5:"Pending",
    6:"Fault",
    7:"N/A 7"
}

map_dict = {
    1:"Drive Aisle",
    2:"Obstacle",
    3:"Storage",
    4:"Queue",
    5:"Maintenance",
    6:"Workstation",
    7:"Charger",
    8:"Queue In",
    9:"Queue Out"
}

color_for_txt = {
    "Fault":        Fore.RED,
    "Pause":        Fore.BLUE,
    "Connection":   Fore.CYAN,
    "Idle":         Fore.YELLOW,
    "Charging":     Fore.GREEN,
    "Ignore":       Fore.MAGENTA,
    "N/A 7":        Fore.WHITE,
    "Success":      Fore.GREEN,
}


