# Get and load json
import json
import requests

# Os cmd
import os
import sys
import ctypes

# Time
import time
import datetime

# Catch key
import msvcrt

# Multithreading and signal
import threading
import signal

# User package
from usr_package import print_alert
from usr_package import command
from usr_package import field

from collections import defaultdict
from colorama import Fore
import colorama

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

botStatus_dict = {
    1:"Available",
    2:"Reserved",
    3:"Busy",
    4:"Charging",
    5:"Pending",
    6:"Fault",
    7:"N/A 7"
}

info = {
    "IP":       0,
    "Status":   1,
    "Axis":     2,
    "Pod":      3,
    "Battery":  4,
    "ID":       5,
    "Location": 6
}

color = {
    "Fault":        Fore.RED,
    "Pause":        Fore.BLUE,
    "Connection":   Fore.CYAN,
    "Idle":         Fore.YELLOW,
    "Charging":     Fore.GREEN,
    "Ignore":       Fore.MAGENTA,
    "N/A 7":        Fore.WHITE,
    "Success":      Fore.GREEN,
    "Information":  Fore.CYAN,
    "Complete":     Fore.GREEN,
    "NotComplete":  Fore.YELLOW,
    "True":         Fore.GREEN,
    "False":        Fore.RED
}

connected = "connectedBots"
is_estopped = "isEmergencyStopped"

warehouse = "Elgin"

url_query = {
    "field":    "https://wes-agv-portal-gateway.atlanta.iherb.net/api/Field",
    "bot_live": "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/liveUpdates",
    "connect":  "https://wes-agv-portal-gateway.iherbscs.net/api/bots/connected",
    "estop":    "https://wes-agv-portal-gateway.iherbscs.net/api/bots/emergencystop"
}

battery_limit = 40
idle_time_limit = 60
connection_time_limit = 30
bot_idle_threshold = 5

keep_windows_from_lock = True
time_press_cycle = 180

idle_location_reference = ["Drive Aisle", "Storage", "Workstation", "Queue Out", "Charger", "Maintenance"]
idle_status_reference = ['Busy']

rq_timeout = 10

print_field_2d = False

# Field location: x-y:'Location'
field_location = defaultdict(lambda: 0)

# Bot location: (botname):x-y
bot_info = {}

charging_list = []
idle_list = []
pause_list = []
fault_list = []
connection_list = []
ignore_list = []

terminate_thread = False
pause_all_thread = False
bot_live_pause = False
bot_print_pause = False
bot_idle_pause = False

new_data_print = False
new_data_idle = False
bot_live_json = {}
estop_json = {}

lock = threading.Lock()

def init(conf):
    global warehouse
    global bot_idle_threshold
    global battery_limit
    global idle_time_limit
    global connection_time_limit

    global idle_location_reference
    global idle_status_reference

    global rq_timeout

    global keep_windows_from_lock

    global url_query

    if conf == 0:
        print("Default ...")
    else:
        try:
            bot_idle_threshold = conf['alert']['idle_threshold']
            battery_limit = conf['limitation']['bat_lvl']
            idle_time_limit = conf['limitation']['idle_time']
            connection_time_limit = conf['limitation']['connection_time']
            idle_location_reference = conf['reference']['location_idle']
            idle_status_reference = conf['reference']['status_idle']
            rq_timeout = conf["sw"]["timeout"]
            keep_windows_from_lock = conf['keep_windows_from_lock']
            warehouse = conf['sw']['warehouse']
            url_query = conf['sw'][warehouse]["query"]
            print("Loading url ...")
        except:
            print(color['Fault'] + "App init failed >> Default - Elgin")

def bot_live_update():
    global field_location
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global bot_info

    global terminate_thread

    global bot_live_pause

    global bot_live_json
    global estop_json

    global new_data_idle
    global new_data_print

    connect_err = 0
    connection_new = []
    connection_dict_old = defaultdict(lambda: 0)
    bot_rsp = None
    con_rsp = None
    estop_rsp = None
    connection_set = None
    bot_set = None

    while True:
        charging_list_temp = []
        pause_list_temp = []
        fault_list_temp = []
        connection_list_temp = []
        bot_info_as_name = defaultdict(lambda: 0)
        # Query bot, connection, estop -------------------------------------------------------------------------------

        try:
            bot_rsp = requests.get(url_query["bot_live"], timeout = rq_timeout)
            con_rsp = requests.get(url_query["connect"], timeout = rq_timeout)
            estop_rsp = requests.get(url_query["estop"], timeout = rq_timeout)
        except:
            connect_err += 1
            print(f"!!!Query Error!!! Retrying ... <{connect_err:.>5}>")
            if connect_err == 30:
                terminate_thread = True
                print(color['Fault'] + 'Exceptions has happened too much... Program ended!!!')
                break
            if terminate_thread == True:
                break
            while pause_all_thread == True:
                time.sleep(1)
            time.sleep(1)
            continue
        else:
            connect_err = 0
            pass
        try:
            bot_live_json = bot_rsp.json() # Return a dictionary
            bot_connection_json = con_rsp.json()
            estop_json = estop_rsp.json()
            total_bot_in_field = len(bot_live_json["bots"])
        except:
            print(f"!!!Json Error!!! Retrying ... ")
            time.sleep(1)
            continue
        # Parse bot -------------------------------------------------------------------------------
        for index in range(total_bot_in_field):
            # bot_info_as_name: botName:[ip, stt, xy, pod, bat]
            botName_temp = int(bot_live_json["bots"][index]["botName"])
            xy_axis = print_alert.get_location_in_xy(bot_live_json["bots"][index]["location"])
            bot_info_as_name[botName_temp] = [bot_live_json["bots"][index]["botIp"],\
                        botStatus_dict[bot_live_json["bots"][index]["status"]],\
                        xy_axis,\
                        bot_live_json["bots"][index]["podName"],\
                        bot_live_json["bots"][index]["chargeLevel"],\
                        bot_live_json["bots"][index]["id"],\
                        field_location[xy_axis]]
            if botName_temp not in ignore_list:
                if bot_info_as_name[botName_temp][1] == 'N/A 7':
                    print_alert.print_a_bot_info(bot_live_json["bots"][index], 'N/A 7')
                # Get fault
                if bot_info_as_name[botName_temp][1] == 'Fault':
                    if bot_live_json["bots"][index]["botName"]:
                        fault_list_temp.append(int(botName_temp))
                # Get other status if not fault
                elif estop_json[is_estopped] == False:
                    # Get pause
                    if bot_live_json["bots"][index]["isPaused"] == True:
                        pause_list_temp.append(int(botName_temp))

                    # Get charge
                    if bot_info_as_name[botName_temp][4] <= battery_limit:
                        charging_list_temp.append(int(botName_temp))

        # Parse Connection -------------------------------------------------------------------------------
        if len(bot_connection_json[connected]) == len(bot_info_as_name.keys()):
            # Clear temp data
            connection_dict_old = defaultdict(lambda: 0)
        else:
            # Get new bot
            time_now = datetime.datetime.strptime(time.ctime(), "%c")
            bot_set = set(bot_info_as_name.keys())
            connection_set = set(bot_connection_json[connected])
            connection_new = list(bot_set.difference(connection_set))

            del_list = []
            # Remove what in old, not in new > old
            for key in connection_dict_old.keys():
                if key not in connection_new:
                    del_list.append(key)
            for key in del_list:
                del connection_dict_old[key]

            # Keep time of what in old and in new
            # Add what in new, not in old to old and update time
            for item in connection_new:
                if item not in connection_dict_old.keys():
                    connection_dict_old[item] = time_now

            # Append to connection list if bot is disconnected more than 30s
            for key, value in connection_dict_old.items():
                if (time_now - value).total_seconds() >= connection_time_limit:
                    if key not in ignore_list:
                        connection_list_temp.append(key)

        lock.acquire()
        bot_info = bot_info_as_name
        charging_list = charging_list_temp
        pause_list = pause_list_temp
        fault_list = fault_list_temp
        connection_list = connection_list_temp
        new_data_print = True
        new_data_idle = True
        lock.release()
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            # bot_live_pause = True
            time.sleep(1)
        # bot_live_pause = False
    print('Bot live ended!!!')

def bot_idle_predict():

    global bot_idle_pause
    global idle_list
    global bot_info
    global new_data_idle

    # Bot location:     (botname):'x-y'
    # Bot old location: (botname):['x-y', time]
    bot_location_old = defaultdict(lambda: 0)
    # > {0:['0-0',0]}
    idle_list_temp = None
    del_list = None

    while True:
        if new_data_idle == True:
            lock.acquire()
            bot_info_idle = bot_info
            new_data_idle = False
            lock.release()
            time.sleep(1)
        else:
            time.sleep(1)
            continue

        idle_list_temp = []
        del_list = []
        if len(bot_info_idle) == 0:
            continue
        # Get all bot location
        time_now = datetime.datetime.strptime(time.ctime(), "%c")
        # Query through new bot
        if type(bot_location_old) == int or type(bot_info_idle) == int:
            continue
        for bot, bot_data in bot_info_idle.items():
            if type(bot_data) == int:
                continue
            # Check if the bot in bot_info_idle (new) in bot_location_old
            if bot in bot_location_old.keys():
                if bot_data[info["Axis"]] != bot_location_old[bot][0] or bot_data[info["Status"]] not in idle_status_reference:
                    # if True and location is different > update time
                    bot_location_old[bot] = [bot_data[info["Axis"]], time_now]
            else:
                # Add new bot if not in bot_location_old
                bot_location_old[bot] = [bot_data[info["Axis"]] ,time_now]

        # Query through old bot to delete 'what in old, not in new'
        for bot in bot_location_old.keys():
            if bot not in bot_info_idle.keys():
                del_list.append(bot)
        for bot in del_list:
            del bot_location_old[bot]
        if len(bot_location_old) == 0:
            bot_location_old = defaultdict(lambda: 0)

        # Check if Current - last time >= 60s
        for bot, bot_data in bot_location_old.items():
            if bot not in ignore_list:
                if (time_now - bot_data[1]).total_seconds() >= idle_time_limit:
                    # if (field_location[bot_data[0]] in idle_location_reference) and bot_info[bot][1] in idle_status_reference:
                    if (field_location[bot_data[0]] in idle_location_reference):
                        idle_list_temp.append(bot)

        # Handle when field is esstop
        if len(estop_json) != 0:
            if estop_json[is_estopped] == False:
                idle_list = idle_list_temp
            else:
                idle_list = []

        if terminate_thread == True:
            break
        while pause_all_thread == True:
            # bot_idle_pause = True
            time.sleep(1)
        # bot_idle_pause = False
    print('Bot idle ended!!!')

def print_status(path):

    global bot_print_pause
    global new_data_print

    last_update = time.ctime()

    while True:
        os.system("cls")

        # Show ignore
        print_alert.print_by_name(bot_info, ignore_list, 'Ignore')
        # Show pause
        print_alert.print_by_name(bot_info, pause_list, 'Pause')
        # Show charging
        # print(charging_list)
        print_alert.print_by_name(bot_info, charging_list, 'Charging')
        # Show idle
        print_alert.print_by_name(bot_info, idle_list, 'Idle')
        # Show connection
        print_alert.print_by_name(bot_info, connection_list, 'Connection')
        # Show fault
        print_alert.print_by_name(bot_info, fault_list, 'Fault')

        if print_field_2d == True:
            if warehouse == "Elgin":
                field.print_field(bot_info)
            elif warehouse == "Atlanta":
                print(color["False"] + "Do not have function to print field in Atlanta, warehouse is too large")

        print(f"\n{time.ctime()} << Running\n{last_update} << Last Update")
        try:
            if estop_json["isEmergencyStopped"]:
                print(f"{warehouse} - Emergency Stop: " + color["True"] + "True")
            else:
                print(f"{warehouse} - Emergency Stop: " + color["False"] + "False")
        except:
            print(f"{warehouse} - Emergency Stop: Querying...")

        # Alert, fault is the highest priority
        if len(fault_list) > 0:
            print_alert.alert('Fault', path)
        elif len(connection_list) > 0:
            print_alert.alert('Connection', path)
        elif len(idle_list) >= bot_idle_threshold:
            print_alert.alert('Idle', path)
        elif len(charging_list) > 0:
            print_alert.alert('Charging', path)
        elif len(pause_list) > 0:
            print_alert.alert('Pause', path)
        elif len(ignore_list) > 0:
            print_alert.alert('Ignore', path)
        # print_alert.alert("Connection", path)
        if new_data_print == True:
            lock.acquire()
            new_data_print = False
            lock.release()
            last_update = time.ctime()

        time.sleep(1)
        if terminate_thread == True:
                break
        while pause_all_thread == True:
            bot_print_pause = True
            time.sleep(1)
        bot_print_pause = False
    print('Bot print ended!!!')


def signal_handler(sig, frame):
    terminate_thread = True
    time.sleep(1)
    os._exit(1)
    pass

def get_path():
    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    elif __file__:
        path = os.path.abspath(os.path.dirname(__file__))
    return path

# main thread
if __name__ == "__main__":
    # Init signal handler
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init(autoreset = True)
    cwd = get_path()
    print("Initializing ...")
    print("Loading configuration ...")
    # Init config
    try:
        f = open(cwd + '\\config.json', 'r')
        config = json.load(f)
        print_alert.init(config['alert']['sound'])
        command.init(config)
        init(config)
        f.close()
        print(color["Success"] + "Loaded configuration!!! >> " + config["sw"]["warehouse"])
    except:
        print(color['Fault'] + "Failed to load configuration file, using default configuration for Elgin")
        print_alert.init(0)
        command.init(0)
        init(0)

    time.sleep(1)
    print("Getting field information ...")
    # Get field information
    location_err = 0
    while True:
        try:
            json_response = requests.get(url_query["field"])
        except:
            location_err += 1
            print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
            if location_err == 30:
                print(color['Fault'] + "Exceptions has happened too much... Program ended!!!")
                os._exit(1)
                break
            time.sleep(1)
        else:
            field_json = json_response.json()
            for a_list in field_json['layout']:
                for element in a_list:
                    if element != None:
                        location_str = str(int(element['location']['x'])) + '-' + str(int(element['location']['y']))
                        field_location[location_str] = map_dict[element['nodeType']]
            print(color["Success"] + "Field information > Done")
            time.sleep(1)
            break

    time.sleep(1)
    # Create and start some thread
    thread_bot_live_update = threading.Thread(target = bot_live_update, args = ())
    thread_bot_live_update.start()
    thread_bot_idle_predict = threading.Thread(target = bot_idle_predict, args = ())
    thread_bot_idle_predict.start()
    thread_print_status = threading.Thread(target = print_status, args = (cwd,))
    thread_print_status.start()

    ES_DISPLAY_REQUIRED = 0x00000002
    time_ref = datetime.datetime.strptime(time.ctime(), "%c")
    time_now = datetime.datetime.strptime(time.ctime(), "%c")
    key = 0
    # Catch and run command mode
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if ord(key) == ord("c") or ord(key) == ord("C"):
                pause_all_thread = True
                while bot_print_pause == False:
                    time.sleep(1)

                if bot_live_json == {}:
                    print("You haven't haven any data to use command mode!!!")
                    pause_all_thread = False
                else:
                    command.execute_cmd(bot_info, field_location, idle_list, pause_list, ignore_list, cwd)
                    fault_list = []
                    pause_all_thread = False
                    # try:
                    #     command.execute_cmd(bot_info, field_location, idle_list, pause_list, ignore_list, cwd)
                    #     fault_list = []
                    #     pause_all_thread = False
                    # except:
                    #     print("Cmd failed!!! > Back to query ...")
                    #     time.sleep(2)
                    #     pause_all_thread = False
            elif ord(key) == ord("f") or ord(key) == ord("F"):
                print_field_2d = not print_field_2d
            elif ord(key) == ord("j") or ord(key) == ord("J"):
                ignore_list.extend(fault_list)
                fault_list = []
            elif ord(key) == ord("k") or ord(key) == ord("K"):
                ignore_list.extend(connection_list)
                connection_list = []
            elif ord(key) == ord("l") or ord(key) == ord("L"):
                ignore_list.extend(pause_list)
                pause_list = []
            elif ord(key) == ord("u") or ord(key) == ord("U"):
                ignore_list = []
            elif ord(key) == ord("q") or ord(key) == ord("Q"):
                terminate_thread = True
        if keep_windows_from_lock == True:
            time_now = datetime.datetime.strptime(time.ctime(), "%c")
            if (time_now - time_ref).total_seconds() >= time_press_cycle:
                time_ref = time_now
                ctypes.windll.kernel32.SetThreadExecutionState(ES_DISPLAY_REQUIRED)
        if (thread_bot_live_update.is_alive() == False\
                or thread_bot_idle_predict.is_alive() == False\
                or thread_print_status.is_alive() == False) and terminate_thread == False:
            print(f"Bot live {thread_bot_live_update.is_alive()}")
            print(f"Bot idle {thread_bot_idle_predict.is_alive()}")
            print(f"Bot print {thread_print_status.is_alive()}")
            terminate_thread = True
            while True:
                print_alert.alert("Crash", cwd)
                time.sleep(1)

        if terminate_thread == False:
            time.sleep(1)
        else:
            break
