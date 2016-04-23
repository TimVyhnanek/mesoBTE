import numpy as np
import math
import random

class randomStack():
	def __init__(self,n,filename):
		self.stack = self.randGenerate(n,filename)
		self.currentCard = 0
		self.deckLength = n
	
	def draw(self):
		k = self.stack[self.currentCard]
		self.currentCard = (self.currentCard+1)%self.deckLength
		return k
    
	def findInterval(self,randX,arrayX):
		if len(arrayX) == 2:
			return arrayX
		elif randX > arrayX[len(arrayX)/2]:
			return(self.findInterval(float(randX), arrayX[len(arrayX)/2:]))
		elif randX < arrayX[len(arrayX)/2]:
			return(self.findInterval(float(randX), arrayX[:(len(arrayX)+1)/2]))

	def linApprox(self,randX,intervalX,arrayX,arrayY): #approximates value of function at x = randX linearly
	    yi = arrayY[np.where(arrayX == intervalX[0])]
	    yf = arrayY[np.where(arrayX == intervalX[1])]
	    m = (yf-yi)/(intervalX[1]-intervalX[0])
	    return yi+m*(randX-intervalX[0])

	def trapezoidalRule(self,arrayX,arrayY): #calculates area under pdf function using trapezoidal rule (numerical integration)
	    a = 0
	    deltaX = arrayX[1]-arrayX[0]
	    for i in range(len(arrayY)):
		    if i == 1 or i == len(arrayY-1):
			    a += arrayY[i]
		    else:
			    a += 2*arrayY[i]
	    area = 0.5*a*deltaX
	    return area	

	def normalizePDF(self,arrayX,arrayY):	#normalizes pdf by multiplying it with k such that area under pdf = 1
	    normalizingConstant = 1/trapezoidalRule(arrayX,arrayY)
	    for i in range(len(arrayY)):
	    	arrayY[i] = normalizingConstant*arrayY[i]
	    return arrayX, arrayY

	def randGenerate(self,n,filename): #generates array of n randomized values from arbitrary pdf <--- This is what we need
	    arrayX, arrayY = np.loadtxt(filename,delimiter=',',unpack=True)
	    k=1
	    outarray = []
	    while k<=n:
		    randX = random.uniform(min(arrayX),max(arrayX))
		    randY = random.uniform(0,max(arrayY))
		    if randY <= self.linApprox(randX,self.findInterval(randX,arrayX),arrayX,arrayY):
			    outarray.append(randX)
			    k=k+1
	    return outarray
