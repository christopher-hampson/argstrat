from argumentation.framework import *
import time
import datetime
import sys
import itertools
import subprocess
from parser import *
from parser.argparser import Parser
import numpy as np
import cProfile as cp
from misc.math import powerset
import re
import indexer

def normalise(line,width): 	# places final box marker for formatting
	for k in range(len(line),width):
			line += " "

	line += "%%\n"

	return line


def natural_split(name,X,width): # creates a natural split in formatting of long lists

	line_list = []

	line = "; %% " + str(name) + " = "

	white_space = len(str(name)) + 4

	for i in range(len(X)):

		if len(line+str(X[i]).translate(None,"[]'")) < width-1:
			line += str(X[i]).translate(None,"[]'")
		else:
			# push to list and make new line
			line_list.append(line)

			line = "; %%"

			for k in range(white_space):
				line += " "

			line += str(X[i]).translate(None,"[]'")

		if i<len(X)-1:
			# add comma if not last element
			line += ", "

	line_list.append(line)

	return line_list



def generatePDDL(filename, AF,  Prop, model): # Generates the PDDL specificatation
	I = Indexer(AF.getArgs())

	with open(filename,"w") as f:

		## Preamble
		ts = time.time()
		st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
		width = 100
		bar = str(["%" for i in range(0,width)]).translate(None," ,[]'")


		f.write("; " + bar + "\n")

		line = "; %% Example generated: {0}".format(st)

		f.write(normalise(line,width))
		f.write(normalise("; %%",width))

		for line in natural_split("Args",AF.getArgs(),width):
			f.write(normalise(line,width))

		for line in natural_split("Attacks",AF.getAttacks(),width):
			f.write(normalise(line,width))


		f.write(normalise("; %% Goals = {0}".format(AF.getGoals()),width))

		f.write("; " + bar + "\n\n\n")



		## Domain
		f.write("(define (problem temp)\n")
		f.write("    (:domain StrategicArgumentation)\n")

		## Objects
		f.write("    (:objects {0} - arg\n".format(str(AF.getArgs()).translate(None,",[]'")))

		# Objects (proponent sets)
		f.write("              ")
		for S in powerset(Prop.getArgs()):
			f.write("S{0} ".format(I.indexOf(S)))
		f.write("- setOfArgsP\n")

		# Objects (opponent sets)
		f.write("              ")
		for T in powerset(model.getArgs()):
			f.write("T{0} ".format(I.indexOf(T)))
		f.write("- setOfArgsO\n")

		
		# Objects (Agents)
		f.write("              ")
		for Opp in model.getModels():
			f.write("A{0} ".format(model.getID(Opp)))
		f.write("- agent )\n\n")

		## Initial Conditions
		f.write("    (:init (= (stage) 0)\n\n")

		## Can Assert
		for a in Prop.getArgs():
			f.write("           (canAssertP {0})\n".format(a))

		f.write("\n")


		## Oppenent Model
		for Opp in model.getModels():
			f.write("           (= (prob-belief A{0}) {1})\n".format(model.getID(Opp),model.probability(Opp)))


		## Probability of Success
		f.write("\n           (= (prob-of-success) 0)\n\n")


		## Successful Dialogues
		for S in powerset(Prop.getArgs()):
			for T in powerset(model.getArgs()):

				indexS = I.indexOf(S) #getIndex(Prop.getArgs(),S)
				indexT = I.indexOf(T) # getIndex(model.getArgs(),T)

				if AF.isSuccessful(set(S) | set(T)):
					f.write("           (successful S{0} T{1})".format(indexS,indexT))
					f.write("           ; " + str(S) + ", " + str(T) + "\n")


				'''sub_args = set(CommonKnowledge + S + T)		#set of arguments at end of dialogue

				subframe = frame.subframe(sub_args)


				if acceptable(subframe,goals):
					f.write("           (successful S{0} T{1})".format(indexS,indexT))
					f.write("           ; " + str(S) + ", " + str(T) + "\n")'''


		f.write("\n")


		## Dialogue
		f.write("           (dialogueP S0)\n")
		for Opp in model.getModels():
			f.write("           (dialogueO A{0} T0)\n".format(model.getID(Opp)))

		f.write("\n")


		## Add for proponent args
		for a in Prop.getArgs():
			for S1 in powerset(Prop.getArgs()):
				S2 = list(set(S1) | set([a]))

				f.write("           (addP {0} S{1} S{2})".format(a,I.indexOf(S1),I.indexOf(S2)))
				f.write("           ; " + str(a) + " + " + str(S1) + " = " + str(S2) +  "\n")

		f.write("\n")


		## Add for opponent args
		for T1 in powerset(model.getArgs(),min_size=0):
			for T2 in powerset(model.getArgs()):
				T3 = list(set(T1) | set(T2))

				f.write("           (addO T{0} T{1} T{2})".format(I.indexOf(T1),I.indexOf(T2),I.indexOf(T3)))
				f.write("           ; " + str(T1) + " + " + str(T2) + " = " + str(T3) +  "\n")

		f.write("\n")


		## Closure
		for Opp in model.getModels():
			for S in powerset(Prop.getArgs()):
				known_args = Opp.getArgs() | set(S)
				inferred_args = Opp.getClosure().get(known_args).difference(S)

				for T in powerset(inferred_args,min_size=0):
						f.write("           (canAssertO T{0} A{1} S{2})\n".format(I.indexOf(T),model.getID(Opp),I.indexOf(S)))
						f.write("           ; A{1}: {2} -> {0}\n".format(T,model.getID(Opp),S))


		f.write("    )\n\n")
		f.write("    (:goal (> (prob-of-success) 0))\n\n")
		
		f.write("    (:metric maximize (prob-of-success) )\n")
		f.write(")")


def getStrategy(domain_file, problem_file, planner_path="./rewrite-clp", show_output=False):	# Reads planner output and outputs strategy and data
	domain_file = str(domain_file)
	problem_file = str(problem_file)
	planner_path = str(planner_path)

	start = time.time()
	proc = subprocess.Popen([planner_path, '--optimise', domain_file, problem_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	plan_out = proc.communicate()[0]
	end = time.time()

	
	# Process output of planner
	strategy, move, metric = [], set(), 0
	reported_time = 0

	# write to backup
	with open('backup_plan.txt','a') as f:
		for line in plan_out.split("\n"):
			f.write(line + "\n")


	# Get strategy and metric
	for line in plan_out.split("\n"):
		if show_output: print line

		if "; Time" in line:
			reported_time = float(re.findall("; Time ([0-9]+.[0-9]+)",line)[0])

		if "Metric value" in line:
			metric = int(re.findall("; Metric value ([0-9]+)",line)[0])

		if "Solution Found" in line:
			strategy, move, metric = [], set(), 0

		if ": (proponent" in line:
			arg = re.findall("[0-9]+: \(proponent ([a-z0-9]+)\)",line)[0]
			move.add(arg)

		if "(opponent)" in line:
			strategy += [move]
			move = set([])

	return strategy, metric, round(end-start,5), round(reported_time,5)