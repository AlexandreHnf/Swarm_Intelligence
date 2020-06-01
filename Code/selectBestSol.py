import csv

def selectBestSol(filename, conv_thresh):
    best_sol = {"id": 0, "sol": 0, "evals": [], "avg": 100000, "conv": 0,"pvalue": 0}  # best

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        i = 0

        for row in csv_reader:
            if i != 0 : # if not names
                sol = int(row[7])
                evals = [int(e) for e in row[8][1:-1].split(",") if (int(e) < conv_thresh)]
                pvalue = row[-1]
                conv = float(row[9])
                average = sum(evals) / len(evals)
                # print(row)
                # print("average: ", average)

                if average < best_sol["avg"] and conv >= 90:
                    best_sol = {"id": i, "sol": sol, "evals": evals, "avg": average, "conv": conv, "pvalue": pvalue}

            i += 1

    return best_sol

def selectBestPhis(conv_thresh):
    phis = [(1,1), (0,1), (1,0), (1,2), (2,1), (0.5,3), (3,0.5)]
    filenames = ["../Results/pso-wt-10_10_10_20_1_1_2020-06-01 20:26:09.898600.csv",
                 "../Results/pso-wt-10_10_10_20_0_1_2020-06-01 20:29:44.871141.csv",
                 "../Results/pso-wt-10_10_10_20_1_0_2020-06-01 20:34:15.171368.csv",
                 "../Results/pso-wt-10_10_10_20_1_2_2020-06-01 20:38:25.227213.csv",
                 "../Results/pso-wt-10_10_10_20_2_1_2020-06-01 20:41:58.325743.csv",
                 "../Results/pso-wt-10_10_10_20_0.5_3_2020-06-01 20:46:41.536688.csv",
                 "../Results/pso-wt-10_10_10_20_3_0.5_2020-06-01 20:50:37.491889.csv"
                 ]

    ultimate_best_sol = None
    best_phi = None
    filename = None

    for i in range(len(filenames)):
        print(filenames[i])
        best_sol = selectBestSol(filenames[i], conv_thresh)
        print("best sol = ", best_sol)

        if (ultimate_best_sol == None) or \
                (best_sol["avg"] < ultimate_best_sol["avg"]) or \
                (best_sol["avg"] == ultimate_best_sol["avg"] and \
                best_sol["conv"] > ultimate_best_sol["conv"]):

            ultimate_best_sol = best_sol
            best_phi = phis[i]
            filename = filenames[i]

    return ultimate_best_sol, best_phi, filename

conv_thresh = 500
ultimate_best_sol, best_phi, filename = selectBestPhis(conv_thresh)

print("Ultimate best sol with phi1 = {} and phi2 = {} is : ".format(best_phi[0], best_phi[1]))
print(ultimate_best_sol)
print("file : ", filename)
