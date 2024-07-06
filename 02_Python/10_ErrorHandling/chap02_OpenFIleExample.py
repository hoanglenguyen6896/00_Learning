try:
	f = open('testFile', 'r')
	f.write('Write a line')
except TypeError:
	print("There was type error!")
except OSError:
	print("Hey OS Error!")
except:
	# All other than these exeptions above
	print('All other exceptions!!!!')
finally:
	# Always run
	print("I always run")
