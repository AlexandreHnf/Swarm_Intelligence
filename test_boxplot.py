from scipy.stats import ranksums
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def testRanksums():
    z = [232, 270, 293, 377, 311, 862, 278, 396, 401, 277, 320, 262, 302, 295, 508, 259, 391, 222, 366, 471, 282, 288, 509, 245, 632, 315, 360, 230, 283, 334, 514, 364, 521, 458, 437, 386, 261, 279, 372, 399, 428, 264, 423, 343, 316, 274, 543, 278, 375, 319, 450, 453, 279, 389, 347, 450, 480, 400, 534, 351, 283, 316, 556, 306, 527, 731, 269, 264, 300, 276, 283, 277, 262, 334, 282, 355, 216, 378, 269, 448, 416, 288, 333, 295, 278, 361, 311, 1000, 361, 271, 204, 292, 672, 297, 269, 431, 249, 293, 222, 352]

    count = 0
    for i in z:
        if i > 500:
            count += 1
    print("nb of > 500 : ", count)


    x = [280, 289, 276, 267, 230, 281, 271, 224, 200, 301]
    y = []

    for i in z:
        if i < 500:
            y.append(i)

    print(x)
    print(y)
    p_value = ranksums(x, y)
    print("pvalue = ", p_value)

def testRanksums2():
    x = [280]
    y = [232, 270, 293, 377, 311, 862, 278, 396, 401, 277]
    p_value = ranksums(x, y)
    print("pvalue = ", p_value)


def test_boxplots():

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    # fake up some data
    spread = np.random.rand(50) * 100
    center = np.ones(25) * 50
    # flier_high = np.random.rand(10) * 100 + 100
    # flier_low = np.random.rand(10) * -100
    # data = np.concatenate((spread, center, flier_high, flier_low))
    data = np.concatenate((spread, center))

    print("spread: ", spread)
    print("center: ", center)
    # print("flier_high: ", flier_high)
    # print("flier_low: ", flier_low)
    print("data: ", data)

    fig1, ax1 = plt.subplots()
    ax1.set_title('Basic Plot')
    ax1.boxplot(data)

    plt.show()

def test_boxplots2():
    # center = np.ones(25) * 280
    center = [280]
    spread = [232, 270, 293, 377, 311, 278, 396, 401, 277]
    data = np.concatenate((spread, center))

    fig1, ax1 = plt.subplots()
    ax1.set_title('Basic Plot')
    ax1.boxplot(data)

    plt.show()

def test_boxplots3():
    inc = 0.1
    e1 = np.random.normal(0, 1, size=500)
    e2 = np.random.normal(0, 1, size=500)
    e3 = np.random.normal(0, 1 + inc, size=500)
    e4 = np.random.normal(0, 1 + 2 * inc, size=500)

    treatments = [e1, e2, e3, e4]
    med1, CI1 = 0.1, (-0.25, 0.25)
    med2, CI2 = 0.2, (-0.35, 0.50)
    medians = [None, None, med1, med2]
    conf_intervals = [None, None, CI1, CI2]

    fig, ax = plt.subplots()
    pos = np.array(range(len(treatments))) + 1
    bp = ax.boxplot(treatments, sym='k+', positions=pos,
                    notch=1, bootstrap=5000,
                    usermedians=medians,
                    conf_intervals=conf_intervals)

    ax.set_xlabel('treatment')
    ax.set_ylabel('response')
    plt.setp(bp['whiskers'], color='k', linestyle='-')
    plt.setp(bp['fliers'], markersize=3.0)
    plt.show()

def test_boxplots4():
    z = [232, 270, 293, 377, 311, 862, 278, 396, 401, 277, 320, 262, 302, 295, 508, 259, 391, 222, 366, 471, 282, 288,
         509, 245, 632, 315, 360, 230, 283, 334, 514, 364, 521, 458, 437, 386, 261, 279, 372, 399, 428, 264, 423, 343,
         316, 274, 543, 278, 375, 319, 450, 453, 279, 389, 347, 450, 480, 400, 534, 351, 283, 316, 556, 306, 527, 731,
         269, 264, 300, 276, 283, 277, 262, 334, 282, 355, 216, 378, 269, 448, 416, 288, 333, 295, 278, 361, 311, 1000,
         361, 271, 204, 292, 672, 297, 269, 431, 249, 293, 222, 352]

    y = []
    for i in range(0, len(z), 10):
        # print(z[i:i+10])
        y.append(z[i:i+10])
    medians = [280, 289, 276, 267, 230, 281, 271, 224, 200, 301]

    fig, ax = plt.subplots()
    pos = np.array(range(len(y))) + 1
    bp = ax.boxplot(y, sym='k+', positions=pos,
                    usermedians=medians)

    ax.set_xlabel('Evaluations')
    ax.set_ylabel('PSO solutions')
    # plt.setp(bp['whiskers'], color='k', linestyle='-')
    # plt.setp(bp['fliers'], markersize=3.0)

    plt.savefig("boxplot{}.png".format(datetime.today()))
    # plt.show()

# testRanksums()
# testRanksums2()
# test_boxplots()
# test_boxplots2()
# test_boxplots3()
test_boxplots4()