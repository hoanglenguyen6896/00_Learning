from collections import Counter

mylist = [1,1,1,1,1,2,2,2,2,2,3,3,3,3,3]

print(f"{'':=^80}")
new_list = Counter(mylist)
print(new_list[1])
print(list(new_list))
print(f"{'':=^80}")

print(f"{'':=^80}")
new_list_char = Counter('AanscabscBCBAsc')
print(new_list_char)
print(new_list_char['a'])
print(list(new_list_char))
print(f"{'':=^80}")

print(f"{'':=^80}")
new_list_word = Counter("Hello Hi I am I me you, Hello, Hi, hi".split())
print(new_list_word)
print(f"{'':=^80}")

from collections import defaultdict
print(f"\n{'Normal dictionaries':=^80}")
d = {'a':10}

print(d)

print(f"\n{'Default dictionaries':=^80}")
# Create a default dict, must like below in my knowledge till June 20 2021
d = defaultdict(lambda: 0)
# add a key and value
d['correct'] = 100
print(d)
# call a wrong key
print(d['kekek'])
print(d)

print(f"\n{'Tuple':=^80}")
my_tuple = (12,23,34)
print(my_tuple[1])

from collections import namedtuple

Dog = namedtuple('Dog', ['age', 'breed', 'name'])
print(Dog)

Sammy = Dog(5, 'Husky', 'Sam')

print(Sammy)
print(Sammy.age)
print(Sammy[0])