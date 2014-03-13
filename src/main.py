#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import matplotlib as mtlb
import BallisticModel as bm
import Projectile as pjtl


def main():
    # sample_bullet = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.223]["PRA223RB"])
    # theta =pjtl.zero_in(sample_bullet, 0.065, 600.0, 0.0001, 0.95)
    # pjtl.plot_trajectories(sample_bullet)
    # plt.savefig("sample_bullet.png", bbox_inches="tight", dpi=240)
    #
    # w308 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.308]["R308W1"])
    # theta = pjtl.zero_in(w308, 0.065, 600, 0.0001, 0.95)
    # pjtl.plot_trajectories(w308)
    # plt.savefig("winchester308.png", bbox_inches="tight", dpi=240)
    
    # Compare the lapua 338 against various models.  
    bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    lm338 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.338]["4318013"])
    compare_models(lm338)
    
    # Compare the winchester 308 against various models. 
    bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    wnchstr338 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.308]["R308W1"])
    compare_models(wnchstr338)
 
def compare_models(bllt, theta=0.06):
    bllt.model = bm.G1()
    bllt.set_integration_params(0.0, 2.5, 0.001)
    theta = pjtl.zero_in(bllt, theta, 600.0, 0.001, 0.80) #zero in at 200 yards. 
    x_g1 = np.array(bllt.x)
    v_g1 = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    bllt.model = bm.G2()
    bllt.set_fireing_angle(theta)
    bllt.fire()
    x_g2 = np.array(bllt.x)
    v_g2 = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    bllt.model = bm.G5()
    bllt.set_fireing_angle(theta)
    bllt.fire()
    x_g5 = np.array(bllt.x)
    v_g5 = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    bllt.model = bm.G7()
    bllt.set_fireing_angle(theta)
    bllt.fire()
    x_g7 = np.array(bllt.x)
    v_g7 = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    bllt.model = bm.G8()
    bllt.set_fireing_angle(theta)
    bllt.fire()
    x_g8 = np.array(bllt.x)
    v_g8 = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    cust_mod = bm.Custom_Model()
    diam = bm.mm2ft(bllt.diameter)
    cust_mod.csa = bm.diam4csa(diam)
    bllt.model = cust_mod
    bllt.set_fireing_angle(theta)
    bllt.fire()
    x_cust = np.array(bllt.x)
    v_cust = bllt.get_velocity_trajectory()
    bllt.reset_trajectory()

    l_1, = plt.plot(x_g1[:, 0]/3., x_g1[:, 1]*12., 'b')
    l_2, = plt.plot(x_g2[:, 0]/3., x_g2[:, 1]*12., 'g')
    l_5, = plt.plot(x_g5[:, 0]/3., x_g5[:, 1]*12., 'r')
    l_7, = plt.plot(x_g7[:, 0]/3., x_g7[:, 1]*12., 'c')
    l_8, = plt.plot(x_g8[:, 0]/3., x_g8[:, 1]*12., 'y')
    l_cust, = plt.plot(x_cust[:, 0]/3., x_cust[:, 1]*12., 'k')
    lrt = bllt.plot_lrt()
    title = "Trajectories of a %s: %d grain Bullet" % (bllt.name, bllt.mass)
    plt.title(title)
    plt.xlabel("Yards (yd)")
    plt.ylabel(r"Inches (in)")
    plt.legend([l_1, l_2, l_5, l_7, l_8, l_cust, lrt], 
            [bm.G1().name, bm.G2().name, bm.G5().name, bm.G7().name, bm.G8().name, cust_mod.name, "Long Range Traj."])
    plt.savefig("../img/%s_dist_comp.png" % bllt.name, bbox_inches="tight", dpi=240)
    plt.close()


    l_1, = plt.plot(x_g1[:, 0]/3., v_g1, 'b')
    l_2, = plt.plot(x_g2[:, 0]/3., v_g2, 'g')
    l_5, = plt.plot(x_g5[:, 0]/3., v_g5, 'r')
    l_7, = plt.plot(x_g7[:, 0]/3., v_g7, 'c')
    l_8, = plt.plot(x_g8[:, 0]/3., v_g8, 'y')
    l_cust, = plt.plot(x_cust[:, 0]/3., v_cust, 'k')
    lrt = bllt.plot_vrt()
    title = "Velocity of a %s: %d grain Bullet" % (bllt.name, bllt.mass)
    plt.title(title)
    plt.xlabel("Yards (yd)")
    plt.ylabel(r"Velocity $^{ft}/_s$")
    plt.legend([l_1, l_2, l_5, l_7, l_8, l_cust, lrt], 
            [bm.G1().name, bm.G2().name, bm.G5().name, bm.G7().name, bm.G8().name, cust_mod.name, "Long Range Traj."])
    plt.savefig("../img/%s_vel_comp.png" % bllt.name, bbox_inches="tight", dpi=240)
    plt.close()

if __name__ == '__main__':
    main()
