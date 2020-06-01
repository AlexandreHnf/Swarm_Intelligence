from Simulation import Simulation
from Particle import Particle
from Solution import Solution
from pso import ParticleSwarmOpti

import time
import random
import threading
import math
import Utils

import results as RES



class multiplePSO:

    def __init__(self, seeds, nb_runs, nb_params, nb_particles, nb_it, nb_eval, phi1, phi2, inertia, conv_tresh):
        self.seeds = seeds
        self.nb_runs = nb_runs

        self.nb_params = nb_params
        self.nb_particles = nb_particles
        self.nb_it = nb_it
        self.nb_eval = nb_eval
        self.phi1 = phi1
        self.phi2 = phi2
        self.inertia = inertia

        self.convergence_threshold = conv_tresh

        self.best_solutions = [0 for _ in range(self.nb_runs)]

    def runOnePSO(self, nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia, run_id, conv_tresh):
        pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2, run_id, conv_tresh)
        pso.run()
        return pso.getFinalBestSolution()

    def thread_function(self, name):

        best_sol = self.runOnePSO(self.nb_params, self.nb_particles, self.nb_it, self.nb_eval, self.seeds[name],
                                  self.phi1, self.phi2, self.inertia, name+1, self.convergence_threshold)

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

        return self.best_solutions

def runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seed, phi1, phi2, inertia, run_id, conv_tresh):
    pso = ParticleSwarmOpti(nb_it, nb_eval, nb_params, seed, nb_particles, inertia, phi1, phi2, run_id, conv_tresh)
    pso.run()
    return pso.getFinalBestSolution()

def iterativeMultiplePSO(seeds, nb_runs, nb_params, nb_particles, nb_it, nb_eval, phi1, phi2, inertia, convergence_threshold):

    best_solutions = []

    global_start_time = time.time()

    for i in range(nb_runs):  # i + 1 = run ID

        best_sol = runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seeds[i], phi1, phi2, inertia, i + 1, convergence_threshold)
        best_solutions.append(best_sol)

    Utils.displayTiming(global_start_time)

    return best_solutions
# ==============================================================================

def psoVSmanual(manual_sol, best_pso_sol):
    best_solutions = []
    best_pso = Solution()
    best_pso.setValues(best_pso_sol)
    best_pso.setEval(167)
    manual = Solution()
    manual.setValues(manual_sol)
    manual.setEval(450)
    best_solutions.append(manual)
    best_solutions.append(best_pso)

    return best_solutions

def main():
    seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
    nb_runs = 10
    nb_params = 7
    nb_particles = 10
    nb_it = 10
    nb_eval = 0
    phi1 = 3
    phi2 = 0.5
    inertia = 1
    convergence_threshold = 500
    nb_evals = 20

    phi1s = [1, 0, 1, 1, 2, 0.5, 3]
    phi2s = [1, 1, 0, 2, 1, 3, 0.5]

    # ==============================
    # ========= ITERATIVE ==========
    # ==============================

    # best_solutions = iterativeMultiplePSO(seeds, nb_runs, nb_params, nb_particles, nb_it, nb_eval, phi1, phi2, inertia, convergence_threshold)

    # ==============================
    # ========= THREADS ============
    # ==============================

    # mpso = multiplePSO(seeds, nb_runs, nb_params, nb_particles, nb_it, nb_eval, phi1, phi2, inertia, convergence_threshold)
    # best_solutions = mpso.run_with_threads()

    # ==============================
    # ========= pso VS manual ======
    # ==============================

    manual_sol = [80, 10, 0.15, 0.03, 10, 50, 50]
    best_pso_sol = [574.934, 15.284, 0.329, 0.058, 9.645, 12.392, 454.535]
    best_solutions = psoVSmanual(manual_sol, best_pso_sol)

    # ==============================
    # ========= RESULTS ============
    # ==============================

    # RES.displayBestSol(best_solutions)

    evals = RES.getAllEvals(best_solutions, nb_params, nb_evals, convergence_threshold)
    # evals = RES.getAllEvals2(best_solutions, nb_params, nb_evals, convergence_threshold)
    # p_values = RES.ranksumTest(evals, convergence_threshold)
    p_values = []
    print("evals: ", evals, len(evals))
    # RES.displayEvals(evals, p_values)

    RES.boxplots(evals, phi1, phi2, nb_evals)
    RES.boxplotsConv(evals, convergence_threshold, phi1, phi2, nb_evals)

    # RES.writeSolToCsv(best_solutions, phi1, phi2, nb_evals)
    # RES.writeStatsToCsv(evals, p_values, phi1, phi2, nb_evals, convergence_threshold)
    RES.writeTestToCsv(best_solutions, p_values, evals, phi1, phi2, nb_evals, convergence_threshold)



if __name__ == "__main__":
    main()
