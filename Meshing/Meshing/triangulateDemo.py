import Triangulate as tri

## Quick demo of the Triangulate class
## Feel free to ask me any questions you have about how it works
## Here's another link to the Triangle documentation: https://www.cs.cmu.edu/~quake/triangle.html

# Creates instance of Triangulate class
# test2 will be the name of our input and ouput files
# Feel free to change this to anything you wish
test_tri = tri.Triangulate("test2")

# Adds a 10 sides hole centered at x=0.5, y=0.5, with a radius of .1
test_tri.add_hole(test_tri.POLYGON, .5, .5, 10, .1)
# Adds a rectangular hole centered at x=0.2, y=0.2, and width=0.1, height=0.15
test_tri.add_hole(test_tri.RECTANGLE, .2, .2, .1, .15)
# Creates the actual triangulation
# "-q34" restricts the angle size of the triangulation to make it more accurate
# Feel free to play around with the different flags
test_tri.Delaunay("-q34")
# Returns the array of triangles
# Use this getter method instead of accessing the array directly to prevent data corruption
triangles = test_tri.get_triangles()

##Prints of the triangles array 
for i in triangles:
	print i
	print "\n"
