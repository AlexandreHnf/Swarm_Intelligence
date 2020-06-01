import random
from datetime import datetime



def getRandomSeeds(nb_seeds):
    random.seed(datetime.now())
    seeds = []
    for _ in range(nb_seeds):
        seeds.append(random.randint(1, 10000))

    print("random seeds: ", seeds)

def testClassicRandom():
    random.seed(443)
    x = [random.randrange(50, 1000) for _ in range(10)]
    print("with random.seed(443) : ", x)

    random.seed(4849)
    y = [random.randrange(50, 1000) for _ in range(10)]
    print("with random.seed(4849) : ", y)

def testRandomRandom():
    rng = random.Random(443)
    x = [rng.randrange(50, 1000) for _ in range(5)]
    print("with rng(443): ", x)

    rng2 = random.Random(4849)
    y = [rng2.randrange(50, 1000) for _ in range(5)]
    print("with rng2(4849): ", y)

    x = [rng.randrange(50, 1000) for _ in range(5)]
    print("with rng(443): ", x)

    y = [rng2.randrange(50, 1000) for _ in range(5)]
    print("with rng2(4849): ", y)

def main():
    # getRandomSeeds(10)
    testClassicRandom()
    testRandomRandom()


if __name__ == "__main__":
    main()