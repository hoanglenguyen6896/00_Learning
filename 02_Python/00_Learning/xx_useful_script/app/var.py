from colorama import Fore

bot = 'bots'
id = 'id'
botName = 'botName'
status = 'status'
isLifted = 'isLifted'
podName = 'podName'
chargerLevel = 'chargeLevel'
chargerId = 'chargerId'
location = 'location'
path = 'path'
dateUpdated = 'dateUpdated'
isPaused = 'isPaused'
botIp = 'botIp'
taskStatus = 'taskStatus'

botStatus_dict = {1:'Idle', 2:'Station', 3:'Busy', 4:'Charging', 5:'Pending', 6:'Fault', 7:'N/A 7'}

color_for_txt = {
    'Fault':        Fore.RED,
    'Pause':        Fore.CYAN,
    'Connection':   Fore.BLUE,
    'Idle':         Fore.YELLOW,
    'Charging':     Fore.GREEN,
    'Ignore':       Fore.WHITE,
    'N/A 7':        Fore.WHITE
}