usecols = [
	'name',
	'age',
	'email',
]
df = pd.read_csv('users.csv', usecols=usecols)
