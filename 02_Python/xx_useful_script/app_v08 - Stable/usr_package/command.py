import datetime
import pytz
import threading

from usr_package import fw
from usr_package import sw
from usr_package import field
from usr_package import print_alert
from colorama import Fore

success = [0, 200, 202, 204]

info = {
    "IP":       0,
    "Status":   1,
    "Axis":     2,
    "Pod":      3,
    "Battery":  4,
    "ID":       5,
    "Location": 6
}

warehouse = "Elgin"

def init(config):
    global cmd_url
    global rq_timeout
    global warehouse
    if config == 0:
        fw.init(0)
        sw.init(0)
        return 0
    try:
        warehouse = config["sw"]["warehouse"]
        fw.init(config["fw"])
        sw.init(config["sw"])
    except:
        print("Default - Elgin")

def bot_fix(bot, bot_info):
    response = sw.enable(bot)
    if response in success:
        print(Fore.GREEN + f"{bot: <3}| Bot is reconnected!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Reconnect Error..." + " | " + str(response))

    if warehouse == "Elgin":
        response = sw.unpause(bot)
    elif warehouse == "Atlanta":
        # Check estop:
        estop_stt = sw.estop_status()
        if estop_stt[0] == False:
            response = sw.unpause(bot)
        else:
            response = ('Field is estopped, can not unpause', 998)
    if response[1] in success and len(response[0]) == 0:
        print(Fore.GREEN + f"{bot: <3}| Unpause Successfully!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Unpause: " + response[0] + " | " + str(response[1]))

    response = sw.unfault(bot_info[int(bot)][info["ID"]])
    if response[1] in success and len(response[0]) == 0:
        print(Fore.GREEN + f"{bot: <3}| Unfault/Requests Successfully!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Unfault: " + response[0] + " | " + str(response[1]))

    response = sw.retry(bot_info[int(bot)][info["ID"]])
    if response in success:
        print(Fore.GREEN + f"{bot: <3}| Retry Successfully!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Retry Error..." + " | " + str(response))

def global_bot_fix_all_faulted(bot_info):
    confirm = input("       Enable, unpause, unfault, retry all faulted bots? (Y/N):")
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        for bot, data in bot_info.items():
            if data[info["Status"]] == "Fault":
                bot_fix(bot, bot_info)
        print(Fore.GREEN + "Fix all > finished")

def global_unpause_all_pause(pause_list):
    if len(pause_list) == 0:
        print(Fore.YELLOW + "There aren't any paused bot")
        return -1
    confirm = input("       Retry last command for all idle bots? (Y/N):")
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        for bot in pause_list:
            response = sw.unpause(str(bot))
            if response[1] in success and len(response[0]) == 0:
                print(Fore.GREEN + f"{bot: <3}| Unpause Successfully!!!")
            else:
                print(Fore.YELLOW + f"{bot: <3}| Unpause: " + response[0] + " | " + str(response[1]))
            print(Fore.GREEN + "Unpause all > finished")

def global_retry_idle(idle_list, bot_info):
    if len(idle_list) == 0:
        print(Fore.YELLOW + "There aren't any idle bot")
        return -1
    confirm = input("       Retry last command for all idle bots? (Y/N):")
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        for bot in idle_list:
            response = sw.retry(bot_info[bot][info["ID"]])
            if response in success:
                print(Fore.GREEN + f"{bot: <3}: Retry Successfully!!!")
            else:
                print(Fore.YELLOW + f"{bot: <3}: Retry Error..." + str(response))
        print(Fore.GREEN + "Retry all > finished")

def global_unfault_all_fault(bot_info):
    confirm = input("       Unfault all faulted bots? (Y/N):")
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        for bot, data in bot_info.items():
            if data[info["Status"]] == "Fault":
                response = sw.unfault(bot_info[bot][info["ID"]])
                if response[1] in success and len(response[0]) == 0:
                    print(Fore.GREEN + f"{bot: <3}| Unfault/Requests Successfully!!!")
                else:
                    print(Fore.YELLOW + + f"{bot: <3}| Unfault: " + response[0] + " | " + str(response[1]))
        print(Fore.GREEN + "Unfault all > finished")

def global_power_cycle_all_bots(bot_info):
    confirm = input("       Power cycle all bots? (Y/N):")
    custom_ignore = []
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        print("       All bots will be power cycle, except bots at Charger, Maintenance and new FW (M4) bot")
        while confirm.upper() != 'Q':
            confirm = input("       Add a bot you also don't want to be power cycled (Q - quit): ")
            if confirm.isdigit() == True:
                custom_ignore.append(int(confirm))

        confirm = input("       Power cycle new FW (M4) (Y/N): ")
        if confirm.upper() == "Y":
            decide = "Yes"
        else:
            decide = "No"

        for bot, data in bot_info.items():
            if (data[info["Location"]] not in ["Charger", "Maintenance"]) and (bot not in custom_ignore):
                try:
                    t = threading.Thread(target = fw.power_cycle_with_check, args = (data[info["IP"]], bot, decide))
                    # t = threading.Thread(target = fw.get_fw_type, args = (data[info["IP"]], bot))
                    t.start()
                except:
                    print(f"Can't create a thread to power cycle bot {bot}")
            else:
                print_alert.print_a_bot_info(bot_info[int(bot)], 'Information', int(bot))

def global_check_fw(bot_info):
    for bot, data in bot_info.items():
        try:
            t = threading.Thread(target = fw.print_fw_new, args = (data[info["IP"]], bot))
            t.start()
        except:
            print(f"Can't create a thread to power cycle bot {bot}")

def help_menu():
    print(f"{' QUERY MODE ':=^80}")
    print(f"{'':=<8}{'  C': <10}: {'Enter command mode': <52}{'':=<8}")
    print(f"{'':=<8}{'  J': <10}: {'Quick ignore fault bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  K': <10}: {'Quick ignore connection bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  L': <10}: {'Quick ignore pause bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  F': <10}: {'Show/Hide field (hide Available, Charging)': <52}{'':=<8}")
    print(f"{'':=<8}{'  Q': <10}: {'Quit program': <52}{'':=<8}")
    print(f"{' COMMAND MODE ':=^80}")
    print(f"{' FW ':-^80}")
    print(f"{'':=<8}{'  RST': <10}: {'Restart firmware of a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  KILL': <10}: {'Kill firmware': <52}{'':=<8}")
    print(f"{'':=<8}{'  PWR': <10}: {'Power cycle a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  WTCL': <10}: {'Get a robot log (q - quit - Not recommend)': <52}{'':=<8}")
    print(f"{'':=<8}{'  P71': <10}: {'Get a P71 read code': <52}{'':=<8}")
    print(f"{'':=<8}{'  LOG': <10}: {'Save log to /fw_log/<date>/BOT_<name>_<time>': <52}{'':=<8}")
    print(f"{'':=<8}{'  FWT': <10}: {'Get fw type of a robot': <52}{'':=<8}")
    print(f"{' GLOBAL FW':-^80}")
    print(f"{'':=<8}{'  GFWN': <10}: {'Get new FW (M4) bot': <52}{'':=<8}")
    print(f"{'':=<8}{'  GPWRAB': <10}: {'PWR all robot (except at Charger, Maintenance)': <52}{'':=<8}")
    print(f"{' SW ':-^80}")
    print(f"{'':=<8}{'  BUF': <10}: {'Unfault a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BRLC': <10}: {'Retry last command of a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BF': <10}: {'Enable, unpause, unfault and retry': <52}{'':=<8}")
    print(f"{'':=<8}{'  BUP': <10}: {'Unpause a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BE': <10}: {'Enable/Reconnect a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BD': <10}: {'Disable/Disconnect a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BIG': <10}: {'Ignore a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BUIG': <10}: {'Un-Ignore a robot': <52}{'':=<8}")
    print(f"{'':=<8}{'  BINF': <10}: {'Show information of a robot': <52}{'':=<8}")
    print(f"{' GLOBAL SW':-^80}")
    print(f"{'':=<8}{'  GBUPAP': <10}: {'BUP all paused bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  GBRLCI': <10}: {'BRLC all idle bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  GBUFAF': <10}: {'BUF all faulted bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  GBFAF': <10}: {'BF all faulted bots': <52}{'':=<8}")
    print(f"{'':=<8}{'  F': <10}: {'Show field (hide Available, Charging)': <52}{'':=<8}")
    print(f"{'':=<8}{'  H': <10}: {'Help': <52}{'':=<8}")
    print(f"{'':=<8}{'  Q': <10}: {'Quit': <52}{'':=<8}")
    print("Example: BUF 10: unfault bot 10")
    print("Example: BUF 10 20 30: unfault bot 10, 20, 30")
    print("!!!!!! At present, I only develop 1 commands/input")

def execute_cmd(bot_info, location, idle_list, pause_list, ignore_list, cwd):

    print(f"\n{' Command mode (H - Help, Q - Quit) ':=^80}")

    while True:
        action = input('>> ')

        # Unfault
        if action.upper() == 'Q':
            break
        elif action.upper() == 'H':
            help_menu()
        elif action.upper() == "GFWN":
            global_check_fw(bot_info)
        elif action.upper() == 'F':
            if warehouse == "Elgin":
                field.print_field(bot_info)
            elif warehouse == "Atlanta":
                print(Fore.RED + "Do not have function to print field in Atlanta, warehouse is too large")
        elif action.upper() == 'GPWRAB':
            global_power_cycle_all_bots(bot_info)
        elif action.upper() == 'GBUPAP':
            global_unpause_all_pause(pause_list)
        elif action.upper() == 'GBRLCI':
            global_retry_idle(idle_list, bot_info)
        elif action.upper() == "GBUFAF":
            global_unfault_all_fault(bot_info)
        elif action.upper() == "GBFAF":
            global_bot_fix_all_faulted(bot_info)
        else:
            # Parse and execute
            split_cmd = action.split(' ')
            for bot in split_cmd[1:]:
                if bot.isdigit() == False:
                    print(Fore.RED + f'Bot {bot} does not exist')
                    continue
                elif int(bot) not in bot_info.keys():
                    print(Fore.RED + f'Bot {bot} does not exist')
                    continue
                # FW ---------------------------------------------------------------------
                # Restart fw
                if split_cmd[0].upper() == "RST":
                    response = fw.restart_fw(bot_info[int(bot)][info["IP"]])
                    if response[1] in success:
                        print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                    else:
                        print(Fore.CYAN + f"{response[0]}")
                # Power cycle
                elif split_cmd[0].upper() == "PWR":
                    response = fw.power_cycle(bot_info[int(bot)][info["IP"]])
                    if response[1] in success:
                        print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                    else:
                        print(Fore.CYAN + f"{response[0]}")
                # Kill fw process
                elif split_cmd[0].upper() == "KILL":
                    response = fw.kill(bot_info[int(bot)][info["IP"]])
                    if response[1] in success:
                        print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                    else:
                        print(Fore.CYAN + f"{response[0]}")
                # Watch log
                elif split_cmd[0].upper() == "WTCL":
                    response = fw.wtc_live_log(bot_info[int(bot)][info["IP"]])
                    if response[1] in success:
                        print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                    else:
                        print(Fore.CYAN + f"{response[0]}")
                    break
                # Get P71 Emergency code
                elif split_cmd[0].upper() == "P71":
                    response = fw.p71_code(bot_info[int(bot)][info["IP"]])
                    print(Fore.YELLOW + f"{response}")
                # Save log
                elif split_cmd[0].upper() == "LOG":
                    # 2021-08-18T20:51:26.998694-07:00
                    iso_time_format = datetime.datetime.now(pytz.timezone('US/Pacific')).isoformat()
                    dir_date = iso_time_format[:10:]
                    dir_log = "BOT_" + str(bot) + "_" + iso_time_format[11:16:].replace(":", "")
                    log_thread = threading.Thread(target = fw.get_log, args = (bot_info[int(bot)][info["IP"]], cwd, dir_date, dir_log))
                    log_thread.start()
                elif split_cmd[0].upper() == "FWT":
                    response, val = fw.get_fw_type_v2(bot_info[int(bot)][info["IP"]], bot)
                    print(f"Bot {bot} is running {response} FW")
                # SW ---------------------------------------------------------------------
                # UNFAULT
                elif split_cmd[0].upper() == "BUF":
                    response = sw.unfault(bot_info[int(bot)][info["ID"]])
                    if response[1] in success and len(response[0]) == 0:
                        print(Fore.GREEN + f"{bot: <3}| Unfault/Requests Successfully!!!")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Unfault: " + response[0] + " | " + str(response[1]))

                # RETRY
                elif split_cmd[0].upper() == "BRLC":
                    response = sw.retry(bot_info[int(bot)][info["ID"]])
                    if response in success:
                        print(Fore.GREEN + f"{bot: <3}| Retry Successfully!!!")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Retry Error..." + " | " + str(response))

                elif split_cmd[0].upper() == "BUP":
                    if warehouse == "Elgin":
                        response = sw.unpause(bot)
                    elif warehouse == "Atlanta":
                        # Check estop:
                        estop_stt = sw.estop_status()
                        if estop_stt[0] == False:
                            response = sw.unpause(bot)
                        else:
                            response = ('Field is estopped, can not unpause', 998)
                    if response[1] in success and len(response[0]) == 0:
                        print(Fore.GREEN + f"{bot: <3}| Unpause Successfully!!!")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Unpause: " + response[0] + " | " + str(response[1]))

                elif split_cmd[0].upper() == "BE":
                    response = sw.enable(bot)
                    if response in success:
                        print(Fore.GREEN + f"{bot: <3}| Bot is reconnected!!!")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Reconnect Error..." + " | " + str(response))

                elif split_cmd[0].upper() == "BD":
                    response = sw.disable(bot)
                    if response in success:
                        print(Fore.GREEN + f"{bot: <3}| Bot is disconnected!!!")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Disconnect Error..." + " | " + str(response))

                elif split_cmd[0].upper() == "BF":
                    bot_fix(bot, bot_info)
                elif split_cmd[0].upper() == "BIG":
                    ignore_list.append(int(bot))
                    print(Fore.GREEN + f"{bot: <3}| Ignored bot {bot}")
                elif split_cmd[0].upper() == "BUIG":
                    if int(bot) in ignore_list:
                        ignore_list.remove(int(bot))
                        print(Fore.GREEN + f"{bot: <3}| Un-Ignored bot {bot}")
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Bot {bot} has never been ignored yet ...")
                elif split_cmd[0].upper() == "BINF":
                    print(f"{bot: <3}| Information")
                    print(f"{'':-^80}")
                    print_alert.print_a_bot_info(bot_info[int(bot)], 'Information', int(bot))
                    ctask = sw.task(bot_info[int(bot)][info["ID"]])
                    if ctask[1] in success:
                        print_alert.print_task(ctask[0]["tasks"], 'Information', bot)
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Get task error..." + str(ctask[1]) + " " + bot_info[int(bot)][info["ID"]])
                    print(f"{'':-^80}")
