usecols = [
	'name',
	'age',
	'email',
	# 'address',
	# 'phone',
]
df = pd.read_csv('./testdata/users.csv', usecols=usecols)
