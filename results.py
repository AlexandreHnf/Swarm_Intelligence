import time
from datetime import datetime
import random
import Utils

from pso import ParticleSwarmOpti
from Simulation import Simulation

import csv

from scipy.stats import ranksums
import numpy as np
import matplotlib.pyplot as plt


def ranksumTest(evals, convergence_threshold):
    p_values = []
    conv_pvalues = []
    sol_evals = []
    for i in range(len(evals) - 1):
        sol_evals.append(evals[i][0])  # sol eval)
        x = [evals[i][0]]  # sol eval
        y = evals[i][1]  # sol list of evaluations
        conv_y = list(filter(lambda a: a != convergence_threshold, y))
        p_values.append(ranksums(x, y))
        conv_pvalues.append(ranksums(x, conv_y))

    total_p_value = ranksums(sol_evals, evals["all_evals"])

    only_convergence = list(filter(lambda a: a != convergence_threshold, evals["all_evals"]))
    # print(only_convergence)
    tot_conv_pvalue = ranksums(sol_evals, only_convergence)
    p_values.append(total_p_value)
    conv_pvalues.append(tot_conv_pvalue)

    return p_values, conv_pvalues


def boxplots(evals, phi1, phi2, nb_evals):
    medians = []
    y = []
    for i in range(len(evals) - 1):
        medians.append(evals[i][0])  # sol eval
        y.append(evals[i][1])  # sol list of evaluations

    fig, ax = plt.subplots()
    pos = np.array(range(len(y))) + 1
    bp = ax.boxplot(y, sym='k+', positions=pos, usermedians=medians)

    ax.set_xlabel('PSO runs')
    ax.set_ylabel('Evaluations')
    ax.set_title("10PSO, 10it, 10particles, "
                 "phi1={}, phi2={}, nb evals={}".format(phi1, phi2, nb_evals))

    plt.savefig("Results/boxplot10_10_10_{}_{}_{}_{}.png"
                .format(nb_evals, phi1, phi2, datetime.today()))


def boxplotsConv(evals, convergence_threshold, phi1, phi2, nb_evals):
    medians = []
    y = []
    for i in range(len(evals) - 1):
        medians.append(evals[i][0])  # sol eval
        l = []
        for e in evals[i][1]:
            if e < convergence_threshold:
                l.append(e)
        y.append(l)  # sol list of evaluations

    fig, ax = plt.subplots()
    pos = np.array(range(len(y))) + 1
    bp = ax.boxplot(y, sym='k+', positions=pos, usermedians=medians)

    ax.set_xlabel('PSO runs')
    ax.set_ylabel('Evaluations')
    ax.set_title("10PSO, 10it, 10particles, "
                 "phi1={}, phi2={}, nb evals={}".format(phi1, phi2, nb_evals))

    plt.savefig("Results/boxplotCONV10_10_10_{}_{}_{}_{}.png"
                .format(nb_evals, phi1, phi2, datetime.today()))


def getAllEvals2(best_solutions, nb_params, nb_evals, conv_thresh):

    start_time = time.time()
    e = {"all_evals": []}
    simulation = Simulation(nb_params, 0, None, conv_thresh)  # id 0 so that argos seeds are random
    for i in range(len(best_solutions)):
        all_evaluations, nb_steps = simulation.evaluateMany(best_solutions[i][0], nb_evals)
        e[i] = (best_solutions[i][1], all_evaluations)  # tuple
        e["all_evals"] += all_evaluations
    Utils.displayTiming(start_time)

    return e

def getAllEvals(best_solutions, nb_params, nb_evals, conv_thresh):
    """
	e = {0: (sol1_eval, evaluations), 1 : (sol2_eval, evaluations), .. "tot": [all_evals]}
	"""
    start_time = time.time()
    e = {"all_evals": []}
    simulation = Simulation(nb_params, 0, None, conv_thresh)  # id 0 so that argos seeds are random
    for i in range(len(best_solutions)):
        all_evaluations, nb_steps = simulation.evaluateMany(best_solutions[i].getValues(), nb_evals)
        e[i] = (best_solutions[i].getEval(), all_evaluations)  # tuple
        e["all_evals"] += all_evaluations
    Utils.displayTiming(start_time)

    return e


def displayBestSol(best_solutions):
    print("BEST SOLUTIONS FOUND : ")
    for sol in best_solutions:
        print(f"({sol.getValues()}, {sol.getEval()}),")


def displayEvals(evals, p_values, conv_pvalues):
    print("=============== EVALS with PVALUES: ")
    print("all evals : {}".format(evals["all_evals"]))

    print("global p_value with non convergence: ", p_values[-1].pvalue)
    print("global p_value without non convergence: ", conv_pvalues[-1].pvalue)

    for i in range(len(evals) - 1):
        print("sol = {}, evals = {}, pvalue = {}, conv_pvalue = {}".
              format(evals[i][0], evals[i][1], p_values[i].pvalue, conv_pvalues[i].pvalue))


def writeSolToCsv(best_solutions, phi1, phi2, nb_evals):
    filename = "Results/pso10_10_10_{}_{}_{}_{}.csv".format(nb_evals, phi1, phi2, datetime.today())
    with open(filename, mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"')
        data_names = ["enter_deep_velocity", "rotate_velocity", "align_angle", "avoid_distance",
                      "fwd_velocity", "fwd_steps", "enter_velocity", "nb_steps"]
        result_writer.writerow(data_names)
        for sol in best_solutions:
            # line = sol.getValues()
            # line.append(sol.getEval())
            line = sol[0]
            line.append(sol[1])
            result_writer.writerow(line)


def writeStatsToCsv(evals, p_values, conv_pvalues, phi1, phi2, nb_evals, conv_thresh):
    filename = "Results/stat10_10_10_{}_{}_{}_{}.csv".format(nb_evals, phi1, phi2, datetime.today())
    with open(filename, mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"')
        data_names = ["Solution", "Evaluations", "convergence(%)", "pvalue", "conv_pvalue"]
        result_writer.writerow(data_names)
        for i in range(len(evals) - 1):
            line = [evals[i][0]]  # 1 sol eval
            line.append(evals[i][1])  # n evals
            convergence = ((nb_evals - evals[i][1].count(conv_thresh)) / nb_evals) * 100
            line.append(convergence)
            line.append(p_values[i].pvalue)
            line.append(conv_pvalues[i].pvalue)
            result_writer.writerow(line)
