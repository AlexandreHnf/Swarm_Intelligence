import time 
from Simulation import Simulation 
from Particle import Particle 
from Solution import Solution

BIG_NUMBER = 1000000000

class ParticleSwarmOpti:
	
	def __init__(self, nb_it, nb_eval, n, seed, nb_parti, inertia, phi1, phi2):
		
		self.iteration = 0
		self.max_iterations = nb_it
		self.max_evaluations = nb_eval
		self.evaluations = 0
		self.seed = seed

		self.size = n # problem dimension
		self.nb_particles = nb_parti # number of particles
		self.simulation = Simulation(self.size)

		# particle coefficients /!\ DETERMINE WITH A TOOL
		self.inertia = inertia
		self.phi_1 = phi1
		self.phi_2 = phi2

		# particle swarm
		self.swarm = [] # list of Particles
		self.best_particle = None # ATTENTION ICI PAS DE PARAM? FAUT CHANGER DS PARTICLE

		self.global_best_sol = Solution()
		self.best_timing = BIG_NUMBER # value of the best solution found

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


	def terminateCondition(self):
		if (self.max_iterations != 0 and self.iteration >= self.max_iterations):
			return True 
		if (self.max_evaluations != 0 and self.evaluations > self.max_evaluations):
			return True 

		return False 

	def createSwarm(self):
		print("Creating swarm..")
		for i in range(self.nb_particles):
			p = Particle(i+1, self.simulation, self.phi_1, self.phi_2, self.inertia)
			print(f"Particle {i+1} evaluation: {p.getPbestEvaluation()}")

			self.swarm.append(p)
			
			if (self.global_best_sol.getEval() > p.getPbestEvaluation()):
				self.updateGlobalBest(p.getPbestPosition(), p.getPbestEvaluation())
				self.best_particle = p 

		self.createGbestTopology()
		print("Best initial solution quality: {}".format(self.global_best_sol.getEval()))

def saveBestSol(sol, evaluation):
	with open("best_sol_found.txt", "a+") as sol_file:
		s = "{}, {}, {}, {} => {}\n".format(sol[0], sol[1], sol[2], sol[3], evaluation)
		sol_file.write(s)
		sol_file.write("===================================\n")

def runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia):
	pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2)

	pso.printParameters()

	pso.initialize()
	pso.createSwarm()

	while not pso.terminateCondition():
		pso.moveSwarm()
		# pso.evaluations += nb_particles
		pso.iteration += 1 

	return pso.getBestEval(), pso.getBestSolution()

def runMultiplePSO(nb_run):
	nb_params = 4
	nb_particles = 3
	nb_it = 5
	nb_eval = 0
	seed = 54321
	phi1 = 1
	phi2 = 1
	inertia = 1

	for i in range(nb_run):
		start_time = time.time()

		best_eval, best_sol = runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia)
	
		end_time = time.time() - start_time
		print("Best solution found: {} steps | params = {}".format(best_eval, best_sol))
		print("Time spent: {} seconds = {} minutes".format(end_time, round(end_time/60)))

		saveBestSol(best_sol, best_eval)


# ==============================================================================


def main():
	runMultiplePSO(1)


if __name__ == "__main__":
	main()