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
    "pwrcycle":     "/usr/sbin/i2cset -y 2 0x20 0x00 0x08;nohup /usr/sbin/i2cset -y 2 0x20 0x02",
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
    cmd = "ps -C agv_x2_fw"
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
    if decide == "No":
        fw_type, val = get_fw_type_v2(ip, name)
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

def get_log(ip, cwd, cli_dir_date, cli_dir_log):
    if os.path.isdir(cwd + "\\fw_log") == False:
        try:
            os.mkdir(cwd + "\\fw_log")
        except:
            print("Can not create fw_log directory!!!")
            return -1
    if os.path.isdir(cwd + "\\fw_log\\" + cli_dir_date) == False:
        try:
            os.mkdir(cwd + "\\fw_log\\" + cli_dir_date)
        except:
            print(f"Can not create {cli_dir_date} directory here!!!")
            return -1
    if os.path.isdir(cwd + "\\fw_log\\" + cli_dir_date + "\\" + cli_dir_log) == False:
        try:
            os.mkdir(cwd + "\\fw_log\\" + cli_dir_date + "\\" + cli_dir_log)
        except:
            print(f"Can not create {cli_dir_log} directory here!!!")
            return -1

    cli_log_dir = cwd + "\\fw_log\\" + cli_dir_date + "\\" + cli_dir_log
    sv_log_dir = '/var/log/'
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    log_tail = (".log",".log.0",".log.1",".log.2",".log.3",".log.4",".log.5",".log.6",".log.7",".log.8",".log.9")
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = "ls"
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    for line in ssh_stdout.readlines():
        if line == "agv_x2_fw\n":
            with SCPClient(ssh.get_transport()) as scp:
                try:
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[0], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[1], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[2], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[3], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[4], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[5], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[6], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[7], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[8], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_fw" + log_tail[9], cli_log_dir)
                except:
                    ssh.close()
                    print("End old")
            break
        elif line == "agv_x2_executive\n":
            with SCPClient(ssh.get_transport()) as scp:
                try:
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[0], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[1], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[2], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[3], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[4], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[5], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[6], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[7], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[8], cli_log_dir)
                    scp.get(sv_log_dir + "agv_x2_executive" + log_tail[9], cli_log_dir)
                except:
                    ssh.close()
                    print("End new")
            break
    ssh.close()

def get_bot_dir(ip, name, cwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        ssh.connect(ip, 22, username="root", password="")
    except:
        return ("Error", -1)

    cmd = "tail -n 25 /var/log/agv_x2_executive.log || tail -n 25 /var/log/agv_x2_fw.log"

    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(cmd)

    err = ssh_stderr.readlines()
    ssh.close()
    if len(err) == 2:
        return (err, 999)
    else:
        text = ""
        for line in ssh_stdout.readlines():
            text = text + line
        pattern = r'\) '
        result = re.finditer(pattern, text)
        try:
            list_result = list(result)
            index = list_result[-1].span()[1]
            # print(text[index: index + 5:])
            file_name = cwd + "\\" + name + " - " + text[index: index + 5:]
            f = open(file_name, "w")
            f.close()
        except:
            # print("Error")
            f = open(cwd + "\\" + name + " - Error", "w")
            f.close()
            return ("Error", -1)
'''
['agv_diags\n', 'agv_x2_fw\n', 'backup-config.json\n', 'calibrate-floor-cam-on-target.sh\n', 'cameraOta\n', 'check_cam_version-3126.log\n', 'check_cam_version-3159.log\n', 'config-log.sh\n', 'config.json\n', 'config.json.default\n', 'dev_p71_ioctl-794.log\n', 'dev_p71_ioctl-795.log\n', 'dev_p71_ioctl-796.log\n', 'dev_p71_move_execute-235.log\n', 'dev_p71_move_execute-236.log\n', 'dev_p71_turn_execute-321.log\n', 'dev_p71_turn_execute-322.log\n', 'dev_p71_turn_execute-372.log\n', 'dev_p71_turn_execute-373.log\n', 'dev_p71_turn_execute-374.log\n', 'emergency.log\n', 'got7e.log\n', 'launch_agv_x2_fw.sh\n', 'lock-string\n', 'log_safety.log\n', 'watch_latest_log.sh\n', 'wireshark_traces\n']
'''
if __name__ == '__main__':
    get_bot_dir("172.17.35.71", "271", ".")
    pass