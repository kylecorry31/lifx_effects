import numpy as np
import random

def rand(min, max):
    r = max - min
    return random.random() * r + min

def sample(mean, stdev):
    return stdev * np.random.randn() + mean