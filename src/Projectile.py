import numpy as np
import pylab as py
import matplotlib.pyplot as plt
import math as m
import BallisticModel as bm
import scipy.integrate as integrate

class Projectile:

    def __init__(self, xy_init, angle, velocity, bc, gr, sproj = bm.G1):
        self.xy_init  =  np.array(xy_init).astype(float) # Convert array into floats.
        self.theta = ((float(angle)/360.0)*(2.0*np.pi))  # Convert to radians
        self.v_init = float(velocity) #fps
        self.vx_init = self.v_init*np.cos(self.theta)
        self.vy_init = self.v_init*np.sin(self.theta)
        self.bc = float(bc)

        self.model = sproj # Simplified the balistic model setting process makes it easier to read. 
    
        self.mass = float(gr)
        self.t = np.array([])

        #[x, y, vx, vy]
        self.x = [np.array([self.xy_init[0], self.xy_init[1], self.vx_init, self.vy_init])] # Initial Trajectory

    def move(self, t, x):
        v = np.array([x[2], x[3]])
        vmag = np.linalg.norm(v)
        vu = v/vmag
        am = self.model.get_am(vmag)
        f = ((am[0]/self.bc)*(vmag**((am[1])-1.)))
        ax = -f*(vu[0])*(1./self.mass)
        ay = -32.1522-f*(vu[1])*(1./self.mass)
        out = np.array([v[0], v[1], ax, ay])
        return out

    def fire(self, t0, tfin):
        i = integrate.ode(self.move)
        i.set_integrator('dopri5', method = 'adams')
        i.set_initial_value(self.x[0], t0)
        tf = tfin
        dt = .0001
        times = np.arange(t0, tf, dt)
        for t in times[1:]:
            i.integrate(i.t+dt)
            self.x.append(i.y)
        self.t = times
        
    def plotme(self):
        lr = np.array([[100., 2.0], [150., 1.7], [200., 0.], [250., -3.4], [300., -8.8], [400., -26.2], [500., -54.8]])
        sr = np.array([[50., 0.0], [100., 0.], [150., -1.2], [200., -3.9], [250., -8.4], [300., -14.7]])
        self.x = np.array(self.x)
        plt.plot((self.x[:, 0]/3.), (self.x[:, 1]*12.), 'r')
        plt.plot(lr[:, 0], (lr[:, 1]), 'og')
        #plt.plot(1500., 0., 'ok')
        plt.show()

    def reset_trajectory(self):
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
        theta  =  np.pi / 180.0 * float(theta) #convert to radians.
        self.trajectory[-1][VX]  =  float(self.v_init) * np.cos(float(theta))
        self.trajectory[-1][VY]  =  float(self.v_init) * np.sin(float(theta))
                                                                                
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
            #print "---------------------------------------"
            #print "dist: %0.3f" % dist
            #print "x_%i: %0.3f" % (i,  x[0])
            #print "x_%i: %0.3f" % (i + 1,  x[1])
            if (traj[i,  0] > =  dist):
                bounds  =  np.array([traj[i],  traj[i + 1]])
                #print bounds
                #print bounds[:,  0]
                #print bounds[:,  1]
                y  =  np.interp(dist,  bounds[:,  0],  bounds[:,  1])
                break
        
        return y

    def find_angle(self, dist):
        final = []
        true = 0
        while true =  = 0:
            x = self.get_x()
            point = []
            for element in range(0, len(x)-1, 1):
                if x[element][0]< = (dist+.1) and x[element][0]> = (dist-.1):
                    point.append(x[element][0])
                    point.append(x[element][1])
                
            if point[1]> (.001):
                cur_angle = self.get_theta()
                new_angle = cur_angle/2.0
                self.set_theta(new_angle)
            elif point[1]< (-0.001):
                cur_angle = self.get_theta()
                new_angle = cur_angle+(cur_angle/2.0)
                self.set_theta(new_angle)
            else:
                final.append(point[0])
                final.append(point[1])
                true = 1

            self.vx_init = self.v_init*np.cos(self.theta)
            self.vy_init = self.v_init*np.sin(self.theta)
            self.x = [np.array([self.xy_init[0], self.xy_init[1], self.vx_init, self.vy_init])]
            self.fire(0, 0.5)
        print(final[1])
        print(self.get_theta())



def zero_in(cartridge, starting_theta, dist, tol, r):
    """ Takes a Projectile and zeros it in the specified distance within 
        a tolerance using a binary search algorithm. 

        :param cartridge: the cartridge to zero in
        :param starting_theta: the starting angle in degrees. 
        :param dist: the distance to zero in on.
        :param tol: the tolorance 
        :param r: the ratio (affects the speed at which the search algorithm converges
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

        if y > =  0:
            theta = theta - r**k * theta
        elif y < 0:
            theta = theta + r**k * theta

        k = k + 1

    cartridge.reset_trajectory()

    return theta

