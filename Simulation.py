import subprocess, shlex
import logging, threading
import time
import random
import math 

class Simulation:

	def __init__(self, nb_params):
		self.nb_params = nb_params
		self.lower_bounds = [0.1, 80, 0.001, 1] # a remplir avec les bonnes valeurs 
		self.upper_bounds = [0.3, 1000, 0.05, 30]
		self.threads_values = []

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
		if type(self.lower_bounds[i]) == float:
			return random.uniform(self.lower_bounds[i], self.upper_bounds[i])
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


	def thread_function(self, name):
		"""
		Function executed by a thread : execute one simulation of argos
		"""
		logging.info("Thread %s: starting", name)
		nb_steps = self.run_one_simulation()
		self.threads_values[name] = nb_steps
		# print("nb steps: ", run_one_simulation())
		logging.info("Thread %s: finishing", name)

	def print_threads_results(self):
		""" 
		Show the results obtained by threads
		"""
		print("=========== RESULTS : ")
		nb_failed = 0
		for i in range(len(self.threads_values)):
			if self.threads_values[i] == 3000:
				nb_failed += 1
			print(f"thread {i} : {self.threads_values[i]} steps")
		print("=========== AVERAGE : ", sum(self.threads_values) / len(self.threads_values))
		print(f"=========== CONVERGENCE : {len(self.threads_values) - nb_failed}/{len(self.threads_values)}, \
				nb fails: {nb_failed}")

	def run_with_threads(self, nb_threads):
		"""
		Run n threads and then show the results
		"""

		format = "%(asctime)s: %(message)s"
		logging.basicConfig(format=format, level=logging.INFO,
							datefmt="%H:%M:%S")

		start_time = time.time()

		threads = list()
		for index in range(nb_threads):
			logging.info("Main    : create and start thread %d.", index)
			x = threading.Thread(target=self.thread_function, args=(index,))
			threads.append(x)
			x.start()

		for index, thread in enumerate(threads):
			logging.info("Main    : before joining thread %d.", index)
			thread.join()
			logging.info("Main    : thread %d done", index)

		print_threads_results()

		end_time_sec = time.time() - start_time
		in_minutes = math.floor(end_time_sec/60)
		print("=========== Time spent: ")
		print("{} seconds".format(end_time_sec))
		print("{} minutes and {} seconds".format(in_minutes, end_time_sec - in_minutes*60))


	def write_to_file(self, solution):
		""" 
		Solution = Object containing a list of solution parameters and an
		objective function
		"""
		with open("simulation_parameters.txt", "w") as params_file:
			print(solution)
			for p in solution:
				params_file.write("{}\n".format(p))


	def evaluate(self, solution):
		"""
		Given a solution containing several parameters, first write those params
		in the simulation parameters file and then simulate with argos
		and returns the nb of steps
		"""

		self.write_to_file(solution)
		
		# return self.average_runs(10)
		# return self.run_one_simulation()
		return self.run_with_threads(10)
