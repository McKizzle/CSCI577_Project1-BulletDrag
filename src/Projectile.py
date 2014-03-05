import numpy as np
import pylab as py
import matplotlib.pyplot as plt
import math as m
import BallisticModel as bm
import scipy.integrate as integrate

class Projectile:

    def __init__(self,xy_init,angle,velocity,bc,gr,sproj):
        self.xy_init=xy_init
        self.theta=((float(angle)/360.0)*(2.0*np.pi)) #degrees
        self.v_init=float(velocity) #fps
        self.vx_init=self.v_init*np.cos(self.theta)
        self.vy_init=self.v_init*np.sin(self.theta)
        self.bc=float(bc)
        if sproj==1:
            self.model=bm.G1()
        elif sproj==2:
            self.model=bm.G2()
        elif sproj==5:
            self.model=bm.G5()
        elif sproj==7:
            self.model=bm.G7()
        elif sproj==8:
            self.model=bm.G8()
        else:
            self.model=bm.G1()
        self.mass=float(gr)
        self.t=np.array([])
        #[x,y,vx,vy]
        self.x=[np.array([self.xy_init[0],self.xy_init[1],self.vx_init,self.vy_init])]
	#print(self.x)

    def move(self,t,x):
        v=np.array([x[2],x[3]])
        vmag=np.linalg.norm(v)
        vu=v/vmag
        am=self.model.get_am(vmag)
        f=((am[0]/self.bc)*(vmag**((am[1])-1.)))
        ax=-f*(vu[0])*(1./self.mass)
        ay=-32.1522-f*(vu[1])*(1./self.mass)
        #temp=np.array([x[0],x[1],x[2],x[3],f])
        out=np.array([v[0],v[1],ax,ay])
        #print(temp)
        #exit()
        return out

    def fire(self,t0,tfin):
        i=integrate.ode(self.move)
        i.set_integrator('dopri5',method='adams')
        i.set_initial_value(self.x[0],t0)
        tf=tfin
        dt=.0001
        times=np.arange(t0,tf,dt)
        for t in times[1:]:
            i.integrate(i.t+dt)
            self.x.append(i.y)
        self.t=times
        
    def plotme(self):
        lr=np.array([[100.,2.0],[150.,1.7],[200.,0.],[250.,-3.4],[300.,-8.8],[400.,-26.2],[500.,-54.8]])
        sr=np.array([[50.,0.0],[100.,0.],[150.,-1.2],[200.,-3.9],[250.,-8.4],[300.,-14.7]])
        self.x=np.array(self.x)
        plt.plot((self.x[:,0]/3.),(self.x[:,1]*12.),'r')
        plt.plot(lr[:,0],(lr[:,1]),'og')
        #plt.plot(1500.,0.,'ok')
        plt.show()

    def get_theta(self):
        return self.theta

    def set_theta(self,angle):
        self.theta=angle

    def get_x(self):
        return self.x

    def find_angle(self,dist):
        final=[]
        true=0
        while true==0:
            x=self.get_x()
            point=[]
            for element in range(0,len(x)-1,1):
                if x[element][0]<=(dist+.1) and x[element][0]>=(dist-.1):
                    point.append(x[element][0])
                    point.append(x[element][1])
                
            if point[1]>(.001):
                cur_angle=self.get_theta()
                new_angle=cur_angle/2.0
                self.set_theta(new_angle)
            elif point[1]<(-0.001):
                cur_angle=self.get_theta()
                new_angle=cur_angle+(cur_angle/2.0)
                self.set_theta(new_angle)
            else:
                final.append(point[0])
                final.append(point[1])
                true=1

            self.vx_init=self.v_init*np.cos(self.theta)
            self.vy_init=self.v_init*np.sin(self.theta)
            self.x=[np.array([self.xy_init[0],self.xy_init[1],self.vx_init,self.vy_init])]
            self.fire(0,0.5)
        print(final[1])
        print(self.get_theta())
