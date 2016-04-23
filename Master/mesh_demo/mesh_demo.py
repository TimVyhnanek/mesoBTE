import randomStack as rng
import mesh as mes
import numpy as np
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt
import Triangulate as tri_tim

posdist = rng.randomStack(1000,'boxdist.txt')
veldist = rng.randomStack(1000,'boxdist2.txt')
refdist = rng.randomStack(1000,'reflectdist.txt')

test_tri = tri_tim.Triangulate("test2")

test_tri.add_hole(test_tri.POLYGON, .5, .5, 10, .1)      # Adds a 10 sides hole centered at x=0.5, y=0.5, with a radius of .1 

test_tri.add_hole(test_tri.RECTANGLE, .2, .2, .1, .15)   # Adds a rectangular hole centered at x=0.2, y=0.2, and width=0.1, height=0.15

test_tri.Delaunay("-q34")

p = test_tri.get_points()
print p
s = test_tri.get_indices()
print len(s)

testmesh = mes.mesh(xrange = [0,1],yrange = [0,1],pointsArray = p,simplices = s,initPosDist = [posdist,posdist],initVelDist = [veldist,veldist],initParticles=3)

testmesh.runSim(simduration = 8, dt = 0.01, inputPosDist= [posdist,posdist],inputVelDist=[veldist,veldist],reflectDist = [refdist,refdist],p_scatter = 0.003,decayConst = 1.8)
