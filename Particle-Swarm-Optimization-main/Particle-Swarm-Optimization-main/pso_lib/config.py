import numpy as np
import random

#! member 1
# * fixed seed


def init_seeds():
    np.random.seed(42)
    random.seed(42)


# * reading My Data
FILE_NAME = 'cloudlet_problem_dataset_full.xlsx'
