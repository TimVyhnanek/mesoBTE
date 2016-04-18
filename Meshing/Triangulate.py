import math
import os

class Triangulate():
	
	def __init__(self, filename):
		# Constants to designate hole type
		self.POLYGON = 0
		self.RECTANGLE = 1
		self.ELLIPSE = 2
		# Will determine how precise we make the ellipse, but this isn't finished yet
		self.ELLIPSE_PRECISION = 15
	
		# Name of input and output files
		self.filename = filename

		self.num_holes = 0
		self.num_vertices = 0
		self.num_edges = 0
		# Array of Triangles
		# Structure [triangle_index][edge_index][x_pos, y_pos, boundary]
		self.triangles = []
		# Contains the x,y positions of the center of each hole
		self.hole_centers = []
		self.edges = []
		self.vertices = []

		#Begins with outer square of side length 1
		self.vertices.append((0,0))
		self.vertices.append((0,1))
		self.vertices.append((1,1))
		self.vertices.append((1,0))
		self.num_vertices += 4

		#Connects edges of square
		self.edges.append((1,2))
		self.edges.append((2,3))
		self.edges.append((3,4))
		self.edges.append((4,1))
		self.num_edges += 4

	def add_hole(self, hole_type, x_pos, y_pos, *args):
		self.hole_centers.append((x_pos, y_pos))
		initial_vertex = self.num_vertices + 1
		self.num_holes += 1
		sides = 0

		# Use this for a regular polygon of n-sides
		# Obviously the more sides the hole has, the more holes we end up with
		if(hole_type == self.POLYGON):
			sides = args[0]
			radius = args[1]
			angle = (math.pi * 2) / sides
			angle_number = 0
			
			for j in range(initial_vertex, initial_vertex + sides):
				self.num_vertices += 1
				self.num_edges += 1
				xn = x_pos + (radius * math.cos(angle * angle_number))
				yn = y_pos + (radius * math.sin(angle * angle_number))		
				self.vertices.append((xn,yn))
				angle_number += 1

		
		elif(hole_type == self.RECTANGLE):
			width = args[0]
			height = args[1]
			sides = 4

			self.vertices.append((x_pos + width/2, x_pos + height/2))
			self.vertices.append((x_pos + width/2, x_pos - height/2))
			self.vertices.append((x_pos - width/2, x_pos - height/2))
			self.vertices.append((x_pos - width/2, x_pos + height/2))
			
			self.num_vertices += 4
			self.num_edges += 4
						
		# Still looking for an algorithm that produces
		# An accurate ellipse with a resonable amount of points
		elif(hole_type == self.ELLIPSE):
			x_radius = args[0]
			y_radius = args[1]
			sides = self.ELLIPSE_PRECISION
			################
			###INCOMPLETE###
			################
		
		# Writes edges
		for j in range(initial_vertex, initial_vertex + sides):
				if j == (initial_vertex + sides - 1):
					self.edges.append((j, initial_vertex))
				else:
					self.edges.append((j, j + 1))
	
			
	#Returns the triangles array
	#Use this method instead of directly accessing the array in order to prevent data corruption
	def get_triangles(self):
		return self.triangles

	#filename must have a .poly extension
	def write_poly_file(self):
		f = open(self.filename + ".poly", "w")

		#Initial line (# of Vertices, Dimensions (Always 2), attributes(0 in our case), boundry (Always 1))
		f.write(str(self.num_vertices) + " 2 0 1 \n")

		#Vertices (Vertex #, x, y)
		for i in range(0, self.num_vertices):
			f.write(str(i + 1) + " " + str(self.vertices[i][0]) + " " + str(self.vertices[i][1]) + "\n")

		#Edge initial line (# of edges, boundry)
		f.write(str(self.num_edges) + " 1 \n")

		#Edges (Edge #, Vertex 1, Vertex 2)
		for i in range(0, self.num_edges):
			f.write(str(i + 1) + " " + str(self.edges[i][0]) + " " + str(self.edges[i][1]) + "\n")

		#Number of holes
		f.write(str(self.num_holes) + "\n")

		#Holes (Hole #, center_x, center_y)
		for i in range(0, self.num_holes):
			f.write(str(i + 1) + " " + str(self.hole_centers[i][0]) + " " + str(self.hole_centers[i][1]) + "\n")

	# Reads the .ele and .node files into the triangles array
	def parse_output_files(self):
		node_indices = []
		node_values = []
		
		# Adds null entries at index=0 so the array indices match with the I/O files
		node_indices.append(0)
		node_values.append(0)

		# Reads .ele file, which determines which vertices form each triangle
		f = open(self.filename + ".1.ele", "r")
		first_line = f.readline().split()
		num_triangles = int(first_line[0])
		for i in range(1, num_triangles + 1):
			line = f.readline().split()
			node_indices.append((line[1], line[2], line[3]))

		# Reads .node file, which contains the absolute position of each vertex
		f2 = open(self.filename + ".1.node", "r")
		first_line = f2.readline().split()
		num_points = int(first_line[0])
		for j in range(1, num_points + 1):
			line = f2.readline().split()
			node_values.append((line[1], line[2], line[3]))
		
		for k in range(1, num_triangles + 1):
			temp_tri = []
			for h in range(0,3):
				temp_tri.append((node_values[int(node_indices[k][h])][0], node_values[int(node_indices[k][h])][1], node_values[int(node_indices[k][h])][2]))
			self.triangles.append(temp_tri)
			
			
		
	# Creates the input .poly file, executes Triangle.c, then parses the output files
	def Delaunay(self, flags):
		self.write_poly_file()
		# You may have to download the Triangle program for this to work on your machine
		# On linux, a simple sudo apt-get Triangle should work
		# I'm not sure on Windows or Mac
		# Here's a link to the documentation: https://www.cs.cmu.edu/~quake/triangle.html
		# Feel free to play with the different flags and see how it affects the triangulation
		os.system("triangle -p " + flags + " " + self.filename + ".poly")
		# This is a tool which displays the triangulation, we don't actually need this
		os.system("showme " + self.filename + ".1.ele")
		self.parse_output_files()

	# This can be used to get the physical boundaries of the mesh
	# Can be used in conjuction with the get_edges method
	# This is an alternative to the boundary point value in the triangles array
	def get_vertices(self):
		return self.vertices

	# Returns the edges of the main square and the holes
	# Each edge is denonted by 2 integers
	# These integers are indices of points in the vertices[] array
	def get_edges(self):
		return self.edges


		

		
		
	
