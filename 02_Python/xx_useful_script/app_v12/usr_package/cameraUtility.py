import paramiko
import os
import socket
from scp import SCPClient
import time

SSH_USERNAME = "root"
SSH_PASSWORD = ""

DEBUG_VERBOSE_BYTES=[0xAA,0x37,0x01,0x05,0x72]
FLOOR_SELECT_BYTES = [0xAA, 0x55, 0x00, 0xA9]

GET_IMAGE_BYTES= [0xAA, 0x21, 0x00, 0x11]
CEIL_SELECT_BYTES = [0xAA,0xA5, 0x00, 0xB1]
RESET_CAMERA_BYTES = [0xAA, 0xFF, 0x00, 0xB8]

CAMERA_LENSES_TO_USE=[CEIL_SELECT_BYTES, FLOOR_SELECT_BYTES]
FLOOR_CAM = "F"
CEILING_CAM = "C"
BOTH_CAM = "B"

def get_picture(pic_dir, ip, bot_name, option):
    opt = option.upper()
    if opt == FLOOR_CAM:
        cam_lens = [FLOOR_SELECT_BYTES]
    elif opt == CEILING_CAM:
        cam_lens = [CEIL_SELECT_BYTES]
    elif opt == BOTH_CAM:
        cam_lens = CAMERA_LENSES_TO_USE
    ssh = paramiko.SSHClient()
    ssh_stdin = ssh_stdout = ssh_stderr = None
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        camera_images_captured = 0
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", 15000))
        arr = bytearray(DEBUG_VERBOSE_BYTES)
        s.sendall(arr)
        reply = s.recv(4096)

        for lens in cam_lens:
            arr = bytearray(lens)
            s.sendall(arr)
            reply = s.recv(4096)
            time.sleep(.500)
            arr = bytearray(GET_IMAGE_BYTES)
            s.sendall(arr)
            time.sleep(.500)
            reply = s.recv(4096)
            if(len(reply) < 13):
                time.sleep(1)
                s.sendall(arr)
                reply = s.recv(4096)
                myReplyList=list(reply)
            frameNumArray=reply[-5:-1]
            frameNum = int.from_bytes(frameNumArray, "big", signed=False)
            time.sleep(4)
            ssh.connect(ip, username=SSH_USERNAME, password=SSH_PASSWORD)
            tftp_cmd="tftp -gr Image_" + str(frameNum) + ".bmp 192.168.75.2"
            stdin, stdout, stderr = ssh.exec_command(tftp_cmd)
            time.sleep(5)
            scp = SCPClient(ssh.get_transport());
            imageFilename = "Image_" + str(frameNum) + ".bmp"
            remoteFilename="/home/root/" + imageFilename
            scp.get(remoteFilename)
            # cwd = os.getcwd()
            relocatedFilename = pic_dir + "\\" + imageFilename
            os.rename(imageFilename, relocatedFilename)
            ssh.close()
            fileSize = os.path.getsize(relocatedFilename)
            if(fileSize > 0):
                camera_images_captured = camera_images_captured + 1
            else:
                # print("Image received size is 0 bytes")
                f = open(pic_dir + "\\" + "0", "w")
                f.close()
            f = open(pic_dir + "\\" + "end", "w")
            f.close()
    except Exception as e:
        f = open(pic_dir + "\\" + "e.txt", "w")
        f.write(e)
        f.close()
        print(e)
