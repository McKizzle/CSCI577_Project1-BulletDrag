#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Cartridge as ct

def main():
    sbct = test_ct()
    print sbct.elevation_at(200.0 * 3.0)

def test_ct():
    sbct = ct.smpl_cartridge()
    sbct.muzz_vel = 3300.0
    sbct.set_fireing_angle()
    sbct.fire()
    #sbct.plot_trajectory()
    #sbct.plot_long_range_trajectory()
    #plt.show()

    return sbct;

if __name__ == '__main__':
    main()

