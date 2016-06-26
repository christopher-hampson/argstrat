import itertools

def powerset(X,min_size=0,max_size=None):
	# returns the set of all subsets of X
	# of size between min_size and max_size

	powerset = []

	if max_size==None:
		max_size = len(X)

	for k in range(min_size,max_size+1):
		for z in itertools.combinations(X,k):
			powerset.append(list(z))

	return powerset
