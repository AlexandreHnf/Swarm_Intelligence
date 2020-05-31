import time
from datetime import datetime
from Simulation import Simulation 
from Particle import Particle 
from Solution import Solution
import random
import Utils

import csv

from scipy.stats import ranksums
import numpy as np
import matplotlib.pyplot as plt

BIG_NUMBER = 1000000000

class ParticleSwarmOpti:
	
	def __init__(self, nb_it, nb_eval, n, seed, nb_parti, inertia, phi1, phi2, run_id):
		self.run_id = run_id
		self.iteration = 0
		self.max_iterations = nb_it
		self.max_evaluations = nb_eval
		self.evaluations = 0
		self.seed = seed

		self.rng = random.Random(self.seed)

		self.size = n # problem dimension
		self.nb_particles = nb_parti # number of particles
		self.simulation = Simulation(self.size, run_id, self.rng)

		# particle coefficients /!\ DETERMINE WITH A TOOL
		self.inertia = inertia
		self.phi_1 = phi1
		self.phi_2 = phi2

		# particle swarm
		self.swarm = [] # list of Particles
		self.best_particle = None # ATTENTION ICI PAS DE PARAM? FAUT CHANGER DS PARTICLE

		self.global_best_sol = Solution()
		self.best_timing = BIG_NUMBER # value of the best solution found

		self.printParameters()

		# random.seed(seed)

		self.initialize()
		self.createSwarm()


	def setDefaultParameters(self):
		self.size = 7 # nb of params to optimize
		self.seed = 54321
		self.nb_particles = 10
		self.max_iterations = 50
		self.max_evaluations = 10
		self.inertia = 1
		self.phi_1 = 1
		self.phi_2 = 1

	def printParameters(self):
		print("Particle Swarm Optimization")
		print("Parameters: ")
		print("nb params : ", self.size)
		print("nb particles: ", self.nb_particles)
		print("neighbours topology: ", "G best neighbourhood")
		print("nb iterations: ", self.max_iterations)
		print("inertia : ", self.inertia)
		print("phi 1: ", self.phi_1)
		print("phi 2: ", self.phi_2)
		print("seed: ", self.seed)
		print("=============================================")

	
	def createGbestTopology(self):
		for i in range(self.nb_particles):
			for j in range(self.nb_particles):
				if (i!=j):
					self.swarm[i].addNeighbour(self.swarm[j])

	
	def initialize(self):
		# initialize global best
		self.global_best_sol.initZeros(self.size)
		self.global_best_sol.setEval(BIG_NUMBER)

	
	def updateGlobalBest(self, new_x, new_eval):
		self.global_best_sol.setValues(new_x)
		self.global_best_sol.setEval(new_eval)

	def getFinalBestSolution(self):
		"""
		Returns the best solution found after the whole PSO
		"""
		self.global_best_sol.roundValues()
		return self.global_best_sol

	def getBestEval(self):
		""" 
		Returns the final global best solution evaluation
		"""
		return self.global_best_sol.getEval()

	def getBestSolution(self):
		"""
		Returns the final global best solution (x)
		"""
		return self.global_best_sol.getValues()

	def moveSwarm(self):
		""" 
		Move the all swarm => each particle moves according to their personal best score
		and global best score and based on the neighbourhood
		"""

		print("iteration : ", self.iteration)
		prev_eval = self.global_best_sol.getEval()
		for i in range(self.nb_particles):
			self.swarm[i].move()

			if (self.swarm[i].getPbestEvaluation() < self.global_best_sol.getEval()):
				self.updateGlobalBest(self.swarm[i].getPbestPosition(), self.swarm[i].getPbestEvaluation())
				self.best_particle = self.swarm[i]
		
		if (prev_eval > self.global_best_sol.getEval()):
			print(f"New best solution {self.global_best_sol.getEval()} found at iteration {self.iteration}")
			pass

	def terminateCondition(self):
		if (self.max_iterations != 0 and self.iteration >= self.max_iterations):
			return True 
		if (self.max_evaluations != 0 and self.evaluations > self.max_evaluations):
			return True 

		return False 

	def createSwarm(self):
		print("Creating swarm..")
		for i in range(self.nb_particles):
			p = Particle(i+1, self.run_id, self.rng, self.simulation, self.phi_1, self.phi_2, self.inertia)
			print(f"{self.run_id} Particle {i+1} evaluation: {p.getPbestEvaluation()}")

			self.swarm.append(p)
			
			if (self.global_best_sol.getEval() > p.getPbestEvaluation()):
				self.updateGlobalBest(p.getPbestPosition(), p.getPbestEvaluation())
				self.best_particle = p 

		self.createGbestTopology()
		print(self.run_id, " Best initial solution quality: {}".format(self.global_best_sol.getEval()))

	def run(self):
		"""
		Run n iterations of PSO and find the optimal solution
		"""
		while not self.terminateCondition():
			self.moveSwarm()
			# pso.evaluations += nb_particles
			self.iteration += 1




# ==============================================================================

def saveBestSol(sol, evaluation):
	with open("best_sol_found.txt", "a+") as sol_file:
		s = ""
		for i in range(len(sol)):
			s += str(sol[i]) + ", "
		s = s[:-1] + " => " + str(evaluation) + "\n"
		# s = "{}, {}, {}, {} => {}\n".format(sol[0], sol[1], sol[2], sol[3], evaluation)
		sol_file.write(s)
		sol_file.write("===================================\n")

def runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia, run_id):
	pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2, run_id)
	pso.run()
	return pso.getFinalBestSolution()

def runMultiplePSO(nb_run, seeds):
	nb_params = 7
	nb_particles = 10
	nb_it = 1
	nb_eval = 0
	phi1 = 1
	phi2 = 1
	inertia = 1

	best_solutions = []

	global_start_time = time.time()

	for i in range(nb_run): # i + 1 = run ID
		start_time = time.time()

		best_sol = runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seeds[i], phi1, phi2, inertia, i+1)

		print("Best solution found: {} steps | params = {}".format(best_sol.getEval(), best_sol.getValues()))

		# Utils.displayTiming(start_time)

		# saveBestSol(best_sol.getValues(), best_sol.getEval())

		best_solutions.append(best_sol)

	Utils.displayTiming(global_start_time)

	return best_solutions


def ranksumTest(best_solutions, nb_params):
	x = []
	y = []
	simulation = Simulation(nb_params, 0)  # id 0 so that argos seeds are random
	for sol in best_solutions:
		x.append(sol[1])
		all_evaluations, nb_steps = simulation.evaluateMany(sol[0], 10)
		y += all_evaluations

	print("x = ", x)
	print("y = ", y)
	p_value = ranksums(x,y)
	print("p_value = ", p_value)

def ranksumTest2(evals):
	p_values = []
	sol_evals = []
	for i in range(len(evals)-1):
		sol_evals.append(evals[i][0]) # sol eval)
		x = [evals[i][0]] # sol eval
		y = evals[i][1] # sol list of evaluations
		p_values.append(ranksums(x, y))

	total_p_value = ranksums(sol_evals, evals["all_evals"])

	only_convergence = list(filter(lambda a: a != 1000, evals["all_evals"]))
	# print(only_convergence)
	tot_conv_pvalue = ranksums(sol_evals, only_convergence)
	p_values.append(total_p_value)
	p_values.append(tot_conv_pvalue)

	return p_values


def boxplots(evals):
	medians = []
	y = []
	for i in range(len(evals)-1):
		medians.append(evals[i][0]) # sol eval
		y.append(evals[i][1]) # sol list of evaluations

	fig, ax = plt.subplots()
	pos = np.array(range(len(y))) + 1
	bp = ax.boxplot(y, sym='k+', positions=pos,
					usermedians=medians)

	ax.set_xlabel('PSO runs')
	ax.set_ylabel('Evaluations')

	plt.savefig("Results/boxplot{}.png".format(datetime.today()))
	# plt.show()

def boxplotsConv(evals):
	medians = []
	y = []
	for i in range(len(evals) - 1):
		medians.append(evals[i][0])  # sol eval
		l = []
		for e in evals[i][1]:
			if e < 1000:
				l.append(e)
		y.append(l)  # sol list of evaluations

	fig, ax = plt.subplots()
	pos = np.array(range(len(y))) + 1
	bp = ax.boxplot(y, sym='k+', positions=pos,
					usermedians=medians)

	ax.set_xlabel('PSO runs')
	ax.set_ylabel('Evaluations')

	plt.savefig("Results/boxplotCONV{}.png".format(datetime.today()))


def getAllEvals(best_solutions, nb_params):
	"""
	e = {0: (sol1_eval, evaluations), 1 : (sol2_eval, evaluations), .. "tot": [all_evals]}
	"""
	e = {"all_evals": []}
	simulation = Simulation(nb_params, 0)  # id 0 so that argos seeds are random
	for i in range(len(best_solutions)):
		all_evaluations, nb_steps = simulation.evaluateMany(best_solutions[i].getValues(), 10)
		e[i] = (best_solutions[i].getEval(), all_evaluations) # tuple
		e["all_evals"] += all_evaluations

	return e

def displayBestSol(best_solutions):
	print("BEST SOLUTIONS FOUND : ")
	for sol in best_solutions:
		print(f"sol = {sol.getValues()}, eval = {sol.getEval()} steps")

def displayEvals(evals, p_values):
	print("=============== EVALS with PVALUES: ")
	print("all evals : {}".format(evals["all_evals"]))

	print("global p_value with 1000: ", p_values[-2].pvalue)
	print("global p_value without 1000: ", p_values[-1].pvalue)

	for i in range(len(evals)-1):
		print("sol = {}, evals = {}, pvalue = {}".format(evals[i][0], evals[i][1], p_values[i].pvalue))

def writeSolToCsv(best_solutions):
	with open("Results/pso10_10_10_1_10_v2.csv", mode='w') as result_file:
		result_writer = csv.writer(result_file, delimiter=',', quotechar='"')
		data_names = ["enter_deep_velocity", "rotate_velocity","align_angle", "avoid_distance",
					  "fwd_velocity", "fwd_steps", "enter_velocity", "nb_steps"]
		result_writer.writerow(data_names)
		for sol in best_solutions:
			line = sol.getValues()
			line.append(sol.getEval())
			result_writer.writerow(line)


def writeStatsToCsv(evals, p_values):
	with open("Results/stat10_10_10_1_10_v2.csv", mode='w') as result_file:
		result_writer = csv.writer(result_file, delimiter=',', quotechar='"')
		data_names = ["sol", "e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9", "e10", "pvalue"]
		result_writer.writerow(data_names)
		for i in range(len(evals)-1):
			line = [evals[i][0]] # 1 sol eval
			line += evals[i][1] # 10 evals
			line.append(p_values[i].pvalue)
			result_writer.writerow(line)


def main():
	seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
	# seeds = [6630, 4499, 15, 3207, 2717, 7056, 7093, 9872, 2647, 6606]
	nb_runs = 2
	best_solutions = runMultiplePSO(nb_runs, seeds)
	displayBestSol(best_solutions)

	# evals = {'all_evals': [292, 161, 179, 270, 190, 195, 193, 168, 247, 216, 1000, 185, 268, 525, 183, 165, 235, 136, 203, 197, 175, 205, 205, 224, 202, 167, 189, 180, 237, 178, 167, 352, 204, 144, 268, 321, 152, 158, 1000, 229, 157, 205, 189, 197, 182, 182, 1000, 205, 175, 1000, 1000, 194, 251, 270, 205, 221, 319, 197, 171, 191, 185, 183, 203, 175, 266, 290, 174, 1000, 1000, 1000, 1000, 1000, 189, 190, 205, 196, 189, 301, 1000, 1000, 252, 170, 211, 1000, 212, 255, 170, 212, 139, 182, 173, 162, 207, 1000, 193, 205, 158, 198, 250, 198], 0: (175, [292, 161, 179, 270, 190, 195, 193, 168, 247, 216]), 1: (181, [1000, 185, 268, 525, 183, 165, 235, 136, 203, 197]), 2: (151, [175, 205, 205, 224, 202, 167, 189, 180, 237, 178]), 3: (153, [167, 352, 204, 144, 268, 321, 152, 158, 1000, 229]), 4: (180, [157, 205, 189, 197, 182, 182, 1000, 205, 175, 1000]), 5: (163, [1000, 194, 251, 270, 205, 221, 319, 197, 171, 191]), 6: (165, [185, 183, 203, 175, 266, 290, 174, 1000, 1000, 1000]), 7: (152, [1000, 1000, 189, 190, 205, 196, 189, 301, 1000, 1000]), 8: (144, [252, 170, 211, 1000, 212, 255, 170, 212, 139, 182]), 9: (186, [173, 162, 207, 1000, 193, 205, 158, 198, 250, 198])}
	# evals = getAllEvals(best_solutions, nb_params=7)
	# p_values = ranksumTest2(evals)
	# displayEvals(evals, p_values)
	#
	# boxplots(evals)
	# boxplotsConv(evals)
	#
	# writeSolToCsv(best_solutions)
	# writeStatsToCsv(evals, p_values)


if __name__ == "__main__":
	main()