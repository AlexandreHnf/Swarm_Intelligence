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
    manual = Solution()
    manual.setValues(manual_sol)
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
    best_pso_sol = [885.868, 23.767, 0.5, 0.01, 1, 10.716, 371.674]
    best_solutions = psoVSmanual(manual_sol, best_pso_sol)

    # ==============================
    # ========= TESTING ============
    # ==============================
    # all_best_solutions = [
    #     [([507.943, 15.378, 0.376, 0.1, 7.816, 9.655, 286.799], 185) ,
    #     ([899.776, 19.739, 0.383, 0.039, 7.175, 19.728, 268.658], 181) ,
    #     ([703.797, 16.221, 0.3, 0.097, 1, 14.317, 317.656], 167 ),
    #     ([461.745, 25.015, 0.5, 0.097, 2.678, 16.814, 238.763], 153) ,
    #     ([487, 15, 0.266, 0.043, 6, 15, 472], 180 ),
    #     ([915.742, 14.221, 0.347, 0.089, 7.607, 18.23, 231.52], 163) ,
    #     ([640.631, 20.526, 0.42, 0.026, 7.329, 17.643, 238.153], 165) ,
    #     ([1000, 21.572, 0.5, 0.021, 12.116, 10.908, 358.794], 152 ),
    #     ([1000, 21.939, 0.469, 0.085, 5.857, 9.607, 500], 130 ),
    #     ([388.939, 21.031, 0.476, 0.019, 1.994, 9.07, 393.357], 168)],
    #
    #     [([677.628, 13.548, 0.299, 0.069, 8.511, 15.441, 172.2], 193),
    #     ([669.785, 13.444, 0.323, 0.016, 8.548, 19.225, 327.318], 191),
    #     ([1000, 25.268, 0.5, 0.1, 3.821, 5, 245.05], 162),
    #     ([384.049, 21.363, 0.5, 0.091, 15, 11.609, 444.276], 152),
    #     ([487, 15, 0.266, 0.043, 6, 15, 472], 180),
    #     ([915.742, 14.221, 0.347, 0.089, 7.607, 18.23, 231.52], 163),
    #     ([408.732, 25.586, 0.5, 0.048, 1, 13.479, 198.426], 178),
    #     ([548.03, 22.81, 0.5, 0.1, 15, 8.581, 151.784], 147),
    #     ([850.102, 22.459, 0.473, 0.1, 1, 13.333, 417.349], 131),
    #     ([474.21, 25.379, 0.5, 0.01, 1, 10.331, 500], 165)],
    #
    #     [([622, 18, 0.213, 0.054, 8, 6, 177], 339),
    #     ([478, 26, 0.355, 0.012, 8, 23, 166], 242),
    #     ([913, 14, 0.299, 0.089, 8, 8, 245], 238),
    #     ([548, 21, 0.276, 0.075, 7, 11, 337], 187),
    #     ([487, 15, 0.266, 0.043, 6, 15, 472], 180),
    #     ([887, 16, 0.136, 0.028, 5, 11, 293], 220),
    #     ([278, 26, 0.413, 0.03, 3, 15, 139], 214),
    #     ([827, 11, 0.339, 0.072, 8, 13, 461], 188),
    #     ([562, 16, 0.452, 0.022, 3, 22, 152], 176),
    #     ([211, 14, 0.247, 0.028, 2, 22, 372], 219)],
    #
    #     [([922.051, 18.103, 0.5, 0.074, 8.513, 5, 235.648], 179),
    #     ([1000, 22.218, 0.469, 0.01, 11.427, 13.122, 53.157], 212),
    #     ([969.193, 20.558, 0.451, 0.1, 12.195, 15.985, 235.02], 157),
    #     ([283.95, 30, 0.5, 0.1, 8.294, 7.156, 500], 160),
    #     ([487, 15, 0.266, 0.043, 6, 15, 472], 180),
    #     ([932.934, 19.733, 0.325, 0.041, 7.79, 30, 417.948], 165),
    #     ([349.262, 20.494, 0.391, 0.1, 15, 13.663, 218.724], 158),
    #     ([972.113, 25.272, 0.5, 0.1, 9.731, 8.174, 378.819], 162),
    #     ([961.799, 19.527, 0.269, 0.02, 4.316, 10.395, 228.463], 157),
    #     ([441.591, 17.687, 0.392, 0.04, 4.351, 16.412, 500], 191)],
    #
    #     [([775.319, 15.749, 0.383, 0.077, 8.063, 13.157, 266.716], 175),
    #     ([694.655, 14.999, 0.429, 0.044, 14.09, 10.587, 500], 171),
    #     ([810.097, 16.824, 0.322, 0.1, 3.878, 17.34, 280.602], 172),
    #     ([505.726, 21.0, 0.42, 0.07, 9.991, 11.334, 334.188], 151),
    #     ([381.005, 14.359, 0.288, 0.096, 7.647, 9.567, 475.692], 165),
    #     ([926.057, 15.892, 0.387, 0.075, 7.518, 19.379, 344.591], 150),
    #     ([885.868, 23.767, 0.5, 0.01, 1, 10.716, 371.674], 152),
    #     ([461.127, 17.975, 0.396, 0.079, 6.051, 13.448, 500], 151),
    #     ([212.233, 24.052, 0.5, 0.01, 4.185, 15.314, 201.55], 136),
    #     ([376.446, 18.594, 0.413, 0.06, 4.573, 14.158, 392.163], 184)],
    #
    #     [([229.15, 20.447, 0.5, 0.043, 13.434, 18.539, 87.257], 229),
    #     ([529.116, 21.363, 0.5, 0.01, 15, 30, 210.089], 182),
    #     ([1000, 23.902, 0.5, 0.1, 1, 30, 500], 179),
    #     ([1000, 19.522, 0.406, 0.094, 7.63, 19.034, 500], 168),
    #     ([543.927, 17.196, 0.5, 0.01, 6.335, 7.209, 500], 163),
    #     ([1000, 16.97, 0.327, 0.1, 15, 30, 500], 176),
    #     ([243.477, 22.614, 0.5, 0.01, 13.655, 23.101, 165.605], 176),
    #     ([1000, 30, 0.5, 0.043, 10.226, 5, 500], 187),
    #     ([526.669, 21.53, 0.5, 0.01, 1.307, 23.098, 267.4], 147),
    #     ([411.009, 25.775, 0.5, 0.01, 1, 15.209, 488.798], 172)],
    #
    #     [([509.774, 19.501, 0.416, 0.048, 10.674, 16.294, 186.637], 181),
    #     ([510.311, 17.694, 0.38, 0.057, 7.267, 13.919, 288.598], 167),
    #     ([574.934, 15.284, 0.329, 0.058, 9.645, 12.392, 454.535], 167),
    #     ([448.524, 22.15, 0.5, 0.1, 13.684, 11.721, 423.675], 147),
    #     ([487, 15, 0.266, 0.043, 6, 15, 472], 180),
    #     ([728.691, 18.668, 0.274, 0.03, 8.575, 6.18, 287.832], 153),
    #     ([538.199, 19.355, 0.392, 0.01, 11.418, 11.723, 500], 155),
    #     ([477.677, 16.273, 0.325, 0.1, 3.847, 17.018, 257.512], 167),
    #     ([770.583, 17.941, 0.316, 0.048, 8.496, 18.971, 183.153], 146),
    #     ([1000, 16.788, 0.396, 0.01, 4.947, 9.812, 483.154], 182)]
    # ]

    # evals ={'all_evals': [163, 500, 386, 163, 187, 246, 189, 232, 261, 289, 286, 221, 185, 193, 263, 178, 197, 206, 156, 160, 148, 214, 176, 187, 130, 194, 175, 244, 163, 262, 274, 235, 500, 205, 500, 324, 161, 233, 173, 189, 188, 214, 297, 209, 163, 500, 483, 148, 139, 184, 210, 205, 185, 210, 255, 500, 153, 500, 500, 194, 234, 189, 191, 145, 221, 250, 188, 177, 232, 254, 276, 165, 192, 279, 270, 177, 220, 305, 205, 199, 202, 192, 129, 156, 192, 243, 256, 186, 241, 500, 208, 500, 233, 173, 269, 208, 200, 500, 134, 151, 500, 178, 245, 259, 186, 241, 215, 159, 161, 500, 182, 142, 254, 500, 257, 500, 135, 259, 250, 230, 173, 181, 229, 183, 157, 187, 290, 126, 192, 226, 500, 181, 212, 228, 193, 317, 336, 220, 181, 222, 233, 193, 180, 246, 176, 237, 216, 208, 237, 201, 191, 144, 500, 170, 335, 200, 183, 231, 260, 122, 500, 203, 176, 228, 500, 155, 209, 148, 137, 194, 215, 310, 202, 500, 317, 288, 148, 500, 158, 190, 205, 500, 185, 142, 159, 160, 225, 181, 244, 199, 149, 191, 177, 163, 500, 173, 500, 146, 239, 180], 0: (193, [163, 500, 386, 163, 187, 246, 189, 232, 261, 289, 286, 221, 185, 193, 263, 178, 197, 206, 156, 160]), 1: (191, [148, 214, 176, 187, 130, 194, 175, 244, 163, 262, 274, 235, 500, 205, 500, 324, 161, 233, 173, 189]), 2: (162, [188, 214, 297, 209, 163, 500, 483, 148, 139, 184, 210, 205, 185, 210, 255, 500, 153, 500, 500, 194]), 3: (152, [234, 189, 191, 145, 221, 250, 188, 177, 232, 254, 276, 165, 192, 279, 270, 177, 220, 305, 205, 199]), 4: (180, [202, 192, 129, 156, 192, 243, 256, 186, 241, 500, 208, 500, 233, 173, 269, 208, 200, 500, 134, 151]), 5: (163, [500, 178, 245, 259, 186, 241, 215, 159, 161, 500, 182, 142, 254, 500, 257, 500, 135, 259, 250, 230]), 6: (178, [173, 181, 229, 183, 157, 187, 290, 126, 192, 226, 500, 181, 212, 228, 193, 317, 336, 220, 181, 222]), 7: (147, [233, 193, 180, 246, 176, 237, 216, 208, 237, 201, 191, 144, 500, 170, 335, 200, 183, 231, 260, 122]), 8: (131, [500, 203, 176, 228, 500, 155, 209, 148, 137, 194, 215, 310, 202, 500, 317, 288, 148, 500, 158, 190]), 9: (165, [205, 500, 185, 142, 159, 160, 225, 181, 244, 199, 149, 191, 177, 163, 500, 173, 500, 146, 239, 180])}

    # ==============================
    # ========= RESULTS ============
    # ==============================
    nb_tests = 7
    # for i in range(nb_tests):
    #     best_solutions = all_best_solutions[i]
    #     phi1 = phi1s[i]
    #     phi2 = phi2s[i]

    # RES.displayBestSol(best_solutions)

    # evals = RES.getAllEvals(best_solutions, nb_params, nb_evals, convergence_threshold)
    evals = RES.getAllEvals2(best_solutions, nb_params, nb_evals, convergence_threshold)
    p_values = RES.ranksumTest(evals, convergence_threshold)
    print("evals: ", evals, len(evals))
    # RES.displayEvals(evals, p_values)

    # RES.boxplots(evals, phi1, phi2, nb_evals)
    RES.boxplotsConv(evals, convergence_threshold, phi1, phi2, nb_evals)

    # RES.writeSolToCsv(best_solutions, phi1, phi2, nb_evals)
    # RES.writeStatsToCsv(evals, p_values, phi1, phi2, nb_evals, convergence_threshold)
    RES.writeTestToCsv(best_solutions, p_values, evals, phi1, phi2, nb_evals, convergence_threshold)



if __name__ == "__main__":
    main()
