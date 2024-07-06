import paramiko
import msvcrt
import time
import re

fw_cmd = {
    "p71":          "tail -n 50 emergency.log/p71_extra-\\(null\\)",
    "wtclog":       "./watch_latest_log.sh || ./watch_latest_exec_log.sh",
    "rst":          "systemctl restart agv_x2_fw || systemctl restart agv_exec",
    "kill":         "killall -9 agv_x2_fw || killall -9 agv_executive",
    "pwrcycle":     "systemctl stop agv_x2_fw || systemctl stop agv_exec; sync; /usr/sbin/i2cset -y 2 0x20 0x00 0x08;nohup /usr/sbin/i2cset -y 2 0x20 0x02"
}

def init(config):
    global fw_cmd
    if config != 0:
        fw_cmd = config
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
    if len(err) != 0:
        ssh.close()
        return (err, 999)
    else:
        ssh.close()
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
    if len(err) != 0:
        ssh.close()
        return (err, 999)
    else:
        ssh.close()
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
    if len(err) != 0:
        ssh.close()
        return (err, 999)
    else:
        ssh.close()
        return ("Power cycle > Success", 0)

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
    if stt_code == None:
        return stt_code
    return stt_code.group()
'''
['agv_diags\n', 'agv_x2_fw\n', 'backup-config.json\n', 'calibrate-floor-cam-on-target.sh\n', 'cameraOta\n', 'check_cam_version-3126.log\n', 'check_cam_version-3159.log\n', 'config-log.sh\n', 'config.json\n', 'config.json.default\n', 'dev_p71_ioctl-794.log\n', 'dev_p71_ioctl-795.log\n', 'dev_p71_ioctl-796.log\n', 'dev_p71_move_execute-235.log\n', 'dev_p71_move_execute-236.log\n', 'dev_p71_turn_execute-321.log\n', 'dev_p71_turn_execute-322.log\n', 'dev_p71_turn_execute-372.log\n', 'dev_p71_turn_execute-373.log\n', 'dev_p71_turn_execute-374.log\n', 'emergency.log\n', 'got7e.log\n', 'launch_agv_x2_fw.sh\n', 'lock-string\n', 'log_safety.log\n', 'watch_latest_log.sh\n', 'wireshark_traces\n']
'''
if __name__ == '__main__':
    pass