import scipy.stats as ss
import numpy as np
import math


import random


def multitaskin( partic):
    print ( " multi  " +str( partic))

    x =  ( math.exp(-partic ))

    return x


effect = [ 1, 2,3,4,5]
for f in effect:
        m = multitaskin( f)
        print(m)


