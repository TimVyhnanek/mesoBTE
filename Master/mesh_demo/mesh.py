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
    def __init__(self,xrange,yrange,pointsArray,simplices,initPosDist,initVelDist,initParticles):
        self.fig = plt.figure(1)				#create plot window
        plt.ion()
        self.ax = plt.gca()	
        self.ax.set_autoscale_on(False)
        self.ax.axis([xrange[0],xrange[1],yrange[0],yrange[1]])	#set boundaries

        self.tri_xy = pointsArray		#includes [[x0 x1 x2 ...		points to triangulate
						#           y0 y1 y2 ...  ]]
	self.tri_simplices = simplices		#includes [[p1,p4,p2],[p8,p4,p6]...]	triangulation of said points
	print self.tri_simplices
        plt.triplot(self.tri_xy[:,0],self.tri_xy[:,1],self.tri_simplices)
        
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

    def __electron_amount(self, t, decayConst):
        y = int(decayConst*np.exp(-t))
        return y

    def __electron_input(self, t, xposdistinput,yposdistinput,vxdistinput,vydistinput,decayConst):
        # self.e_array = []
        for i in range(self.__electron_amount(t,decayConst)):
            a = particle(xposdistinput,yposdistinput,vxdistinput,vydistinput)
            self.e_array.append([a, self.ax.plot(a.xpos, a.ypos, 'ro')])
            
    def __scatter(self, dt, xreflectdiststack, yreflectdiststack, p_scatter):
	#scatter electrons
        for i in range(len(self.e_array)):
            if random.uniform(0,1) < p_scatter:
                self.e_array[i][0].vx = xreflectdiststack.draw()
                self.e_array[i][0].vy = yreflectdiststack.draw()
        #update position
        for i in range(len(self.e_array)):
            self.e_array[i][0].xpos = self.e_array[i][0].xpos + self.e_array[i][0].vx * dt
            self.e_array[i][0].ypos = self.e_array[i][0].ypos + self.e_array[i][0].vy * dt
        #collision
            if self.e_array[i][0].ypos >= self.ymax:
                dy = self.e_array[i][0].ypos - self.ymax
                self.e_array[i][0].ypos = self.e_array[i][0].ypos - 2*dy
                self.e_array[i][0].vy = - self.e_array[i][0].vy
            elif self.e_array[i][0].ypos <= self.ymin:
                dy = self.ymin - self.e_array[i][0].ypos
                self.e_array[i][0].ypos = self.e_array[i][0].ypos + 2*dy
                self.e_array[i][0].vy = - self.e_array[i][0].vy
        #remove electrons leaving scope of plot window
        self.e_array = filter(lambda x: (x[0].xpos < self.xmax) and (x[0].xpos > self.xmin), self.e_array)
	self.e_array = filter(lambda x: (x[0].ypos < self.ymax) and (x[0].ypos > self.ymin), self.e_array)
        #update plot
        for i in range(len(self.e_array)):
            self.e_array[i][1][0].set_xdata(self.e_array[i][0].xpos)
            self.e_array[i][1][0].set_ydata(self.e_array[i][0].ypos)
        
    
    def __refreshMesh(self,t,dt, xposdistinput,yposdistinput,vxdistinput,vydistinput,xreflectdiststack,yreflectdiststack,p_scatter,decayConst):
        self.__electron_input(t,xposdistinput,yposdistinput,vxdistinput,vydistinput,decayConst)
        self.__scatter(dt,xreflectdiststack,yreflectdiststack,p_scatter)
    
    def __rectangleCheck(self,tri_xy,tri_simplices):
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

    def __triangleCheck(self,tri_xy,tri_simplices,filteredparticles):
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

    def __getParticlesPerTriangleArray(self,tri_xy,tri_simplices,u):
        return self.__triangleCheck(tri_xy,tri_simplices,self.__rectangleCheck(tri_xy,tri_simplices))[u]

    def runSim(self,simduration,dt,inputPosDist,inputVelDist,reflectDist,p_scatter,decayConst):
        t = 0
	u = input('triangle?')
        while t <= simduration:
            k = len(self.__getParticlesPerTriangleArray(self.tri_xy,self.tri_simplices,u))
            print 'electrons in triangle'+str(u)+':' + str(k)
            plt.draw()
            t = t + dt
            self.__refreshMesh(t,dt, inputPosDist[0],inputPosDist[1],inputVelDist[0],inputVelDist[1],reflectDist[0],reflectDist[1],p_scatter,decayConst)
            time.sleep(dt)


