def ask_for_int():
	try:
		result = int(input('Enter a integer: '))
	except:
		print('Error! That not a integer')
	else:
		print(result)
	finally:
		print('End of try/except/finally')

def ask_loop():
	while True:
		try:
			resultLoop = int(input('Enter a integer: '))
		except:
			print('Error! That not a integer')
			continue
		else:
			print(resultLoop)
			break
		finally:
			print('End of try/except/finally')
			print('Always write in the end of try/except even have break')

ask_loop()