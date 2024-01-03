import datetime
import pytz
import threading
import os
import collections
if __name__ != '__main__':
    from usr_package import fw
    from usr_package import bot_interface
    from usr_package import sw
    # from usr_package import field
    from usr_package import print_alert
    # from colorama import Fore, Back, Style
else:
    import fw
    import bot_interface
    import sw
    # import field
    import print_alert
    # from colorama import Fore, Back, Style
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

cmd_list = (
    "RST", "KILL", "PWR", "WTCL", "P71", "LOG", "FWT",
    "ENTERPWRSAVER", "EXITPWRSAVER",
    "GENTERPWRSAVER", "GEXITPWRSAVER",
    "GFWN", "GPWRAB", "GBOTDIR",
    "BUF", "BUFI", "BRLC", "BRLCI", "BF", "BFI", "BUP", "BUPI",
    "BE", "BEI", "BD", "BDI", "BIG", "BUIG", "BINF",
    "SENDCHARGE", "STOPCHARGE",
    "GBDAB", "GBEAB", "GBUPAP", "GBRLCI", "GBUFAF", "GBFAF",
    "R180CWF", "BDROTATEBE",
    "MV", "RF", "RC"
)

option_list = (
    "-U", "-I"
)

# Initialize fw and sw cmd
# config - json
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

# Get bots' direction
def global_bot_dir(bot_info, cwd, location):
    iso_time = datetime.datetime.now(pytz.timezone('US/Pacific')).isoformat()
    bot_direction_dir = cwd + "\\BOT_DIR_" + str(iso_time).replace(":",".")
    print(bot_direction_dir)
    try:
        os.mkdir(bot_direction_dir)
    except:
        print("Can not create bot_dir directory!!!")
        return -1
    for bot, data in bot_info.items():
        if data[info["Status"]] == "Available":
            bd_thread = threading.Thread(target = fw.get_bot_dir, args = (data[info["IP"]], str(bot), bot_direction_dir, data[info["Axis"]], location))
            bd_thread.start()


# Reconnect, unpause, unfault, retry for a bot
# bot - str
# bot_info - dictionary
def bot_fix(bot, bot_info):
    response = sw.enable(bot)
    if response in success:
        print(Fore.GREEN + f"{bot: <3}| Bot is reconnected!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Reconnect Error..." + " | " + str(response))

    response = sw.unpause(bot)
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

# Reconnect, unpause, unfault, retry for all faulted bots
# bot_info - dictionary
def global_bot_fix_all_faulted(bot_info):
    for bot, data in bot_info.items():
        if data[info["Status"]] == "Fault":
            bfaf_thread = threading.Thread(target = bot_fix, args = (str(bot), bot_info))
            bfaf_thread.start()
            # bot_fix(str(bot), bot_info)

# Unpause all paused bots
# pause_list - List
def global_unpause_all_pause(pause_list):
    for bot in pause_list:
        upap_thr = threading.Thread(target = sw.unpause, args = (str(bot),))
        upap_thr.start()
    print(Fore.GREEN + "Unpause all > finished")

# Retry last cmd for all idle bots
# idle_list - List
# bot_info - dictionary
def global_retry_idle(idle_list, bot_info):
    for bot in idle_list:
        ri_thr = threading.Thread(target = sw.retry, args = (bot_info[bot][info["ID"]],))
        ri_thr.start()
    print(Fore.GREEN + "Retry all > finished")

# Unfault all faulted bots
# bot_info - dictionary
def global_unfault_all_fault(bot_info):
    for bot, data in bot_info.items():
        if data[info["Status"]] == "Fault":
            ufaf_thr = threading.Thread(target = sw.unfault, args = (bot_info[bot][info["ID"]],))
            ufaf_thr.start()
    print(Fore.GREEN + "Unfault all > finished")

# Power cycle all bots with condition (not in charger, maintenance, M4, ...)
# bot_info - dictionary
def global_power_cycle_all_bots(bot_info):
    confirm = input("       Power cycle all bots? (Y/N):")
    custom_ignore = []
    if confirm.upper() == 'N':
        print(Fore.YELLOW + "   >> Cancelled")
        return -1
    elif confirm.upper() == 'Y':
        print("       All bots will be power cycle, except bots at Charger, Maintenance")
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
                    pwrab_thr = threading.Thread(target = fw.power_cycle_with_check, args = (data[info["IP"]], bot, decide))
                    pwrab_thr.start()
                except:
                    print(f"Can't create a thread to power cycle bot {bot}")
            else:
                print_alert.print_a_bot_info(bot_info[int(bot)], 'Information', int(bot))

def global_bot_disconnect(bot_info):
    for bot in bot_info.keys():
        try:
            bdab_thr = threading.Thread(target = sw.disable, args = (str(bot),))
            bdab_thr.start()
        except:
            print(f"Can't create a thread to disconnect bot {bot}")

def global_bot_reconnect(bot_info):
    for bot in bot_info.keys():
        try:
            beab_thr = threading.Thread(target = sw.enable, args = (str(bot),))
            beab_thr.start()
        except:
            print(f"Can't create a thread to reconnect bot {bot}")

# def global_check_fw(bot_info):
#     for bot, data in bot_info.items():
#         try:
#             t = threading.Thread(target = fw.print_fw_new, args = (data[info["IP"]], bot))
#             t.start()
#         except:
#             print(f"Can't create a thread to check fw of bot {bot}")

def help_menu():
    print(Fore.GREEN + f"{' QUERY MODE ':=^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  C': <18}: {'Enter command mode': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  J': <18}: {'Quick ignore fault bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  K': <18}: {'Quick ignore connection bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  L': <18}: {'Quick ignore pause bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  U': <18}: {'Quick un-ignore all ignored bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  Shift + [1 > 0]': <18}: {'Quick enable, unfault bot in fault_list': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  [1 > 0]': <18}: {'Quick enable, unfault bot in ignored_list': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  F': <18}: {'Show/Hide field (hide Available, Charging)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  Q': <18}: {'Quit program': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{' COMMAND MODE ':=^80}")
    # print(Fore.GREEN + f"{' FW ':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' FW ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  RST': <18}: {'Restart firmware of a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  KILL': <18}: {'Kill firmware': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  PWR': <18}: {'Power cycle a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  WTCL': <18}: {'Get a robot log (q - quit - Not recommend)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  P71': <18}: {'Get a P71 read code': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  LOG': <18}: {'Save log to /fw_log/<date>/BOT_<name>_<time>': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  FWT': <18}: {'Get fw type (M4/old)': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' GLOBAL FW':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' GLOBAL FW ':-^74}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GFWN': <18}: {'Get new FW (M4) bot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GPWRAB': <18}: {'PWR all robot (except at Charger, Maintenance)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBORDIR': <18}: {'Get direction of all available robots': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' SW ':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' SW ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BD': <18}: {'Disable/Disconnect a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BE': <18}: {'Enable/Reconnect a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BUF': <18}: {'Unfault a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BRLC': <18}: {'Retry last command of a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BF': <18}: {'Enable, unpause, unfault and retry': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BUP': <18}: {'Unpause a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BIG': <18}: {'Ignore a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BUIG': <18}: {'Un-Ignore a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BINF': <18}: {'Show information of a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  SENDCHARGE': <18}: {'SW - Send bot to a random charger': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  STOPCHARGE': <18}: {'SW - Stop a bot from charging': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' GLOBAL SW':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' GLOBAL SW ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBDAB': <18}: {'BD all paused bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBEAB': <18}: {'BE all paused bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBUPAP': <18}: {'BUP all paused bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBRLCI': <18}: {'BRLC all idle bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBUFAF': <18}: {'BUF all faulted bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GBFAF': <18}: {'BF all faulted bots': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  F': <18}: {'Show field (hide Available, Charging)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  H': <18}: {'Help': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  Q': <18}: {'Quit': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' OPTION':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' OPTION ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  -U': <18}: {'Execute and un-ignore the following bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  -I': <18}: {'Execute and ignore the following bots (NIY)': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' DEBUG':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' DEBUG ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  MV': <18}: {'Move bot. e.x: MV 192 F 0.03': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  RC': <18}: {'Read ceiling': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  RF': <18}: {'Read floor': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' FOR SOME PURPOSES':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' FOR SOME PURPOSES ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  R180CWF': <18}: {'Rotate 180CW, read floor': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BDROTATEBE': <18}: {'Disconnect, rotate 180, reconnect': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  ENTERPWRSAVER': <18}: {'Enter power saver mode (need disconnect from SW)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  EXITPWRSAVER': <18}: {'Exit power saver mode (need disconnect from SW)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GENTERPWRSAVER': <18}: {'Enter power saver mode all bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + '\033[1m' + f"{'  GEXITPWRSAVER': <18}: {'Exit power saver mode all bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=^80}")
    print("Example: BUF 10: unfault bot 10")
    print("Example: BUF 10 20 30: unfault bot 10, 20, 30")

def execute_cmd(bot_info, location, idle_list, pause_list, ignore_list, cwd):

    print(f"\n{' Command mode (H - Help, Q - Quit) ':=^80}")

    while True:

        action = input('>> ')

        # Unfault
        if action.upper() == 'Q':
            break
        elif action.upper() == 'H':
            help_menu()
        # elif action.upper() == 'F':
        #     if warehouse == "Elgin":
        #         field.print_field(bot_info)
        #     elif warehouse == "Atlanta":
        #         print(Fore.RED + "Do not have function to print field in Atlanta, warehouse is too large")
        else:
            # Parse and execute
            split_cmd = action.split(' ')
            if split_cmd[0].upper() not in cmd_list:
                print(Fore.RED + f"Command {split_cmd[0].upper()} is INVALID")
                continue

            if split_cmd[0].upper() == "GBOTDIR":
                global_bot_dir(bot_info, cwd, location)
                continue
            # elif split_cmd[0].upper() == "GFWN":
            #     global_check_fw(bot_info)
            #     continue
            elif split_cmd[0].upper() == "GBDAB":
                global_bot_disconnect(bot_info)
                continue
            elif split_cmd[0].upper() == "GBEAB":
                global_bot_reconnect(bot_info)
                continue
            elif split_cmd[0].upper() == 'GPWRAB':
                global_power_cycle_all_bots(bot_info)
                continue
            elif split_cmd[0].upper() == 'GBUPAP':
                global_unpause_all_pause(pause_list)
                continue
            elif split_cmd[0].upper() == 'GBRLCI':
                global_retry_idle(idle_list, bot_info)
                continue
            elif split_cmd[0].upper() == "GBUFAF":
                global_unfault_all_fault(bot_info)
                continue
            elif split_cmd[0].upper() == "GBFAF":
                global_bot_fix_all_faulted(bot_info)
                continue
            elif split_cmd[0].upper() == "GENTERPWRSAVER":
                counter = 0
                for bot in bot_info.keys():
                    sw.enter_sleep_mode(bot_info[bot][info["IP"]])
                    counter = counter + 1
                    print(str(counter) + " - " + str(bot))
                continue
            elif split_cmd[0].upper() == "GEXITPWRSAVER":
                counter = 0
                od = collections.OrderedDict(sorted(bot_info.items()))
                for bot in od.keys():
                    sw.exit_sleep_mode(od[bot][info["IP"]])
                    counter = counter + 1
                    print(str(counter) + " - " + str(bot))
                continue

            # Disconnect, ask, rotate, reconnect ------------------------------
            elif split_cmd[0].upper() == "BDROTATEBE":
                # Disconnect
                try:
                    for bot in split_cmd[1:]:
                        bdrtbd_thr = threading.Thread(target = sw.disable, args = (str(bot),))
                        bdrtbd_thr.start()
                except Exception as e:
                    print(Fore.RED + str(e))

                # Ask to rotate
                try:
                    cf = input("Execute rotate? (Y/N) >> ")
                    if cf.upper() != "Y":
                        # Do nothing if cf not is Y
                        pass
                    else:
                        for bot in split_cmd[1:]:
                            rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])
                            if rotate_value == -1:
                                rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])
                                if rotate_value == -1:
                                    rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])
                                    if rotate_value == -1:
                                        rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])
                            print(Fore.GREEN + str(bot) + " - " + str(rotate_msg))
                except Exception as e:
                    print(Fore.RED + str(e))


                try:
                    for bot in split_cmd[1:]:
                        be_thr = threading.Thread(target = sw.enable, args = (str(bot),))
                        be_thr.start()
                except Exception as e:
                    print(Fore.RED + str(e))
                continue
            # -----------------------------------------------------------------

            elif split_cmd[0].upper() == "SENDCHARGE":
                for bot in split_cmd[1:]:
                    send_to_charger_thread = threading.Thread(target = sw.send_bot_to_charger, args = (bot_info[int(bot)][info["ID"]],))
                    send_to_charger_thread.start()
                continue

            elif split_cmd[0].upper() == "STOPCHARGE":
                for bot in split_cmd[1:]:
                    stop_charge_thread = threading.Thread(target = sw.stop_bot_charging, args = (bot_info[int(bot)][info["ID"]],))
                    stop_charge_thread.start()
                continue

            # Check un-ignore option
            if "-u" in split_cmd or "-U" in split_cmd:
                for bot in split_cmd[1:]:
                    if bot.upper() in option_list:
                        continue
                    try:
                        if int(bot) in ignore_list:
                            ignore_list.remove(int(bot))
                            print(Fore.GREEN + f"{bot: <3}| Un-Ignored bot {bot}")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Bot {bot} has never been ignored yet ...")
                    except:
                        print(Fore.YELLOW + f"{bot: <3}| Bot {bot} is INVALID ...")

            # Check ignore option
            # if "-i" in split_cmd or "-I" in split_cmd:
            #     for bot in split_cmd[1:]:
            #         if bot.upper() in option_list:
            #             continue
            #         try:
            #             if int(bot) in ignore_list:
            #                 print(Fore.YELLOW + f"{bot: <3}| Already ignored {bot}")
            #             else:
            #                 ignore_list.append(int(bot))
            #                 print(Fore.GREEN + f"{bot: <3}| Ignored bot {bot}")
            #         except:
            #             print(Fore.YELLOW + f"{bot: <3}| Bot {bot} is INVALID ...")

            # Debug cmd MV, RC, RF

            if split_cmd[0].upper() == "MV":
                if len(split_cmd) != 4:
                    print(Fore.YELLOW + f"MV - numbers of argument is INVALID")
                    print(f"e.x: MV 192 F 0.03")
                else:
                    try:
                        bot_interface.debug_move(bot_info[int(split_cmd[1])][info["IP"]], split_cmd[2], split_cmd[3])
                    except Exception as e:
                        print(Fore.RED + str(e))
                        time.sleep(2)
                continue
            elif split_cmd[0].upper() == "RC":
                try:
                    bot_interface.read_ceiling(bot_info[int(split_cmd[1])][info["IP"]])
                except Exception as e:
                    print(Fore.RED + str(e))
                    time.sleep(2)
                continue
            elif split_cmd[0].upper() == "RF":
                try:
                    bot_interface.read_floor(bot_info[int(split_cmd[1])][info["IP"]])
                except Exception as e:
                    print(Fore.RED + str(e))
                    time.sleep(2)
                continue

            for bot in split_cmd[1:]:
                if bot.upper() in option_list:
                    continue

                if bot.isdigit() == False:
                    print(Fore.RED + f'Bot {bot} does NOT exist')
                    continue
                elif int(bot) not in bot_info.keys():
                    print(Fore.RED + f'Bot {bot} does NOT exist')
                    continue
                # FW ---------------------------------------------------------------------
                # Restart fw
                elif split_cmd[0].upper() == "RST":
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
                    response = sw.unpause(bot)
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
                    if int(bot) in ignore_list:
                        print(Fore.YELLOW + f"{bot: <3}| Already ignored {bot}")
                    else:
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
                    # print(f"Bot {bot}'s ID: " + {bot_info[int(bot)][info["ID"]]})
                    try:
                        print(f"Bot {bot}'s ID: " + bot_info[int(bot)][info["ID"]])
                    except:
                        print("No ID")
                    ctask = sw.task(bot_info[int(bot)][info["ID"]])
                    if ctask[1] in success:
                        print_alert.print_task(ctask[0]["tasks"], 'Information', bot)
                    else:
                        print(Fore.YELLOW + f"{bot: <3}| Get task error..." + str(ctask[1]) + " " + bot_info[int(bot)][info["ID"]])
                    print(f"{'':-^80}")


                # Test cmd
                elif split_cmd[0].upper() == "R180CWF":
                    rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])
                    print(rotate_msg)

                # elif split_cmd[0].upper() == "BDROTATEBE":
                #     bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])

                elif split_cmd[0].upper() == "ENTERPWRSAVER":
                    txt, txt2 = sw.enter_sleep_mode(bot_info[int(bot)][info["IP"]])
                    print(txt)
                    print(txt2)

                elif split_cmd[0].upper() == "EXITPWRSAVER":
                    tuple_4 = sw.exit_sleep_mode(bot_info[int(bot)][info["IP"]])
                    print(tuple_4[0])
                    print(tuple_4[1])
                    print(tuple_4[2])
                    print(tuple_4[3])
                # --------------------------------END Test

if __name__ == '__main__':
    # import colorama
    # colorama.init(autoreset = True)
    # help_menu()
    from colorama import init, Fore, Style
    init(autoreset=True)
    print(Fore.RED + 'some red text')
    print(Fore.BLUE + 'some red text')
    print(Fore.CYAN + 'some red text')
    print(Style.BRIGHT + Fore.RED + 'some bright red text')
    print(Style.BRIGHT + Fore.BLUE + 'some bright red text')
    print(Style.BRIGHT + Fore.CYAN + 'some bright red text')
    print(Style.BRIGHT + Fore.MAGENTA + 'some bright red text')
    pass