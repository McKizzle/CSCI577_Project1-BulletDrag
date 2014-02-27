#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Bullet as blt

def main():
    #models = [bm.G1(), bm.G2(),  bm.G5(), bm.G7(), bm.G8()]

    #for model in models:
    #    print model.get_name()

    #G1_1 = bm.BallisticModel()
    #print G1_1.get_name()

    #print G1_1.__dmodel
    test_1()
    #test_2()
    #test_3()

# Sample bullet with G1 Model @ 0.0 deg
def test_1():
    sblt = blt.smpl_bullet_g1()
    sblt.set_velocity(0.06, 3300)
    sblt.launch(0, 0.25, 0.0001)
    sblt.plot_trajectory()

# Sample bullet with G1 Model @ 2.0 deg
def test_2():
    sblt = blt.smpl_bullet_g1()
    sblt.set_velocity(0.06, 3300)
    print sblt.velocity

# Sample bullet with G1 Model @ 4.0 deg
def test_3():
    sblt = blt.smpl_bullet_g1()
    sblt.set_velocity(4.0, 3300)
    print sblt.velocity

if __name__ == '__main__':
    main()

