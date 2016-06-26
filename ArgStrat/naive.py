from ArgStrat.powerset import powerset
from ArgStrat.framework import * 
import time


class Simple: # Simple strategy class
	AF = None
	S = []
	pos = 0

	def __init__(self,AF,S,pos=0):
		self.S = list(S)
		self.AF = AF
		self.pos = int(pos)

	def __str__(self):
		return str(self.S)

	def __repr__(self):
		return list(self.S)

	def getArgs(self):	# returns the set of arguments in S 
		args = set([])
		for move in self.S:
			args |= set(move)
		return args

	def play(self,D):	# returns the move given by S for dialogue state D
		if self.AF.isSuccessful(D) or self.pos >= len(self.S):
			return []

		move = self.S[self.pos]
		self.pos += 1

		return move

	def copyOf(self):	# returns a copy of the dialogue.
		return Simple(self.AF,list(self.S),int(self.pos))

	def csvFriendly(self):
		return str([["{"] + [a for a in M] + ["}"] for M in self.S]).translate(None,"',[]")


class Dialogue:	# Dialogue object
	D = []
	args = []

	def __init__(self,D=[],args=[]):
		self.D = list(D)
		self.args = list(args)

	def __str__(self):
		return str(self.D)

	def __repr__(self):
		return str(self.D)

	def copyOf(self):
		return Dialogue(list(self.D),list(self.args))

	def add(self,M):
		self.D += [M]
		self.args += set(M)

	def getArgs(self):
		args = set([])
		for move in self.D:
			args |= set(move)
		return args
		return list(set(self.args))

	def isTerminated(self):
		k = len(self.D)
		if k < 2:
			return False
		else:
			return self.D[k-1] == [] and self.D[k-2] == []



def getStrategies(Prop): 	# generates a list of all possible sequences for simple strategies

	used = []
	unused = [([],set([]))]

	while True:
		if unused == []:
			break

		(S, args) = unused.pop(0)

		used += [(S, args)]

		possible_moves = powerset(Prop.getKnowledge()-args, min_size=1) 

		for move in possible_moves:
			new_S = S + [set(move)]
			new_args = args | set(move)

			unused += [(new_S,new_args)]

	return [S for (S,args) in used]



def simulate(Opp,AF,strategy):	# Simulates all possible dialogues of strategy S against Opp
	D_empty = Dialogue()
	S = strategy.copyOf()

	dialogue_queue = [(S,D_empty)]

	ineffective = None
	while not dialogue_queue == []:

		# pop first open dialogue
		(S,D) = dialogue_queue.pop()

		# do nothing if terminated
		if D.isTerminated():
			if AF.isSuccessful(D.getArgs()):
				continue	# dialogue is terminated and successful (do not push to queue but search continues)
			else:
				ineffective = D 	# D is terminated and unsuccessful (search over)
				break


		# add proponent move
		else:
			prop_move = S.play(D.getArgs())
			D.add(prop_move)


		# do nothing if terminated
		if D.isTerminated():
			if AF.isSuccessful(D.getArgs()):
				continue 	# dialogue is terminated and successful (do not push to queue but search continues)
			else:
				ineffective = D 	# D is terminated and unsuccessful (search over)
				break


		# add all possible opponent moves (no repeated arguments)
		else:
			K = Opp.getClosure().get(Opp.getKnowledge() | set(D.getArgs()))
			possible_moves = powerset(K-set(D.getArgs()),min_size=0)

			for opp_move in possible_moves:
				D1 = D.copyOf()
				D1.add(opp_move)
				S1 = S.copyOf()
				dialogue_queue += [(S1,D1)]

	return ineffective


def verify(opponent_model, AF, strategy):
	success_count = 0
	for Opp in opponent_model.getModels():
		# get unsuccessful dialogue or None
		D = simulate(Opp,AF,strategy)

		if D == None:
			# effective strategy found
			success_count += opponent_model.probability(Opp)

	return success_count



def naive(AF, Prop, opponent_model,show_output = True,timeout=None):
	# Generate list of all proponent (simple) strategies
	strategies = getStrategies(Prop)
	if show_output: print "Total simple strategies:", len(strategies)

	# Simulate all proponent (simple) strategies
	# Depth-first-search for unsuccessful dialogue
	winning_strategy = Simple(AF,[])
	success_best = 0
	start = time.time()
	for seq in strategies:

		if not timeout == None and time.time()-start > timeout:
			print "\nTimeout Error! Unable to complete search."
			break

		if show_output: print "\nChecking Strategy:", seq 

		# instantiate proponent strategy
		S = Simple(AF,seq)

		# check each opponent model
		success_count = 0
		i = 0
		for Opp in opponent_model.getModels():
			i += 1
			if show_output: print "Model", i, ":", 

			# get unsuccessful dialogue or None
			D = simulate(Opp,AF,S)

			if D == None:
				# effective strategy found
				success_count += opponent_model.probability(Opp)
				if show_output: print "Effective!"
			else:
				# found unsuccessful dialogue
				if show_output: print "Ineffective! (fails in", D, ")"

		if show_output: print "Success rate: ({0}/{1})".format(success_count,len(opponent_model))

		if success_count > success_best:
			if show_output: print "New best strategy found!"
			winning_strategy = S
			success_best = int(success_count)

		if success_count == len(opponent_model):
			if show_output: print "Optimal strategy found!"
			#break

	end = time.time()

	return winning_strategy, success_best, round(end-start,5)



	

















