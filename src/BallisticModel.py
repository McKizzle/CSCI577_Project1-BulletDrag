import numpy as np
import pylab as py
#import matplotlib.pyplot as plt
import math as m

""" Clintons Ballistic coeficient equation.

y=\left\{\begin{array}{cc} f\left( x \right) & x\leq 1.2 \\ f\left( 1.2 \right)\; -\; e^{-1.2}\; +\; e^{-x} & x>1.2 \end{array}\right

"""

G1_DATA = np.array([[ 4230 , 1.477404177730177e-04 , 1.9565 ],
    [ 3680 , 1.920339268755614e-04 , 1.925 ],
    [ 3450 , 2.894751026819746e-04 , 1.875 ],
    [ 3295 , 4.349905111115636e-04 , 1.825 ],
    [ 3130 , 6.520421871892662e-04 , 1.775 ],
    [ 2960 , 9.748073694078696e-04 , 1.725 ],
    [ 2830 , 1.453721560187286e-03 , 1.675 ],  
    [ 2680 , 2.162887202930376e-03 , 1.625 ],
    [ 2460 , 3.209559783129881e-03 , 1.575 ],
    [ 2225 , 3.904368218691249e-03 , 1.55 ],   
    [ 2015 , 3.222942271262336e-03 , 1.575 ],
    [ 1890 , 2.203329542297809e-03 , 1.625 ],
    [ 1810 , 1.511001028891904e-03 , 1.675 ],
    [ 1730 , 8.609957592468259e-04 , 1.75 ],
    [ 1595 , 4.086146797305117e-04 , 1.85 ],
    [ 1520 , 1.954473210037398e-04 , 1.95 ],
    [ 1420 , 5.431896266462351e-05 , 2.125 ],
    [ 1360 , 8.847742581674416e-06 , 2.375 ],
    [ 1315 , 1.456922328720298e-06 , 2.625 ],
    [ 1280 , 2.419485191895565e-07 , 2.875 ],
    [ 1220 , 1.657956321067612e-08 , 3.25 ],
    [ 1185 , 4.745469537157371e-10 , 3.75 ],
    [ 1150 , 1.379746590025088e-11 , 4.25 ],
    [ 1100 , 4.070157961147882e-13 , 4.75 ],
    [ 1060 , 2.938236954847331e-14 , 5.125 ],
    [ 1025 , 1.228597370774746e-14 , 5.25 ],
    [ 980 , 2.916938264100495e-14 , 5.125 ],
    [ 945 , 3.855099424807451e-13 , 4.75 ],
    [ 905 , 1.185097045689854e-11 , 4.25 ],
    [ 860 , 3.566129470974951e-10 , 3.75 ],
    [ 810 , 1.045513263966272e-08 , 3.25 ],
    [ 780 , 1.291159200846216e-07 , 2.875 ],
    [ 750 , 6.824429329105383e-07 , 2.625 ],
    [ 700 , 3.569169672385163e-06 , 2.375 ],
    [ 640 , 1.839015095899579e-05 , 2.125 ],
    [ 600 , 5.71117468873424e-05 , 1.950 ],
    [ 550 , 9.226557091973427e-05 , 1.875 ],
    [ 250 , 9.337991957131389e-05 , 1.875 ],
    [ 100 , 7.225247327590413e-05 , 1.925 ],
    [ 65 , 5.792684957074546e-05 , 1.975 ],
    [ 0 , 5.206214107320588e-05 , 2.000 ]])

G2_DATA = np.array([[ 1674 , .0079470052136733 , 1.36999902851493 ],
    [ 1172 , 1.00419763721974e-03 , 1.65392237010294 ],
    [ 1060 , 7.15571228255369e-23 , 7.91913562392361 ],
    [ 949 , 1.39589807205091e-10 , 3.81439537623717 ],
    [ 670 , 2.34364342818625e-04 , 1.71869536324748 ],
    [ 335 , 1.77962438921838e-04 , 1.76877550388679 ],
    [ 0 , 5.18033561289704e-05 , 1.98160270524632 ]])
    
G5_DATA = np.array([[ 1730 , 7.24854775171929e-03 , 1.41538574492812 ],
    [ 1228 , 3.50563361516117e-05 , 2.13077307854948 ],
    [ 1116 , 1.84029481181151e-13 , 4.81927320350395 ],
    [ 1004 , 1.34713064017409e-22 , 7.8100555281422 ],
    [ 837 , 1.03965974081168e-07 , 2.84204791809926 ],
    [ 335 , 1.09301593869823e-04 , 1.81096361579504 ],
    [ 0 , 3.51963178524273e-05 , 2.00477856801111 ]])

G7_DATA = np.array([[ 4200 , 1.29081656775919e-09 , 3.24121295355962 ],
    [ 3000 , 0.0171422231434847 , 1.27907168025204 ],
    [ 1470 , 2.33355948302505e-03 , 1.52693913274526 ],
    [ 1260 , 7.97592111627665e-04 , 1.67688974440324 ],
    [ 1110 , 5.71086414289273e-12 , 4.3212826264889 ],
    [ 960 , 3.02865108244904e-17 , 5.99074203776707 ],
    [ 670 , 7.52285155782535e-06 , 2.1738019851075 ],
    [ 540 , 1.31766281225189e-05 , 2.08774690257991 ],
    [ 0 , 1.34504843776525e-05 , 2.08702306738884 ]])

G8_DATA = np.array([[ 3571 , .0112263766252305 , 1.33207346655961 ],
    [ 1841 , .0167252613732636 , 1.28662041261785 ],
    [ 1120 , 2.20172456619625e-03 , 1.55636358091189 ],
    [ 1088 , 2.0538037167098e-16 , 5.80410776994789 ],
    [ 976 , 5.92182174254121e-12 , 4.29275576134191 ],
    [ 0 , 4.3917343795117e-05 , 1.99978116283334 ]])


def f_drag_G_models(self, vel):
    """ Drag function """
    Av, Mv = self.model.get_am(vel)
    force = Av / self.bc * vel**(Mv - 1) ## * 100000
     
    return force

class BallisticModel:
    def __init__(self, name="My Model"):
        """ Initializes a balistic model. 
            Expects the model data to be passed in as an array such that column one 
            is the velocity, the second column is A and the third column is M.

            :param model_data: Expects a numpy array. If not passed in defaults to G1. 
        """ 
        self.name = name

    def f(self, vel):
        return vel
 
    def __str__(self):
        return self.name

class G_Model(BallisticModel):
    def __init__(self, model_data=G1_DATA, name="G1"):
        BallisticModel.__init__(self, name)
        self.model = model_data

    def f(self, vel, bc):
        """ Drag function """
        Av, Mv = self.get_am(vel)
        force = Av / bc * vel**(Mv - 1) 
         
        return force
    
    def get_am(self, vel):
        vels=self.model[:,0]
        Av = 0
        Mv = 0
        for i in range(0, len(self.model[:,0]) - 1, 1):
            if(vels[i] >= vel and vels[i+1] < vel):
                # Perform linear interpolation
                bounds = np.array([self.model[i], self.model[i+1]])
                vp = bounds[:, 0]

                # Linear interp for A(v)
                fp = bounds[:, 1]
                Av = np.interp(vel, vp, fp)

                # Linear interp for M(v)
                fp = bounds[:, 2]
                Mv = np.interp(vel, vp, fp)

                break

        return np.array([Av, Mv])

class Custom_Model(BallisticModel):
    def __init__(self, rho=1.293e-3, csa=np.pi, cd=1, name="Custom Drag Coefficient"):
        BallisticModel.__init__(self, name)
        self.rho = rho
        self.csa = csa
        self.cd = cd

    def f(self, vel, bc):
        """ Drag function that takes a custom
            drag coefficient that is dependant of the velocity.
        """
        force = -0.5 * self.rho * vel**2.0 * self.csa * self.cd(vel)

        return force

    def custom_cd(self, vel):
        """ Custom drag coefficient function.
            :param vel: Assumes a velocity of ft/sec
        """
        # 1 116.43701 ft / s
        mach = vel / 1116.43701

        f_vel = 1.0 / (20.0 * ( 1.534 + vel)**2.0)
        f_12 = 1.0 / (20.0 * ( 1.534 + 1.2)**2.0)

        if(mach <= 1.2):
            return f_vel 
        else:
            return f_12 - np.exp(-1.2) 

def diam4csa(diam):
    """ Calcuates the csa of a sphere given a diameter """
    return np.pi * (float(diam) / 2.0)**2
 
def G1():
    return G_Model()

def G2():
    return G_Model(G2_DATA, "G2")

def G5(): 
    return G_Model(G5_DATA, "G5")

def G7():
    return G_Model(G7_DATA, "G7")

def G8():
    return G_Model(G8_DATA, "G8")


 
