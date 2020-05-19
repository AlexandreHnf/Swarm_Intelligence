import time 
from Simulation import Simulation 
from Particle import Particle 
from Solution import Solution

BIG_NUMBER = 1000000000

class ParticleSwarmOpti:
	
	def __init__(self, nb_it, nb_eval, n, seed, nb_parti, inertia, phi1, phi2):
		
		self.iterations = 0
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
		self.best_particle = Particle() # ATTENTION ICI PAS DE PARAM? FAUT CHANGER DS PARTICLE

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
		print("nb params : ", self.n)
		print("nb particles: ", self.nb_particles)
		print("neighbours topology", "G best neighbourhood")
		print("nb iterations: ", self.max_iterations)
		print("inertia : ", self.inertia)
		print("phi 1: ", self.phi_1)
		print("phi 2: ", self.phi_2)
		print("seed: ", seed)

	
	def createGbestTopology(self):
		for i in range(self.nb_particles):
			for j in range(self.nb_particles):
				if (i!=j):
					self.swarm[i].addNeighbour(self.swarm[j])

	
	def initialize(self):
		# initialize global best
		self.global_best_sol = []
		for i in range(self.size):
			self.global_best_sol.setValue(i, 0)
		self.global_best_sol.setEval(BIG_NUMBER)

	
	def updateGlobalBest(new_x, new_eval):
		self.global_best_sol.setValues(new_x)
		self.global_best_sol.setEval(new_eval)

	def getBestEval(self):
		""" 
		Returns the final global best solution evaluation
		"""
		return self.global_best_sol.getEval()

	def moveSwarm(self):
		""" 
		Move the all swarm => each particle moves according to their personal best score
		and global best score and based on the neighbourhood
		"""

		prev_eval = self.global_best_sol.getEval()
		for i in range(self.nb_particles):
			self.swarm[i].move()

			if (self.swarm[i].getPbestEvaluation() < self.global_best_sol.getEval()):
				self.updateGlobalBest(self.swarm[i].getPbestPosition(), self.swarm[i].getPbestEvaluation())
		
		if (prev_eval > self.global_best_sol.getEval()):
		print(f"New best solution {self.global_best_sol.getEval()} found at iteration {self.iterations}")


	def terminateCondition(self):
		if (self.max_iterations != 0 and self.iterations > self.max_iterations):
			return True 
		if (self.max_evaluations != 0 and self.evaluations > self.max_evaluations):
			return True 

		return False 

	def createSwarm(self):
		print("Creating swarm..")
		for i in range(self.nb_particles):
			p = Particle(self.simulation, self.phi_1, self.phi_2, self.inertia)
			print(f"Particle {i} evaluation: {p.getPbestEvaluation()}")

			self.swarm.append(p)
			
			if (self.global_best_sol.getEval() > p.getPbestEvaluation()):
				self.updateGlobalBest(p.getPbestPosition(), p.getPbestEvaluation)
				self.best_particle = p 

		self.createGbestTopology()
		print("Best initial solution quality: {}".format(self.global_best_sol.getEval()))


def main():
	nb_params = 7
	nb_particles = 10
	nb_it = 10
	nb_eval = 0
	nb_run = 1

	seed = 54321
	phi1 = 1
	phi2 = 1
	inertia = 1

	
	pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2)

	pso.printParameters()

	pso.initialize()
	pso.createSwarm()

	start_time = time.time()

	while not pso.terminateCondition():
		pso.moveSwarm()
		# pso.evaluations += nb_particles
		pso.iterations += 1 

	
	end_time = time.time() - start_time
	print("Best solution found: {} steps".format(pso.getBestEval()))
	print("Time spent: {} seconds = {} minutes".format(end_time, round(end_time/60)))




if __name__ == __main__:
	main()