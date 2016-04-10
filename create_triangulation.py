import math

## This script prompts the user for the size, shape, and location of holes in a material
## As of right now, these holes must be regular polygons (circles approximated as n-gons)
## This outputs a .poly file which acts as an input to the Triangle.c program
## The output triangulation is written to a .ele file, which we will read back into Python
## And integrate the triangulation into the physics engine of our code
##
## Link to Triangle.c Documentation: https://www.cs.cmu.edu/~quake/triangle.html

#initialize variables
num_holes = 0
num_vertices = 0
num_edges = 0
vertices = []
hole_centers = []
hole_radii = []
hole_points = []
edges = []

#File that will become the input of the Triangle program
f = open ("test_input.poly", "w")

#Begins with outer square of side length 1
vertices.append((0,0))
vertices.append((0,1))
vertices.append((1,1))
vertices.append((1,0))
num_vertices += 4

#Connects edges of square
edges.append((1,2))
edges.append((2,3))
edges.append((3,4))
edges.append((4,1))
num_edges += 4

#returns the measure of one interior angle of the hole (in radians)
def interior_angle(s):
	return ((s - 2)*math.pi)/s

num_holes = input("Please input the number of holes: ")

#Iterates for each hole in the material
for i in range(0, num_holes):
	print "\nHole #%d" %(i+1)
	sides = input("Enter the number of sides the hole has: ")
	x = input("Enter the x-coordinate of the center of the hole: ")
	y = input("Enter the y-coordinate of the center of the hole: ")
	r = input("Input the radius of the hole (Distance from center to vertex): ")

	hole_centers.append((x,y))
	hole_radii.append(r)
	angle = interior_angle(sides)

	angle_number = 0
	initial_vertex = num_vertices + 1
	for j in range(initial_vertex, initial_vertex + sides):
		num_vertices += 1
		num_edges += 1
		xn = x + (r * math.cos(angle * angle_number))
		yn = y + (r * math.sin(angle * angle_number))
		
		vertices.append((xn,yn))
		if j == (initial_vertex + sides - 1):
			edges.append((j, initial_vertex))
		else:
			edges.append((j, j + 1))
		angle_number += 1


#Initial line (# of Vertices, Dimensions (Always 2), attributes(0 in our case), boundry (Always 1))
f.write(str(num_vertices) + " 2 0 1 \n")

#Vertices (Vertex #, x, y)
for i in range(0, num_vertices):
	f.write(str(i + 1) + " " + str(vertices[i][0]) + " " + str(vertices[i][1]) + "\n")

#Edge initial line (# of edges, boundry)
f.write(str(num_edges) + " 1 \n")

#Edges (Edge #, Vertex 1, Vertex 2)
for i in range(0, num_edges):
	f.write(str(i + 1) + " " + str(edges[i][0]) + " " + str(edges[i][1]) + "\n")

#Number of holes
f.write(str(num_holes) + "\n")

#Holes (Hole #, center_x, center_y)
for i in range(0, num_holes):
	f.write(str(i + 1) + " " + str(hole_centers[i][0]) + " " + str(hole_centers[i][1]) + "\n")




		

