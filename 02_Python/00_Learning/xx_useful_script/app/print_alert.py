import var
import winsound
import time
import os

from playsound import playsound

sound_dir = "\\sound"
sound_file = {
    'Fault':        '\\fault.mp3',
    'Connection':   '\\mute.wav',
    'Pause':        '\\mute.wav',
    'Idle':         '\\mute.wav',
    'Charging':     '\\mute.wav',
    'N/A 7':        '\\mute.wav',
}

# play sound with status
def alert(status):
    full_path = os.path.dirname(os.path.abspath(__file__)) + sound_dir + sound_file[status]
    try:
        playsound(full_path)
    except:
        print('No sound file avaiable for ' + status)

# Print header before print bot info
def print_header(status):
    print(var.color_for_txt[status] + f"{' Bot ':=^9}|{' IP ':=^16}|{' Status ':=^12}|{' Pod ':=^9}|{' Bat ':=^9}|{' Axis ':=^8}|{' Location ':=^10}")

# print a bot info from status and a element (a dict) of json['bots'] list
def print_a_bot_info(dict_elements, status):
    p_name = dict_elements[var.botName]
    p_ip = dict_elements[var.botIp]
    if p_ip == None:
        p_ip = ''
    p_st = var.botStatus_dict[dict_elements[var.status]]
    if p_st == None:
        p_st = ''
    p_pd = dict_elements[var.podName]
    if p_pd == None:
        p_pd = ''
    p_bt = dict_elements[var.chargerLevel]
    if p_pd == None:
        p_pd = ''
    p_xy = str(int(dict_elements["location"]["x"])) + '-' + str(int(dict_elements["location"]["y"]))
    p_lc = "N/A"
    print(var.color_for_txt[status] + f"{p_name: <9}|{p_ip: <16}|{p_st: <12}|{p_pd: <9}|{p_bt: <9}|{p_xy: <8}|{p_lc: <10}")

# print and alert for a issue
def print_with_alert(result_json, para_list , status):
    if len(para_list) != 0:
        print(var.color_for_txt[status] + f"\n{status:=^80}")
        print_header(status)
        if status == 'Ignore' or status == 'Connection':
            for element in para_list:
                for dict_list in result_json[var.bot]:
                    if str(element) in dict_list.values():
                        print_a_bot_info(dict_list, status)
        else:
            for element in para_list:
                print_a_bot_info(result_json[var.bot][element], status)
        # Play sound if Fault or Connection only
        if status == 'Fault':
            alert(status)
        elif status == 'Connection':
            # alert(status)
            pass

def print_summarize(pause_list, charge_list, idle_list, connection_list, fault_list):
    print(f"\n{'':=^80}")
    print(var.color_for_txt['Pause'] + f"{'== Pause ':=<20}: {len(pause_list):.^58}")
    print(var.color_for_txt['Charging'] + f"{'== Charging ':=<20}: {len(charge_list):.^58}")
    print(var.color_for_txt['Idle'] + f"{'== Idle ':=<20}: {len(idle_list):.^58}")
    print(var.color_for_txt['Connection'] + f"{'== Connection ':=<20}: {len(idle_list):.^58}")
    print(var.color_for_txt['Fault'] + f"{'== Fault ':=<20}: {len(fault_list):.^58}")
    print(f"{'':=^80}")
