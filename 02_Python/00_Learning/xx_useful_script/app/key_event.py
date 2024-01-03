import keyboard
import time

# jump_to_cmd = False

# while True:
#     if keyboard.read_key() == 'c':
#         jump_to_cmd = True

#     if jump_to_cmd == True:
#         while True:
#             usr_input = input('Enter something here: ')

def pop_list(list_testing):
    list_testing.pop()

list1 = [1,3,4,5,6]
pop_list(list1)
print(list1)

d = {1:1, 2:2}

print(d[3])