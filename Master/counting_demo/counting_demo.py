import randomStack as rng
import mesh as mes


posdist = rng.randomStack(1000,'boxdist.txt')
veldist = rng.randomStack(1000,'boxdist2.txt')
refdist = rng.randomStack(1000,'reflectdist.txt')

testmesh = mes.mesh(xrange = [0,1.1],yrange = [0,1.1],initPosDist = [posdist,posdist],initVelDist = [veldist,veldist], initParticles=3)

testmesh.runSim(simduration = 8, dt = 0.01, inputPosDist= [posdist,posdist],inputVelDist=[veldist,veldist],reflectDist = [refdist,refdist],p_scatter = 0.003,decayConst = 1.8)


