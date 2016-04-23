This folder contains the classes for the random number generator class and the mesh class.



randomStack(n,'pdf.txt'): Create a stack of n cards, with each card labelled with a random number drawn from a custom PDF from a txt.file

example: normdist = randomStack(1000,'normdist.txt')
creates a deck of 1000 cards, labelled with values drawn from normal distribution specified in normdist.txt.

to return number from the deck, call normdist.draw().



mesh(xrange,yrange,points,simplices,initPosDist,initVelDist,initParticles): Create a material object that spans [xrange[0], xrange[1]], [yrange[0],yrange[1]]. Seeds with initParticles number of electrons, whose position and velocity depends on initPosDist and initVelDist respectively, which each have seperate x and y components.

example: mat = mesh([0,1],[0,1],poimts,simplices,[normdist, normdist],[normdist, normdist],8): creates [0,1]x[0,1] material, with 8 initial electrons with [xpos,ypos],[xvel,yvel] drawn from [normdist, normdist]. triangulation is defined according to points and simplices.

to run simulation, call mat.runsim(simduration,dt,inputPosDist,inputVelDist,scatterDist,scatterprobability,decayConstant). Runs for simduration time, with time step dt.Any new electrons input into the material will have position and velocity from inputVelDist and inputPosDist, and scatter according to scatterDist.

scatterprobability is the probability that the electron will scatter during dt (lambda*dt)/(no. of electrons)

decayConstant refers to the rate at which electrons are added to the material, which exponentially decays with time. not accurate at the moment since input = decayConstant*exp(-t) but easy to fix
