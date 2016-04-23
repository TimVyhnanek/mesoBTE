import math
import random
import numpy as np
import matplotlib.pyplot as plt

def calcPi():

	z = input('Number of Data Points(0 exits):')
	if z:
		plt.clf()
		plt.cla()
		plt.close()
		fig=plt.figure(1)
		plt.axis([0,1,0,1])
		plt.gca().set_aspect('equal',adjustable='box')
		circle1=plt.Circle((0,0),1,color='r',fill=False)
		fig.gca().add_artist(circle1)
		titlestring = "N = %d" % z
		fig.suptitle(titlestring)

		incount = 0

		for i in range(z):
			x = random.random()
			y = random.random()
			if x**2+y**2<1:
				incount+=1
				plt.plot(x,y,marker='o',color='r')
			else:
				plt.plot(x,y,marker='o',color='b')

		q = 4*float(incount)/z
		fig.show()
		print q
		calcPi()

calcPi()
	

	
