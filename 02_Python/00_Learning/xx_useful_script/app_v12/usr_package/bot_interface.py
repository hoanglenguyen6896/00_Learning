import socket
import time
from colorama import Fore

HEAD            = b'\xAA'
DEBUG_MOVE      = b'\x27'

DEBUG_MV_LEN        = 22
DEBUG_MV_SPEED      = b'\xE8\x03\x00\x00'       # 0.1 m/s (Default)
DEBUG_MV_FW         = b'\x00'                   # Move FW
DEBUG_MV_BW         = b'\x01'                   # Move BW
DEBUG_MV_ACC        = b'\x02'                   # 0.2 m/s^2 (Default)
DEBUG_MV_DEC        = b'\x02'                   # 0.2 m/s^2 (Default)

DEBUG_HARD_READ_FLOOR = b'\xAA\x18\x00\x00\x00\x00\x00\x01\x00\x00\x37'
DEBUG_HARD_READ_CEILING = b'\xAA\x18\x00\x00\x00\x00\x00\x01\x00\x01\x06'

cmd = {""}

# return CRC (int)
# To convert to byte use bytes([a]) (not byte(a), this will return a bytearray's length is a)
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

def read_floor(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 2096))
    time.sleep(1)
    s.sendall(DEBUG_HARD_READ_FLOOR)
    time.sleep(1)

    s.shutdown(socket.SHUT_WR)
    s.close()

def read_ceiling(ip):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ip, 2096))
    time.sleep(1)
    s.sendall(DEBUG_HARD_READ_CEILING)
    time.sleep(1)

    s.shutdown(socket.SHUT_WR)
    s.close()

# Move cmd
# HEAD (1) + MOVE (1) + Random bytes (8) + SPEED (4) + DISTANCE (4) + DIRECTION (1) + ACC (1) + DEC (1) + CRC (1)
def debug_move(ip, direction, distance):
    try:
        mov_head    = HEAD
        mov_cmd     = DEBUG_MOVE
        mov_ran8    = b'\x00\x00\x00\x00\x00\x00\x00\x00'
        mov_spd     = DEBUG_MV_SPEED
        # Calculate distance here
        # mov_dist
        if float(distance) > 0.5:
            decision = input(f"Are you sure to move {distance} meters?")
            if decision.upper() != 'Y':
                print(Fore.YELLOW + f"Move {distance} {direction} ABORT")
                return -1
        mov_dist = (int(float(distance)*10000)).to_bytes(4, byteorder = 'little')
        # Calculate direction
        if direction.upper() == 'F':
            mov_dir = DEBUG_MV_FW
        elif direction.upper() == 'B':
            mov_dir = DEBUG_MV_BW
        mov_acc = DEBUG_MV_ACC
        mov_dec = DEBUG_MV_DEC
        mov_cmd_without_crc = mov_head + mov_cmd + mov_ran8 + mov_spd + mov_dist + mov_dir + mov_acc + mov_dec
        if len(mov_cmd_without_crc) != DEBUG_MV_LEN - 1:
            print(Fore.RED + f"Move {distance} {direction} ERROR - cmd_len")
            return -1
        else:
            # print(cal_crc(mov_cmd_without_crc))
            mov_cmd_crc = mov_cmd_without_crc + bytes([cal_crc(mov_cmd_without_crc)])
        # print(str(mov_cmd_crc))

        # execute move cmd
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 2096))
        time.sleep(0.25)
        s.sendall(mov_cmd_crc)
        # time.sleep(1)
        # s.sendall(DEBUG_HARD_READ_FLOOR)
        time.sleep(0.25)
        s.shutdown(socket.SHUT_WR)
        s.close()

    except Exception as e:
        print(e)
        print(Fore.RED + f"Move {distance} {direction} ERROR - except")


def rotate_180_CW_and_read_floor(ip):
    try:
        rotate_180_CW = b'\xAA\x28\x00\xD1\x92\x5C\x72\x06\x00\x01\x02\xD0\x07\x00\x00\xCD'
                      # b'\xAA\x29\x00\x4F\x9E\xDE\x51\x0A\x00\x01\x40\x77\x1B\x00\x04\xD0\x07\x00\x00
                      # AA29004F9EDE510A000140771B0004D0070000
                      # AA280050DE0D5206000102D0070000
        read_fc = b'\xAA\x18\x00\xCF\x82\xE1\x6F\x01\x00\x00\xF2'
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 2096))
        time.sleep(0.25)
        s.sendall(rotate_180_CW)
        time.sleep(5)
        s.sendall(read_fc)
        time.sleep(0.25)

        s.shutdown(socket.SHUT_WR)
        s.close()
        # print("Rotate done!!!!")
        return ("Rotate done!!!!", 1)
    except:
        # print("Rotate and read floor error!!!!")
        return ("Rotate and read floor error!!!!", -1)

if __name__ == '__main__':
    pass
    # IP = "172.17.35.20"