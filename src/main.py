#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt
import BallisticModel as bm
import Projectile as pjtl

def main():
    bullet_data = pjtl.load_yamlfile("BulletData.yaml")
    sample_bullet = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.223]["PRA223RB"])
    theta =pjtl.zero_in(sample_bullet, 0.065, 600.0, 0.0001, 0.95)
    pjtl.plot_trajectories(sample_bullet)
    plt.savefig("sample_bullet.png", bbox_inches="tight", dpi=240)

    w308 = pjtl.dictionary_for_bullet(bullet_data["cartridges"][0.308]["R308W1"])
    theta = pjtl.zero_in(w308, 0.065, 600, 0.0001, 0.95)
    pjtl.plot_trajectories(w308)
    plt.savefig("winchester308.png", bbox_inches="tight", dpi=240)

if __name__ == '__main__':
    main()

