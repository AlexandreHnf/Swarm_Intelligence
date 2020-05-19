import subprocess, shlex
import time
import logging, threading

def run_one_simulation():
	output = subprocess.run(shlex.split("argos3 -c decision-making.argos"), capture_output=True)
	o = str(output.stdout, "utf-8")
	nb_steps = o.strip().split("\x1b[0m\x1b[1;32m")[-1].replace("\x1b[0m\n\x1b[0m", "")

	return int(nb_steps)


def average_runs(nb_runs):
	start_time = time.time()
	tot = 0
	for i in range(nb_runs):
		nb_steps = run_one_simulation() 
		tot += nb_steps 
		print(f"{i}, nb of steps : {nb_steps}")
	
	average = tot / nb_runs

	print(f"average nb of steps on {nb_runs} = {average}")
	print(f"done in {time.time() - start_time}")


def thread_function(name):
	logging.info("Thread %s: starting", name)
	print("nb steps: ", run_one_simulation())
	logging.info("Thread %s: finishing", name)



if __name__ == "__main__":
	# nb_runs = 10
	# average_runs(nb_runs)

	format = "%(asctime)s: %(message)s"
	logging.basicConfig(format=format, level=logging.INFO,
						datefmt="%H:%M:%S")


	start_time = time.time()

	threads = list()
	for index in range(3):
		logging.info("Main    : create and start thread %d.", index)
		x = threading.Thread(target=thread_function, args=(index,))
		threads.append(x)
		x.start()

	for index, thread in enumerate(threads):
		logging.info("Main    : before joining thread %d.", index)
		thread.join()
		logging.info("Main    : thread %d done", index)

	end_time = time.time() - start_time
	print("time spent {} sec, {} min".format(end_time, round(end_time/60)))

	


