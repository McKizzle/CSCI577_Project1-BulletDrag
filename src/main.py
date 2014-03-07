#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import BallisticModel as bm
import Projectile as pjtl

def main():
    #bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    #sample_bullet = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.223]["PRA223RB"])
    #print sample_bullet
    
    #sbct = test_ct()
    #dan_test()
    code_merge_test()
    #print sbct.elevation_at(200.0 * 3.0)
     
    #test_w308()

def test_ct():
    sbct = ct.smpl_cartridge()
    sbct.muzz_vel = 3300.0
    sbct.set_integration_params(0.0, 0.5, 0.001)
    sbct.set_fireing_angle()
    theta = ct.zero_in(sbct, 0.06, 600, 0.0001, 0.95)
    print "Theta: %0.7f" % theta
    print "Y: %0.10f" % sbct.elevation_at(600)
    sbct.plot_trajectory()
    sbct.plot_long_range_trajectory()
    plt.show()

    return sbct;

# Test the merging process. 
def code_merge_test():
    bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    sample_bullet = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.308]["R308W1"])
    sample_bullet.fire()
    pjtl.plot_trajectory(sample_bullet, 0)
    
    #pr=p.Projectile([0.,0.],0.065,2820.,.314,150.,bm.G1())
    #theta = p.zero_in(pr, 0.06, 600, 0.0001, 0.95)
    #pr.fire()
    #p.plot_trajectory(pr, 0)

def dan_test():
    import Projectile as p

    pr=p.Projectile([0.,0.],0.065,2820.,.314,150.,bm.G1())
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

