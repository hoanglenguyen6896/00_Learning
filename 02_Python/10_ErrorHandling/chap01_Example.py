def add(n1, n2):
	print(n1 + n2)

add(10, 20)

number1 = 10
number2 = input('Enter a number: ')

# add(number1, number2)

try:
	# Do something
	# May have an error
	result = 10 + 10
	#result = 10 + '10'
except:
	print("Looks error")
else:
	print(result)