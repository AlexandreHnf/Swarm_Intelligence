import copy

BIG_NUMBER = 1000000


class Solution:

	def __init__(self):

		self.x = [] # d-dimensional array (d = nb of simulation params)

		self.eval = BIG_NUMBER # Objective function = nb of simulation steps 

	def initZeros(self, n):
		if len(self.x) == 0 :
			for i in range(n):
				self.x.append(0)

	def initRandom(self, n, simulation):
		for i in range(n):
			if len(self.x) == 0:
				self.x.append(simulation.getRandomX(i))
			else:
				self.x[i] = simulation.getRandomX(i)

	def setValues(self, new_x):
		self.x = copy.deepcopy(new_x)

	def getValues(self):
		return self.x

	def getValue(self, i):
		return self.x[i]

	def setValue(self, i, v):
		self.x[i] = v

	def getEval(self):
		return self.eval

	def setEval(self, e):
		self.eval = e

	
	