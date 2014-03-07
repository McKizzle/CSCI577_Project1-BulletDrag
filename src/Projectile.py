import numpy as np
import pylab as py
import matplotlib.pyplot as plt
import math as m
import BallisticModel as bm
import scipy.integrate as integrate
import yaml as yaml

LB_GRAIN = 1.0/7000.0

GRS = "grains"
BCF = "ballistic coefficient"
MVL = "muzzle velocity"
VTR = "velocity trajectory"
SRT = "short range trajectory"
LRT = "long range trajectory"

def dictionary_for_bullet(dictionary):
    """ Converts a dictionary into a bullet
        Defaults to G1 for all bullets. 
    """
    xy_init  = [0.0, 0.0]
    angle    = 0.065 # zero degrees
    velocity = dictionary[MVL]
    bc = dictionary[BCF]
    gr = dictionary[GRS]
    projectile     = Projectile(xy_init, angle, velocity, bc, gr)
    projectile.vtr = np.array(dictionary[VTR])
    projectile.lrt = np.array(dictionary[LRT])
    projectile.srt = np.array(dictionary[SRT])
    return projectile

def load_yamlfile(file_name):
    """ Loads a YAML file as a dictionary """
    stream = open(file_name, "r")
    bullets = yaml.load(stream)
    return bullets

def plot_trajectories(bullet, bullet_golden):
    """ Plot and compare the bullet trajectory and velocity to the 
        long range trajectory and velocity golden data.
        :param bullet: A bullet to plot.
    """

    plt.subplots(nrows=2, ncols=1)
    plt.tight_layout()
    plt.subplot(211)
    bullet.plotme()
    bullet.plot_lrt()
    plt.title("Height vs Position")
    plt.subplot(212)
    bullet.plot_vel()
    bullet.plot_vrt()
    plt.title("Velocity vs Position")
    plt.show()
    

def zero_in(cartridge, starting_theta, dist, tol, r):
    """ Takes a Projectile and zeros it in the specified distance within 
        a tolerance using a 'geometric' search algorithm. 

        :param cartridge: the cartridge to zero in
        :param starting_theta: the starting angle in degrees. 
        :param dist: the distance to zero in on. Expects the distance to be yards.
        :param tol: the tolorance 
        :param r: the ratio (affects the speed at which the search algorithm converges)
    """
 
    zeroed_in = False
    k = 1.0
    theta = starting_theta
    while not zeroed_in:
        print "Iteration %d" % k

        cartridge.reset_trajectory()
        cartridge.set_fireing_angle(theta)
        cartridge.fire()
        y = cartridge.elevation_at(dist)
 
        if np.abs(y) < tol:
            zeroed_in = True

        if y >=  0:
            theta = theta - r**k * theta
        elif y < 0:
            theta = theta + r**k * theta

        k = k + 1

    cartridge.reset_trajectory()
    cartridge.set_fireing_angle(theta)
    cartridge.fire() # fire the trajectory so the user can plot right away. 

    return theta

class Projectile:
    def __init__(self, xy_init, angle, velocity, bc, gr, sproj = bm.G1()):
        self.xy_init  =  np.array(xy_init).astype(float) # Convert array into floats.
        
        # Set initial directional velocity.
        self.theta = ((float(angle)/360.0)*(2.0*np.pi))  # Convert to radians
        self.v_init = float(velocity) #fps
        self.vx_init = self.v_init*np.cos(self.theta)
        self.vy_init = self.v_init*np.sin(self.theta)
        
        self.bc = float(bc) # Ballistic coefficient.
        
        # Simplified the balistic model setting process makes it easier to read. 
        self.model = sproj 
    
        self.mass = float(gr) #* LB_GRAIN  
        self.t = np.array([])

        #[x, y, vx, vy]
        # Initial Trajectory
        self.x = [np.array([self.xy_init[0], self.xy_init[1], self.vx_init, self.vy_init])] 

        # Default integration rules (seconds)
        self.t_0 = 0.0
        self.t_max = 0.5
        self.dt = 0.001
        
        # Velocity Trajectory
        self.vrt = np.array([[100, 2889], [200, 2514], [300, 2168], [400, 1851], [500, 1568]])
        # Long Range Trajectory
        self.lrt = np.array([[100., 2.0], [150., 1.7], [200., 0.], [250., -3.4], [300., -8.8], [400., -26.2], [500., -54.8]])
        # Short Range Trajectory
        self.srt = np.array([[50., 0.0], [100., 0.], [150., -1.2], [200., -3.9], [250., -8.4], [300., -14.7]])

    def move(self, t, x, g=32.1522):
        """ ODE System that models bullet movement. Send to ODE solver. """
        v = np.array([x[2], x[3]])
        vmag = np.linalg.norm(v)
        vu = v/vmag
        
        f = self.f(vmag) 
        ax = -f*(v[0])*vu[0]
        ay = -g-f*(v[1])*vu[1]
        
        out = np.array([v[0], v[1], ax, ay])
        
        return out

    def f(self, vel):
        """ Drag function """
        Av, Mv = self.model.get_am(vel)
        force = Av / self.bc * vel**(Mv - 1) ## * 100000
         
        return force

    def set_integration_params(self, start_time, max_time, dt):
        """ Set the start time, stop time, and dt values that
            the fire method will use.
        """
        self.t_0 = start_time
        self.t_max = max_time
        self.dt = dt

    def fire(self):
        """ Start the simulation """
        t0 = self.t_0
        tf = self.t_max
        dt = self.dt

        i = integrate.ode(self.move)
        i.set_integrator('dopri5', method = 'adams')
        i.set_initial_value(self.x[0], self.t_0)
        times = np.arange(self.t_0, self.t_max, self.dt)
        for t in times[1:]:
            i.integrate(i.t+self.dt)
            self.x.append(i.y)
        self.t = times
        
    def plotme(self):
        x = np.array(self.x)
        plt.plot(x[:, 0]/3., x[:, 1]*12., 'k')
        plt.xlabel("x-position (yards)")
        plt.ylabel("y-position (inches)")

    def plot_vel(self): 
        x = np.array(self.x)
        vels = [np.linalg.norm(x[i,2:4]) for i in range(0, x.shape[0])]
        vels = np.array(vels)

        plt.plot(x[:, 0]/3., vels, 'k')
        plt.ylabel(r"velocity $\frac{ft}{s}$")
        plt.xlabel("x-position (yards)")

    def plot_vrt(self):
        plt.plot(self.vrt[:, 0], self.vrt[:, 1], '-rs')

    def plot_lrt(self):
        plt.plot(self.lrt[:, 0], self.lrt[:, 1], '-rs')

    def plot_srt(self):
        plt.plot(self.srt[:, 0], self.srt[:, 1], '-rs')

    def reset_trajectory(self):
        """ Reset the trajectory to its initial values. 
            Make sure to set the fireing angle afterwards
        """
        self.x = [np.array([self.xy_init[0], self.xy_init[1], 0.0 , 0.0])] # Initial Trajectory

    def get_theta(self):
        """ Returns the fireing angle in radians """
        return self.theta

    def set_theta(self, angle):
        """ Set the fireing angle. Expects the angle to be in radians """
        self.theta = angle

    def set_fireing_angle(self, theta=0.06):
        """ Sets the initial x y velocitites based on the fireing angle.  
            :param theta: Firing angle in degrees (def: 0.0 deg)
        """
        theta  =  np.pi / 180.0 * float(theta)  #convert to radians.
        self.x[-1][2]  =  float(self.v_init) * np.cos(float(theta)) # Set the X velocity.
        self.x[-1][3]  =  float(self.v_init) * np.sin(float(theta)) # Set the Y velocity.
                                                                                
    def get_x(self):
        """ Return the trajectory """
        return self.x

    def elevation_at(self,  dist):
        """ Finds the elevation at a specified distance. 
            Don't forget to pass in the distance as feet
        """
        dist  =  float(dist)
        traj  =  np.array(self.x)
        y  =  None
        for i in range(0,  traj.shape[0] - 1):
            x  =  traj[i:(i + 2),  0]
            if (traj[i,  0] >=  dist):
                bounds  =  np.array([traj[i],  traj[i + 1]])
                y  =  np.interp(dist,  bounds[:,  0],  bounds[:,  1])
                break

        return y

