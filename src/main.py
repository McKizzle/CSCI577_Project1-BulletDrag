#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Cartridge as ct

def main():
    #sbct = test_ct()
    dan_test()
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

def code_merge_test()
    import Projectile as p
    pr=p.Projectile([0.,0.],0.065,2820.,.314,150.,bm.GM1())
    pr.fire(0,0.5)
    pr.find_angle(200.0)
    pr.plotme()

def dan_test():
    import Projectile as p
    #kg=1
    #while kg==1:
    #	angle=float(input('enter barrel angle (degrees) '))
    #	vel=float(input('enter muzzle velocity (feet/second) '))
    #	bc=float(input('enter ballistic coefficient '))
    #	w=float(input('enter bullet weight (grains) '))
    #	tf=float(input('enter simulation duration (seconds) '))
    #	g=input('enter standard projectile (1,2,5,7,8) ')
    #	pr=p.Projectile([0.,0.],angle,vel,bc,w,g)
    #	pr.fire(0.,tf)
    #	pr.plotme()
    #	kg=input('enter 1 to repeat, 0 to exit ')

    pr=p.Projectile([0.,0.],0.065,2820.,.314,150.,1)
    pr.fire(0,0.5)
    pr.find_angle(200.0)
    pr.plotme()

#def test_w308():
#    w308 = ct.winchester_308_remmignton_express()
#    w308.set_fireing_velocity_angle(vel=2820, theta=0.07)
#    w308.fire(0, 0.5, 0.0001)
#    w308.plot_trajectory()
#    w308.plot_long_range_trajectory()
#    plt.show()

if __name__ == '__main__':
    main()

