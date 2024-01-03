def function_1(n):
    return [str(num) for num in range(n)]

print(function_1(10))

def function_2(n):
    return list(map(str, range(n)))

print(function_2(10))


# Method 1: Not accurate with short and fast function
import time

start = time.time()

result = function_1(10000)

end = time.time()

print(end - start)

start = time.time()

result = function_2(10000)

end = time.time()

print(end - start)

# Method 2: timeit
import timeit
stmt = """
function_1(100)
"""
setup ="""
def function_1(n):
    return [str(num) for num in range(n)]
"""
timediff = timeit.timeit(stmt, setup, number=100000)
print(timediff)

stmt2 = """
function_2(100)
"""
setup2 ="""
def function_2(n):
    return list(map(str, range(n)))
"""
timediff = timeit.timeit(stmt2, setup2, number=100000)
print(timediff)