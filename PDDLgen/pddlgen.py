from ArgStrat.framework import *
from ArgStrat.indexer import Indexer
from ArgStrat.powerset import powerset


def generatePDDL(filename, AF,  Prop, model): # Generates the PDDL specificatation
	I = Indexer(AF.getArgs())	# assigns a label to each subset of AF.getArgs()

	with open(filename,"w") as f:

		## Domain
		f.write("(define (problem temp)\n")
		f.write("    (:domain StrategicArgumentation)\n")

		## Objects
		f.write("    (:objects {0} - arg\n".format(str(AF.getArgs()).translate(None,",[]'")))

		# Objects (proponent sets)
		f.write("              ")
		for S in powerset(Prop.getArgs()):
			f.write("S{0} ".format(I.getIndex(S)))
		f.write("- setOfArgsP\n")

		# Objects (opponent sets)
		f.write("              ")
		for T in powerset(model.getArgs()):
			f.write("T{0} ".format(I.getIndex(T)))
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
				if AF.isSuccessful(set(S) | set(T)):
					f.write("           (successful S{0} T{1})		; ({2}, {3})\n".format(I.getIndex(S),I.getIndex(T),S,T))

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

				f.write("           (addP {0} S{1} S{2})		; {0} + {3} = {4}\n".format(a,I.getIndex(S1),I.getIndex(S2),S1,S2))

		f.write("\n")


		## Add for opponent args
		for T1 in powerset(model.getArgs(),min_size=0):
			for T2 in powerset(model.getArgs()):
				T3 = list(set(T1) | set(T2))

				f.write("           (addO T{0} T{1} T{2})		; {3} + {4} = {5}\n".format(I.getIndex(T1),I.getIndex(T2),I.getIndex(T3),T1,T2,T3))

		f.write("\n")


		## Closure
		for Opp in model.getModels():
			for S in powerset(Prop.getArgs()):
				known_args = Opp.getArgs() | set(S)
				inferred_args = Opp.getClosure().get(known_args).difference(S)

				for T in powerset(inferred_args,min_size=0):
						f.write("           (canAssertO T{0} A{1} S{2})		; A{1}: {3} -> {4}\n".format(I.getIndex(T),model.getID(Opp),I.getIndex(S),S,T))


		f.write("    )\n\n")
		f.write("    (:goal (> (prob-of-success) 0))\n\n")
		
		f.write("    (:metric maximize (prob-of-success) )\n")
		f.write(")")

