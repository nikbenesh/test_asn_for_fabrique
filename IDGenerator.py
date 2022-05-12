def generateID(filename='ids.csv'):
	try:
		with open(filename, 'r') as file:
			ids = file.read().split(',')
			if (ids == ['']):
				raise FileNotFoundError
			id = int(ids[-1]) + 1
			ids.append(str(id))
	except FileNotFoundError as err:
		id = 1
		ids = [str(id)]
	file = open(filename, 'w')
	file.write(','.join(ids))
	file.close()
	return id

