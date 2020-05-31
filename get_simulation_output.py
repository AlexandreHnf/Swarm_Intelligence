import subprocess, shlex
import time
import logging
import threading
import math
import Utils

threads_values = []

def run_one_simulation(number):
	"""
	Run one simulation of argos
	"""

	# argos_command = "argos3 -c decision-making{}.argos".format(number + 1)
	argos_command = "argos3 -c decision-making.argos"
	# print(argos_command)
	output = subprocess.run(shlex.split(argos_command), capture_output=True)
	o = str(output.stdout, "utf-8")
	nb_steps = o.strip().split("Experiment ends at: \x1b[0m\x1b[1;32m")[1].replace("\x1b[0m\n\x1b[0m", "")
	# nb_steps = o.strip().split("\x1b[0m\x1b[1;32m")[-1].replace("\x1b[0m\n\x1b[0m", "")

	return int(nb_steps)


def average_runs(nb_runs):
	"""
	Average nb of steps over n simulations without threads
	"""

	start_time = time.time()
	tot = 0
	for i in range(nb_runs):
		nb_steps = run_one_simulation(i+1)
		tot += nb_steps 
		print(f"{i}, nb of steps : {nb_steps}")
	
	average = tot / nb_runs

	print(f"average nb of steps on {nb_runs} = {average}")
	Utils.displayTiming(start_time)


def thread_function(name):
	"""
	Function executed by a thread : execute one simulation of argos
	"""
	# logging.info("Thread %s: starting", name)
	nb_steps = run_one_simulation(name)
	threads_values[name] = nb_steps
	# print("nb steps: ", run_one_simulation())
	# logging.info("Thread %s: finishing", name)

def print_threads_results(convergence_limit):
	""" 
	Show the results obtained by threads
	"""
	print("=========== RESULTS : ")
	nb_failed = 0
	for i in range(len(threads_values)):
		if threads_values[i] == convergence_limit:
			nb_failed += 1
		print(f"thread {i} : {threads_values[i]} steps")
	print("=========== AVERAGE : ", int(sum(threads_values) / len(threads_values)))

	only_convergence = list(filter(lambda a: a != 1000, threads_values))
	print("=========== AVERAGE WITHOUT 1000 : ", int(sum(only_convergence) / len(only_convergence)))

	print(f"=========== CONVERGENCE : {len(threads_values) - nb_failed}/{len(threads_values)}, \
			nb fails: {nb_failed}")
	print("steps: ", threads_values)

def run_with_threads(nb_threads):
	"""
	Run n threads and then show the results
	"""

	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
						datefmt="%H:%M:%S")

	start_time = time.time()

	threads = list()
	for index in range(nb_threads):
		# logging.info("Main    : create and start thread %d.", index)
		x = threading.Thread(target=thread_function, args=(index,))
		threads.append(x)
		x.start()

	for index, thread in enumerate(threads):
		# logging.info("Main    : before joining thread %d.", index)
		thread.join()
		# logging.info("Main    : thread %d done", index)

	convergence_limit = 1000
	print_threads_results(convergence_limit)

	Utils.displayTiming(start_time)



if __name__ == "__main__":
	# nb_runs = 10
	# average_runs(nb_runs)
	nb_threads = 10
	threads_values = [0 for i in range(nb_threads)]
	run_with_threads(nb_threads)

	

	


