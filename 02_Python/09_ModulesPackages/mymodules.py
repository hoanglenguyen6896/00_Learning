'''
def my_func():
	print('This is my_func')

print('Top level')

if __name__ == '__main__':
	print('Running Directly')
else:
	print('Being import')
'''

# Irl

def my_func():
	print('This is my_func')

def func1():
	pass
def func2():
	pass

if __name__ == '__main__':
	func1()
	func2()