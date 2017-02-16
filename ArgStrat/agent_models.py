from ArgStrat.powerset import powerset
import random
import sys



class ClosureFunction:	# Closure function object

	rules = {}

	def __init__(self,rules=[]):
		self.rules = {}

		for r in rules:
			self.add_rule(r[0],r[1])

	def __repr__(self):
		return str(self.rules)

	def add_rule(self,body,head):
		# incorporate rule into closure operator
		self.rules[tuple(set(body))] = set(head)

	def all_inferences(self):
		# returns all possible inferences
		inf = set([])
		for body in self.rules:
			inf |= self.rules[body]
		return inf

	def get(self,X):
		# get closure of X
		Y = set(X)
		for body in self.rules:
			if set(body).issubset(Y):
				Y |= self.rules[body]
	
		if Y == X:
			return X
		else:
			return self.get(Y)

class Agent: 
	K = set([])
	mu = ClosureFunction()

	def __init__(self,K,mu=None):
		self.K = set(K)
		if mu:
			self.mu = mu
		else:
			self.mu = ClosureFunction()

	def __repr__(self):
		return str((list(self.K),self.mu))

	def getClosure(self):
		return self.mu

	def getKnowledge(self):
		return self.K

	def getArgs(self):
		return self.K


class OpponentModel:
	model = {}
	model_size = 0
	ID = None

	def __init__(self):
		self.model = {}
		self.size = 0
		self.ID = None

	def __repr__(self):
		return str(dict([(X,round(self.model[X],2)) for X in self.model]))

	def addID(self,ID):
		self.ID = str(ID)

	def get_seed(self):
		return self.ID

	def totalProbability(self):
		total_prob = 0
		for Opp in self.model:
			total_prob += self.model[Opp]
		return total_prob


	def getArgs(self):
		args = set([])
		for Opp in self.model:
			inf = Opp.getClosure().all_inferences()
			args |= Opp.getArgs()
			args |= inf
		return args

	def getID(self,Opp):
		if Opp not in self.model:
			return 0
		else:
			return self.model.keys().index(Opp)


	def getModels(self):
		return sorted(self.model.keys())

	def __len__(self):
		return self.model_size

	def probability(self,Opp):
		if not Opp in self.model:
			return 0
		else:
			return self.model[Opp]

	def add_model(self,Opp,p):
		if not Opp in self.model:
			self.model[Opp] = p
			self.model_size += 1
		else:
			self.model[Opp] = p

	def standardise(self,accuracy=2):
		# make all probabilities integers
		self.normalise()
		factor = 10**accuracy

		for Opp in self.model:
			self.model[Opp] = int(round(self.model[Opp]*factor,0))

	def normalise(self):
		# normalise total probability to 1
		total_prob = self.totalProbability()

		for Opp in self.model:
			self.model[Opp] = float(self.model[Opp])/total_prob




def getUniformModel(Args,size,seed=None): # generates a random uniform opponent model of given size
	M = OpponentModel()

	all_models = powerset(Args)

	# get random seed:
	if not seed:
		seed = random.randint(0,sys.maxint)

	M.addID(seed)
	random.seed(seed)

	if size > len(all_models) or size==None:
		selection = all_models
	else:
		selection = random.sample(all_models,size)

	i = 0
	for K in selection:
		Opp = Agent(K)
		M.add_model(Opp,1)
		i += 1

	#M.normalise()
	return M


def getUniformModelwithClosure(Args,size,seed=None,K_prop=[],closure_size=1): # generates a random uniform opponent model of given size
	M = OpponentModel()

	all_models = powerset(Args)

	# get random seed:
	if not seed:
		seed = random.randint(0,sys.maxint)

	M.addID(seed)
	random.seed(seed)

	if size > len(all_models) or size==None:
		selection = all_models
	else:
		selection = random.sample(all_models,size)

	mu = getRandomClosure(K_prop,Args,size=closure_size)
	i = 0
	for K in selection:	
		Opp = Agent(K,mu)
		M.add_model(Opp,1)
		i += 1

	#M.normalise()
	return M


def getRandomClosure(A,B,size=0):
	rules = []
	for i in range(size):
		try:
			body = [random.choice(A)]
			head = [random.choice(B)]
			rules += [(body,head)]
		except:
			rules += []

	return ClosureFunction(rules)
