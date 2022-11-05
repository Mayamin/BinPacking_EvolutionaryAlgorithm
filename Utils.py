
import random

def flip(prob):
	return random.random() < prob

def randInt(low, high):
	return random.randint(low, high-1)
