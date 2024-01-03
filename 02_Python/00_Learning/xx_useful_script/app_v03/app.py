# Get and load json
import json
import requests

# Os cmd
import os

# Time
import time
import datetime

# Catch key
import msvcrt

# Multithreading and signal
import threading
import signal

# User package
import print_alert
import var
import command

from collections import defaultdict
from colorama import init

# Field location: x-y:'Location'
field_location = defaultdict(lambda: 0)

bot_list = []
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
bot_print_ready = False

bot_live_json = {}

lock = threading.Lock()

def bot_live_update():
    global field_location
    global bot_list
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global terminate_thread
    global pause_all_thread
    global bot_print_ready

    global bot_live_pause

    global bot_live_json

    connect_err = 0
    connection_new = []
    connection_dict_old = defaultdict(lambda: 0)
    connection_dict_old[0] = 0

    while True:

        bot_list_temp = []
        charging_list_temp = []
        idle_list_temp = []
        pause_list_temp = []
        fault_list_temp = []
        connection_list_temp = []

        # Query bot, connection -------------------------------------------------------------------------------

        try:
            bot_rsp = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/liveUpdates')
            con_rsp = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/bots/connected')
        except:
            connect_err += 1
            print(f"!!!Query Error!!! Retrying ... <{connect_err:.>5}>")
            if connect_err == 30:
                print('Exceptions has happened too much... Program ended!!!')
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
        total_bot_in_field = len(bot_live_json[var.bot])

        # Parse bot -------------------------------------------------------------------------------

        for index in range(total_bot_in_field):
            bot_list_temp.append(int(bot_live_json[var.bot][index][var.botName]))
            if bot_live_json[var.bot][index][var.botName] in ignore_list:
                continue
            if var.botStatus_dict[bot_live_json[var.bot][index][var.status]] == 'N/A 7':
                print_alert.print_a_bot_info(bot_live_json[var.bot][index], 'N/A 7')
            # Get fault
            if var.botStatus_dict[bot_live_json[var.bot][index][var.status]] == 'Fault':
                if bot_live_json[var.bot][index][var.botName]:
                    fault_list_temp.append(index)
            # Get other status if not fault
            else:
                # Get pause
                if bot_live_json[var.bot][index][var.isPaused] == True:
                    pause_list_temp.append(index)

                # Get charge
                if bot_live_json[var.bot][index][var.chargerLevel] < 40:
                    charging_list_temp.append(index)

                # Get idle
        # Parse Connection -------------------------------------------------------------------------------

        if len(bot_connection_json['connectedBots']) == len(bot_list_temp):
            # Clear temp data
            connection_dict_old = defaultdict(lambda: 0)
            connection_dict_old[0] = 0
        else:
            # Get new bot
            time_now = datetime.datetime.strptime(time.ctime(), "%c")
            bot_set = set(bot_list)
            connection_set = set(bot_connection_json['connectedBots'])
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
                if int((time_now - value).total_seconds()) >= 30:
                    if str(key) not in ignore_list:
                        connection_list_temp.append(key)

        # Print -------------------------------------------------------------------------------
        # print(ignore_list)
        # Wait to print complete
        lock.acquire()
        bot_list = bot_list_temp
        charging_list = charging_list_temp
        idle_list = idle_list_temp
        pause_list = pause_list_temp
        fault_list = fault_list_temp
        connection_list = connection_list_temp
        lock.release()
        time.sleep(1)
        if terminate_thread == True:
            break
        while pause_all_thread == True:
            bot_live_pause = True
            time.sleep(1)
        bot_live_pause = False
    print('Bot live ended!!!')

# def bot_idle_predict():

#     global idle_list

#     global bot_live_json

#     while True:

#     # Get all bot location

#     # Check if new == old
#     # False > update time

#     # Check if Current - last time >= 60s
#     # True > show


#         if terminate_thread == True:
#             break
#         while pause_all_thread == True:
#             bot_live_pause = True
#             time.sleep(1)
#         bot_live_pause = False
#     print('Bot idle ended!!!')

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
        lock.acquire()
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

        lock.release()
        time.sleep(1)
        if terminate_thread == True:
                break
        a = 1
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

    init(autoreset = True)
    # Init signal handler
    signal.signal(signal.SIGINT, signal_handler)

    location_err = 0
    print("Initializing ...")
    while True:
        try:
            json_response = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/Field')
            print("...")
        except:
            location_err += 1
            print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
            if location_err == 30:
                print('Exceptions has happened too much... Program ended!!!')
                os._exit(1)
                break
            time.sleep(1)
        else:
            print("...")
            field_json = json_response.json()
            for a_list in field_json['layout']:
                for element in a_list:
                    if element != None:
                        location_str = str(int(element['location']['x'])) + '-' + str(int(element['location']['y']))
                        field_location[location_str] = var.map_dict[element['nodeType']]
            break

    print("Initialized")

    # Create and start bot_live_update thread
    thread_bot_live_update = threading.Thread(target = bot_live_update, args = ())
    thread_bot_live_update.start()
    thread_print_status = threading.Thread(target = print_status, args = ())
    thread_print_status.start()
    key = 0

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if ord(key) == ord('c'):
                pause_all_thread = True
                while bot_live_pause == False or bot_print_pause == False:
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
