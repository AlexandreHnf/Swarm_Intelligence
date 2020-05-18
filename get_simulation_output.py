import subprocess, shlex
import time

def run_one_simulation():
	output = subprocess.run(shlex.split("argos3 -c decision-making.argos"), capture_output=True)
	encoding = "utf-8"
	o = str(output.stdout, encoding)
	# \x1b[0m\x1b[1;32m1969\x1b[0m\n\x1b[0m
	nb_steps = o.strip().split("\x1b[0m\x1b[1;32m")[-1].replace("\x1b[0m\n\x1b[0m", "")
	# print("number steps: ", nb_steps)
	# print(len(nb_steps))

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


if __name__ == "__main__":
	nb_runs = 10
	average_runs(nb_runs)


