#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Cartridge as ct

def main():
    sbct = test_ct()
    #print sbct.elevation_at(200.0 * 3.0)
     
    #test_w308()

def test_ct():
    sbct = ct.smpl_cartridge()
    sbct.muzz_vel = 3300.0
    sbct.set_integration_params(0.0, 0.5, 0.001)
    sbct.set_fireing_angle()
    theta = ct.zero_in(sbct, 0.06, 600, 0.0001, 0.95)
    print "Theta: %0.7f" % theta
    sbct.set_fireing_angle(theta)
    sbct.fire()
    print "Y: %0.10f" % sbct.elevation_at(600)
    sbct.plot_trajectory()
    sbct.plot_long_range_trajectory()
    plt.show()

    return sbct;

#def test_w308():
#    w308 = ct.winchester_308_remmignton_express()
#    w308.set_fireing_velocity_angle(vel=2820, theta=0.07)
#    w308.fire(0, 0.5, 0.0001)
#    w308.plot_trajectory()
#    w308.plot_long_range_trajectory()
#    plt.show()

if __name__ == '__main__':
    main()

