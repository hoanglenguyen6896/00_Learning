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
from usr_package import sw
# from usr_package import field

from collections import defaultdict
from colorama import Fore
import colorama

CMD_KEY = (b'c', b'C')

ENABLE_UNFAULT_UNIGNORE_IGNORE_KEY = (b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9', b'0')
ENABLE_UNFAULT_UNIGNORE_UNFAULT_KEY = {b'!':0, b'@':1, b'#':2, b'$':3, b'%':4, b'^':5, b'&':6, b'*':7, b'(':8, b')':9}
Q_IGNORE_FAULT_KEY = (b'j', b'J')
Q_IGNORE_WIFI_KEY = (b'k', b'K')
Q_IGNORE_PAUSE_KEY = (b'l', b'L')
Q_UNIGNORE_KEY = (b'u', b'U')

EXIT_KEY = (b'q', b'Q')

ES_DISPLAY_REQUIRED = 0x00000002

SCREEN_UP_CYCLE = 180

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
color = {
    "Fault":        Fore.RED,
    "Pause":        Fore.BLUE,
    "Connection":   Fore.CYAN,
    "Idle":         Fore.YELLOW,
    "Charging":     Fore.GREEN,
    "Ignore":       Fore.WHITE,
    "N/A 7":        Fore.MAGENTA,
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
    "estop":    "https://wes-agv-portal-gateway.iherbscs.net/api/bots/emergencystop",
    "packwall": "https://wes-agv-packwall.iherbscs.net/api/packstations"
}

battery_limit = 40
idle_time_limit = 60
connection_time_limit = 30
bot_idle_threshold = 5
network_timeout = 30

keep_windows_from_lock = True

idle_location_reference = ["Drive Aisle", "Storage", "Workstation", "Queue Out", "Charger", "Maintenance"]
idle_status_reference = ["Busy", "Pending"]

rq_timeout = 10

print_field_2d = False

cwd = ""

# Field location: x-y:'Location'
field_location = defaultdict(lambda: 0)
packwall_info = defaultdict(lambda: 0)

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
bot_print_pause = False

new_data_print = False
new_data_idle = False
bot_live_json = {}
estop_json = {}


bot_rsp = None
con_rsp = None
estop_rsp = None

lock = threading.Lock()

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

def append_to_file(path, file_name, content):
    try:
        file = open(path + "\\" + file_name, "a")
        file.write(f"\n{time.ctime():-^80}\n")
        file.write(str(content))
        file.write(f"\n{'':-^80}\n")
        file.close()
    except Exception as e:
        print(e)

def init(conf):
    global warehouse
    global bot_idle_threshold
    global battery_limit
    global idle_time_limit
    global connection_time_limit
    global network_timeout

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
            network_timeout = conf['limitation']['network_time']
            idle_location_reference = conf['reference']['location_idle']
            idle_status_reference = conf['reference']['status_idle']
            rq_timeout = conf["sw"]["timeout"]
            keep_windows_from_lock = conf['keep_windows_from_lock']
            warehouse = conf['sw']['warehouse']
            url_query = conf['sw'][warehouse]["query"]
            # print("Loading url ...")
        except Exception as e:
            print(color["Fault"] + e)
            append_to_file(cwd, "exception.txt", e)
            print(color['Fault'] + "App init failed >> Default - Elgin")
            time.sleep(1)

def get_bot_live():
    global bot_rsp

    global terminate_thread

    global new_data_idle
    global new_data_print

    connect_err = 0

    while True:
        try:
            bot_rsp = requests.get(url_query["bot_live"], timeout = rq_timeout)
            connect_err = 0
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            print(f"Retrying ... <{connect_err:.>5}>")
            if terminate_thread == True:
                break
            while pause_all_thread == True:
                time.sleep(1)
            time.sleep(1)
            continue
        time.sleep(1)
        lock.acquire()
        new_data_print = True
        new_data_idle = True
        lock.release()
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            time.sleep(1)
    print("Get live ended!!!")

def get_connection():
    global con_rsp

    global terminate_thread
    connect_err = 0
    while True:
        try:
            con_rsp = requests.get(url_query["connect"], timeout = rq_timeout)
            connect_err = 0
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            print(f"Retrying ... <{connect_err:.>5}>")
            if terminate_thread == True:
                break
            while pause_all_thread == True:
                time.sleep(1)
            time.sleep(1)
            continue
        time.sleep(1)
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            time.sleep(1)
    print("Get connection ended!!!")

def get_estop():
    global estop_rsp

    global terminate_thread
    connect_err = 0
    while True:
        try:
            estop_rsp = requests.get(url_query["estop"], timeout = rq_timeout)
            connect_err = 0
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            print(f"Retrying ... <{connect_err:.>5}>")
            if terminate_thread == True:
                break
            while pause_all_thread == True:
                time.sleep(1)
            time.sleep(1)
            continue
        time.sleep(1)
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            time.sleep(1)
    print("Get estop ended!!!")

def bot_live_update():
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global bot_info

    global terminate_thread

    global bot_live_json
    global estop_json

    connect_err = 0
    connection_new = []
    connection_dict_old = defaultdict(lambda: 0)
    connection_set = None
    bot_set = None

    while True:
        charging_list_temp = []
        pause_list_temp = []
        fault_list_temp = []
        connection_list_temp = []
        bot_info_as_name = defaultdict(lambda: 0)
        # Query bot, connection, estop -------------------------------------------------------------------------------

        # try:
        #     bot_rsp = requests.get(url_query["bot_live"], timeout = rq_timeout)
        #     # bot_rsp_thread = threading.Thread(target = get_json_from_rq, args = (url_query["bot_live"], resp_list, 0))
        #     con_rsp = requests.get(url_query["connect"], timeout = rq_timeout)
        #     # con_rsp_thread = threading.Thread(target = get_json_from_rq, args = (url_query["connect"], resp_list, 0))
        #     estop_rsp = requests.get(url_query["estop"], timeout = rq_timeout)
        #     # estop_rsp_thread = threading.Thread(target = get_json_from_rq, args = (url_query["estop"], resp_list, 0))
        # except Exception as e:
        #     print(color["Fault"] + str(e))
        #     append_to_file(cwd, "exception.txt", e)
        #     if terminate_thread == True:
        #         break
        #     while pause_all_thread == True:
        #         time.sleep(1)
        #     time.sleep(1)
        #     continue
        # else:
        #     connect_err = 0
        #     pass

        try:
            bot_live_json = bot_rsp.json() # Return a dictionary
            bot_connection_json = con_rsp.json()
            estop_json = estop_rsp.json()
            total_bot_in_field = len(bot_live_json["bots"])
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            if terminate_thread == True:
                break
            while pause_all_thread == True:
                time.sleep(1)
            time.sleep(1)
            continue
        # Parse bot -------------------------------------------------------------------------------
        for index in range(total_bot_in_field):
            # ip, stt, xy, pod, bat, id, loc,
            botName_temp = int(bot_live_json["bots"][index]["botName"])
            xy_axis = print_alert.get_location_in_xy(bot_live_json["bots"][index]["location"])
            bot_info_as_name[botName_temp] = {"ip": bot_live_json["bots"][index]["botIp"],\
                        "stt": botStatus_dict[bot_live_json["bots"][index]["status"]],\
                        "xy": xy_axis,\
                        "pod": bot_live_json["bots"][index]["podName"],\
                        "bat": bot_live_json["bots"][index]["chargeLevel"],\
                        "id": bot_live_json["bots"][index]["id"],\
                        "loc": field_location[xy_axis]}
            if botName_temp not in ignore_list:
                if bot_info_as_name[botName_temp]["stt"] == 'N/A 7':
                    # print_alert.print_a_bot_info(bot_live_json["bots"][index], 'N/A 7')
                    pass
                # Get fault
                if bot_info_as_name[botName_temp]["stt"] == 'Fault':
                    if bot_live_json["bots"][index]["botName"]:
                        fault_list_temp.append(int(botName_temp))
                # Get other status if not fault
                elif estop_json[is_estopped] == False:
                    # Get pause
                    if bot_live_json["bots"][index]["isPaused"] == True:
                        pause_list_temp.append(int(botName_temp))

                    # Get charge
                    if bot_info_as_name[botName_temp]["bat"] <= battery_limit:
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
        charging_list_temp.sort()
        pause_list_temp.sort()
        fault_list_temp.sort()
        connection_list_temp.sort()
        time.sleep(1)
        lock.acquire()
        bot_info = bot_info_as_name
        # if len(charging_list_temp) == 0
        charging_list = charging_list_temp
        pause_list = pause_list_temp
        fault_list = fault_list_temp
        connection_list = connection_list_temp
        ignore_list.sort()
        lock.release()
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            time.sleep(1)
    print('Bot live ended!!!')

def bot_idle_predict():

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
            # print("1")
            lock.acquire()
            bot_info_idle = bot_info
            new_data_idle = False
            lock.release()
            time.sleep(1)
        else:
            # print("2")
            time.sleep(1)
            continue

        idle_list_temp = []
        del_list = []
        if len(bot_info_idle) == 0:
            # print("3")
            time.sleep(1)
            continue
        # Get all bot location
        time_now = datetime.datetime.strptime(time.ctime(), "%c")
        # Query through new bot
        # if type(bot_location_old) == int or type(bot_info_idle) == int:
        #     continue
        for bot, bot_data in bot_info_idle.items():
            if type(bot_data) == int:
                continue
            # Check if the bot in bot_info_idle (new) in bot_location_old
            if bot in bot_location_old.keys():
                if bot_data["xy"] != bot_location_old[bot][0] or bot_data["stt"] not in idle_status_reference:
                    # if True and location is different > update time
                    bot_location_old[bot] = [bot_data["xy"], time_now]
            else:
                # Add new bot if not in bot_location_old
                bot_location_old[bot] = [bot_data["xy"] ,time_now]

        # Query through old bot to delete 'what in old, not in new'
        for bot in bot_location_old.keys():
            if bot not in bot_info_idle.keys():
                del_list.append(bot)
        for bot in del_list:
            del bot_location_old[bot]
        if len(bot_location_old) == 0:
            bot_location_old = defaultdict(lambda: 0)

        # Check if Current - last time >= 60s (bot_location_old ["xy", time])
        for bot, bot_data in bot_location_old.items():
            if bot not in ignore_list:
                if (time_now - bot_data[1]).total_seconds() >= idle_time_limit:
                    # if (field_location[bot_data[0]] in idle_location_reference) and bot_info[bot][1] in idle_status_reference:
                    if (field_location[bot_data[0]] in idle_location_reference):
                        idle_list_temp.append(bot)
        idle_list_temp.sort()
        # Handle when field is e-stop
        if len(estop_json) != 0:
            if estop_json[is_estopped] == False:
                idle_list = idle_list_temp
            else:
                idle_list = []

        if terminate_thread == True:
            break
        while pause_all_thread == True:
            time.sleep(1)
    print('Bot idle ended!!!')

def print_status(path):

    global bot_print_pause
    global new_data_print

    last_update = time.ctime()
    # alerting = False
    alert_thread = threading.Thread(target = None, args = ())
    while True:
        os.system("cls")
        # Show ignore
        print_alert.print_by_name(bot_info, ignore_list, 'Ignore')
        # Show pause
        print_alert.print_by_name(bot_info, pause_list, 'Pause')
        # Show charging
        print_alert.print_by_name(bot_info, charging_list, 'Charging')
        # Show idle
        print_alert.print_by_name(bot_info, idle_list, 'Idle')
        # Show connection
        print_alert.print_by_name(bot_info, connection_list, 'Connection')
        # Show fault
        print_alert.print_by_name(bot_info, fault_list, 'Fault')

        # if print_field_2d == True:
        #     if warehouse == "Elgin":
        #         field.print_field(bot_info)
        #     elif warehouse == "Atlanta":
        #         print(color["False"] + "Do not have function to print field in Atlanta, warehouse is too large")

        print(f"\n{time.ctime()} << Running\n{last_update} << Last Update")
        try:
            if estop_json["isEmergencyStopped"]:
                print(f"{warehouse} - Emergency Stop: " + color["True"] + "True")
            else:
                print(f"{warehouse} - Emergency Stop: " + color["False"] + "False")
        except:
            print(f"{warehouse} - Emergency Stop: Querying...")

        if new_data_print == True:
            lock.acquire()
            new_data_print = False
            lock.release()
            last_update = time.ctime()

        # time_now = datetime.datetime.strptime(time.ctime(), "%c")
        time_last_update = datetime.datetime.strptime(last_update, "%c")
        if alert_thread.is_alive() == False:
            # Alert, network is the highest priority
            if (datetime.datetime.strptime(time.ctime(), "%c") - time_last_update).total_seconds() >= network_timeout:
                # print_alert.alert('Network', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Network', path))
                alert_thread.start()
            elif len(fault_list) > 0:
                # print_alert.alert('Fault', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Fault', path))
                alert_thread.start()
            elif len(connection_list) > 0:
                # print_alert.alert('Connection', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Connection', path))
                alert_thread.start()
            elif len(idle_list) >= bot_idle_threshold:
                # print_alert.alert('Idle', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Idle', path))
                alert_thread.start()
            elif len(charging_list) > 0:
                # print_alert.alert('Charging', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Charging', path))
                alert_thread.start()
            elif len(pause_list) > 0:
                # print_alert.alert('Pause', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Pause', path))
                alert_thread.start()
            elif len(ignore_list) > 0:
                # print_alert.alert('Ignore', path)
                alert_thread = threading.Thread(target = print_alert.alert, args = ('Ignore', path))
                alert_thread.start()
        time.sleep(1)
        if terminate_thread == True:
                break
        while pause_all_thread == True:
            bot_print_pause = True
            time_last_update = datetime.datetime.strptime(last_update, "%c")
            time.sleep(1)
        bot_print_pause = False
    print('Bot print ended!!!')

# main thread
if __name__ == "__main__":
    # Init signal handler
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init(autoreset = True)
    cwd = get_path()
    print("Initializing ...")
    print("Loading configuration ...", end = ">> ")

    # Init config
    try:
        f = open(cwd + '\\config.json', 'r')
        config = json.load(f)
        print_alert.init(config['alert']['sound'])
        command.init(config)
        init(config)
        f.close()
        print(color["Success"] + "Loaded configuration!!! >> " + config["sw"]["warehouse"])
    except Exception as e:
        print(color["Fault"] + str(e))
        append_to_file(cwd, "exception.txt", e)
        print(color['Fault'] + "Failed to load configuration file, using default configuration for Elgin")
        print_alert.init(0)
        command.init(0)
        init(0)

    # time.sleep(1)

    # Get field information
    print("Getting field information ...", end = ">> ")
    location_err = 0
    while True:
        try:
            json_response = requests.get(url_query["field"])
            field_json = json_response.json()
            for a_location in field_json['layout']:
                for element in a_location:
                    if element != None:
                        location_str = str(int(element['location']['x'])) + '-' + str(int(element['location']['y']))
                        field_location[location_str] = map_dict[element['nodeType']]
            print(color["Success"] + "Field information > Done")
            # time.sleep(1)
            break
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            location_err += 1
            print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
            if location_err == 30:
                print(color['Fault'] + "Exceptions has happened too much... Program ended!!!")
                terminate_thread = True
                os._exit(1)
                break
            time.sleep(1)
            os._exit(1)

    # Get packstation information
    print("Getting packwall information ...", end = ">> ")
    while True:
        try:
            json_response = requests.get(url_query["packwall"])
            packwall_json = json_response.json()
            for a_packwall in packwall_json['packStations']:
                # print(a_packwall["name"] + " " + a_packwall["id"])
                packwall_info[a_packwall["name"]] = a_packwall["id"]
            print(color["Success"] + "Packwall information > Done")
            time.sleep(1)
            break
        except Exception as e:
            print(color["Fault"] + str(e))
            append_to_file(cwd, "exception.txt", e)
            location_err += 1
            print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
            if location_err == 30:
                print(color['Fault'] + "Exceptions has happened too much... Program ended!!!")
                terminate_thread = True
                os._exit(1)
                break
            time.sleep(1)
            os._exit(1)
    # time.sleep(1)
    # f_temp = open("loc_temp.txt", "w")
    # f_temp.write(str(field_location))
    # f_temp.close()
    # pass
    # Create and start query thread
    thread_get_bot_live = threading.Thread(target = get_bot_live, args = ())
    thread_get_bot_live.start()
    thread_get_bot_connection = threading.Thread(target = get_connection, args = ())
    thread_get_bot_connection.start()
    thread_get_estop = threading.Thread(target = get_estop, args = ())
    thread_get_estop.start()

    # Create and start parse thread
    thread_bot_live_update = threading.Thread(target = bot_live_update, args = ())
    thread_bot_live_update.start()
    thread_bot_idle_predict = threading.Thread(target = bot_idle_predict, args = ())
    thread_bot_idle_predict.start()
    while len(bot_info) == 0:
        time.sleep(1)
        print("Waiting for data ...")
    thread_print_status = threading.Thread(target = print_status, args = (cwd,))
    thread_print_status.start()

    time_ref = datetime.datetime.strptime(time.ctime(), "%c")
    time_now = time_ref

    key = 0

    # Catch and run command
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch() # return byte type b'c'
            if key in CMD_KEY:
                pause_all_thread = True
                while bot_print_pause == False:
                    time.sleep(1)
                try:
                    command.execute_cmd(bot_info, field_location, idle_list, pause_list, ignore_list, cwd, packwall_info)
                except Exception as e:
                    print(color["Fault"] + str(e))
                    append_to_file(cwd, "exception.txt", e)
                    print("Exiting command mode ...")
                    time.sleep(2)
                fault_list = []
                pause_all_thread = False
            # elif ord(key) == ord("f") or ord(key) == ord("F"):
            #     print_field_2d = not print_field_2d
            elif key in Q_IGNORE_FAULT_KEY:
                ignore_list.extend(fault_list)
                fault_list = []
            elif key in Q_IGNORE_WIFI_KEY:
                ignore_list.extend(connection_list)
                connection_list = []
            elif key in Q_IGNORE_PAUSE_KEY:
                ignore_list.extend(pause_list)
                pause_list = []
            elif key in Q_UNIGNORE_KEY:
                ignore_list = []

            elif key in ENABLE_UNFAULT_UNIGNORE_UNFAULT_KEY.keys():
                try:
                    q_fault_index = ENABLE_UNFAULT_UNIGNORE_UNFAULT_KEY[key]
                    sw.enable(str(fault_list[q_fault_index]))
                    sw.unfault(bot_info[fault_list[q_fault_index]]["id"])
                    fault_list.pop(q_fault_index)
                except Exception as e:
                    print(color["Fault"] + str(e))
                    append_to_file(cwd, "exception.txt", e)

            elif key in ENABLE_UNFAULT_UNIGNORE_IGNORE_KEY:
                try:
                    q_ignore_index = int(chr(ord(key)))
                    if q_ignore_index == 0:
                        q_ignore_index = 10
                    else:
                        q_ignore_index = q_ignore_index - 1
                    sw.enable(str(ignore_list[q_ignore_index]))
                    sw.unfault(bot_info[ignore_list[q_ignore_index]]["id"])
                    ignore_list.pop(q_ignore_index)
                except Exception as e:
                    print(color["Fault"] + str(e))
                    append_to_file(cwd, "exception.txt", e)

            elif key in EXIT_KEY:
                pause_all_thread = True
                time.sleep(1)
                cf = input("Exit program? (Y/N) >> ")
                if cf.upper() == "Y":
                    pause_all_thread = False
                    terminate_thread = True
                else:
                    pause_all_thread = False
                # terminate_thread = True
        if keep_windows_from_lock == True:
            time_now = datetime.datetime.strptime(time.ctime(), "%c")
            if (time_now - time_ref).total_seconds() >= SCREEN_UP_CYCLE:
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
    pass
