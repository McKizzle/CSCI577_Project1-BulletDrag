#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import matplotlib as mtlb
import BallisticModel as bm
import Projectile as pjtl

def main():
    bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    # sample_bullet = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.223]["PRA223RB"])
    # theta =pjtl.zero_in(sample_bullet, 0.065, 600.0, 0.0001, 0.95)
    # pjtl.plot_trajectories(sample_bullet)
    # plt.savefig("sample_bullet.png", bbox_inches="tight", dpi=240)
    #
    # w308 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.308]["R308W1"])
    # theta = pjtl.zero_in(w308, 0.065, 600, 0.0001, 0.95)
    # pjtl.plot_trajectories(w308)
    # plt.savefig("winchester308.png", bbox_inches="tight", dpi=240)

    #lm338 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.338]["4318013"])
    #lm338.set_integration_params(0.0, 2.5, 0.001)
    #lm338.set_fireing_angle(0.043527024669)
    #lm338.fire()
    ##theta = pjtl.zero_in(lm338, 0.065, 109.361 * 3.0, 0.001, 0.80)
    ##print theta
    #pjtl.plot_trajectories(lm338)
    #plt.savefig("lapuamagnum338.png", bbox_inches="tight", dpi=240)
    #plt.close()

    # Bullet using my drag coefficient function. 
    lm338 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.338]["4318013"])
    lm338.set_integration_params(0.0, 2.5, 0.001)
    lm338.set_fireing_angle(0.043527024669)
    lm338.fire()
    #theta = pjtl.zero_in(lm338, 0.065, 109.361 * 3.0, 0.001, 0.80)
    #print theta
    pjtl.plot_trajectories(lm338)
    plt.savefig("lapuamagnum338.png", bbox_inches="tight", dpi=240)
    plt.close()

if __name__ == '__main__':
    main()
