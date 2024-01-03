from usr_package import var
import time

from playsound import playsound

sound_dir = "sound\\"
sound_file = {
    "Fault":        "fault.wav",
    "Connection":   "connection.wav",
    "Pause":        "mute.wav",
    "Idle":         "idle.wav",
    "Charging":     "mute.wav",
    "Ignore":       "mute.wav",
    "N/A 7":        "mute.wav"
}

def init(file_dict):
    global sound_file
    if file_dict == 0:
        return 0
    try:
        sound_file = file_dict
    except:
        print("Default")

def get_location_in_xy(location):
    xy_loc = str(int(location["x"])) + '-' + str(int(location["y"]))
    return xy_loc

# play sound with status
# def alert(status):
#     full_path = os.getcwd() + '\\' + sound_dir + sound_file[status]
#     try:
#         playsound(full_path)
#     except:
#         print(var.color_for_txt[status] + "Sound file error ...")
#         print(full_path)


def alert(status, path):
    full_path = path + '\\' + sound_dir + sound_file[status]
    try:
        playsound(full_path)
    except:
        print(var.color_for_txt[status] + "Sound file error ...")
        print(full_path)

# Print header before print bot info
def print_header(status):
    print(var.color_for_txt[status] + f"|{' Bot ':=^9}|{' IP ':=^15}|{' Status ':=^12}|{' Axis ':=^8}|{' Pod ':=^9}|{' Bat ':=^7}|{' Location ':=^12}|")
    print(var.color_for_txt[status] + f"{'':=^80}")

# print a bot info from status and a element (a dict) of json['bots'] list
def print_a_bot_info(element, status, location, name = 0):
    # bot_info_as_name: botName:[ip, stt, xy, pod, bat]
    p_name = name
    p_ip = element[0]
    if p_ip == None:
        p_ip = '----'
    p_st = element[1]
    if p_st == None:
        p_st = '----'
    p_pd = element[3]
    if p_pd == None:
        p_pd = '----'
    p_bt = element[4]
    if p_pd == None:
        p_pd = '----'
    p_xy = element[2]
    if p_xy in location.keys():
        p_lc = location[p_xy]
    else:
        p_lc = '----'
    print(var.color_for_txt[status] + f"|   {p_name: <6}| {p_ip: <14}|   {p_st: <9}| {p_xy: <7}|   {p_pd: <6}|  {p_bt: <5}|{p_lc: <12}|")

def print_by_name(bot_info_dict, para_list , status, location):
    if len(para_list) != 0:
        print(var.color_for_txt[status] + f"\n{status:=^80}")
        print_header(status)
        for bot in para_list:
            print_a_bot_info(bot_info_dict[bot], status, location, bot)
        print(var.color_for_txt[status] + f"{'':-^80}")

def print_task(task, status, bot):
    if len(task) == 0:
        print(var.color_for_txt[status] + f"{bot}: No Task")
    else:
        for task_info in task:
            if task_info["isCompleted"] == True:
                print(var.color_for_txt["Complete"] + task_info["task"])
            else:
                print(var.color_for_txt["NotComplete"] + task_info["task"])
