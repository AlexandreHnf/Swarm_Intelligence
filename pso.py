from Simulation import Simulation
from Particle import Particle 
from Solution import Solution
import random

BIG_NUMBER = 1000000000

class ParticleSwarmOpti:
	
	def __init__(self, nb_it, nb_eval, n, seed, nb_parti, inertia, phi1, phi2, run_id, conv_threshold):
		self.run_id = run_id
		self.iteration = 0
		self.max_iterations = nb_it
		self.max_evaluations = nb_eval
		self.evaluations = 0
		self.seed = seed

		self.convergence_threshold = conv_threshold

		self.rng = random.Random(self.seed)

		self.size = n # problem dimension
		self.nb_particles = nb_parti # number of particles
		self.simulation = Simulation(self.size, run_id, self.rng, self.convergence_threshold)

		# particle coefficients
		self.inertia = inertia
		self.phi_1 = phi1
		self.phi_2 = phi2

		# particle swarm
		self.swarm = [] # list of Particles
		self.best_particle = None # ATTENTION ICI PAS DE PARAM? FAUT CHANGER DS PARTICLE

		self.global_best_sol = Solution()
		self.best_timing = BIG_NUMBER # value of the best solution found

		self.printParameters()

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




# def main():
# 	seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
# 	# seeds = [6630, 4499, 15, 3207, 2717, 7056, 7093, 9872, 2647, 6606]
# 	nb_runs = 2
# 	best_solutions = runMultiplePSO(nb_runs, seeds)
# 	displayBestSol(best_solutions)
#
# 	# evals = {'all_evals': [292, 161, 179, 270, 190, 195, 193, 168, 247, 216, 1000, 185, 268, 525, 183, 165, 235, 136, 203, 197, 175, 205, 205, 224, 202, 167, 189, 180, 237, 178, 167, 352, 204, 144, 268, 321, 152, 158, 1000, 229, 157, 205, 189, 197, 182, 182, 1000, 205, 175, 1000, 1000, 194, 251, 270, 205, 221, 319, 197, 171, 191, 185, 183, 203, 175, 266, 290, 174, 1000, 1000, 1000, 1000, 1000, 189, 190, 205, 196, 189, 301, 1000, 1000, 252, 170, 211, 1000, 212, 255, 170, 212, 139, 182, 173, 162, 207, 1000, 193, 205, 158, 198, 250, 198], 0: (175, [292, 161, 179, 270, 190, 195, 193, 168, 247, 216]), 1: (181, [1000, 185, 268, 525, 183, 165, 235, 136, 203, 197]), 2: (151, [175, 205, 205, 224, 202, 167, 189, 180, 237, 178]), 3: (153, [167, 352, 204, 144, 268, 321, 152, 158, 1000, 229]), 4: (180, [157, 205, 189, 197, 182, 182, 1000, 205, 175, 1000]), 5: (163, [1000, 194, 251, 270, 205, 221, 319, 197, 171, 191]), 6: (165, [185, 183, 203, 175, 266, 290, 174, 1000, 1000, 1000]), 7: (152, [1000, 1000, 189, 190, 205, 196, 189, 301, 1000, 1000]), 8: (144, [252, 170, 211, 1000, 212, 255, 170, 212, 139, 182]), 9: (186, [173, 162, 207, 1000, 193, 205, 158, 198, 250, 198])}
# 	evals = getAllEvals(best_solutions, nb_params=7)
# 	p_values = ranksumTest(evals)
# 	displayEvals(evals, p_values)
#
# 	boxplots(evals)
# 	boxplotsConv(evals)
#
# 	writeSolToCsv(best_solutions)
# 	writeStatsToCsv(evals, p_values)


# if __name__ == "__main__":
# 	main()