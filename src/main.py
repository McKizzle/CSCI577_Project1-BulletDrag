#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Cartridge as ct

def main():
    #test_ct()
    test_w308()

def test_w308():
    w308 = ct.winchester_308_remmignton_express()
    w308.set_fireing_velocity_angle(vel=2820, theta=0.07)
    w308.fire(0, 0.5, 0.0001)
    w308.plot_trajectory()
    w308.plot_long_range_trajectory()
    plt.show()

def test_ct():
    sbct = ct.smpl_cartridge()
    sbct.set_fireing_velocity_angle()
    sbct.fire(0, 0.40, 0.001)
    sbct.plot_trajectory()
    sbct.plot_short_range_trajectory()
    sbct.plot_long_range_trajectory()
    plt.show()

if __name__ == '__main__':
    main()

