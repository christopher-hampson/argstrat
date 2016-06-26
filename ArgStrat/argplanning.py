import subprocess
import time
import re


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