# Get and load json
import json
import requests

# Os cmd
import os
import sys

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
from usr_package import var
from usr_package import command

from collections import defaultdict
import colorama

url_query = {
    "bot_live": "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/liveUpdates",
    "connect":  "https://wes-agv-portal-gateway.iherbscs.net/api/bots/connected",
    "estop":    "https://wes-agv-portal-gateway.iherbscs.net/api/bots/emergencystop"
}

battery_limit = 40
idle_time_limit = 60
connection_time_limit = 30

idle_location_reference = ['Charger', 'Queue', 'Queue In' ,'Maintenance']
idle_status_reference = ['Busy']

# Field location: x-y:'Location'
field_location = defaultdict(lambda: 0)

# Bot location: (botname):x-y
bot_location_temp = defaultdict(lambda: 0)
bot_location = {}

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

bot_live_json = {}
estop_json = {}



def init(limit, refer, url):
    global battery_limit
    global idle_time_limit
    global connection_time_limit

    global idle_location_reference
    global idle_status_reference
    global url_query

    if limit == refer == url == 0:
        print("Default ...")
    else:
        try:
            battery_limit = limit['bat_lvl']
            idle_time_limit = limit['idle_time']
            connection_time_limit = limit['connection_time']
            idle_location_reference = refer['location_idle']
            idle_status_reference = refer['status_idle']
            if url['warehouse'] == "Elgin":
                url_query = url["Elgin"]["query"]
            elif url['warehouse'] == "Atlanta":
                url_query = url["Atlanta"]["query"]
            print("Loading url ...")
        except:
            print(var.color_for_txt['Fault'] + "Failed to load configuration file, using default configuration for Elgin")
            print("Default ...")

def bot_live_update():
    global field_location
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global bot_location

    global terminate_thread
    global pause_all_thread
    global bot_print_ready

    global bot_live_pause

    global bot_live_json

    global battery_limit
    global connection_time_limit

    connect_err = 0
    connection_new = []
    connection_dict_old = defaultdict(lambda: 0)
    connection_dict_old[0] = 0
    temp_list = []

    while True:
        bot_location_temp = defaultdict(lambda: 0)
        charging_list_temp = []
        pause_list_temp = []
        fault_list_temp = []
        connection_list_temp = []

        # Query bot, connection -------------------------------------------------------------------------------

        try:
            bot_rsp = requests.get(url_query["bot_live"])
            con_rsp = requests.get(url_query["connect"])
            estop_rsp = requests.get(url_query["estop"])
        except:
            connect_err += 1
            print(f"!!!Query Error!!! Retrying ... <{connect_err:.>5}>")
            if connect_err == 30:
                print(var.color_for_txt['Fault'] + 'Exceptions has happened too much... Program ended!!!')
                break
            if terminate_thread == True:
                break
            time.sleep(1)
            continue
        else:
            connect_err = 0
            pass

        bot_live_json = bot_rsp.json() # Return a dictionary
        bot_connection_json = con_rsp.json()
        estop_json = estop_rsp.json()
        total_bot_in_field = len(bot_live_json[var.bot])

        # Parse bot -------------------------------------------------------------------------------

        for index in range(total_bot_in_field):
            # bot_location_temp: botName:[ip, stt, xy, pod, bat]
            botName_temp = int(bot_live_json[var.bot][index][var.botName])
            temp_list = [bot_live_json[var.bot][index][var.botIp],\
                        var.botStatus_dict[bot_live_json[var.bot][index][var.status]],\
                        print_alert.get_location_in_xy(bot_live_json[var.bot][index][var.location]),\
                        bot_live_json[var.bot][index][var.podName],\
                        bot_live_json[var.bot][index][var.chargerLevel]]
            bot_location_temp[botName_temp] = temp_list
            temp_list = []
            if str(botName_temp) in ignore_list:
                continue
            if bot_location_temp[botName_temp][1] == 'N/A 7':
                print_alert.print_a_bot_info(bot_live_json[var.bot][index], 'N/A 7')
            # Get fault
            if bot_location_temp[botName_temp][1] == 'Fault':
                if bot_live_json[var.bot][index][var.botName]:
                    fault_list_temp.append(index)
            # Get other status if not fault
            else:
                # Get pause
                if bot_live_json[var.bot][index][var.isPaused] == True:
                    pause_list_temp.append(index)

                # Get charge
                if bot_location_temp[botName_temp][4] < battery_limit:
                    charging_list_temp.append(index)

                # Get idle
        # Parse Connection -------------------------------------------------------------------------------

        if len(bot_connection_json[var.connected]) == len(bot_location_temp.keys()):
            # Clear temp data
            connection_dict_old = defaultdict(lambda: 0)
            connection_dict_old[0] = 0
        else:
            # Get new bot
            time_now = datetime.datetime.strptime(time.ctime(), "%c")
            bot_set = set(bot_location_temp.keys())
            connection_set = set(bot_connection_json[var.connected])
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
                if int((time_now - value).total_seconds()) >= connection_time_limit:
                    if str(key) not in ignore_list:
                        connection_list_temp.append(key)

        # Print -------------------------------------------------------------------------------
        # Wait to print complete
        bot_location = bot_location_temp
        charging_list = charging_list_temp
        pause_list = pause_list_temp
        fault_list = fault_list_temp
        connection_list = connection_list_temp
        time.sleep(1)
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            bot_live_pause = True
            time.sleep(1)
        bot_live_pause = False
    print('Bot live ended!!!')

def bot_idle_predict():
    global idle_time_limit
    global bot_idle_pause

    global idle_list

    global bot_location
    global field_location

    global idle_location_reference
    global idle_status_reference

    # Bot location:     (botname):'x-y'
    # Bot old location: (botname):['x-y', time]
    bot_location_old = defaultdict(lambda: 0)

    bot_location_old[0] = ['0-0', 0]
    # > {0:['0-0',0]}

    while True:
        idle_list_temp = []
        del_list = []

        # Get all bot location
        time_now = datetime.datetime.strptime(time.ctime(), "%c")
        # Query through new bot
        for bot, new_location in bot_location.items():
            if bot in bot_location_old.keys():
                # print('bot in')
                # Check if the bot in bot_location (new) in bot_location_old or not
                if new_location[2] != bot_location_old[bot][0]:
                    # if True and location is different > update time
                    bot_location_old[bot] = [new_location[2], time_now]
                # Do nothing if True and location if the same
            else:
                # print('bot not in old ' + str(bot) + ' ' + str(new_location))
                # Add new bot if not in bot_location_old
                bot_location_old[bot] = [new_location[2] ,time_now]
        # Query through old bot to delete 'what in old, not in new'
        for bot in bot_location_old.keys():
            if bot not in bot_location.keys():
                # print('bot not in new ' + str(bot) + ' ' + str(bot_location_old[bot][0]))
                del_list.append(bot)
        for bot in del_list:
            del bot_location_old[bot]
        # print(del_list)
        # Check if Current - last time >= 60s
        for bot, data_list in bot_location_old.items():
            # int((time_now - value).total_seconds())
            if int((time_now - data_list[1]).total_seconds()) >= idle_time_limit:
                if (field_location[data_list[0]] not in idle_location_reference)\
                                    and (bot_location[bot][1] in idle_status_reference):
                    idle_list_temp.append(bot)
        # Handle when field is esstop


        idle_list = idle_list_temp
        # print(bot_location_old)
        time.sleep(1)
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            bot_idle_pause = True
            time.sleep(1)
        bot_idle_pause = False
    print('Bot idle ended!!!')

def print_status():
    global field_location
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global terminate_thread
    global pause_all_thread
    global bot_print_pause

    while True:
        os.system("cls")
        print(f"Tool is still running: {time.ctime()}")
        # Show ignore
        print_alert.print_with_alert(bot_live_json, ignore_list, 'Ignore', field_location)
        # Show pause
        print_alert.print_with_alert(bot_live_json, pause_list, 'Pause', field_location)
        # Show charging
        print_alert.print_with_alert(bot_live_json, charging_list, 'Charging', field_location)
        # Show idle
        print_alert.print_with_alert(bot_live_json, idle_list, 'Idle', field_location)
        # Show connection
        print_alert.print_with_alert(bot_live_json, connection_list, 'Connection', field_location)
        # Show fault
        print_alert.print_with_alert(bot_live_json, fault_list, 'Fault', field_location)

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

# main thread
if __name__ == "__main__":


    # Init signal handler
    signal.signal(signal.SIGINT, signal_handler)
    colorama.init(autoreset = True)
    cwd = os.getcwd()
    print("Initializing ...")
    print("Loading configuration ...")
    # Init config
    try:
        f = open(cwd + '\\config.json', 'r')
        config = json.load(f)
        print_alert.init(config['alert']['sound'], config['alert']['idle_threshold'])
        command.init(config["url"])
        init(config['limitation'], config['reference'], config['url'])
        f.close()
        print(var.color_for_txt["Success"] + "Loaded configuration!!!")
    except:
        print(var.color_for_txt['Fault'] + "Failed to load configuration file, using default configuration for Elgin")
        print_alert.init()
        command.init(0)
        init(0,0,0)
    time.sleep(1)
    print("Getting field information ...")
    # Get field information
    location_err = 0
    while True:
        try:
            json_response = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/Field')
        except:
            location_err += 1
            print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
            if location_err == 30:
                print(var.color_for_txt['Fault'] + "Exceptions has happened too much... Program ended!!!")
                os._exit(1)
                break
            time.sleep(1)
        else:
            field_json = json_response.json()
            for a_list in field_json['layout']:
                for element in a_list:
                    if element != None:
                        location_str = str(int(element['location']['x'])) + '-' + str(int(element['location']['y']))
                        field_location[location_str] = var.map_dict[element['nodeType']]
            print(var.color_for_txt["Success"] + "Field information > Done")
            time.sleep(1)
            break

    time.sleep(1)
    # Create and start some thread
    thread_bot_live_update = threading.Thread(target = bot_live_update, args = ())
    thread_bot_live_update.start()
    thread_print_status = threading.Thread(target = print_status, args = ())
    thread_print_status.start()
    thread_bot_idle_predict = threading.Thread(target = bot_idle_predict, args = ())
    thread_bot_idle_predict.start()

    key = 0
    # Catch and run command mode
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if ord(key) == ord('c'):
                pause_all_thread = True
                while bot_live_pause == False or bot_print_pause == False or bot_idle_pause == False:
                    time.sleep(1)
                if bot_live_json == {}:
                    print("You haven't haven any data to use command mode!!!")
                    pause_all_thread = False
                else:
                    command.execute_cmd(bot_live_json, ignore_list)
                    fault_list = []
                    pause_all_thread = False
            elif ord(key) == ord('q'):
                terminate_thread = True
        if terminate_thread == False:
            time.sleep(1)
        else:
            break
