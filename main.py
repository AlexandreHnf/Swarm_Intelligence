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

        best_sol = runOnePSO(nb_params, nb_particles, nb_it, nb_eval, seeds[i], phi1, phi2, inertia, i + 1, conv_tresh)
        best_solutions.append(best_sol)

    Utils.displayTiming(global_start_time)

    return best_solutions
# ==============================================================================


def main():
    seeds = [443, 4849, 6554, 328, 1050, 3110, 4868, 902, 8460, 5416]
    nb_runs = 10
    nb_params = 7
    nb_particles = 10
    nb_it = 10
    nb_eval = 0
    phi1 = 0
    phi2 = 1
    inertia = 1
    convergence_threshold = 500
    nb_evals = 20

    # phi1s = [1, 0, 1, 1, 2, 0.5, 3]
    # phi2s = [1, 1, 0, 2, 1, 3, 0.5]

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
    # ========= TESTING ============
    # ==============================
    best_solutions = [([677.628, 13.548, 0.299, 0.069, 8.511, 15.441, 172.2], 193),
    ([669.785, 13.444, 0.323, 0.016, 8.548, 19.225, 327.318], 191),
    ([1000, 25.268, 0.5, 0.1, 3.821, 5, 245.05], 162),
    ([384.049, 21.363, 0.5, 0.091, 15, 11.609, 444.276], 152),
    ([487, 15, 0.266, 0.043, 6, 15, 472], 180),
    ([915.742, 14.221, 0.347, 0.089, 7.607, 18.23, 231.52], 163),
    ([408.732, 25.586, 0.5, 0.048, 1, 13.479, 198.426], 178),
    ([548.03, 22.81, 0.5, 0.1, 15, 8.581, 151.784], 147),
    ([850.102, 22.459, 0.473, 0.1, 1, 13.333, 417.349], 131),
    ([474.21, 25.379, 0.5, 0.01, 1, 10.331, 500], 165),
                    ]

    evals ={'all_evals': [163, 500, 386, 163, 187, 246, 189, 232, 261, 289, 286, 221, 185, 193, 263, 178, 197, 206, 156, 160, 148, 214, 176, 187, 130, 194, 175, 244, 163, 262, 274, 235, 500, 205, 500, 324, 161, 233, 173, 189, 188, 214, 297, 209, 163, 500, 483, 148, 139, 184, 210, 205, 185, 210, 255, 500, 153, 500, 500, 194, 234, 189, 191, 145, 221, 250, 188, 177, 232, 254, 276, 165, 192, 279, 270, 177, 220, 305, 205, 199, 202, 192, 129, 156, 192, 243, 256, 186, 241, 500, 208, 500, 233, 173, 269, 208, 200, 500, 134, 151, 500, 178, 245, 259, 186, 241, 215, 159, 161, 500, 182, 142, 254, 500, 257, 500, 135, 259, 250, 230, 173, 181, 229, 183, 157, 187, 290, 126, 192, 226, 500, 181, 212, 228, 193, 317, 336, 220, 181, 222, 233, 193, 180, 246, 176, 237, 216, 208, 237, 201, 191, 144, 500, 170, 335, 200, 183, 231, 260, 122, 500, 203, 176, 228, 500, 155, 209, 148, 137, 194, 215, 310, 202, 500, 317, 288, 148, 500, 158, 190, 205, 500, 185, 142, 159, 160, 225, 181, 244, 199, 149, 191, 177, 163, 500, 173, 500, 146, 239, 180], 0: (193, [163, 500, 386, 163, 187, 246, 189, 232, 261, 289, 286, 221, 185, 193, 263, 178, 197, 206, 156, 160]), 1: (191, [148, 214, 176, 187, 130, 194, 175, 244, 163, 262, 274, 235, 500, 205, 500, 324, 161, 233, 173, 189]), 2: (162, [188, 214, 297, 209, 163, 500, 483, 148, 139, 184, 210, 205, 185, 210, 255, 500, 153, 500, 500, 194]), 3: (152, [234, 189, 191, 145, 221, 250, 188, 177, 232, 254, 276, 165, 192, 279, 270, 177, 220, 305, 205, 199]), 4: (180, [202, 192, 129, 156, 192, 243, 256, 186, 241, 500, 208, 500, 233, 173, 269, 208, 200, 500, 134, 151]), 5: (163, [500, 178, 245, 259, 186, 241, 215, 159, 161, 500, 182, 142, 254, 500, 257, 500, 135, 259, 250, 230]), 6: (178, [173, 181, 229, 183, 157, 187, 290, 126, 192, 226, 500, 181, 212, 228, 193, 317, 336, 220, 181, 222]), 7: (147, [233, 193, 180, 246, 176, 237, 216, 208, 237, 201, 191, 144, 500, 170, 335, 200, 183, 231, 260, 122]), 8: (131, [500, 203, 176, 228, 500, 155, 209, 148, 137, 194, 215, 310, 202, 500, 317, 288, 148, 500, 158, 190]), 9: (165, [205, 500, 185, 142, 159, 160, 225, 181, 244, 199, 149, 191, 177, 163, 500, 173, 500, 146, 239, 180])}

    # ==============================
    # ========= RESULTS ============
    # ==============================

    # RES.displayBestSol(best_solutions)

    # evals = RES.getAllEvals(best_solutions, nb_params, nb_evals, convergence_threshold)
    # evals = RES.getAllEvals2(best_solutions, nb_params, nb_evals, convergence_threshold)
    p_values, conv_pvalues = RES.ranksumTest(evals, convergence_threshold)
    print("evals: ", evals, len(evals))
    RES.displayEvals(evals, p_values, conv_pvalues)

    RES.boxplots(evals, phi1, phi2, nb_evals)
    RES.boxplotsConv(evals, convergence_threshold, phi1, phi2, nb_evals)

    RES.writeSolToCsv(best_solutions, phi1, phi2, nb_evals)
    RES.writeStatsToCsv(evals, p_values, conv_pvalues, phi1, phi2, nb_evals, convergence_threshold)



if __name__ == "__main__":
    main()
