import math

value = 4.45
print(f"{'round':=^80}")
print(math.floor(value))
print(math.ceil(value))
print(round(value))
print(round(4.5))
print(round(5.5))

print(f"\n{'specical num':=^80}")
print(math.pi)
print(math.e)
print(math.inf)
print(math.nan)

print(f"\n{'logarite':=^80}")
print(math.log(math.e)) # Base e
print(math.log(10))
print(math.log(100,10)) # Base 10

print(f"\n{'angle, sin, cos, ...':=^80}")
print(math.sin(math.pi/6))
print(math.degrees(math.pi/2))

print(f"\n{'degree > radian':=^80}")
print(math.radians(180))

import random

print(f"\n{' random ':=^80}")
print(random.randint(0, 100))

# print(f"\n{' random with seed ':=^80}")
# random.seed(101)
# print(random.randint(0, 100))
# print(random.randint(0, 100))
# print(random.randint(0, 100))
# print(random.randint(0, 100))
# print(random.randint(0, 100))
# print(random.randint(0, 100))

print(f"\n{' random from a list ':=^80}")
# get a random value, list stay same
mylist = list(range(0,21))
print(random.choice(mylist))
# a value in list can be chosen many times, return list 10 value
print(random.choices(population = mylist, k = 10))
# a value can be chosen only once, return list 10 value
print(random.sample(population = mylist, k = 10))
# shuffle list, affect the list
random.shuffle(mylist)
print(mylist)

# random a number, can be float
print(random.uniform(a = 0, b = 100))

# random gauss < what is this?
print(random.gauss(mu = 0, sigma = 1))