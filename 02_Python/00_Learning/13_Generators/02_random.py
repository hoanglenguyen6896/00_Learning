import random

def rand_num(low, high, n):
    for num in range(0,n):
        yield random.randint(low, high)

if __name__ == '__main__':
    for num in rand_num(1,10,12):
        print(num)