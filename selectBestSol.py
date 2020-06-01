import csv

def selectBestSol(filename, conv_thresh):
    best_sol = {"id": 0, "sol": 0, "evals": [], "avg": 100000, "conv": 0,"pvalue": 0, "conv_pvalue": 0}  # best

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        i = 0

        for row in csv_reader:
            if i != 0 : # if not names
                sol = int(row[0])
                evals = [int(e) for e in row[1][1:-1].split(",") if (int(e) < conv_thresh)]
                pvalue = float(row[-2])
                conv_pvalue = float(row[-1])
                conv = float(row[2])
                # print(evals)
                average = sum(evals) / len(evals)
                print(row)
                print("average: ", average)

                if average < best_sol["avg"] and conv >= 90:
                    best_sol = {"id": i, "sol": sol, "evals": evals, "avg": average, "conv": conv, "pvalue": pvalue, "conv_pvalue": conv_pvalue}

            i += 1

    return best_sol

def selectBestPhis(conv_thresh):
    phis = [(1,1), (0,1), (1,0), (1,2), (2,1), (0.5,3), (3,0.5)]
    filenames = ["Results/stat10_10_10_20_1_1_2020-06-01 17:37:19.673179.csv",
                 "Results/stat10_10_10_20_0_1_2020-06-01 17:43:01.113775.csv",
                 "Results/stat10_10_10_20_1_0_2020-06-01 17:48:25.044962.csv",
                 "Results/stat10_10_10_20_1_2_2020-06-01 17:52:37.832200.csv",
                 "Results/stat10_10_10_20_2_1_2020-06-01 17:58:41.295725.csv",
                 "Results/stat10_10_10_20_0.5_3_2020-06-01 18:04:32.152520.csv",
                 "Results/stat10_10_10_20_3_0.5_2020-06-01 18:10:23.641877.csv"
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
