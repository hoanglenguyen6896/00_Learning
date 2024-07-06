import time
import threading

def printx():
  time.sleep(1)
  for i in range(10):
    print(10/(5-i))
    time.sleep(1)

if __name__ == '__main__':
  a = int(input(1. ))
  # b = int(input(2. ))
  # c = int(input(3. ))

  if a == b == c == 2:
    print(1)