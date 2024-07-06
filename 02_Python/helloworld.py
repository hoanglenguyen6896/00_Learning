import sys
import os
import json
import requests
import socket
import threading
import time
import msvcrt
# print(sys.executable)
# print(os.path.dirname(sys.executable))
# config_name = 'myapp.cfg'

# # determine if application is a script file or frozen exe
# if getattr(sys, 'frozen', False):
#     print(os.path.dirname(sys.executable))
# elif __file__:
#     print(os.path.dirname(os.path.realpath(__file__)))

# while True:
#     pass

# import os
# print(__file__)
# print(os.path.join(os.path.dirname(__file__), '..'))
# print(os.path.dirname(os.path.realpath(__file__)))
# print(os.path.abspath(os.path.dirname(__file__)))

# Print iterations progress
# def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
#     """
#     Call in a loop to create terminal progress bar
#     @params:
#         iteration   - Required  : current iteration (Int)
#         total       - Required  : total iterations (Int)
#         prefix      - Optional  : prefix string (Str)
#         suffix      - Optional  : suffix string (Str)
#         decimals    - Optional  : positive number of decimals in percent complete (Int)
#         length      - Optional  : character length of bar (Int)
#         fill        - Optional  : bar fill character (Str)
#         printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
#     """
#     percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
#     filledLength = int(length * iteration // total)
#     bar = fill * filledLength + '-' * (length - filledLength)
#     print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
#     # Print New Line on Complete
#     if iteration == total:
#         print()
# import time
# # A List of Items
# items = list(range(0, 57))
# l = len(items)

# # Initial call to print 0% progress
# printProgressBar(0, l, prefix = 'Progress:', suffix = 'Complete', length = 50)
# for i, item in enumerate(items):
#     # Do stuff...
#     time.sleep(0.01)
#     # Update Progress Bar
#     printProgressBar(i + 1, l, prefix = 'Progress:', suffix = 'Complete', length = 50)


# TCP_IP = '172.17.35.45'
# TCP_PORT = 2096
# BUFF = 1024
# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect((TCP_IP, TCP_PORT))
# time.sleep(2)
# s.sendto(bytes("AA180096B2AA59010000","utf-8"), (TCP_IP, TCP_PORT))
# s.close()


# def CalCrc(byte[] array, int len)
#         {
#             byte crc = 0xFF;
#             for (int i = 0; i < len; i++)
#             {
#                 crc ^= array[i];
#                 for (int j = 0; j < 8; j++)
#                 {
#                     if ((crc & 0x80) != 0)
#                     {
#                         crc = (byte)((crc << 1) ^ 0x31);
#                     }
#                     else
#                     {
#                         crc <<= 1;
#                     }
#                 }
#             }
#             return crc;
#         }

# return int
# To convert to byte use bytes([a])
def cal_crc(byte_arr):
    crc = 255
    # byte_arr_int = int(byte_arr)
    for index in range(len(byte_arr)):
        crc = crc ^ byte_arr[index]
        for sub_index in range(8):
            if (crc & ord(b'\x80')) != 0:
                crc = (crc << 1) ^ ord(b'\x31')
            else:
                crc = crc << 1
    return crc & 255


read_fc = b'\xAA\x18\x00\xCF\x82\xE1\x6F\x01\x00\x00\xF2'
rotate_180_CW = b'\xAA\x28\x00\xD1\x92\x5C\x72\x06\x00\x01\x02\xD0\x07\x00\x00\xCD'
def netcat(host, port, cmd):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    time.sleep(1)
    s.sendall(rotate_180_CW)
    time.sleep(5)
    s.sendall(read_fc)
    time.sleep(1)

    s.shutdown(socket.SHUT_WR)
    s.close()

if __name__ == '__main__':
    a = None
    # if type(a) == None or a.is_alive() == True:
    #     # a = a+1
    #     print(a)
    # else:
    #     print('xxxx')
    thread_x = threading.Thread(target = None, args = ())
    # thread_x.start()
    print(thread_x.is_alive())
    # byte_test = b'\xAA\xFF\x6F\x05\xAE\x59\x2A\x02\x00\x00\x01'
    # crc_chk = cal_crc(byte_test)
    # print(byte_test + bytes([crc_chk]))
    # netcat("172.17.35.45", 2096, "AA180096B2AA5901000079")
    # t1 = threading.Thread(target = netcat, args = ("172.17.35.45", 2096, "AA180096B2AA5901000079"))
    # t2 = threading.Thread(target = netcat, args = ("172.17.35.29", 2096, "AA180096B2AA5901000079"))
    # t1.start()
    # t2.start()
    # for a_byte in read_fc:
    #     print(a_byte)
    #
    # while True:
    #     if msvcrt.kbhit():
    #         key = msvcrt.getch()
    #         print(">> ", end = "")
    #         print(key, end = "-")
    #         print(ord(key), end = "-")
    #         # print(int(chr(ord(key))), end = "-")
    #         print(" <<zz")
    # from collections import defaultdict
    # packwall_info = defaultdict(lambda: 0)
    # while True:
    #     try:
    #         json_response = requests.get("https://wes-agv-packwall.atlanta.iherb.net/api/packstations")
    #         packwall_json = json_response.json()
    #         for pack_info in packwall_json['packStations']:
    #             # print(pack_info["name"] + " " + pack_info["id"])
    #             packwall_info[pack_info["name"]] = pack_info["id"]
    #         print(packwall_info)
    #         # print(color["Success"] + "Packwakk information > Done")
    #         time.sleep(1)
    #         break
    #     except Exception as e:
    #         print(color["Fault"] + str(e))
    #         append_to_file(cwd, "exception.txt", e)
    #         location_err += 1
    #         print(f"!!!Query Error!!! Retrying ... <{location_err:.>5}>")
    #         if location_err == 30:
    #             # print(color['Fault'] + "Exceptions has happened too much... Program ended!!!")
    #             terminate_thread = True
    #             os._exit(1)
    #             break
    #         time.sleep(1)
    #         os._exit(1)

'''
CRC:
'''


'''
FW 0.1

0xAA 0x27 0x00 0xC9 0x89 0x60 0x34 0x0C 0x00 0x02 0xE8 0x03 0x00 0x00 0xE8 0x03 0x00 0x00 0x01 0x02 0x02 0xE2

BW 0.03
0xAA 0x27 0x00 0xC9 0xAC 0xF5 0x35 0x0C 0x00 0x02 0xE8 0x03 0x00 0x00 0x2C 0x01 0x00 0x00 0x00 0x02 0x02 0x8A

R 90 CW
0xAA 0x28 0x00 0xFB 0x5C 0xC1 0x44 0x06 0x00 0x01 0x00 0xD0 0x07 0x00 0x00 0xF1
0xAA 0x28 0x00 0xFD 0xE7 0x60 0x47 0x06 0x00 0x01 0x00 0xD0 0x07 0x00 0x00 0x1B
0xAA 0x28 0x00 0xFE 0xAB 0xB2 0x4A 0x06 0x00 0x01 0x00 0xD0 0x07 0x00 0x00 0x6F


R 90 CWW
0xAA 0x28 0x00 0xFB 0xD8 0x35 0x45 0x06 0x00 0x01 0x01 0xD0 0x07 0x00 0x00 0x90
0xAA 0x28 0x00 0xFE 0x27 0x73 0x48 0x06 0x00 0x01 0x01 0xD0 0x07 0x00 0x00 0xB8
0xAA 0x28 0x00 0xFE 0x78 0x0C 0x49 0x06 0x00 0x01 0x01 0xD0 0x07 0x00 0x00 0x30


'''
