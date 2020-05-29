import time 
from Simulation import Simulation 
from Particle import Particle 
from Solution import Solution
import random

from scipy.stats import ranksums

BIG_NUMBER = 1000000000

class ParticleSwarmOpti:
	
	def __init__(self, nb_it, nb_eval, n, seed, nb_parti, inertia, phi1, phi2, run_id):
		
		self.iteration = 0
		self.max_iterations = nb_it
		self.max_evaluations = nb_eval
		self.evaluations = 0
		self.seed = seed

		self.size = n # problem dimension
		self.nb_particles = nb_parti # number of particles
		self.simulation = Simulation(self.size, run_id)

		# particle coefficients /!\ DETERMINE WITH A TOOL
		self.inertia = inertia
		self.phi_1 = phi1
		self.phi_2 = phi2

		# particle swarm
		self.swarm = [] # list of Particles
		self.best_particle = None # ATTENTION ICI PAS DE PARAM? FAUT CHANGER DS PARTICLE

		self.global_best_sol = Solution()
		self.best_timing = BIG_NUMBER # value of the best solution found

		# self.printParameters()

		random.seed(seed)

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

		# print("iteration : ", self.iteration)
		prev_eval = self.global_best_sol.getEval()
		for i in range(self.nb_particles):
			self.swarm[i].move()

			if (self.swarm[i].getPbestEvaluation() < self.global_best_sol.getEval()):
				self.updateGlobalBest(self.swarm[i].getPbestPosition(), self.swarm[i].getPbestEvaluation())
				self.best_particle = self.swarm[i]
		
		if (prev_eval > self.global_best_sol.getEval()):
			# print(f"New best solution {self.global_best_sol.getEval()} found at iteration {self.iteration}")
			pass

	def terminateCondition(self):
		if (self.max_iterations != 0 and self.iteration >= self.max_iterations):
			return True 
		if (self.max_evaluations != 0 and self.evaluations > self.max_evaluations):
			return True 

		return False 

	def createSwarm(self):
		# print("Creating swarm..")
		for i in range(self.nb_particles):
			p = Particle(i+1, self.simulation, self.phi_1, self.phi_2, self.inertia)
			# print(f"Particle {i+1} evaluation: {p.getPbestEvaluation()}")

			self.swarm.append(p)
			
			if (self.global_best_sol.getEval() > p.getPbestEvaluation()):
				self.updateGlobalBest(p.getPbestPosition(), p.getPbestEvaluation())
				self.best_particle = p 

		self.createGbestTopology()
		# print("Best initial solution quality: {}".format(self.global_best_sol.getEval()))

	def run(self):
		"""
		Run n iterations of PSO and find the optimal solution
		"""
		while not self.terminateCondition():
			self.moveSwarm()
			# pso.evaluations += nb_particles
			self.iteration += 1


def saveBestSol(sol, evaluation):
	with open("best_sol_found.txt", "a+") as sol_file:
		s = "{}, {}, {}, {} => {}\n".format(sol[0], sol[1], sol[2], sol[3], evaluation)
		sol_file.write(s)
		sol_file.write("===================================\n")

def runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia, run_id):
	pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2, run_id)
	pso.run()
	return pso.getFinalBestSolution()

def runMultiplePSO(nb_run, seeds):
	nb_params = 4
	nb_particles = 10
	nb_it = 10
	nb_eval = 0
	phi1 = 1
	phi2 = 1
	inertia = 1

	best_solutions = []

	for i in range(nb_run): # i + 1 = run ID
		start_time = time.time()

		best_sol = runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seeds[i], phi1, phi2, inertia, i+1)

		end_time = time.time() - start_time
		print("Best solution found: {} steps | params = {}".format(best_sol.getEval(), best_sol.getValues()))
		print("Time spent: {} seconds = {} minutes".format(end_time, round(end_time/60)))

		saveBestSol(best_sol.getValues(), best_sol.getEval())

		best_solutions.append(best_sol)

	return best_solutions


def ranksumTest(best_solutions, nb_params):
	x = []
	y = []
	simulation = Simulation(nb_params, 0) # id 0 so that argos seeds are random
	for sol in best_solutions:
		x.append(sol.getEval())
		all_evaluations, nb_steps = simulation.evaluateMany(sol.getValues(), 10)
		y += all_evaluations

	p_value = ranksums(x,y)
	print("p_value = ", p_value)

# ==============================================================================

def displayBestSol(best_solutions):
	print("BEST SOLUTIONS FOUND : ")
	for sol in best_solutions:
		print(f"sol = {sol.getValues()}, eval = {sol.getEval()} steps")

def main():
	seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
	# seeds = [4849, 443, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
	nb_runs = 1
	best_solutions = runMultiplePSO(nb_runs, seeds)
	displayBestSol(best_solutions)

	# best_solutions = [([212.736147464836, 19.573044622727608, 0.4001092164203171, 0.08374353425434194], 280),
	# 				  ([420.45592575519413, 17.92061612388558, 0.4283722490788896, 0.08176026649594798], 289),
	# 				  ([515.1380035694767, 25.254513362671315, 0.4840204934812594, 0.07714880092810156], 276),
	# 				  ([298.14062356443884, 24.680678992737228, 0.4564638937586887, 0.02403460126093475], 267),
	# 				  ([590.2624238768972, 24.189712516156963, 0.5, 0.06353384453135309], 230),
	# 				  ([293.478778080981, 19.8710290222967, 0.22200230837319782, 0.07516463985673903], 281),
	# 				  ([1000, 26.219112640278986, 0.5, 0.03331872619773328], 271),
	# 				  ([541.1680110360132, 17.21222986461231, 0.35699825798664797, 0.1], 224),
	# 				  ([232.31644227469013, 21.626420276077194, 0.446538792584363, 0.02059718131143208], 200),
	# 				  ([885.8713065146162, 17.329087086711827, 0.3688214387901522, 0.06437088347876216], 301),
	# 				  ]
	# ranksumTest(best_solutions, nb_params=4)



if __name__ == "__main__":
	main()