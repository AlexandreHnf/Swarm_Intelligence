import random
from datetime import datetime

random.seed(datetime.now())

def getRandomSeeds(nb_seeds):
    seeds = []
    for _ in range(nb_seeds):
        seeds.append(random.randint(1, 10000))

    print("random seeds: ", seeds)


def main():
    getRandomSeeds(10)

if __name__ == "__main__":
    main()