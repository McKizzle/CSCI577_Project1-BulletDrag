#!/usr/bin/env python
import scipy.integrate as scint
import numpy as np
import math as mt
import matplotlib.pyplot as plt

import BallisticModel as bm
import Cartridge as ct

def main():
    test_ct()

def test_ct():
    sbct = ct.Cartridge()
    sbct.set_fireing_velocity_angle()
    sbct.fire(0, 0.25, 0.0001)
    sbct.plot_trajectory()

if __name__ == '__main__':
    main()

