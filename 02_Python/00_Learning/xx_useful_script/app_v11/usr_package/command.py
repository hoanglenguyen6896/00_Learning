from concurrent.futures import thread
import datetime
import pytz
import threading
import os
import collections
import time
if __name__ != '__main__':
    from usr_package import fw
    from usr_package import bot_interface
    from usr_package import sw
    # from usr_package import field
    from usr_package import print_alert
    from usr_package import cameraUtility
else:
    import fw
    import bot_interface
    import sw
    # import field
    import print_alert
    import cameraUtility
from colorama import Fore

success = [0, 200, 202, 204]
DIR_FW_LOG = "fw_log"
DIR_BOT_DIRECTION = "bot_direction"
DIR_BOT_CAMERA = "bot_camera"

FLOOR_CAM = "F"
CEILING_CAM = "C"
BOTH_CAM = "B"
CAM_OPT = (FLOOR_CAM, CEILING_CAM, BOTH_CAM)

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
    "BUF", "BUFI", "BRLC", "BRLCI", "BF", "BFI", "BP", "BUP", "BUPI",
    "BE", "BEI", "BD", "BDI", "BIG", "BUIG", "BINF",
    "REPLAN", "SETIDLE", "RFHMI",
    "SENDCHARGE", "STOPCHARGE",
    "GBDAB", "GBEAB", "GBUPAP", "GBRLCI", "GBUFAF", "GBFAF",
    "R180CWF", "BDROTATEBE", "BDROTATEBE2",
    "MV", "RF", "RC",
    "CAM"
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

# return cwd\\base\\para1\\para2 directory
# cwd should be current directory
def create_dir(cwd, base, para1, para2):
    if os.path.isdir(cwd + "\\" + base) == False:
        try:
            os.mkdir(cwd + "\\" + base)
        except Exception as e:
            print(Fore.RED + str(e))
            return -1
    bot_dir = cwd + "\\" + base

    if os.path.isdir(bot_dir + "\\" + para1) == False:
        try:
            os.mkdir(bot_dir + "\\" + para1)
        except Exception as e:
            print(Fore.RED + str(e))
            return -1
    bot_dir = bot_dir + "\\" + para1
    if os.path.isdir(bot_dir + "\\" + para2) == False:
        try:
            os.mkdir(bot_dir + "\\" + para2)
        except Exception as e:
            print(Fore.RED + str(e))
            return -1
    bot_dir = bot_dir + "\\" + para2
    return bot_dir

# Get bots' direction
def global_bot_dir(bot_info, cwd, location):
    iso_time = datetime.datetime.now(pytz.timezone('US/Pacific')).isoformat()
    date_dir = iso_time[:10:]
    time_dir = iso_time[11:19].replace(":",".")
    bot_dir = create_dir(cwd, DIR_BOT_DIRECTION, date_dir, time_dir)
    print(bot_dir)
    for bot, data in bot_info.items():
        if data["stt"] == "Available":
            bd_thread = threading.Thread(target = fw.get_bot_dir, args = (data["ip"], str(bot), bot_dir, data["xy"], location))
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

    response = sw.unfault(bot_info[int(bot)]["id"])
    if response[1] in success and len(response[0]) == 0:
        print(Fore.GREEN + f"{bot: <3}| Unfault/Requests Successfully!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Unfault: " + response[0] + " | " + str(response[1]))

    response = sw.retry(bot_info[int(bot)]["id"])
    if response in success:
        print(Fore.GREEN + f"{bot: <3}| Retry Successfully!!!")
    else:
        print(Fore.YELLOW + f"{bot: <3}| Retry Error..." + " | " + str(response))

# Reconnect, unpause, unfault, retry for all faulted bots
# bot_info - dictionary
def global_bot_fix_all_faulted(bot_info):
    for bot, data in bot_info.items():
        if data["stt"] == "Fault":
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
        ri_thr = threading.Thread(target = sw.retry, args = (bot_info[bot]["id"],))
        ri_thr.start()
    print(Fore.GREEN + "Retry all > finished")

# Unfault all faulted bots
# bot_info - dictionary
def global_unfault_all_fault(bot_info):
    for bot, data in bot_info.items():
        if data["stt"] == "Fault":
            ufaf_thr = threading.Thread(target = sw.unfault, args = (bot_info[bot]["id"],))
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
            if (data["loc"] not in ["Charger", "Maintenance"]) and (bot not in custom_ignore):
                try:
                    pwrab_thr = threading.Thread(target = fw.power_cycle_with_check, args = (data["ip"], bot, decide))
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

def rotate_bot_advanced(bot_ip, bot_name):
    rotate_msg = ""
    rotate_value = -1
    rotate_retry_counter = 0
    while rotate_value == -1 and rotate_retry_counter <5:
        rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_ip)
        rotate_retry_counter = rotate_retry_counter + 1
    if rotate_value == 1:
        print(Fore.GREEN + str(bot_name) + " - " + str(rotate_value))
    else:
        print(Fore.RED + str(bot_name) + " - " + str(rotate_value))

def check_threads_alive(thread_dict):
    _temp_dict = thread_dict.copy()
    # print(type(_temp_dict))
    # print(type(thread_dict))
    while len(thread_dict) != 0:
        for bot, _thread in thread_dict.items():
            if _thread.is_alive() == False:
                be_thr = threading.Thread(target = sw.enable, args = (str(bot),))
                be_thr.start()
                _temp_dict.pop(bot)
        thread_dict = _temp_dict.copy()
        time.sleep(3)

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
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  WTCL': <18}: {'Get a robot live log (q - quit - Not recommend)': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  P71': <18}: {'Get a P71 read code': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  LOG': <18}: {'Save log to /<fw_log>/<date>/BOT_<name>_<time>': <54}" + Fore.GREEN + f"{'':=<3}")
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
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BP': <18}: {'Pause a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BUP': <18}: {'Unpause a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BIG': <18}: {'Ignore a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BUIG': <18}: {'Un-Ignore a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BINF': <18}: {'Show information of a robot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  SENDCHARGE': <18}: {'SW - Send bot to a random charger': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  STOPCHARGE': <18}: {'SW - Stop a bot from charging': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  REPLAN': <18}: {'SW - Replan a bot': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  SETIDLE': <18}: {'SW - Setidle a packwall': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  RFHMI': <18}: {'SW - RefreshHMI a packwall': <54}" + Fore.GREEN + f"{'':=<3}")
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
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  CAM': <18}: {'Get camera picture. e.x: CAM 141 F/C/B': <54}" + Fore.GREEN + f"{'':=<3}")
    # print(Fore.GREEN + f"{' FOR SOME PURPOSES':-^80}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.CYAN + f"{' FOR SOME PURPOSES ':-^74}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  R180CWF': <18}: {'Rotate 180CW, read floor': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  BDROTATEBE': <18}: {'Disconnect, rotate 180, reconnect': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  ENTERPWRSAVER': <18}: {'Enter power saver mode (need disconnect from SW)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  EXITPWRSAVER': <18}: {'Exit power saver mode (need disconnect from SW)': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GENTERPWRSAVER': <18}: {'Enter power saver mode all bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=<3}" + Fore.WHITE + f"{'  GEXITPWRSAVER': <18}: {'Exit power saver mode all bots': <54}" + Fore.GREEN + f"{'':=<3}")
    print(Fore.GREEN + f"{'':=^80}")
    print("Example: BUF 10: unfault bot 10")
    print("Example: BUF 10 20 30: unfault bot 10, 20, 30")

def execute_cmd(bot_info, location, idle_list, pause_list, ignore_list, cwd, packwall_info):

    print(f"\n{' Command mode (H - Help, Q - Quit) ':=^80}")

    while True:

        action = input('>> ')

        if action.upper() == 'Q':
            break
        elif action.upper() == 'H':
            help_menu()
        else:
            # Parse and execute
            split_cmd = action.split(' ')
            upper_cmd = split_cmd[0].upper()
            para_list = split_cmd[1:]
            # Check valid cmd
            if upper_cmd not in cmd_list:
                print(Fore.RED + f"Command {upper_cmd} is INVALID")
                continue

            # Check un-ignore option
            if "-u" in split_cmd or "-U" in split_cmd:
                for bot in para_list:
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

# AS CMD -----------------------------------------------------------
            if upper_cmd == "GBOTDIR":
                global_bot_dir(bot_info, cwd, location)
            elif upper_cmd == "GBDAB":
                global_bot_disconnect(bot_info)
            elif upper_cmd == "GBEAB":
                global_bot_reconnect(bot_info)
            elif upper_cmd == 'GPWRAB':
                global_power_cycle_all_bots(bot_info)
            elif upper_cmd == 'GBUPAP':
                global_unpause_all_pause(pause_list)
            elif upper_cmd == 'GBRLCI':
                global_retry_idle(idle_list, bot_info)
            elif upper_cmd == "GBUFAF":
                global_unfault_all_fault(bot_info)
            elif upper_cmd == "GBFAF":
                global_bot_fix_all_faulted(bot_info)
            elif upper_cmd == "GENTERPWRSAVER":
                counter = 0
                od = collections.OrderedDict(sorted(bot_info.items()))
                for bot, data in od.values():
                    sw.enter_sleep_mode(data["ip"])
                    counter = counter + 1
                    print(str(counter) + " - " + str(bot))
            elif upper_cmd == "GEXITPWRSAVER":
                counter = 0
                od = collections.OrderedDict(sorted(bot_info.items()))
                for bot, data in od.values():
                    sw.exit_sleep_mode(data["ip"])
                    counter = counter + 1
                    print(str(counter) + " - " + str(bot))

            # Disconnect, ask, rotate, reconnect ------------------------------
            elif upper_cmd == "BDROTATEBE":
                # Disconnect
                try:
                    for bot in para_list:
                        if int(bot) not in bot_info.keys():
                            continue
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
                        for bot in para_list:
                            if int(bot) not in bot_info.keys():
                                print(f"{bot} - SKIP")
                                continue
                            rotate_bot_advanced(bot_info[int(bot)]["ip"], bot)
                except Exception as e:
                    print(Fore.RED + str(e))
                try:
                    for bot in para_list:
                        be_thr = threading.Thread(target = sw.enable, args = (str(bot),))
                        be_thr.start()
                except Exception as e:
                    print(Fore.RED + str(e))
            # -----------------------------------------------------------------elif upper_cmd == "BDROTATEBE":
                # Disconnect
            elif upper_cmd == "BDROTATEBE2":
                thread_defaultdict = collections.defaultdict(lambda: 0)
                # thread_defaultdict.
                try:
                    for bot in para_list:
                        if int(bot) not in bot_info.keys():
                            continue
                        bdrtbd_thr = threading.Thread(target = sw.disable, args = (str(bot),))
                        bdrtbd_thr.start()
                        thread_defaultdict[bot] = bdrtbd_thr
                except Exception as e:
                    print(Fore.RED + str(e))
                # Ask to rotate
                try:
                    cf = input("Execute rotate? (Y/N) >> ")
                    if cf.upper() != "Y":
                        # Do nothing if cf not is Y
                        pass
                    else:
                        for bot in para_list:
                            if int(bot) not in bot_info.keys():
                                print(f"{bot} - SKIP")
                                continue
                            rotate_thread = threading.Thread(target = rotate_bot_advanced, args = (bot_info[int(bot)]["ip"], bot))
                            rotate_thread.start()
                            thread_defaultdict[bot] = rotate_thread
                except Exception as e:
                    print(Fore.RED + str(e))
                try:
                    check_rtt_alive = threading.Thread(target = check_threads_alive, args = (thread_defaultdict,))
                    check_rtt_alive.start()
                except Exception as e:
                    print(Fore.RED + str(e))
            # -----------------------------------------------------------------
            elif upper_cmd == "SENDCHARGE":
                for bot in para_list:
                    send_to_charger_thread = threading.Thread(target = sw.send_bot_to_charger, args = (bot_info[int(bot)]["id"],))
                    send_to_charger_thread.start()

            elif upper_cmd == "STOPCHARGE":
                for bot in para_list:
                    stop_charge_thread = threading.Thread(target = sw.stop_bot_charging, args = (bot_info[int(bot)]["id"],))
                    stop_charge_thread.start()

            # Packwall
            elif upper_cmd == "SETIDLE":
                for ps in para_list:
                    ps_upper = "PS-" + ps.upper()
                    if ps_upper in packwall_info.keys():
                        txt, code = sw.setidle(packwall_info[ps_upper])
                        if code in success:
                            print(Fore.GREEN + f"{ps_upper} was setidle")
                        else:
                            print(Fore.YELLOW + f"{ps_upper} - {txt}")
                        # print(packwall_info[ps_upper])
                    else:
                        print(Fore.YELLOW + f"{ps_upper} is INVALID")
            elif upper_cmd == "RFHMI":
                for ps in para_list:
                    ps_upper = "PS-" + ps.upper()
                    if ps_upper in packwall_info.keys():
                        txt, code = sw.refreshhmi(packwall_info[ps_upper])
                        if code in success:
                            print(Fore.GREEN + f"{ps_upper} was refreshhmi")
                        else:
                            print(Fore.YELLOW + f"{ps_upper} - {txt}")
                        # print(packwall_info[ps_upper])
                    else:
                        print(Fore.YELLOW + f"{ps_upper} is INVALID")
            # Debug cmd MV, RC, RF
            elif upper_cmd == "MV":
                if len(split_cmd) != 4:
                    print(Fore.YELLOW + "MV - syntax is INVALID")
                    print(f"e.x: MV 192 F 0.03")
                else:
                    try:
                        if int(split_cmd[1]) in bot_info.keys():
                            bot_interface.debug_move(bot_info[int(split_cmd[1])]["ip"], split_cmd[2], split_cmd[3])
                        else:
                            print(Fore.RED + f'Bot {bot} does NOT exist')
                    except Exception as e:
                        print(Fore.RED + str(e))
                        time.sleep(2)
            elif upper_cmd == "RC":
                try:
                    bot_interface.read_ceiling(bot_info[int(split_cmd[1])]["ip"])
                except Exception as e:
                    print(Fore.RED + str(e))
                    time.sleep(2)
            elif upper_cmd == "RF":
                try:
                    bot_interface.read_floor(bot_info[int(split_cmd[1])]["ip"])
                except Exception as e:
                    print(Fore.RED + str(e))
                    time.sleep(2)
            elif upper_cmd == "CAM":
                if len(split_cmd) != 3 or split_cmd[1].isdigit() == False or split_cmd[2].upper() not in CAM_OPT:
                    print(Fore.YELLOW + "CAM - syntax is INVALID" + f" {len(split_cmd)} {split_cmd[1]} {split_cmd[2]}")
                elif int(split_cmd[1]) not in bot_info.keys():
                    print(Fore.RED + f'Bot {split_cmd[1]} does NOT exist')
                else:
                    print("ssh -o StrictHostKeyChecking=no -L 15000:192.168.75.2:5000 root@" + str(bot_info[int(split_cmd[1])]["ip"]))
                    tunnel_ask = input("    Have you created ssh tunnel yet? (Y/N) >> ")
                    if tunnel_ask.upper() == "Y":
                        iso_time = datetime.datetime.now(pytz.timezone('US/Pacific')).isoformat()
                        date_dir = iso_time[:10:]
                        bot_cam_dir = "BOT_" + str(split_cmd[1]) + "_" + iso_time[11:19:].replace(":", ".")
                        cam_dir = create_dir(cwd, DIR_BOT_CAMERA, date_dir, bot_cam_dir)
                        print(cam_dir)
                        cam_thread = threading.Thread(target = cameraUtility.get_picture,
                                                    args = (cam_dir, bot_info[int(split_cmd[1])]["ip"], split_cmd[1] ,split_cmd[2]))
                        cam_thread.start()
                        # cameraUtility.get_picture(cam_dir, split_cmd[2])
# AS BOT -----------------------------------------------------------
            else:
                for bot in para_list:
                    if bot.upper() in option_list or bot.isdigit() == False:
                        continue
                    if int(bot) not in bot_info.keys():
                        print(Fore.RED + f'Bot {bot} does NOT exist')
                        continue
                    # FW ---------------------------------------------------------------------
                    # Restart fw
                    elif upper_cmd == "RST":
                        rst_thread = threading.Thread(target = fw.restart_fw, args = (bot_info[int(bot)]["ip"],))
                        rst_thread.start()
                        print(Fore.GREEN + f"{bot}: Restarting")
                        # response = fw.restart_fw(bot_info[int(bot)]["ip"])
                        # if response[1] in success:
                        #     print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                        # else:
                        #     print(Fore.CYAN + f"{response[0]}")
                    # Power cycle
                    elif upper_cmd == "PWR":
                        pwr_thread = threading.Thread(target = fw.power_cycle, args = (bot_info[int(bot)]["ip"],))
                        pwr_thread.start()
                        print(Fore.GREEN + f"{bot}: Power Cycling")
                        # response = fw.power_cycle(bot_info[int(bot)]["ip"])
                        # if response[1] in success:
                        #     print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                        # else:
                        #     print(Fore.CYAN + f"{response[0]}")
                    # Kill fw process
                    elif upper_cmd == "KILL":
                        kill_thread = threading.Thread(target = fw.kill, args = (bot_info[int(bot)]["ip"],))
                        kill_thread.start()
                        print(Fore.GREEN + f"{bot}: Killing")
                        # response = fw.kill(bot_info[int(bot)]["ip"])
                        # if response[1] in success:
                        #     print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                        # else:
                        #     print(Fore.CYAN + f"{response[0]}")
                    # Watch log
                    elif upper_cmd == "WTCL":
                        response = fw.wtc_live_log(bot_info[int(bot)]["ip"])
                        if response[1] in success:
                            print(Fore.GREEN + f"{bot}: " + f"{response[0]}")
                        else:
                            print(Fore.CYAN + f"{response[0]}")
                        break
                    # Get P71 Emergency code
                    # elif upper_cmd == "P71":
                    #     response = fw.p71_code(bot_info[int(bot)]["ip"])
                    #     print(Fore.YELLOW + f"{response}")
                    # Save log
                    elif upper_cmd == "LOG":
                        # 2021-08-18T20:51:26.998694-07:00
                        iso_time_format = datetime.datetime.now(pytz.timezone('US/Pacific')).isoformat()
                        dir_date = iso_time_format[:10:]
                        dir_log = "BOT_" + str(bot) + "_" + iso_time_format[11:19:].replace(":", "")
                        log_dir = create_dir(cwd, DIR_FW_LOG, dir_date, dir_log)
                        log_thread = threading.Thread(target = fw.get_log, args = (bot_info[int(bot)]["ip"], log_dir))
                        log_thread.start()
                    # elif upper_cmd == "FWT":
                    #     response, val = fw.get_fw_type_v2(bot_info[int(bot)]["ip"], bot)
                    #     print(f"Bot {bot} is running {response} FW")

                    # SW ---------------------------------------------------------------------
                    # UNFAULT
                    elif upper_cmd == "BUF":
                        response = sw.unfault(bot_info[int(bot)]["id"])
                        if response[1] in success and len(response[0]) == 0:
                            print(Fore.GREEN + f"{bot: <3}| Unfault/Requests Successfully!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Unfault: " + response[0] + " | " + str(response[1]))

                    # RETRY
                    elif upper_cmd == "BRLC":
                        response = sw.retry(bot_info[int(bot)]["id"])
                        if response in success:
                            print(Fore.GREEN + f"{bot: <3}| Retry Successfully!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Retry Error..." + " | " + str(response))

                    elif upper_cmd == "BP":
                        response = sw.pause(bot)
                        if response[1] in success and len(response[0]) == 0:
                            print(Fore.GREEN + f"{bot: <3}| Pause Successfully!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Pause: " + response[0] + " | " + str(response[1]))

                    elif upper_cmd == "BUP":
                        response = sw.unpause(bot)
                        if response[1] in success and len(response[0]) == 0:
                            print(Fore.GREEN + f"{bot: <3}| Unpause Successfully!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Unpause: " + response[0] + " | " + str(response[1]))

                    elif upper_cmd == "BE":
                        response = sw.enable(bot)
                        if response in success:
                            print(Fore.GREEN + f"{bot: <3}| Bot is reconnected!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Reconnect Error..." + " | " + str(response))

                    elif upper_cmd == "BD":
                        response = sw.disable(bot)
                        if response in success:
                            print(Fore.GREEN + f"{bot: <3}| Bot is disconnected!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Disconnect Error..." + " | " + str(response))

                    elif upper_cmd == "BF":
                        bot_fix(bot, bot_info)
                    elif upper_cmd == "BIG":
                        if int(bot) in ignore_list:
                            print(Fore.YELLOW + f"{bot: <3}| Already ignored {bot}")
                        else:
                            ignore_list.append(int(bot))
                            print(Fore.GREEN + f"{bot: <3}| Ignored bot {bot}")
                    elif upper_cmd == "BUIG":
                        if int(bot) in ignore_list:
                            ignore_list.remove(int(bot))
                            print(Fore.GREEN + f"{bot: <3}| Un-Ignored bot {bot}")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Bot {bot} has never been ignored yet ...")
                    elif upper_cmd == "BINF":
                        print(f"{bot: <3}| Information")
                        print(f"{'':-^80}")
                        print_alert.print_a_bot_info(bot_info[int(bot)], 'Information', int(bot))
                        # print(f"Bot {bot}'s ID: " + {bot_info[int(bot)][info["ID"]]})
                        try:
                            print(f"Bot {bot}'s ID: " + bot_info[int(bot)]["id"])
                        except Exception as e:
                            print(e)
                            # print("No ID")
                        # ctask = sw.task(bot_info[int(bot)]["id"])
                        # if ctask[1] in success:
                        #     print_alert.print_task(ctask[0]["tasks"], 'Information', bot)
                        # else:
                        #     print(Fore.YELLOW + f"{bot: <3}| Get task error..." + str(ctask[1]) + " " + bot_info[int(bot)]["id"])
                        # print(f"{'':-^80}")
                    elif upper_cmd == "REPLAN":
                        response = sw.replan(bot_info[int(bot)]["id"])
                        if response[1] in success and len(response[0]) == 0:
                            print(Fore.GREEN + f"{bot: <3}| Replan/Requests Successfully!!!")
                        else:
                            print(Fore.YELLOW + f"{bot: <3}| Replan: " + response[0] + " | " + str(response[1]))

                    # Test cmd
                    elif upper_cmd == "R180CWF":
                        rotate_msg, rotate_value = bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)]["id"])
                        print(rotate_msg)

                    # elif upper_cmd == "BDROTATEBE":
                    #     bot_interface.rotate_180_CW_and_read_floor(bot_info[int(bot)][info["IP"]])

                    elif upper_cmd == "ENTERPWRSAVER":
                        txt, txt2 = sw.enter_sleep_mode(bot_info[int(bot)]["ip"])
                        # print(txt)
                        # print(txt2)

                    elif upper_cmd == "EXITPWRSAVER":
                        tuple_4 = sw.exit_sleep_mode(bot_info[int(bot)]["ip"])
                        # print(tuple_4[0])
                        # print(tuple_4[1])
                        # print(tuple_4[2])
                        # print(tuple_4[3])
                    # --------------------------------END Test



if __name__ == '__main__':
    # import colorama
    # colorama.init(autoreset = True)
    # help_menu()
    # from colorama import init, Fore, Style
    # init(autoreset=True)
    # print(Fore.RED + 'some red text')
    # print(Fore.BLUE + 'some red text')
    # print(Fore.CYAN + 'some red text')
    # print(Style.BRIGHT + Fore.RED + 'some bright red text')
    # print(Style.BRIGHT + Fore.BLUE + 'some bright red text')
    # print(Style.BRIGHT + Fore.CYAN + 'some bright red text')
    # print(Style.BRIGHT + Fore.MAGENTA + 'some bright red text')
    # global_bot_dir(0, "..", 0)
    ip_list = ["172.16.28.103", "172.16.28.111", "172.16.28.81", "172.16.28.68"]
    # testing_thread(ip_list)
    # bot_interface.rotate_180_CW_and_read_floor(ip_list[0])
    # print(ip_list[0])
    # for bot_ip in ip_list:
    #         t = threading.Thread(target = bot_interface.rotate_180_CW_and_read_floor, args = (bot_ip,))
    #         t.start()
    pass