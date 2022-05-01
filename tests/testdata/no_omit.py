usecols = [
	'name',
	'age',
	'email',
	# 'address',
	# 'phone',
]
df = pd.read_csv('users.csv', usecols=usecols)
