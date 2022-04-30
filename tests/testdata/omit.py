usecols = [
	'name',
	'age',
	'email',
]
df = pd.read_csv('./testdata/users.csv', usecols=usecols)
