#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm

def main():
    models = [bm.G1(), bm.G2(),  bm.G5(), bm.G7(), bm.G8()]

    for model in models:
        print model.get_name()

    G1_1 = bm.BallisticModel()
    print G1_1.get_name()


if __name__ == '__main__':
    main()

