import copy


class Solution:

	def __init__(self):

		self.x = [] # d-dimensional array (d = nb of simulation params)

		self.eval = 0 # Objective function = nb of simulation steps 

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

	def initRandom(self):
		pass

	