import subprocess, shlex
import time
import random

class Simulation:

	def __init__(self, nb_params):
		self.nb_params = nb_params
		self.lower_bounds = [] # a remplir avec les bonnes valeurs 
		self.upper_bounds = []

	def getLowerBound(self, i):
		return self.lower_bounds[i]

	def getUpperBound(self, i):
		return self.upper_bounds[i]


	def get_nb_params(self):
		return self.nb_params

	def getRandomX(self, i):
		"""
		Get a random number in the range [lower bound, upper bound]
		/!\ Float values ?, here int for the moment
		"""
		return random.randrange(self.lower_bounds[i], self.upper_bounds[i])

	def run_one_simulation(self):
		""" 
		Runs one argos simulation and returns the nb of steps elapsed
		"""
		
		output = subprocess.run(shlex.split("argos3 -c decision-making.argos"), capture_output=True)
		encoding = "utf-8"
		o = str(output.stdout, encoding)
		nb_steps = o.strip().split("\x1b[0m\x1b[1;32m")[-1].replace("\x1b[0m\n\x1b[0m", "")

		return int(nb_steps)

	def average_runs(self, nb_runs):
		start_time = time.time()
		tot = 0
		for i in range(nb_runs):
			nb_steps = run_one_simulation() 
			tot += nb_steps 
			print(f"{i}, nb of steps : {nb_steps}")
		
		average = tot / nb_runs

		# print(f"average nb of steps on {nb_runs} = {average}")
		# print(f"done in {time.time() - start_time}")

		return average

	def write_to_file(self, solution):
		""" 
		Solution = Object containing a list of solution parameters and an
		objective function
		"""
		with open("simulation_parameters.txt", "w") as params_file:
			for p in solution.get_x():
				params_file.write("{}\n".format(p))


	def evaluate(self, solution):
		"""
		Given a solution containing several parameters, first write those params
		in the simulation parameters file and then simulate with argos
		and returns the nb of steps
		"""

		self.write_to_file(solution)
		
		# return self.average_runs(10)
		return self.run_one_simulation()
