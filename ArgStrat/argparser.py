import re
import sys

class Parser:

	def __init__(self, src):
		self.src = src
		self.pos = 0

		self.title = None
		self.args = None
		self.attacks = None
		self.proargs = []
		self.oppmodel = None
		self.ckargs = []
		self.goals = None
		self.rules = {}

	def getTitle(self):
		return self.title

	def getArgs(self):
		return self.args

	def getAttacks(self):
		return self.attacks

	def getGoals(self):
		return self.goals

	def getProponentArgs(self):
		return self.proargs

	def getOpponentArgs(self):
		return self.oppargs

	def getOpponentModel(self):
		return self.oppmodel

	def getCommonKnowledge(self):
		return self.ckargs

	def getRules(self):
		return self.rules




	def parse_ws(self,min_ws=0):
		# parse whitespace
		r_match = re.match("[\s]*", self.src[self.pos:])
		if r_match:
			if len(r_match.group(0))>=min_ws:
				self.pos += len(r_match.group(0))
			else:
				SyntaxError("Expecting at least {0} whitespace. Got only {1}".format(min_ws,len(r_match.group(0))))
		else:
			SyntaxError("Expecting whitespace. Got {0}".format(self.src[self.pos:self.pos+15]))


	def parse_regex(self,regex):
		# parses a given regex
		r_match = re.match(regex, self.src[self.pos:])		# find longest match of regex
		if r_match:
			self.pos += len(r_match.group(0))		# move position to end of match
			return r_match.group(0)					# return match
		else:
			raise SyntaxError("Expecting pattern {0}. Got {1}".format(regex, self.src[self.pos:self.pos+15]))


	def parse_int(self):
		# parses an interger
		r_match = re.match("[0-9]+", self.src[self.pos:])		# find longest match of regex
		if r_match:
			try:
				self.pos += len(r_match.group(0)) 	# move position to end of match
				return int(r_match.group(0))				# return match
			except ValueError:
				print("Integer value too large %d", r_match.group(0))
				return 0

		else:
			raise SyntaxError("Expecting integer. Got {0}".format(self.src[self.pos:self.pos+15]))



	def parse(self):
		#import pdb; pdb.set_trace()

		# First parse title
		self.parse_ws()
		self.parse_regex("Title:")
		self.parse_title()


		while self.pos < len(self.src):
			# Declarations (Arguments, Attacks, Proponent, Opponent, Common Knowledge)
			# may be given in any order.
			self.parse_ws()

			mode = self.parse_regex("[a-zA-Z][a-zA-Z_\s]*:")

			if mode == "Arguments:" and not self.args:
				self.args = self.parse_list_of_args()
				#
			elif mode == "Attacks:" and not self.attacks:
				self.attacks = self.parse_list_of_attacks()
				#
			elif mode == "Proponent:":
				self.proargs = self.parse_list_of_args()
				#
			elif mode == "Opponent:" and not self.oppmodel:
				self.oppmodel, self.oppargs = self.parse_list_of_models()
				#
			elif mode == "Common Knowledge:":
				self.ckargs = self.parse_list_of_args()
				#
			elif mode == "Goals:" and not self.goals:
				self.goals = self.parse_list_of_args()
				#
			elif mode == "Rules:":
				self.rules, heads = self.parse_list_of_rules()
				self.oppargs += heads
				#
			else:
				break

		if self.args == None:
			raise SyntaxError("No arguments speficied.")

		if self.attacks == None:
			raise SyntaxError("No attacks speficied.")

		if self.oppmodel == None:
			raise SyntaxError("No opponent models speficied.")

		if self.goals == None:
			raise SyntaxError("No goal speficied.")


	## Title ##
	def parse_title(self):
		# parses title
		self.parse_ws()
		self.title = self.parse_regex(r"[a-zA-Z0-9]([-_]{0,1}[a-zA-Z0-9_]+)*")
		self.parse_ws()


	## Arguments ##
	def parse_list_of_args(self):
		# parses list of arguments
		arg_list = []

		self.parse_ws()
		arg = self.parse_arg()
		arg_list += [arg]

		while True:
			try:
				self.parse_regex("[\s]*,?[\s]*")
				arg = self.parse_arg()
				arg_list += [arg]
			except:
				break

		return arg_list
		

	def parse_arg(self):
		#parses arguments
		return self.parse_regex("[a-z][a-z0-9]*")



	## Attacks ##
	def parse_list_of_attacks(self):
		# pases list of attacks
		attack_list = []

		self.parse_ws()
		attack = self.parse_attack()
		attack_list += [attack]

		while True:
			try:
				self.parse_regex("[\s]*,?[\s]*")
				attack = self.parse_attack()
				attack_list += [attack]
			except:
				break

		return attack_list


	def parse_attack(self):
		# parses attack
		self.parse_regex(r"\([\s]*")
		arg1 = self.parse_arg()
		self.parse_regex("[\s]*,[\s]*")
		arg2 = self.parse_arg()
		self.parse_regex(r"[\s]*\)")

		return (arg1,arg2)



	## Opponent Model ##
	def parse_list_of_models(self):
		# pases list of things
		list_of_models = []
		list_of_args = set([])

		self.parse_ws()
		model = self.parse_model()
		list_of_models += [model]
		list_of_args = list_of_args | set(model[0])

		while True:
			try:
				self.parse_regex("[\s]*,?[\s]*")
				model = self.parse_model()
				list_of_models += [model]
				list_of_args = list_of_args | set(model[0])
			except:
				break

		return list_of_models, list(list_of_args)

	def parse_dict_of_models(self):
		# pases list of things
		dict_of_models = {}
		list_of_args = []

		self.parse_ws()
		model = self.parse_model()
		dict_of_models[tuple(model[0])] = model[1]
		list_of_args += model[0]

		while True:
			try:
				self.parse_regex("[\s]*,?[\s]*")
				model = self.parse_model()
				dict_of_models[tuple(model[0])] = model[1]
				list_of_args += model[0]
			except:
				break

		return dict_of_models, list_of_args


	def parse_model(self):
		# parses opponent model
		self.parse_regex(r"\([\s]*\{[\s]*")
		model = self.parse_list_of_args()
		self.parse_regex(r"[\s]*\}[\s]*:[\s]*")
		prob = self.parse_int()
		self.parse_regex(r"[\s]*\)")

		return (model,prob)



	## Inferred Arguments ##
	def parse_list_of_rules(self):
		# parses list of rules
		list_of_rules = []
		list_of_heads = []

		self.parse_ws()
		rule = self.parse_rule()
		list_of_rules += [rule]
		list_of_heads += rule[1]

		while True:
			try:
				self.parse_regex("[\s]*,?[\s]*")
				rule = self.parse_rule()
				list_of_rules += [rule]
				list_of_heads += rule[1]
			except:
				break

		return list_of_rules, list_of_heads

	def parse_rule(self):
		# parses rule
		self.parse_regex(r"\([\s]*")
		body = self.parse_list_of_args()
		self.parse_regex(r"[\s]*=>[\s]*")
		head = self.parse_list_of_args()
		self.parse_regex(r"[\s]*\)")

		return (body,head)



if __name__ == "__main__" and len(sys.argv)>1:

	f = open(sys.argv[1])
	p = Parser(f.read())
	p.parse()
	print "Title:", p.title
	print "Arguments:", p.args
	print "Attacks:", p.attacks
	print "Proponent:", p.proargs
	print "Opponent Model:", p.oppmodel
	print "Common Knowledge:", p.ckargs


	print ""