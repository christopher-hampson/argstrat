import random
import itertools
from ArgStrat.powerset import powerset

class ArgFrame:

	def __init__(self,Args,Attacks,name = ""):
		self.name = name
		self.Args = list(Args)
		self.Attacks  = list(Attacks)
		self.goals = []
		self.success = None


	def __repr__(self):
		return "< {" + str(self.Args)[1:-1] + "}, {" + str(self.Attacks)[1:-1] + "} >"

	def getArgs(self):
		return self.Args

	def getAttacks(self):
		return self.Attacks

	def setGoals(self,goals):
		try:
			self.goals = list(goals)
		except:
			self.goals = []

	def getGoals(self):
		return self.goals

	def setName(self,name):
		self.name = name

	def getName(self):
		return self.name

	def buildSuccess(self,semantics):
		X = powerset(self.Args)
		Y = []
		for A in X:
			subAF = self.subframe(A)

			for g in self.goals:
				if not g in semantics(subAF).In:
					Y += [A]
					continue

		self.success = [set(A) for A in X if A not in Y]

	def isSuccessful(self,X):
		return set(X) in [set(Y) for Y in self.success]

	def getSuccess(self):
		return self.success


	def subframe(self,X):
		Args = set(self.Args)
		X = set(X)
		Y = Args.intersection(X)
		S = [(a,b) for a in Y for b in Y if (a,b) in self.Attacks]
		return ArgFrame(Y,S)

	def copy(self):
		# creates a copy of the AF
		return ArgFrame(self.Args,self.Attacks)

	def attacks(self,a,b):
		# returns true if (a,b) in Attacks
		return (a,b) in self.Attacks

	def get_attacked_by(self,a):
		attacked_by = []
		for b in self.Args:
			if attacks(b,a):
				attacked_by.append(b)
		return attacked_by


	def add_new_edge(self,edges):
		#adds a random edge from 'edges' that doesn't already exist
		if len(edges)>0:
			random_edge = random.choice(edges)
			if random_edge in self.Attacks:
				new_edges = edges
				self.add_new_edge(new_edges)
			else:
				self.Attacks.append(random_edge)


	def add_dag_edge(self):
		# adds a random 'upstream' directed edge (i,j) for i>j
		n = len(self.Args)
		possible_edges = []
		for i in range(n):
			for j in range(i):
				possible_edges.append((self.Args[i],self.Args[j]))
		self.add_new_edge(possible_edges)


	def add_cycle_edge(self):
		# adds a random 'downstream' directed edge (j,i) for j<i
		n = len(self.Args)
		possible_edges = []
		for i in range(n):
			for j in range(i):
				possible_edges.append((self.Args[j],self.Args[i]))
		self.add_new_edge(possible_edges)

	def add_self_attack_edge(self):
		# adds a random self-attack edge (i,i)
		n = len(self.Args)
		possible_edges = []
		for i in range(n):
			possible_edges.append((self.Args[i],self.Args[i]))
		self.add_new_edge(possible_edges)


def new_random_AF(Args,dag_density,cycle_density,self_attack_density):
	#generates a new random argumentation framework of size 'size'

	size = len(Args)
	Attacks = []

	A = ArgFrame(Args,Attacks)

	dag_number = int(math.floor(triangle_number(size-1)*dag_density))
	for i in range(dag_number):
		A.add_dag_edge()

	cycle_number = int(math.floor(triangle_number(size-1)*cycle_density))
	for i in range(cycle_number):
		A.add_cycle_edge()

	loop_number = int(math.floor(size*self_attack_density))
	for i in range(loop_number):
		A.add_self_attack_edge()

	return A




def triangle_number(n):
	# returns the nth triangular number
	return (n*(n+1)/2)



class Semantics:
	def __init__(self,In,Out,Undec):
		self.In = set(In)
		self.Out = set(Out)
		self.Undec = set(Undec)

	def putIn(self,a):
		In = self.In
		self.In = set(In).union(set([a]))

	def putOut(self,a):
		Out = self.Out
		self.Out = set(Out).union(set([a]))

	def putUndec(self,a):
		Undec = self.Undec
		self.Undec = set(Undec).union(set([a]))

	def isIn(self,a):
		return a in self.In

	def isOut(self,a):
		return a in self.Out

	def isUndec(self,a):
		return a in self.Undec

	def isLabelled(self,a):
		return self.isIn(a) | self.isOut(a) | self.isUndec(a)

	def clone(self):
		return Semantics(self.In,self.Out,self.Undec)

def grounded(A):

	G = Semantics([],[],[])

	updated = True
	while updated:

		updated = False

		#Set T:=G
		T = G.clone()

		for a in A.Args:
			if not G.isLabelled(a):

				makeIn = True
				makeOut = False

				for b in set(A.Args):
					if A.attacks(b,a) and T.isIn(b):
						# Out(a) iff (exists b) R(b,a) & In(b) 
						makeOut = True	

					if A.attacks(b,a) and not T.isOut(b):
						#  In(a) iff (forall b) R(b,a) -> Out(b)
						# !In(a) iff (exists b) R(b,a) & !Out(b)
						makeIn = False

				if makeIn:
					G.putIn(a)
					updated = True

				if makeOut:
					G.putOut(a)
					updated = True

	for a in A.Args:
		if not G.isLabelled(a):
			# Undec(a) iff !In(a) & !Out(a)
			G.putUndec(a) 

	return G

