from ArgStrat.argparser import *	# parses input
from ArgStrat.framework import *	# defined AF classes and semantics
from ArgStrat.agent_models import *	# defined opponent model
from ArgStrat.powerset import powerset
from ArgStrat.argplanning import getStrategy	# parses output
from PDDLgen.pddlgen import *	# generates pddl files
from ArgStrat.naive import *	# naive algorithm

from results.writesql import write_to_file

import sys
from datetime import date


run_date = str(date.today())


# Set example file
if len(sys.argv) > 2:
	example_file = sys.argv[1]
	size = int(sys.argv[2])
else:
	raise Exception("Input filename or size not supplied. See README.md for more informtaion.")
	quit()

for i in range(50):
	# Open example file.
	try:
		f = open(example_file)
	except:
		raise IOError("File {0} not found.".format(example_file))
		quit()

	# Parse input 
	p = Parser(f.read())
	p.parse()

	# catch size errors
	K_opp = p.getOpponentArgs()
	max_size = 2**len(K_opp)
	if size > max_size:
		raise Exception("Size {0} exceeds maximum {1}.".format(size,max_size))
		quit()

	print "\n###############################"
	print "## Example {0} - size {1} - round {2} ###\n".format(p.getTitle(),size,i)

	

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
	opponent_model = getUniformModel(K_opp,size)		


	results = {}
	winning_strategy = {'planner':None, 'naive':None}
	search_time = {'planner': 0, 'naive':0}
	success_rate = {'planner': 0, 'naive':0}

	# Generate PDDL
	problem_file = "temp.pddl"
	print "Generating PDDL...",
	sys.stdout.flush()
	generatePDDL(problem_file, AF, Prop, opponent_model)
	print "done\n"

	# Run planner
	domain_file = "./PDDLgen/domain.pddl"
	print "Running planner...",
	sys.stdout.flush()
	results = getStrategy(domain_file, problem_file, show_output=False)
	winning_strategy['planner'] = Simple(AF,results[0])
	success_rate['planner'] = results[1]
	search_time['planner'] = results[2]
	print "done"


	# Run naive search
	print "Running naive search...",
	sys.stdout.flush()
	results = naive(AF, Prop, opponent_model, show_output=False,timeout = 3600)
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


	# Write to DB
	planner_data = [str(winning_strategy['planner']), search_time['planner'], success_rate['planner']]
	naive_data = [str(winning_strategy['naive']), search_time['naive'], success_rate['naive']]

	write_to_file('./results/results.sqlite',run_date,AF,opponent_model,planner_data,naive_data)


