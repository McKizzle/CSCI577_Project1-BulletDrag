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
        self.__weight = float(weight)
        self.__ballistic_coefficient = float(ballistic_coefficient)
        self.__times = [0]
        self.__steps = 0
        
        if ballistic_model is not None:
            self.__ballistic_model = ballistic_model
        else:
            self.__ballistic_model = bm.G1()

    def move(self, t, x, g=32.1522):
        """ ODE system for bullet movement """
        v = np.array(x[VX:VY + 1])
        v_norm = np.linalg.norm(v)
        v_u = v / v_norm

        a_x = -self.f(v_norm) * v_u[0] / self.__weight
        a_y = -g - self.f(v_norm) * v_u[1] / self.__weight
         
        dxdt = np.array([v[0], v[1], a_x, a_y])
        #print dxdt
        #exit()
        return dxdt

    def f(self, vel):
        Av, Mv = self.__ballistic_model.get_am(vel)
        force = Av / self.__ballistic_coefficient * vel **(Mv - 1) 
        
        return force

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
    
    def plot_trajectory(self):
        traj = np.array(self.__trajectory) 
        plt.plot(traj[:,X]/3, traj[:,Y])#, "ko")
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
     
    def weight(self):
        return self.__weight
 
    def set_weight(self, weight):
        self.__weight = weight
    
    def get_ballistic_coefficient(self):
        return self.__ballistic_coefficient

    def set_ballistic_coefficient(self, ballistic_coefficient):
        self.__ballistic_coefficient = float(ballistic_coefficient)

    def get_position(self):
        self.__trajectory[-1][X:Y+1]
    
    def set_position(self, x, y):
        self.__trajectory[-1][X] = x
        self.__trajectory[-1][Y] = y
    
    def get_velocity(self):
        return self.__trajectory[-1][VX:VY + 1]

    def set_velocity(self, theta, vel):
        """ Sets the x, y velocities based on an initial velocity and 
            fireing angle.
            :param vel: Velocity in ft/s (def: 3300ft/s)
            :param theta: Firing angle in degrees (def: 0.0 deg)
        """
        theta = np.pi / 180.0 * float(theta) #convert to radians.
        self.__trajectory[-1][VX] = float(vel) * np.cos(float(theta))
        self.__trajectory[-1][VY] = float(vel) * np.sin(float(theta))
    

def smpl_bullet_g1():
    smpl = Bullet(ballistic_model = bm.G1())
    smpl.set_weight(50.0)
    smpl.set_ballistic_coefficient(0.242)

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
