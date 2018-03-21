import sqlite3
from ArgStrat.framework import *


def write_to_file(filename,run_date,AF,opp_model,planner_dat=[None,0,0],naive_dat=[None,0,0]):

	conn = sqlite3.connect(filename)
	cur = conn.cursor()

	# Drop Tables (setup-only)
	#cur.execute('DROP TABLE IF EXISTS ArgFrame')
	#cur.execute('DROP TABLE IF EXISTS Experiments')

	# Create Tables if none exist
	cur.execute('''CREATE TABLE IF NOT EXISTS ArgFrame 
					(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
					name TEXT NOT NULL UNIQUE, 
					args TEXT NOT NULL,
					attacks TEXT NOT NULL)''')

	cur.execute('''CREATE TABLE IF NOT EXISTS Experiments 
					(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, 
					run_date DATE,
					ArgFrame_id INTEGER REFERENCES ArgFrame,
					Opp_model_size INTEGER,
					Planner_strat TEXT,
					Planner_time REAL,
					Planner_success REAL,
					Naive_strat TEXT,
					Naive_time REAL,
					Naive_success REAL)''')


	# Add AF to ArgFrame table (if not exsits)
	name = str(AF.getName())
	args = str(AF.getArgs())
	attacks = str(AF.getAttacks())
	cur.execute('''INSERT OR IGNORE INTO ArgFrame (name,args,attacks) VALUES (?,?,?)''', (name,args,attacks))
	conn.commit()

	cur.execute('''SELECT id FROM ArgFrame WHERE name= ? AND args = ? AND attacks = ? LIMIT 1''', (name,args,attacks))
	AF_id = cur.fetchone()[0]

	# Add experiment data
	model_size = len(opp_model)
	cur.execute('''INSERT INTO Experiments (run_date,ArgFrame_id,Opp_Model_size,
											Planner_strat,Planner_time,Planner_success,
											Naive_strat,Naive_time,Naive_success) 
							VALUES (?,?,?,?,?,?,?,?,?)''', 
				(run_date,AF_id,model_size,planner_dat[0],planner_dat[1],planner_dat[2],naive_dat[0],naive_dat[1],naive_dat[2]))
	conn.commit()
	

	cur.close()


def scatter_plot(filename,XYmax=None, XYmin=None):

	sql_query = "SELECT ArgFrame_id, opp_model_size, AVG(Planner_time), AVG(Naive_time) FROM Experiments GROUP BY ArgFrame_id, opp_model_size "

	conn = sqlite3.connect(filename)
	cur = self.conn.cursor()
	cur.execute(sql_query)
	dataset = cur.fetchall()

	print dataset
	quit()

	color_code = {1:'red', 2: 'orange', 4: 'green', 8: 'blue', 16: 'cyan', 32: 'purple'}
	marker_code = {}
	marker_list = ['^','o','+','x', 'v'] # best so far
	#marker_list = ['^','o','v','x', '.']
	marker_list = ['^','o','_','x', '+']

	pair_list = []

	X = {}
	Y = {}

	with open(filename, 'r') as f:
		for line in f:
			data = line[:-1].split(',')

			example = str(data[0])
			model_size = int(data[1])
			planner = float(data[5])
			try:
				naive = float(data[9])
			except:
				continue

			if example not in example_list or model_size not in size_list:
				continue

			if planner<XYmin or planner>XYmax or naive<XYmin or naive>XYmax:
				continue


			pair = (example,model_size)
			try:
				X[pair] += [planner]
				Y[pair] += [naive]
			except:
				X[pair] = [planner]
				Y[pair] = [naive]

			# asign markers
			if example not in marker_code:
				next_mark = marker_list.pop(0)
				marker_code[example] = next_mark
				marker_list += [next_mark]

	print marker_code

	P = {}
	for pair in sorted(X.keys()):

		XYmax = XYmax or max([XYmax,10**int(math.ceil(math.log(max(X[pair]+Y[pair]+[10]),10)))])
		XYmin = XYmin or min([XYmin,10**int(math.floor(math.log(min(X[pair]+Y[pair]+[10]),10)))])
		try:
			P[pair] = plt.scatter(X[pair][:truncate], Y[pair][:truncate], s=50, marker=marker_code[pair[0]], color=color_code[pair[1]], label="n = {0}, m = {1}".format(pair[0][5:6],pair[1]))
		except:
			print "error with", pair
			continue

	plt.xscale('log')
	plt.yscale('log')

	plt.plot([XYmin,XYmax],[XYmin,XYmax],color='black')
	plt.axis([XYmin,XYmax,XYmin,XYmax])

	plt.xlabel('Planner time (s)')
	plt.ylabel('Naive time (s)')

	#plt.legend(loc='lower right', ncol=1, bbox_to_anchor=(0, 0))
	#plt.legend([P[i] for i in sorted(P)], ["n = {0}, m = {1}".format(pair[0][5:6],pair[1]) for pair in sorted(P)], loc='lower center', ncol=3)

	class_colours = ['red', 'orange', 'green', 'blue']
	recs = []
	for i in range(len(class_colours)):
	    recs += [mpatches.Rectangle((0,0),1,1,fc=class_colours[i])]

	plt.legend(recs, ['m = {0}'.format(i) for i in [1,2,4,8]], loc=4)
	plt.show()



if __name__ == '__main__':

	scatter_plot('./results/results.sqlite')





# SELECT opp_model_size, AVG(Planner_time), AVG(Naive_time) FROM Experiments GROUP BY opp_model_size