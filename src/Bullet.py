import numpy as np
import pylab as py
import matplotlib.pyplot as plt
import math as m
import scipy.integrate as scint
import BallisticModel as bm


X = 0
Y = 1
VX = 2
VY = 3

class Bullet:
    """ Represents a bullet
        TODO: Seperate the into two classes. A cartrige class and rifle class.
    """
    def __init__(self, initial_conditions=np.array([0,0,0,0]), weight=1.0,
            ballistic_coefficient=1.0, ballistic_model = None):
        self.__trajectory = [initial_conditions] 
        self.__weight = weight
        self.__ballistic_coefficient = ballistic_coefficient
        self.__times = [0]
        
        if ballistic_model is not None:
            self.__ballistic_model = ballistic_model
        else:
            self.__ballistic_model = bm.G1()

    def move(self, t, x, g=32.174):
        dxdt = np.zeros(np.size(x))
        dxdt[X] = x[VX]
        dxdt[Y] = x[VY]

        v = np.array(x[VX:VY + 1])
        v_norm = np.linalg.norm(v)
        v_n = v / v_norm
        
        dxdt[VX] = -self.f(v_norm) * v_n[0] / self.__weight
        dxdt[VY] = -g - self.f(v_norm) * v_n[1] / self.__weight

        return dxdt

    def f(self, vel):
        Av, Mv = self.__ballistic_model.get_am(vel)
        F_d = - Av / self.__ballistic_coefficient * vel ** -1 * Mv
        
        return F_d 

    def launch(self, t_0, t_max, dt):
        """ Launch the bullet """
        intgr = scint.ode(self.move)
        intgr.set_integrator('dopri5', method = 'adams')
        intgr.set_initial_value(self.__trajectory[-1])
        times = np.arange(t_0, t_max, dt)
        for t in times[1:]:
            intgr.integrate(intgr.t + dt)
            self.__trajectory.append(intgr.y)
        self.__times = times
        
        print np.array(self.__trajectory)

    def plot_trajectory(self):
        traj = self.__trajectory
        plt.plot(traj[X], traj[Y])#, "ko")
        plt.show()

    def __str__(self):
        wg = "Weight: %0.2f\n" % self.__weight
        bc = "Balistic Coefficient: %0.2f\n" % self.__ballistic_coefficient
        in_cn = "Initial Conditions: " + self.__trajectory[-1].__str__()

        return wg + bc + in_cn + "\n"

    @property
    def cartridge_information(self):
        return sefl.__cartridge_info
    
    @cartridge_information.setter
    def cartridge_information(self, cartridge_info):
        """ Sets the cartridge information
            :param cartridge_info: Expects an array such that
                Index 0: Index Number
                Index 1: Cartridge Type
                Index 2: Bullet Style
                Index 3: Primer No. 
                Index 4: Ballistic Coefficient
        """
        self.__cartridge_info = cartridge_info
     
    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, weight):
        self.__weight = weight

    @property
    def ballistic_coefficient(self):
        return self.__ballistic_coefficient

    @ballistic_coefficient.setter
    def ballistic_coefficient(self, ballistic_coefficient):
        self.__ballistic_coefficient = ballistic_coefficient

    @property
    def position(self):
        self.__trajectory[-1][X:Y+1]
    
    @position.setter
    def position(self, x, y):
        self.__trajectory[-1][X] = x
        self.__trajectory[-1][Y] = y
    
    @property
    def velocity(self):
        return self.__trajectory[-1][VX:VY + 1]

    def set_velocity(self, theta, vel):
        """ Sets the x, y velocities based on an initial velocity and 
            fireing angle.
            :param vel: Velocity in ft/s (def: 3300ft/s)
            :param theta: Firing angle in degrees (def: 0.0 deg)
        """
        theta = np.pi / 180.0 * theta #convert to radians.
        self.__trajectory[-1][VX] = vel * np.cos(theta)
        self.__trajectory[-1][VY] = vel * np.sin(theta)
    

def smpl_bullet_g1():
    smpl = Bullet(ballistic_model = bm.G1())
    smpl.weight = 50
    smpl.ballistic_coeficient = 0.242

    return smpl


#@property
#def weight(self):
#    return self.__weight
#
#@weight.setter
#def weight(self, weight):
#    self.__weight = weight

#@property
#def mass(self):
#    return self.__mass
#
#@mass.setter
#def mass(self, mass):
#    self.__mass = mass
