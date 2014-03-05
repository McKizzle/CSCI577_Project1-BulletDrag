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

LB_GRAIN = 1.0/7000.0

def zero():
    return 0.0

def smpl_long_range():
    return np.array(
        [[100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0],
         [-0.1, 1.3, zero(), -2.6, -6.9, -21.2, -45.8]])

def smpl_short_range():
    return np.array(
        [[50.0, 100.0, 150.0, 200.0, 250.0, 300.0],
         [0.0, 0.5, zero(), -1.7, -4.8, -9.4]])

def smpl_cartridge():
    smpl = Cartridge()
    smpl.set_fireing_angle()
    smpl.set_short_range_trajectory()
    smpl.set_long_range_trajectory()

    return smpl

def zero_in(cartridge, starting_theta, dist, tol, r):
    """ Takes a Cartridge and zeros it in the specified distance within 
        a tolerance using a binary search algorithm. 

        :param cartridge: the cartridge to zero in
        :param starting_theta: the starting angle in degrees. 
        :param dist: the distance to zero in on.
        :param tol: the tolorance 
        :param r: the ratio (affects the speed at which the search algorithm converges
    """
    
    zeroed_in = False
    theta = starting_theta
    while not zeroed_in:
        catridge.set_fireing_angle(theta)
        print "Searching"

#def winchester_308_remmignton_express():
#    w308 = Cartridge(mass_grains=150, ballistic_coefficient=.314)
#    w308_long_range = np.array(
#            [[100.0, 150.0, 200.0, 250.0, 300.0, 400.0, 500.0],
#             [2.0, 1.7, zero(), -3.4, -8.8, -26.2, -54.8]]
#    w308.set_long_range_trajectory(long_range_trajectory=w308_long_range)
#
#    return w308

class Cartridge:
    """ Represents a catridge object, 
        which contains the bullet properties and range trajectories
    """
    def __init__(   self, 
                    initial_conditions=np.array([0.0,0.0,0.0,0.0]), 
                    mass_grains=50.0,
                    ballistic_coefficient=0.242, 
                    ballistic_model = bm.G1()
                    ):
        self.trajectory = [initial_conditions] 
        self.mass_grains = float(mass_grains) * LB_GRAIN
        self.ballistic_coefficient = float(ballistic_coefficient)
        self.times = [0]
        self.ballistic_model = ballistic_model
        self.dt = 0.001
        self.t_0 = 0.0
        self.t_max = 0.5
        self.muzz_vel = 3300.0
    
    def set_fireing_angle(self, theta=0.06):
        """ Sets the x, y velocities based on an initial velocity and 
            fireing angle.
            :param vel: Velocity in ft/s (def: 3300ft/s)
            :param theta: Firing angle in degrees (def: 0.0 deg)
        """
        theta = np.pi / 180.0 * float(theta) #convert to radians.
        self.trajectory[-1][VX] = float(self.muzz_vel) * np.cos(float(theta))
        self.trajectory[-1][VY] = float(self.muzz_vel) * np.sin(float(theta))

    def move(self, t, x, g=32.1522):
        """ ODE system for bullet movement """
        v = np.array(x[VX:VY + 1])
        v_norm = np.linalg.norm(v)
        v_u = v / v_norm

        a_x = -self.f(v_norm) * v_u[0] / self.mass_grains
        a_y = -g - self.f(v_norm) * v_u[1] / self.mass_grains
         
        dxdt = np.array([v[0], v[1], a_x, a_y])
        return dxdt

    def f(self, vel):
        """ Drag function """
        Av, Mv = self.ballistic_model.get_am(vel)
        force = Av / self.ballistic_coefficient * vel **(Mv - 1) 
        
        return force

    def fire(self):
        """ Launch the bullet """
        intgr = scint.ode(self.move)
        intgr.set_integrator('dopri5', method = 'adams')
        intgr.set_initial_value(self.trajectory[-1])
        times = np.arange(self.t_0, self.t_max, self.dt)
        for t in times[1:]:
            intgr.integrate(intgr.t + self.dt)
            self.trajectory.append(intgr.y)
        self.times = times

    def elevation_at(self, dist):
        """ Finds the elevation at a specified distance. 
            Don't forget to pass in the distance as feet
        """
        traj = np.array(self.trajectory)
        print traj.shape

        for i in range(0, traj.shape[0] - 1):
            print "---------------------------------------"
            print "dist: %0.3f" % dist
            print "x_%i: %0.3f" % (i, traj[i, 0])
            print "x_%i: %0.3f" % (i + 1, traj[i + 1, 0])
            if traj[i, 0] >= dist and traj[i + 1, 0] < dist:
                bounds = np.array([traj[i], traj[i + 1]])
                print bounds
                return 0

        #for i in range(0, len(self.__model[:,0]) - 1, 1):
        #    if(vels[i] >= vel and vels[i+1] < vel):
        #        # Perform linear interpolation
        #        bounds = np.array([self.__model[i], self.__model[i+1]])
        #        vp = bounds[:, 0]

        #        # Linear interp for A(v)
        #        fp = bounds[:, 1]
        #        Av = np.interp(vel, vp, fp)

        #        # Linear interp for M(v)
        #        fp = bounds[:, 2]
        #        Mv = np.interp(vel, vp, fp)

        #        break
    
    def plot_trajectory(self):
        traj = np.array(self.trajectory) 
        tr, = plt.plot(traj[:,X] / 3, traj[:,Y] * 12, 'b')
        plt.xlabel("Yards")
        plt.ylabel("Inches")
        plt.title("Bullet Trajectory")
        return tr
    
    def plot_short_range_trajectory(self):
        srt, = plt.plot(self.srt[0,:], self.srt[1,:], '.c')

    def plot_long_range_trajectory(self):
        lrt, = plt.plot(self.lrt[0, :], self.lrt[1, :], '4b') 
     
    def set_long_range_trajectory(self, long_range_trajectory=smpl_long_range()):
        """ Set the long range trajectory. Assumes that the trajectory are inches vs yards.
            :param long_range_trajectory: Expects a 2D numpy array. The first row contains the x-vals the
                second contains the y-vals. 
        """
        self.lrt = long_range_trajectory
    
    def set_short_range_trajectory(self, short_range_trajectory=smpl_short_range()):
        """ Set the short range trajectory. Assumes that the trajectory are inches vs yards.
            :param long_range_trajectory: Expects a 2D numpy array. The first row contains the x-vals the
            :param short_range_trajectory: Expects a 2D numpy array. The first row contains the x-vals the
                second contains the y-vals. 
        """
        self.srt = short_range_trajectory 

    def set_integration_params(start_time, max_time, dt):
        self.t_0 = start_time
        self.t_max = max_time
        self.dt = dt

    def __str__(self):
        wg = "Grains: %0.2f\n" % self.mass_grains
        bc = "Balistic Coefficient: %0.2f\n" % self.ballistic_coefficient
        in_cn = "Initial Conditions: " + self.trajectory[-1].__str__()

        return wg + bc + in_cn + "\n"

