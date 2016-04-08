import numpy as np
import pylab
import math
import matplotlib.tri as tri
import matplotlib.pyplot as plt

TAU = (math.pi) * 2

num_holes = 0
num_vertices = 0
num_edges = 0
vertices = []
x_coords = []
y_coords = []
hole_centers = []
hole_radii = []
hole_points = []
edges = []


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
edges.append((4,0))
num_edges += 4

#returns the measure of one interior angle of the hole (in radians)
def interior_angle(s):
	return ((s - 2)*math.pi)/s

print "%f" %(interior_angle(4))

num_holes = input("Please input the number of holes: ")

for i in range(0, num_holes):
	print "\nHole #%d" %(i+1)
	sides = input("Enter the number of sides the hole has: ")
	x = input("Enter the x-coordinate of the center of the hole: ")
	y = input("Enter the y-coordinate of the center of the hole: ")
	r = input("Input the radius of the hole (Distance from center to vertex): ")

	hole_centers.append((x,y))
	hole_radii.append(r)
	angle = interior_angle(sides)

	angle_number = 1
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

for a in vertices:
	x_coords.append(a[0])
	y_coords.append(a[1])

triang = tri.Triangulation(x_coords, y_coords)

mask = []

for i in triang.triangles:
	mask.append(False)

for i in range(0, len(triang.triangles)):
	for j in range(0, num_holes):
		if((triang.triangles[i][0].mean() - hole_centers[j][0])**2 + (triang.triangles[i][1].mean() - hole_centers[j][1])**2 < hole_radii[j]):
			mask[i] = True


triang.set_mask(mask)

plt.figure()
plt.gca().set_aspect('equal')
plt.triplot(triang, 'bo-')
plt.title('triplot of Delaunay triangulation')
plt.show()

"""#Initial line (# of Vertices, Dimensions (Always 2), attributes(0 in our case), boundry (Always 1))
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
"""



		














	
