import numpy as np
import random
import matplotlib.pyplot as plt
import time
from scipy.spatial import Delaunay

class particle():
    def __init__(self,xposdist,yposdist,vxdist,vydist):
        self.xpos = xposdist.draw()
        self.ypos = yposdist.draw()
        self.vx = vxdist.draw()
        self.vy = vydist.draw()
    
class mesh():
    def __init__(self,xrange,yrange,initPosDist,initVelDist,initParticles):
        self.fig = plt.figure(1)
        plt.ion()
        self.ax = plt.gca()	
        self.ax.set_autoscale_on(False)
        self.ax.axis([xrange[0],xrange[1],yrange[0],yrange[1]])

        self.tri_xy = np.zeros([5,2])
        self.tri_xy[0,0] = 0.1 #hardcoded the vertices for triangulation for now at least
        self.tri_xy[0,1] = 0.2 
        self.tri_xy[1,0] = 1
        self.tri_xy[1,1] = 0.3
        self.tri_xy[2,0] = 0.4
        self.tri_xy[2,1] = 1
        self.tri_xy[3,0] = 1
        self.tri_xy[3,1] = 1
        self.tri_xy[4,0] = 0.7
        self.tri_xy[4,1] = 0.1

        self.tri = Delaunay(self.tri_xy)
        plt.triplot(self.tri_xy[:,0], self.tri_xy[:,1], self.tri.simplices.copy())
        print self.tri.simplices.copy()
        self.ax.plot(self.tri_xy[:,0], self.tri_xy[:,1], 'o')

        self.fig.show()
        self.e_array = []

        self.xmin = xrange[0]
        self.xmax = xrange[1]
        self.ymin = yrange[0]
        self.ymax = yrange[1]

        for i in range(0, initParticles):
            a = particle(initPosDist[0],initPosDist[1],initVelDist[0],initVelDist[1])
            self.e_array.append([a, self.ax.plot(a.xpos, a.ypos, 'ro')])

    def electron_amount(self, t, decayConst):
        y = int(decayConst*np.exp(-t))
        return y

    def electron_input(self, t, xposdistinput,yposdistinput,vxdistinput,vydistinput,decayConst):
        # self.e_array = []
        for i in range(self.electron_amount(t,decayConst)):
            a = particle(xposdistinput,yposdistinput,vxdistinput,vydistinput)
            self.e_array.append([a, self.ax.plot(a.xpos, a.ypos, 'ro')])
            
    def scatter(self, dt, xreflectdiststack, yreflectdiststack, p_scatter):
        # updating position
        for i in range(len(self.e_array)):
            self.e_array[i][0].xpos = self.e_array[i][0].xpos + self.e_array[i][0].vx * dt
            self.e_array[i][0].ypos = self.e_array[i][0].ypos + self.e_array[i][0].vy * dt
        # bouncing back
            if self.e_array[i][0].ypos >= self.ymax:
                dy = self.e_array[i][0].ypos - self.ymax
                self.e_array[i][0].ypos = self.e_array[i][0].ypos - 2*dy
                self.e_array[i][0].vy = - self.e_array[i][0].vy
            elif self.e_array[i][0].ypos <= self.ymin:
                dy = self.ymin - self.e_array[i][0].ypos
                self.e_array[i][0].ypos = self.e_array[i][0].ypos + 2*dy
                self.e_array[i][0].vy = - self.e_array[i][0].vy
        # update velocity
        for i in range(len(self.e_array)):
            if random.uniform(0,1) < p_scatter:
                self.e_array[i][0].vx = xreflectdiststack.draw()
                self.e_array[i][0].vy = yreflectdiststack.draw()
        # passing through if x<0 or x>1
        self.e_array = filter(lambda x: (x[0].xpos < self.xmax) and (x[0].xpos > self.xmin), self.e_array)
        #print '\r electrons still simulated: ' + str(len(self.e_array)),
        for i in range(len(self.e_array)):
            self.e_array[i][1][0].set_xdata(self.e_array[i][0].xpos)
            self.e_array[i][1][0].set_ydata(self.e_array[i][0].ypos)
        
    
    def refreshMesh(self,t,dt, xposdistinput,yposdistinput,vxdistinput,vydistinput,xreflectdiststack,yreflectdiststack,p_scatter,decayConst):
        self.electron_input(t,xposdistinput,yposdistinput,vxdistinput,vydistinput,decayConst)
        self.scatter(dt,xreflectdiststack,yreflectdiststack,p_scatter)
    
    def rectangleCheck(self,tri_xy,tri_simplices):
        preliminaryfilter = []
        for simplice in tri_simplices:
            particles_in_rectangle = []
            x = np.zeros(3)
            y = np.zeros(3)
            x = [tri_xy[simplice[0]][0],tri_xy[simplice[1]][0],tri_xy[simplice[2]][0]]
            y = [tri_xy[simplice[0]][1],tri_xy[simplice[1]][1],tri_xy[simplice[2]][1]]

            xmin = min(x)
            xmax = max(x)
            ymin = min(y)
            ymax = max(y)

            for particle in self.e_array:
                if particle[0].xpos >= xmin and particle[0].xpos <= xmax and particle[0].ypos >= ymin and particle[0].xpos <= ymax:
                    particles_in_rectangle.append(particle)

            preliminaryfilter.append(particles_in_rectangle)
        return preliminaryfilter

    def triangleCheck(self,tri_xy,tri_simplices,filteredparticles):
        arrayofparticlespersimplice = []
        j = 0
        for simplice in tri_simplices:
            particles_in_simplice = []
            for particle in filteredparticles[j]:
                a = ((tri_xy[simplice[1]][1] - tri_xy[simplice[2]][1])*(particle[0].xpos - tri_xy[simplice[2]][0]) + (tri_xy[simplice[2]][0] - tri_xy[simplice[1]][0])*(particle[0].ypos - tri_xy[simplice[2]][1])) / ((tri_xy[simplice[1]][1] - tri_xy[simplice[2]][1])*(tri_xy[simplice[0]][0] - tri_xy[simplice[2]][0]) + (tri_xy[simplice[2]][0] - tri_xy[simplice[1]][0])*(tri_xy[simplice[0]][1] - tri_xy[simplice[2]][1]))
                b = ((tri_xy[simplice[2]][1] - tri_xy[simplice[0]][1])*(particle[0].xpos - tri_xy[simplice[2]][0]) + (tri_xy[simplice[0]][0] - tri_xy[simplice[2]][0])*(particle[0].ypos - tri_xy[simplice[2]][1])) / ((tri_xy[simplice[1]][1] - tri_xy[simplice[2]][1])*(tri_xy[simplice[0]][0] - tri_xy[simplice[2]][0]) + (tri_xy[simplice[2]][0] - tri_xy[simplice[1]][0])*(tri_xy[simplice[0]][1] - tri_xy[simplice[2]][1]))
                c = 1 - a - b
                if a >= 0 and a <= 1 and b <= 1 and b >= 0 and c >= 0:
                    particles_in_simplice.append(particle)
            arrayofparticlespersimplice.append(particles_in_simplice)
            j = j+1
        return arrayofparticlespersimplice

    def getParticleCount(self,tri_xy,tri_simplices):
        u = input('count electrons in which triangle?')
        print(len(self.triangleCheck(tri_xy,tri_simplices,self.rectangleCheck(tri_xy,tri_simplices))[u]))
        #print '\r electrons in triangle'+str(u)+':' + str(k),

    def runSim(self,simduration,dt,inputPosDist,inputVelDist,reflectDist,p_scatter,decayConst):
        t = 0
        while t <= simduration:
            plt.draw()
            self.getParticleCount(self.tri_xy,self.tri.simplices.copy())
            t = t + dt
            self.refreshMesh(t,dt, inputPosDist[0],inputPosDist[1],inputVelDist[0],inputVelDist[1],reflectDist[0],reflectDist[1],p_scatter,decayConst)
            time.sleep(dt)


