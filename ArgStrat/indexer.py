

class Indexer:
	# Indexer is used to provide relative indices for subsets of AF (convenient hack)
	U = []
	size = 0

	def __init__(self,U):
		self.U = list(U)
		self.size = len(U)

	def getIndex(self,X):
		if not set(X)<=set(self.U):
			return None
		else:
			index = 0
			for i in range(self.size):
				if self.U[i] in X:
					index += 2**i
			return index
