import requests
from requests.structures import CaseInsensitiveDict
from collections import defaultdict
from colorama import init, Fore

cmd_url = {
    'retry':    "https://wes-agv-fleet.iherbscs.net/api/Bots/{}/commands/retry-task",
    'enable':   "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/{}/enable",
    'disable':  "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/{}/disable",
    'unfault':  "https://wes-agv-portal-gateway.iherbscs.net/api/Fleet/Bots/{}/Unfault",
    'unpause':  "https://wes-agv-iherbdriver.iherbscs.net/api/Bots/commands/unpause-bot/{}"
}

success = [200, 202, 204]

# Retry last cmd
def retry(bot_id, url = cmd_url['retry']):
    try:
        resp = requests.put(url.format(bot_id))
    except:
        return 999
    return resp.status_code

# Enable/Reconnect a bot
def enable(bot_name, url = cmd_url['enable']):
    try:
        resp = requests.put(url.format(bot_name))
    except:
        return 999
    return resp.status_code

# Disable/Disconnect a bot
def disable(bot_name, url = cmd_url['disable']):
    try:
        resp = requests.put(url.format(bot_name))
    except:
        return 999
    return resp.status_code

# Unpause a bot
def unpause(bot_name, url = cmd_url['unpause']):
    headers = CaseInsensitiveDict()
    headers["accept"] = "*/*"
    headers["Content-Type"] = "application/x-www-form-urlencoded"
    headers["Content-Length"] = "0"
    try:
        resp = requests.post(url.format(bot_name), headers=headers)
    except:
        return ('Post Error ...', 999)
    return (resp.text, resp.status_code)

# Unfault a bot
def unfault(bot_id, url = cmd_url['unfault']):

    headers = CaseInsensitiveDict()
    headers["accept"] = "application/json"
    headers["Content-Type"] = "application/json-patch+json"

    data = '{ "botId": "' + bot_id + '"}'
    try:
        resp = requests.patch(url.format(bot_id), headers = headers, data = data)
    except:
        return ("Can't Unfault", 999)
    return (resp.text[12:-13], resp.status_code)

def show_help():
    print(f"{' QUERY MODE ':=^80}")
    print(f"{'':=<15}{'  C': <10}: {'Enter command mode': <38}{'':=<15}")
    print(f"{'':=<15}{'  H': <10}: {'Help': <38}{'':=<15}")
    print(f"{'':=<15}{'  Q': <10}: {'Quit': <38}{'':=<15}")
    print(f"{' COMMAND MODE ':=^80}")
    print(f"{'':=<15}{'  BUF': <10}: {'Unfault a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BRLC': <10}: {'Retry last command of a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BF': <10}: {'Enable, unpause, unfault and retry': <38}{'':=<15}")
    print(f"{'':=<15}{'  BUP': <10}: {'Unpause a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BE': <10}: {'Enable/Reconnect a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BD': <10}: {'Disable/Disconnect a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BIG': <10}: {'Ignore a bot': <38}{'':=<15}")
    print(f"{'':=<15}{'  BUIG': <10}: {'Un-Ignore a bot': <38}{'':=<15}")
    print("Example: BUF 10: unfault bot 10")
    print("Example: BUF 10 20 30: unfault bot 10, 20, 30")
    print("!!!!!! At present, I only develop 1 commands/input")

def execute_cmd(result_json, ignore_list):

    bot_dict = defaultdict(lambda: 0)

    for index in range(len(result_json["bots"])):
        bot_dict[result_json["bots"][index]["botName"]] = result_json["bots"][index]["id"]

    print(f"{' Command mode (H - Help, Q - Quit) ':=^80}")

    while True:
        action = input('>> ')

        # Unfault
        if action.upper() == 'Q':
            break
        elif action.upper() == 'H':
            show_help()
        else:
            # Parse and execute
            split_cmd = action.split(' ')
            for bot in split_cmd[1:]:
                # UNFAULT
                if bot not in bot_dict.keys():
                    print(Fore.RED + f'Bot {bot} does not exist')
                    continue
                if split_cmd[0].upper() == 'BUF':
                    response = unfault(bot_dict[bot])
                    if response[1] in success:
                        if len(response[0]) != 0:
                            print(Fore.GREEN + response[0])
                        print(Fore.GREEN + 'Unfault/Requests Successfully!!!')
                    else:
                        print(Fore.CYAN + response[0])
                        print(Fore.CYAN + str(response[1]))

                # RETRY
                elif split_cmd[0].upper() == 'BRLC':
                    response = retry(bot_dict[bot])
                    if response in success:
                        print(Fore.GREEN + "Retry Successfully!!!")
                    else:
                        print(Fore.RED + "Retry Error..." + str(response))

                elif split_cmd[0].upper() == 'BUP':
                    response = unpause(bot)
                    if response[1] in success:
                        if len(response[0]) != 0:
                            print(Fore.GREEN + response[0])
                        print(Fore.GREEN + "Unpause Successfully!!!")
                    else:
                        print(Fore.CYAN + response[0])
                        print(Fore.CYAN + str(response[1]))

                elif split_cmd[0].upper() == 'BE':
                    response = enable(bot)
                    if response in success:
                        print(Fore.GREEN + "Bot is reconnected!!!")
                    else:
                        print(Fore.RED + "Reconnect Error..." + str(response))

                elif split_cmd[0].upper() == 'BD':
                    response = disable(bot)
                    if response in success:
                        print(Fore.GREEN + "Bot is disconnected!!!")
                    else:
                        print(Fore.RED + "Disconnect Error..." + str(response))

                elif split_cmd[0].upper() == 'BF':
                    response = enable(bot)
                    if response in success:
                        print(Fore.GREEN + "Bot is reconnected!!!")
                    else:
                        print(Fore.RED + "Reconnect Error..." + str(response))

                    response = unpause(bot)
                    if response[1] in success:
                        if len(response[0]) != 0:
                            print(Fore.GREEN + response[0])
                        print(Fore.GREEN + "Unpause Successfully!!!")
                    else:
                        print(Fore.CYAN + response[0])
                        print(Fore.CYAN + str(response[1]))

                    response = unfault(bot_dict[bot])
                    if response[1] in success:
                        if len(response[0]) != 0:
                            print(Fore.GREEN + response[0])
                        print(Fore.GREEN + 'Unfault/Requests Successfully!!!')
                    else:
                        print(Fore.CYAN + response[0])
                        print(Fore.CYAN + str(response[1]))

                    response = retry(bot_dict[bot])
                    if response in success:
                        print(Fore.GREEN + "Retry Successfully!!!")
                    else:
                        print(Fore.RED + "Retry Error..." + str(response))
                elif split_cmd[0].upper() == 'BIG':
                    ignore_list.append(bot)
                    print(Fore.GREEN + f'Ignored bot {bot}')
                elif split_cmd[0].upper() == 'BUIG':
                    if bot in ignore_list:
                        ignore_list.remove(bot)
                        print(Fore.GREEN + f'Un-Ignored bot {bot}')
                    else:
                        print(Fore.RED + f'Bot {bot} has never been ignored yet ...')

if __name__ == '__main__':
    init(autoreset = True)

    r = open("output_check.json", "r")
    result_json = json.load(r)
    print(type(result_json))

    execute_cmd(result_json, [1])
