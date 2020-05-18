import get_simulation_output as sim 
from Solution import Solution
import Utils 


class Particle:
	def __init__(self, simulation, phi_1, phi_2, inertia):

		self.simulation = simulation # optim
		self.current = Solution()
		self.pbest = Solution()
		self.gbest = Solution()
		self.size = self.simulation.get_nb_params()
		self.phi_1 = phi_1
		self.phi_2 = phi_2
		self.inertia = inertia
		self.velocity = [] # size = nb param simulation

		self.neighbours = [] # list of neighbours particles
		self.init = True

		self.initializeUniform()

	def initializeUniform(self):

		self.current.init_random()
		self.pbest.setValues(self.current.getValues())
		for i in range(self.size):
			self.velocity[i] = 0

		self.evaluateSolution()

	def move(self):
		self.findGbestParticle() # the global best depends on the topology


		for i in range(self.size):
			u1 = Utils.getRandom01() # random value for the personal component
			u2 = Utils.getRandom01() # random value for the social component

			inertia = self.inertia * self.velocity[i]
			cognitive_influence = self.phi1 * u1 * (self.pbest.getValue(i) - self.current.getValue(i))
			social_influence = self.phi_2 * u2 * (self.gbest.getValue(i) - self.current.getValue(i))

			self.velocity[i] = (inertia) + (cognitive_influence) + (social_influence)
			self.current.setValue(i, self.current.getValue(i) + self.velocity[i])

			if self.current.getValue(i) < self.simulation.getLowerBound(i):
				self.current.setValue(i, self.simulation.getLowerBound(i))
			if self.current.getValue(i) > self.simulation.getUpperBound(i):
				self.current.setValue(i, self.simulation.getUpperBound(i))
		
		self.evaluateSolution()


	def evaluateSolution(self):
		""" 
		If the new solution is better than the personal best, update it
		"""
		self.current.setEval(self.simulation.evaluate(self.current.getValues()))
		if (self.current.getEval() < self.pbest.getEval()):
			self.pbest.setValues(self.current.getValues())	
			self.pbest.setEval(self.current.getEval())


	def findGBestParticle(self):
		"""
		Check the neighbourhood for the best particle
		""" 
		best = -1

		if self.pbest.getEval() < self.gbest.getEval():
			self.updateGbestParticle(self.pbest.getValues(), self.pbest.getEval())

		aux_eval = self.gbest.getEval()
		for i in range(len(self.neighbours)):
			if (aux_eval > self.neighbours[i].getPBestEvaluation()):
				best = i 
		
		if best != -1 :
			self.updateGbestParticle(self.neighbours[best].getPbestPosition(),
									 self.neighbours[best].getPBestEvaluation())


	def updateGbestParticle(self, x, new_eval):

		self.pbest.setValues(x)
		self.gbest.setEval(new_eval)


	def getCurrentPosition(self):
		return self.current.getValues()

	def getCurrentEvaluation(self):
		return self.current.getEval()

	def getPbestPosition(self):
		return self.pbest.getValues()

	def getPBestEvaluation(self):
		return self.pbest.getEval()

	def addNeighbor(self, particle):
		""" 
		Add a new particle to the list of neighbours
		"""
		self.neighbours.append(particle)

	def printPosition(self):
		print("Solution: {}, eval = {}".format(self.getCurrentPosition(),
											   self.getCurrentEvaluation()))