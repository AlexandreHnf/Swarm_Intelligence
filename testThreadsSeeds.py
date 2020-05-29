import time
import random
import threading
import math


class Lol:

    def __init__(self, my_id):
        self.random_numbers = []
        random.seed(my_id)

    def generateRandoms(self):
        for i in range(10):
            r = random.randint(1, 1000)
            self.random_numbers.append(r)
        return self.random_numbers


class testThread:

    def __init__(self, nb_threads):
        self.nb_threads = nb_threads
        self.all_random_numbers = [0 for _ in range(self.nb_threads)]

    def thread_function(self, name):
        lol = Lol(name+1)
        self.all_random_numbers[name] = lol.generateRandoms()

    def run_with_threads(self):
        start_time = time.time()

        threads = list()
        for index in range(self.nb_threads):
            x = threading.Thread(target=self.thread_function, args=(index,))
            threads.append(x)
            x.start()

        for index, thread in enumerate(threads):
            thread.join()

        end_time_sec = time.time() - start_time
        in_minutes = math.floor(end_time_sec / 60)

        print("=========== Time spent in total: ")
        print("{} seconds".format(end_time_sec))
        print("{} minutes and {} seconds".format(in_minutes, end_time_sec - in_minutes * 60))

        self.display()

    def display(self):
        for i in range(len(self.all_random_numbers)):
            print(f"{i} : {self.all_random_numbers[i]}")

if __name__ == "__main__":
    tt = testThread(2)
    tt.run_with_threads()