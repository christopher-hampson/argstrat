from ArgStrat.argparser import *	# parses input
from ArgStrat.framework import *	# defined AF classes and semantics
from ArgStrat.agent_models import *	# defined opponent model
from ArgStrat.powerset import powerset
from ArgStrat.argplanning import getStrategy	# parses output

from PDDLgen.pddlgen import *	# generates pddl files
from ArgStrat.naive import *	# naive algorithm

import sys


# Default files and directories
example_dir = "./examples/"
output_file = "./results_new.csv"


# Set example file
example_file = "ECAI-example.txt"
example_file = raw_input("Please enter problem file: ") or example_file
try:
	f = open(example_dir + example_file)
except:
	print "Error! File not found."
	quit()

# Parse input 

print "Parsing input file...",
sys.stdout.flush()
p = Parser(f.read())
p.parse()
print "done"


# Framework
Args = p.getArgs()
Attacks = p.getAttacks()
AF = ArgFrame(Args,Attacks, name = p.getTitle())


# Find successful states
print "Building successful states...",
sys.stdout.flush()
AF.setGoals(p.getGoals())
AF.buildSuccess(grounded)
print "done"


# Proponent model
K_prop =  p.getProponentArgs()
Prop = Agent(K_prop)


# Opponent model
K_opp = p.getOpponentArgs()

if p.getRules():
	mu = ClosureFunction(p.getRules())
else:
	mu = ClosureFunction([])

opponent_model = OpponentModel()
for (K,p) in p.getOpponentModel():
	Ag = Agent(K,mu)
	opponent_model.add_model(Ag,p)

print opponent_model


# Generate PDDL
problem_file = example_dir + example_file[:-3] + "pddl"
print "Generating PDDL...",
sys.stdout.flush()
generatePDDL(problem_file, AF, Prop, opponent_model)
print "done"



winning_strategy = {'planner':None, 'naive':None}
search_time = {'planner': 0, 'naive':0}
success_rate = {'planner': 0, 'naive':0}

# Run planner
domain_file = "./PDDLgen/domain.pddl"
print "Running planner...",
sys.stdout.flush()
results = getStrategy(domain_file, problem_file, show_output=True)

#print results
winning_strategy['planner'] = Simple(AF,results[0])
success_rate['planner'] = results[1]
search_time['planner'] = results[2]
print "done\n"


# Run naive search
print "Running naive search...",
sys.stdout.flush()
results = naive(AF, Prop, opponent_model, show_output=False)
winning_strategy['naive'] = results[0]
success_rate['naive'] = results[1]
search_time['naive'] = results[2]
print "done\n"



print "#### Results ####"
print "Planner : {0} ({1}/{2})".format(winning_strategy['planner'],success_rate['planner'],opponent_model.totalProbability())
print "  -- Search Time: {0}s".format(round(search_time['planner'],3))
print "Naive   : {0} ({1}/{2})".format(winning_strategy['naive'],success_rate['naive'],opponent_model.totalProbability())
print "  -- Search Time: {0}s".format(round(search_time['naive'],3))

if success_rate['planner'] < success_rate['naive']:
	print "~~~ SUBOPTIMAL PLAN FOUND ~~~"
	#quit()

if search_time['planner'] < search_time['naive']:
	print "~~~ WINNER : Planner ~~~"
else:
	print "~~~ WINNER : Naive ~~~"


quit()
# Write to DB
planner_data = [str(winning_strategy['planner']), success_rate['planner'], search_time['planner']]
naive_data = [str(winning_strategy['naive']), success_rate['naive'], search_time['naive']]

write_to_file('test.sqlite',AF,planner_data,naive_data)