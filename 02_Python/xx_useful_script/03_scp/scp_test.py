import paramiko
from scp import SCPClient
log_dir = '/var/log/'
ip = '172.16.28.48'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
log_tail = [".log",".log.0",".log.1",".log.2",".log.3",".log.4",".log.5",".log.6",".log.7",".log.8",".log.9"]
log_type = ["agv_x2_fw", "agv_x2_executive"]
try:
    ssh.connect(ip, 22, username="root", password="")
except:
    print("Error")
with SCPClient(ssh.get_transport()) as scp:
    # for typ in log_type:
    #     for tail in log_tail:
    #         try:
    #             scp.get(log_dir + typ + tail, "./fw_log") # Copy my_file.txt to the server
    #         except:
    #             continue
    scp.get(log_dir + log_type[1] + log_tail[0])
ssh.close()