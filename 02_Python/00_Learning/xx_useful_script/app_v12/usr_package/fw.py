import paramiko
import msvcrt
import time
import re
import os
from scp import SCPClient
from colorama import Fore

fw_cmd = {
    "p71":          "tail -n 50 emergency.log/p71_extra-\\(null\\)",
    "wtclog":       "./watch_latest_exec_log.sh || ./watch_latest_log.sh",
    "rst":          "systemctl restart agv_x2_fw || systemctl restart agv_exec",
    "kill":         "killall -9 agv_x2_fw || killall -9 agv_executive",
    "pwrcycle":     "systemctl stop agv_x2_fw || systemctl stop agv_exec; sync; /usr/sbin/i2cset -y 2 0x20 0x00 0x08;nohup /usr/sbin/i2cset -y 2 0x20 0x02",
}


def init(cmd):
    global fw_cmd
    if cmd != 0:
        fw_cmd = cmd["fw_cmd"]
    else:
        print("Command: Default - Elgin")

def get_fw_type(ip, name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)
    cmd = "ls"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    for line in ssh_stdout.readlines():
        if line == "agv_x2_fw\n":
            ssh.close()
            return("Old", 1)
        if line == "agv_x2_executive\n":
            ssh.close()
            return("New", 1)
    ssh.close()

def get_fw_type_v2(ip, name):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)
    cmd = "ps -C agv_x2_fw" # OLD
    # cmd = "ps -C agv_x2_executiv" # NEW
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    out = ""
    for line in ssh_stdout.readlines():
        out += line
    ssh.close()
    out_list = out.split(" ")
    if 'agv_x2_fw\n' in out_list:
        return("Old", 1)
    else:
        return("New", 1)

def print_fw_new(ip, name):
    fw_t, val = get_fw_type_v2(ip, name)
    if fw_t == "New":
        print(name)

def wtc_live_log(ip):
    key = 0

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = fw_cmd["wtclog"]
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if ord(key) == ord('q') or ord(key) == ord('Q'):
                ssh.close()
                break
        else:
            out = ssh_stdout.readline()
            if len(out) != 0:
                print(out, end = "")
            time.sleep(0.005)
    return ("Success", 0)

def restart_fw(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = fw_cmd["rst"]

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    err = ssh_stderr.readlines()
    ssh.close()
    if len(err) == 2:
        return (err, 999)
    else:
        return ("Restart fw > Success", 0)

def kill(ip):
    directory = []
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = fw_cmd["kill"]

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    err = ssh_stderr.readlines()
    ssh.close()
    if len(err) == 2:
        return (err, 999)
    else:
        return ("Kill fw > Success", 0)

def power_cycle(ip):
    directory = []
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = fw_cmd["pwrcycle"]

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    err = ssh_stderr.readlines()
    ssh.close()
    if len(err) == 2:
        return (err, 999)
    else:
        return ("Power cycle > Success", 0)

def power_cycle_with_check(ip, name, decide):
    fw_type, val = get_fw_type_v2(ip, name)
    if decide == "No":
        if fw_type == "New":
            print(Fore.YELLOW + f"Bot {name} is running new FW > Do not power cycle")
            return -1
        if fw_type == "Error":
            print(Fore.YELLOW + f"Can't check fw type of bot {name} > Do not power cycle")
            return -1
        if fw_type == "Old":
            print(Fore.GREEN + f"Power cycling bot {name}")
            power_cycle(ip)
            return 1
    elif decide == "Yes":
        if fw_type == "Error":
            print(Fore.YELLOW + f"Can't check fw type of bot {name} > Do not power cycle")
            return -1
        else:
            print(Fore.GREEN + f"Power cycling bot {name}")
            power_cycle(ip)
            return 1
def p71_code(ip):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)
    cmd = fw_cmd["p71"]
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    out = ''
    for line in ssh_stdout.readlines():
        out += line
    stt_code = re.search(r'\dx\d\d', out)
    ssh.close()
    if stt_code == None:
        return stt_code
    return stt_code.group()
# scp root@172.16.28.52:/var/log/agv_x2_executive.log* . || scp root@172.16.28.52:/var/log/agv_x2_fw.log* .

def get_log(ip, log_dir):
#     if os.path.isdir(cwd + "\\fw_log") == False:
#         try:
#             os.mkdir(cwd + "\\fw_log")
#         except Exception as e:
#             print(Fore.RED + str(e))
#             return -1
#     if os.path.isdir(cwd + "\\fw_log\\" + cli_dir_date) == False:
#         try:
#             os.mkdir(cwd + "\\fw_log\\" + cli_dir_date)
#         except Exception as e:
#             print(Fore.RED + str(e))
#             return -1
#     if os.path.isdir(cwd + "\\fw_log\\" + cli_dir_date + "\\" + cli_dir_log) == False:
#         try:
#             os.mkdir(cwd + "\\fw_log\\" + cli_dir_date + "\\" + cli_dir_log)
#         except Exception as e:
#             print(Fore.RED + str(e))
#             return -1

    sv_log_dir = '/var/log/'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log_tail = (".log",".log.0",".log.1",".log.2",".log.3",".log.4",".log.5",".log.6",".log.7",".log.8",".log.9")

    try:
        ssh.connect(ip, 22, username="root", password="")
    except Exception as e:
        print(Fore.RED + str(e))

    cmd = "ps -C agv_x2_fw"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    out = ""
    for line in ssh_stdout.readlines():
        out += line
    out_list = out.split(" ")
    if 'agv_x2_fw\n' in out_list:
        fw = False
    else:
        fw = True

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)
    if fw == False:
        with SCPClient(ssh.get_transport()) as scp:
            try:
                for line in log_tail:
                    scp.get(sv_log_dir + "agv_x2_fw" + line, log_dir)
            except Exception as e:
                print("End old")
                print(Fore.RED + str(e))
                ssh.close()

    else:
        with SCPClient(ssh.get_transport()) as scp:
            try:
                for line in log_tail:
                    scp.get(sv_log_dir + "agv_x2_executive" + line, log_dir)
            except Exception as e:
                print("End new")
                print(Fore.RED + str(e))
                ssh.close()
    print("END")
    ssh.close()

# return rotation or not
# loc:              "x-y"
# orientation:      ["North", "East", "South", "West"]
# field_location:   dict {'123-34': 'Storage', '124-34': 'Drive Aisle', '125-34': 'Storage', ...}
def loc_dir_to_rotation(loc, orientation, field_location):
    try:
        x, y = loc.split("-")
        x = int(x)
        y = int(y)
        # Get location which bot facing to
        loc_4_dir = {"North":[x, y + 1], "East":[x + 1, y], "South":[x, y - 1], "West":[x - 1, y]}
        loc_4_pos_name = []
        # print(loc_4_dir)
        for axis in loc_4_dir.values():
            try:
                loc_4_pos_name.append(field_location[str(axis[0]) + "-" + str(axis[1])])
                # print(str(axis[0]) + "-" + str(axis[1]))
            except Exception as e:
                # print(e)
                loc_4_pos_name.append("Unavailable")
        # print(loc_4_pos_name)
        x_next, y_next = loc_4_dir[orientation]
        # Check if location is valid
        loc_next = str(x_next) + "-" + str(y_next)
        if loc_next in field_location.keys():
            if field_location[loc_next] == "Drive Aisle":
                return "No_"
            else:

                return "Rotate_"
        else:
            return "Rotate_"
    except Exception as e:
        return e

def get_bot_dir(ip, name, cwd, axis, field_location):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = "tail -n 200 /var/log/agv_x2_executive.log || tail -n 200 /var/log/agv_x2_fw.log"

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    err = ssh_stderr.readlines()
    ssh.close()
    if len(err) == 2:
        f = open(cwd + "\\" + "__" + name + "__Command_Error_(" + axis + ").txt", "w")
        f.close()
    else:
        text = ""
        for line in ssh_stdout.readlines():
            text = text + line
        pattern = r'\) '
        result = re.finditer(pattern, text)
        list_result = list(result)
        orientation = None
        try:
            i = -1
            while orientation not in ["North", "East", "South", "West"]:
                index = list_result[i].span()[1]
                orientation = str(text[index: index + 5:]).replace(" ","")
                if orientation not in ["North", "East", "South", "West"]:
                    i -= 1
                    continue
                rotate_chk = loc_dir_to_rotation(axis, orientation, field_location)
                file_name = cwd + "\\" + rotate_chk + "_" + name + " - " + orientation + "_(" + axis + ").txt"
                f = open(file_name, "w")
                f.write(text)
                f.close()
        except:
            # print("Error")
            f = open(cwd + "\\" + "__" + name + "__Parse_Error_(" + axis + ").txt", "w")
            f.write(text)
            f.close()
            return ("Error", -1)

if __name__ == '__main__':
    get_log("172.17.35.134", "D:\\Libraries\\Documents\\Python\\xx_useful_script\\app_v10\\usr_package", "test", "334")
    # f = open("loc_temp.txt", "r")
    # dict_temp = f.read()
    # f.close()
    # import json
    # # print(type(json.loads(dict_temp.replace("\'","\""))))
    # field_loc = json.loads(dict_temp.replace("\'","\""))
    # temp = loc_dir_to_rotation("110-50", "North", field_loc)
    # print(temp)
    # # get_bot_dir("172.17.35.48", "248", ".", "1-1", loc)
    # rotate_180_CW_and_read_floor("172.17.35.45")
    pass
