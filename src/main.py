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
    sample_bullet.fire()
    pjtl.plot_trajectory(sample_bullet, 0)

if __name__ == '__main__':
    main()

