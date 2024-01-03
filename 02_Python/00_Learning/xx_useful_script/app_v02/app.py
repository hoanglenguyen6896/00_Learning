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

bot_live_json = {}

def bot_live_update():
    global bot_list
    global charging_list
    global idle_list
    global pause_list
    global fault_list
    global ignore_list
    global connection_list

    global terminate_thread
    global pause_all_thread

    global bot_live_pause

    global bot_live_json

    connect_err = 0
    connection_new = []
    connection_dict_old = defaultdict(lambda: 0)
    connection_dict_old[0] = 0

    while True:
        bot_list = []
        charging_list = []
        idle_list = []
        pause_list = []
        fault_list = []
        connection_list = []

        # Query bot, connection -------------------------------------------------------------------------------

        try:
            bot_rsp = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/liveUpdates')
            con_rsp = requests.get('https://wes-agv-portal-gateway.iherbscs.net/api/bots/connected')
        except:
            os.system('cls')
            connect_err += 1
            print(f"!!!Query Error!!! Retrying ... <{connect_err:.>5}>")
            if connect_err == 30:
                print('Network Ended ...')
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
            bot_list.append(int(bot_live_json[var.bot][index][var.botName]))
            if var.botStatus_dict[bot_live_json[var.bot][index][var.status]] == 'N/A 7':
                print_alert.print_a_bot_info(bot_live_json[var.bot][index], 'N/A 7')
            # Get fault
            if var.botStatus_dict[bot_live_json[var.bot][index][var.status]] == 'Fault':
                if bot_live_json[var.bot][index][var.botName] not in ignore_list:
                    fault_list.append(index)
            # Get other status if not fault
            else:
                # Get pause
                if bot_live_json[var.bot][index][var.isPaused] == True:
                    pause_list.append(index)

                # Get charge
                if bot_live_json[var.bot][index][var.chargerLevel] < 40:
                    charging_list.append(index)
                # Get idle


        # Parse Connection -------------------------------------------------------------------------------

        if len(bot_connection_json['connectedBots']) == len(bot_list):
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
                    connection_list.append(key)

        # Print -------------------------------------------------------------------------------
        os.system("cls")
        print(f"Tool is still running + {time.ctime()}... !!!")
        # Show ignore
        print_alert.print_with_alert(bot_live_json, ignore_list, 'Ignore')
        # Show pause
        print_alert.print_with_alert(bot_live_json, pause_list, 'Pause')
        # Show charging
        print_alert.print_with_alert(bot_live_json, charging_list, 'Charging')
        # Show idle
        print_alert.print_with_alert(bot_live_json, idle_list, 'Idle')
        # Show connection
        print_alert.print_with_alert(bot_live_json, connection_list, 'Connection')
        # Show fault
        print_alert.print_with_alert(bot_live_json, fault_list, 'Fault')

        if terminate_thread == True:
            break
        while pause_all_thread == True:
            bot_live_pause = True
            time.sleep(1)
        bot_live_pause = False
    print('Bot live ended!!!')

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

    resume_thread = 0

    # Create and start bot_live_update thread
    thread_bot_live_update = threading.Thread(target = bot_live_update, args = ())
    thread_bot_live_update.start()
    key = 0
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if ord(key) == ord('c'):
                pause_all_thread = True
                while bot_live_pause == False:
                    time.sleep(1)
                if bot_live_json == {}:
                    print("You haven't haven any data to use command mode!!!")
                    pause_all_thread = False
                else:
                    resume_thread = command.execute_cmd(bot_live_json, ignore_list)
                    if resume_thread == 1:
                        pause_all_thread = False
                        resume_thread = 0
            elif ord(key) == ord('q'):
                terminate_thread = True
        if terminate_thread == False:
            time.sleep(1)
        else:
            breakq
