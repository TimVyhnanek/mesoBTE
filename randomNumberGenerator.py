from __future__ import division
import random
import math

# Distribution determined by x^n
def xN(x, n):
	return x ** n

#Uniform distribution 0.0 <= x <= 1.0
def uniform(x):
	return x

# Unit Trangle function with height of 1 at x=0.5
# And a width of 1
def unitTriangle(x):
	if(x < 0.5):
		return 2 * x
	else:
		return 1 - (2 * (x - 0.5))

# Gaussian distrobution with a height of peak_height,
# The x-coordinate of the peak at peak-pos,
# And a standard deviation of std_dev
def gaussian(x, peak_height, peak_pos, std_dev):
	exponent = -((x-peak_pos)**2)/(2*(std_dev)**2)
	return peak_height * math.exp(exponent)

#Finds the arithmetic mean of a list of numbers
def findMean(numbers):
	total = 0.0
	n = len(numbers)
	for x in numbers:
		total += x
	return total / n

#Finds the variance in a list of numbers
def findVariance(numbers):
	mean = findMean(numbers)
	n = len(numbers)
	total_variance = 0
	for x in numbers:
		total_variance += (mean - x)**2
	return total_variance/n

#Finds Standard Deviation in a set of numbers
def findStdDev(numbers):
	return math.sqrt(findVariance(numbers))

#Uses Accept/Reject method to find a number that fits into
#any given probability distrobution
#
#*This will benefit greatly from GPU acceleration
def genNum(prob_distro, *args):
	in_distro = False
	random_number = 0
	while(in_distro == False):
		#Returns uniform distrobution
		x_val = random.random()
		if(len(args) > 0):
			distro_max = prob_distro(x_val, *args)
		else:
			distro_max = prob_distro(x_val)
		y_val = random.random()
		in_distro = y_val <= distro_max
		random_number = x_val
	return random_number


numbers = list()
#Number of iterations
n = 100
for i in range(0,n):
	#num = genNum(gaussian, 1, 0.5, 0.02)
	#num = genNum(unitTriangle)
	#num = genNum(uniform)
	num = genNum(xN, 7)
	numbers.append(num)
	print "%f\n" % (num)

#Prints Stats about the distrobution
print "\nMean is: %f" %(findMean(numbers))
print "Variance is: %f" %(findVariance(numbers))
print "Standard Deviation is: %f" %(findStdDev(numbers))


	

	
		
