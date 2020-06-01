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
    """
    Wilcoxon Ranksum test with each pair of solutions of the 10 runs of PSo
    """
    p_values = []

    for i in range(len(evals)- 1):
        p_vals = []
        for j in range(len(evals)-1):
            if i == j :
                p_vals.append("-")
            else:
                x = evals[i][1]  # list of evals
                y = evals[j][1]    # list of evals
                p_vals.append(ranksums(x, y).pvalue)
        p_values.append(p_vals)

    return p_values # table of pvalues


def boxplots(evals, phi1, phi2, nb_evals):
    """
    Save boxplots of all evaluations
    """
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

    plt.savefig("../Results/pso-bxp-10_10_10_{}_{}_{}_{}.png"
                .format(nb_evals, phi1, phi2, datetime.today()))


def boxplotsConv(evals, convergence_threshold, phi1, phi2, nb_evals):
    """
    save the boxplots of the evaluations but with only convergence
    """
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

    plt.savefig("../Results/boxplotCONV10_10_10_{}_{}_{}_{}.png"
                .format(nb_evals, phi1, phi2, datetime.today()))


def getAllEvals2(best_solutions, nb_params, nb_evals, conv_thresh):
    """
    Get all evaluations but with lists and not Solution objects
    """

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
    Get all evaluations of 10 PSO runs with Solution objects
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


def displayEvals(evals, p_values):
    print("=============== EVALS with PVALUES: ")
    print("all evals : {}".format(evals["all_evals"]))

    for i in range(len(evals) - 1):
        print("sol = {}, evals = {}, pvalue = {}".
              format(evals[i][0], evals[i][1], p_values[i]))


def writeTestToCsv(best_solutions, p_values, evals, phi1, phi2, nb_evals, conv_thresh):
    """
    Write all values in csv file
    """
    filename = "../Results/pso-wt-10_10_10_{}_{}_{}_{}.csv".format(nb_evals, phi1, phi2, datetime.today())
    with open(filename, mode='w') as result_file:
        result_writer = csv.writer(result_file, delimiter=',', quotechar='"')
        data_names = ["enter_deep_velocity", "rotate_velocity", "align_angle", "avoid_distance",
                      "fwd_velocity", "fwd_steps", "enter_velocity", "nb_steps", "Evaluations", "convergence(%)", "pvalues"]
        result_writer.writerow(data_names)
        for i in range(len(evals) - 1):
            line = best_solutions[i].getValues()
            line.append(best_solutions[i].getEval())
            # line = best_solutions[i][0]
            # line.append(best_solutions[i][1])

            line.append(evals[i][1])  # n evals
            convergence = ((nb_evals - evals[i][1].count(conv_thresh)) / nb_evals) * 100
            line.append(convergence)
            # line.append(p_values[i])

            result_writer.writerow(line)

def writePvaluesToCsv(p_values):
    filename = "table_pvalues.csv"
    with open(filename, mode="w") as p_file:
        writer = csv.writer(p_file, delimiter=",")
        names=[""] + ["sol" + str(i+1) for i in range(10)]
        writer.writerow(names)
        for i in range(len(p_values)):
            line = ["sol" + str(i+1)]
            for p in p_values[i]:
                if p == "-":
                    line.append("-")
                else:
                    line.append(round(p, 5))
            writer.writerow(line)

p_values = [
['-', 0.05651653736796189, 0.7763905055505131, 0.7557428276359095, 0.061977574433805, 5.8959172179215014e-05, 0.25029679750351186, 0.1332831707493199, 0.01606401314826911, 0.5427717015170068],
[0.05651653736796189, '-', 0.20845355458876536, 0.6359445511344555, 0.44074988359834266, 0.0023412726074935374, 0.6456228047372299, 0.9031164959895642, 0.6263280630826087, 0.49033426450951045],
[0.7763905055505131, 0.20845355458876536, '-', 0.8498180212406273, 0.10751135969600566, 0.00024706130132229516, 0.3039952778179398, 0.17621399555130546, 0.06786818721248442, 0.6948910198677665],
[0.7557428276359095, 0.6359445511344555, 0.8498180212406273, '-', 0.49033426450951045, 0.06786818721248442, 0.9031164959895642, 0.6359445511344555, 0.35772797019341296, 0.9568553503696526],
[0.061977574433805, 0.44074988359834266, 0.10751135969600566, 0.49033426450951045, '-', 0.08341508335601154, 0.39417090995164517, 0.5427717015170068, 0.7049097275727512, 0.23932370336933684],
[5.8959172179215014e-05, 0.0023412726074935374, 0.00024706130132229516, 0.06786818721248442, 0.08341508335601154, '-', 0.005795918475717191, 0.00490497196539969, 0.0027986021909070804, 0.0023412726074935374],
[0.25029679750351186, 0.6456228047372299, 0.3039952778179398, 0.9031164959895642, 0.39417090995164517, 0.005795918475717191, '-', 0.6359445511344555, 0.40172032908792543, 0.6750141566504884],
[0.1332831707493199, 0.9031164959895642, 0.17621399555130546, 0.6359445511344555, 0.5427717015170068, 0.00490497196539969, 0.6359445511344555, '-', 0.4569506196695641, 0.49033426450951045],
[0.01606401314826911, 0.6263280630826087, 0.06786818721248442, 0.35772797019341296, 0.7049097275727512, 0.0027986021909070804, 0.40172032908792543, 0.4569506196695641, '-', 0.21840551261012597],
[0.5427717015170068, 0.49033426450951045, 0.6948910198677665, 0.9568553503696526, 0.23932370336933684, 0.0023412726074935374, 0.6750141566504884, 0.49033426450951045, 0.21840551261012597, '-']


]

writePvaluesToCsv(p_values)


