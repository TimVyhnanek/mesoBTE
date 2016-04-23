import numpy as np
import math
import random
import matplotlib.pyplot as plt

def findInterval(randX,arrayX): #recursive binary search to find the interval in arrayX that randX lies
    if len(arrayX) == 2:
        return arrayX
    elif randX > arrayX[len(arrayX)/2]:
        return(findInterval(float(randX), arrayX[len(arrayX)/2:]))
    elif randX < arrayX[len(arrayX)/2]:
        return(findInterval(float(randX), arrayX[:(len(arrayX)+1)/2]))

def linApprox(randX,intervalX,arrayX,arrayY): #approximates value of function at x = randX linearly
	yi = arrayY[np.where(arrayX == intervalX[0])]
	yf = arrayY[np.where(arrayX == intervalX[1])]
	m = (yf-yi)/(intervalX[1]-intervalX[0])
	return yi+m*(randX-intervalX[0])

def randGenerate(n,arrayX,arrayY): #generates array of n randomized values from arbitrary pdf <--- This is what we need
	k=1
	outarray = []
	while k<=n:
		randX = random.uniform(min(arrayX),max(arrayX))
		randY = random.uniform(0,max(arrayY))
		if randY <= linApprox(randX,findInterval(randX,arrayX),arrayX,arrayY):
			outarray.append(randX)
			k=k+1
	return outarray

def trapezoidalRule(arrayX,arrayY): #calculates area under pdf function using trapezoidal rule (numerical integration)
	a = 0
	deltaX = arrayX[1]-arrayX[0]
	for i in range(len(arrayY)):
		if i == 1 or i == len(arrayY-1):
			a += arrayY[i]
		else:
			a += 2*arrayY[i]
	area = 0.5*a*deltaX
	return area	

def normalizePDF(arrayX,arrayY):	#normalizes pdf by multiplying it with k such that area under pdf = 1
	normalizingConstant = 1/trapezoidalRule(arrayX,arrayY)
	for i in range(len(arrayY)):
		arrayY[i] = normalizingConstant*arrayY[i]
	return arrayX, arrayY

#example pdf for demonstration purposes
print ("Welcome to the randGenerate demo.\n")
u = input("enter 1 for negative exp dist, 2 for positive exp dist,3 for norm dist")
x = np.linspace(0,10,100)
y = np.zeros(len(x))
if u == 1:
	for i in range(len(x)):
		y[i] = math.exp(-x[i])
elif u == 2:
	for i in range(len(x)):
		y[i] = math.exp(x[i])
elif u == 3:
	x, y = np.loadtxt('normdist.txt',delimiter=',',unpack = True)

#normalizing the pdf
z, ynorm = normalizePDF(x,y)

h1 = plt.hist(randGenerate(10000,x,y),np.linspace(0,10,100),normed=1) #histogram of results form randGenerate
h2 = plt.plot(z,ynorm,'r')						#plotting normalized pdf over it

fig = plt.gcf()
plt.autoscale(tight=True)
fig.show()																#let there be light
u = input("press anything to exit")

