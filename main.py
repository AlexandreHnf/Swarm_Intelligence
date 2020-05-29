from Simulation import Simulation
from Particle import Particle
from Solution import Solution
from pso import ParticleSwarmOpti

import time
import random
import threading
import math

from scipy.stats import ranksums

class multiplePSO:

    def __init__(self):
        self.seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
        self.nb_runs = 2

        self.nb_params = 4
        self.nb_particles = 10
        self.nb_it = 10
        self.nb_eval = 0
        self.phi1 = 1
        self.phi2 = 1
        self.inertia = 1

        self.best_solutions = [0 for _ in range(self.nb_runs)]

    def saveBestSol(self, sol, evaluation):
        with open("best_sol_found.txt", "a+") as sol_file:
            s = "{}, {}, {}, {} => {}\n".format(sol[0], sol[1], sol[2], sol[3], evaluation)
            sol_file.write(s)
            sol_file.write("===================================\n")


    def runOnePSO(self, nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia, run_id):
        pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2, run_id)
        pso.run()
        return pso.getFinalBestSolution()

    def thread_function(self, name):
        # start_time = time.time()

        best_sol = self.runOnePSO(self.nb_params, self.nb_particles, self.nb_it, self.nb_eval, self.seeds[name],
                                  self.phi1, self.phi2, self.inertia, name+1)

        # end_time = time.time() - start_time
        # print("Best solution found: {} steps | params = {}".format(best_sol.getEval(), best_sol.getValues()))
        # print("Time spent: {} seconds = {} minutes".format(end_time, round(end_time / 60)))

        self.best_solutions[name] = best_sol


    def run_with_threads(self):
        start_time = time.time()

        threads = list()
        for index in range(self.nb_runs):
            x = threading.Thread(target=self.thread_function, args=(index,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        end_time_sec = time.time() - start_time
        in_minutes = math.floor(end_time_sec / 60)

        print("=========== Time spent in total: ")
        print("{} seconds".format(end_time_sec))
        print("{} minutes and {} seconds".format(in_minutes, end_time_sec - in_minutes*60))

        self.displayAllSolutions()


    def displayAllSolutions(self):
        print("All solutions: ")
        for i in range(self.nb_runs):
            print(f"pso {i+1} gives : ")
            print(f"    {self.best_solutions[i].getValues()} => {self.best_solutions[i].getEval()}")


    def ranksumTest(self, nb_params):
        x = []
        y = []
        simulation = Simulation(nb_params, 0)  # id 0 so that argos seeds are random
        for sol in self.best_solutions:
            x.append(sol.getEval())
            all_evaluations, nb_steps = simulation.evaluateMany(sol.getValues(), 10)
            y += all_evaluations

        p_value = ranksums(x, y)
        print("p_value = ", p_value)


# ==============================================================================


def main():
    # seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
    # # seeds = [4849, 443, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
    # nb_runs = 10
    # # best_solutions = runMultiplePSO(nb_runs, seeds)
    #
    # best_solutions = [([212.736147464836, 19.573044622727608, 0.4001092164203171, 0.08374353425434194], 280),
    #                   ([420.45592575519413, 17.92061612388558, 0.4283722490788896, 0.08176026649594798], 289),
    #                   ([515.1380035694767, 25.254513362671315, 0.4840204934812594, 0.07714880092810156], 276),
    #                   ([298.14062356443884, 24.680678992737228, 0.4564638937586887, 0.02403460126093475], 267),
    #                   ([590.2624238768972, 24.189712516156963, 0.5, 0.06353384453135309], 230),
    #                   ([293.478778080981, 19.8710290222967, 0.22200230837319782, 0.07516463985673903], 281),
    #                   ([1000, 26.219112640278986, 0.5, 0.03331872619773328], 271),
    #                   ([541.1680110360132, 17.21222986461231, 0.35699825798664797, 0.1], 224),
    #                   ([232.31644227469013, 21.626420276077194, 0.446538792584363, 0.02059718131143208], 200),
    #                   ([885.8713065146162, 17.329087086711827, 0.3688214387901522, 0.06437088347876216], 301),
    #                   ]
    # ranksumTest(best_solutions, nb_params=4)
    mpso = multiplePSO()
    mpso.run_with_threads()

if __name__ == "__main__":
    main()
