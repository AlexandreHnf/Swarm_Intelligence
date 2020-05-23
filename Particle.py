import get_simulation_output as sim 
from Solution import Solution
import Utils 



class Particle:
	def __init__(self, my_id, simulation=None, phi_1=1, phi_2=1, inertia=1):

		self.id = my_id
		self.simulation = simulation # optim
		self.current = Solution()
		self.pbest = Solution()
		self.gbest = Solution()
		self.size = self.simulation.get_nb_params()
		self.phi_1 = phi_1
		self.phi_2 = phi_2
		self.inertia = inertia
		self.velocity = []  # size = nb param simulation

		self.neighbours = [] # list of neighbours particles
		self.init = True

		self.initSolutions()
		self.initializeUniform()

	def initSolutions(self):
		self.current.initZeros(self.size)
		self.pbest.initZeros(self.size)
		self.gbest.initZeros(self.size)


	def initializeUniform(self):
		
		for i in range(self.size):
			# self.current.setValue(i, self.simulation.getRandomX(i))
			self.velocity.append(0)
		
		self.current.initRandom(self.size, self.simulation)
		self.pbest.setValues(self.current.getValues())
		self.evaluateSolution()
		# print("new eval : ", self.current.getEval())

	def move(self):
		self.findGbestParticle() # the global best depends on the topology

		for i in range(self.size):
			u1 = Utils.getRandom01() # random value for the personal component
			u2 = Utils.getRandom01() # random value for the social component

			new_inertia = self.inertia * self.velocity[i]
			cognitive_influence = self.phi_1 * u1 * (self.pbest.getValue(i) - self.current.getValue(i))
			social_influence = self.phi_2 * u2 * (self.gbest.getValue(i) - self.current.getValue(i))

			self.velocity[i] = (new_inertia) + (cognitive_influence) + (social_influence)
			self.current.setValue(i, self.current.getValue(i) + self.velocity[i])

			if self.current.getValue(i) < self.simulation.getLowerBound(i):
				self.current.setValue(i, self.simulation.getLowerBound(i))
			if self.current.getValue(i) > self.simulation.getUpperBound(i):
				self.current.setValue(i, self.simulation.getUpperBound(i))
		
		self.evaluateSolution()
		print("particle {} after move : {} steps".format(self.id, self.current.getEval()))


	def evaluateSolution(self):
		""" 
		If the new solution is better than the personal best, update it
		"""
		print("current sol = ", self.current.getValues())
		new_eval = self.simulation.evaluate(self.current.getValues())
		# print("new eval : ", new_eval)
		self.current.setEval(new_eval)
		if (self.current.getEval() < self.pbest.getEval()):
			self.pbest.setValues(self.current.getValues())	
			self.pbest.setEval(self.current.getEval())


	def findGbestParticle(self):
		"""
		Check the neighbourhood for the best particle
		""" 
		best = -1

		if self.pbest.getEval() < self.gbest.getEval():
			self.updateGbestParticle(self.pbest.getValues(), self.pbest.getEval())

		aux_eval = self.gbest.getEval()
		for i in range(len(self.neighbours)):
			if (aux_eval > self.neighbours[i].getPbestEvaluation()):
				best = i 
		
		if best != -1 :
			self.updateGbestParticle(self.neighbours[best].getPbestPosition(),
									 self.neighbours[best].getPbestEvaluation())


	def updateGbestParticle(self, x, new_eval):

		self.gbest.setValues(x)
		self.gbest.setEval(new_eval)


	def getCurrentPosition(self):
		return self.current.getValues()

	def getCurrentEvaluation(self):
		return self.current.getEval()

	def getPbestPosition(self):
		return self.pbest.getValues()

	def getPbestEvaluation(self):
		return self.pbest.getEval()

	def addNeighbour(self, particle):
		""" 
		Add a new particle to the list of neighbours
		"""
		self.neighbours.append(particle)

	def printPosition(self):
		print("Solution: {}, eval = {}".format(self.getCurrentPosition(),
											   self.getCurrentEvaluation()))