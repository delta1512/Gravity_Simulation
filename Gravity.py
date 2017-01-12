from __future__ import division
from visual import *
import random

global Canvas, MaxMass, MatterTable, MatterCount
Canvas = (500, 500) #Size of the scene (x, y)
MaxMass = 50 #Mass of each blob (how much blobs affect each other)
MatterTable = []
MatterCount = 50 #Amount of blobs

class Matter:
	def __init__(self): #Sets initial variables
		self.mass = 0
		self.velocity = vector(random.uniform(-2, 2), random.uniform(-2, 2), 0)
		self.vectors = []
		self.position = [0, 0, 0]
		self.mass = round(random.uniform(1, MaxMass), 3)
		for i in range(0, len(self.position)):
			if i != 2: #remove for future 3D
				self.position[i] = round(random.uniform(-Canvas[i]/2, Canvas[i]/2), 3)
		self.MatterObj = sphere(pos=tuple(self.position),
								radius=-(1.01**(-self.mass+300))+20,
								color=color.green)

	def Sum_Vectors(self): #Sums every vector in 'self.vectors'
		res = [0, 0, 0]
		if len(self.vectors) > 0:
			for x in self.vectors:
				res = [res[0]+x[0], res[1]+x[1], 0] #res[2]+x[2] (3D)
		self.velocity = vector(res[0], res[1], res[2])
		self.vectors = []

	def Move(self): #Updates the object based on its velocity
		self.Sum_Vectors()
		self.MatterObj.velocity = self.velocity
		self.MatterObj.pos = self.MatterObj.pos + self.MatterObj.velocity

def Distance(a, b): #Finds the distance between 2 vectors
	res = Vect_Diff(a, b)
	res = round(sqrt((res[0]**2) + (res[1]**2) + (res[2]**2)), 3)
	return res

def Vect_Diff(a, b): #Finds the vector from b to a
	res = []
	for x in range(0, 3):
		res.append(a[x] - b[x])
	return res

def Grav_Vect(a, b, Mass): #Calculate the power of the gravity
	Dist = Distance(a, b)
	Vect = Vect_Diff(a, b)
	res = []
	Grav = 1.03**-(Dist+(Mass*3))
	EquationMax = 1.03**-(0+(Mass*3))
	for x in Vect: #Convert it to a vector format and apply a proportion equation
		res.append((Grav / EquationMax) * x)
	return res

for x in range(0, MatterCount): #Spawn all the objects
	MatterTable.append(Matter())

while True: #Mainloop
	rate(60) #Set framerate
	'''
	The nested for loop below does the following:
	For every object, go through every other object other than the initial one
	If the mass of the first one is greater than the one from the second loop:
		Then calculate the gravity vector and put it in the smaller object's
		self.vectors
	'''
	for i, x in enumerate(MatterTable):
		for j, y in enumerate(MatterTable):
				if j != i and x.mass > y.mass:
					y.vectors.append(Grav_Vect(x.MatterObj.pos, y.MatterObj.pos, x.mass))

	for x in MatterTable: #Update all the objects
		x.Move()
