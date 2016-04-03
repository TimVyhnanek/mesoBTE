from __future__ import division
import random


sum = 0.0
n = 1000000

for i in range(0, n):
	x = random.random()
	y = random.random()
	if (x*x + y*y) < 1.0:
		sum+=1

pi = 4.0 * (sum/n)
print "Pi is about equal to %f" % (pi)
