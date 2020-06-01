import random
import time
import math

def getRandom01(rng):
	""" 
	random function for values in [0,1]
	"""
	return rng.random()

def displayTiming(start_time):
	end_time_sec = time.time() - start_time
	in_minutes = math.floor(end_time_sec / 60)
	print("=========== Time spent: ")
	print("{} seconds".format(end_time_sec))
	print("{} minutes and {} seconds".format(in_minutes, end_time_sec - in_minutes*60))