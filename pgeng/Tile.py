'''Functions and classes for tiles and physics objects'''
#IMPORTS
import pygame
#IMPORTS

#VARIABLES
tile_size = 0
#VARIABLES

#TILE
class Tile:
	'''A tile used by the Entity object to check collision
	size can be a single number and it will be the width and the height, or it can be a tuple or list
	It also supports ramps (45 degrees)
	If the width and height are not the same, ramp will be 0
	ramp 0 = no ramp
	ramp 1 = top left
	ramp 2 = top right
	ramp 3 = bottom right
	ramp 4 = bottom left


	Attributes:

	location

	size

	ramp'''
	#__INIT__
	def __init__(self, location, size, ramp=0):
		'''Initialising a Tile object'''
		self.location = list(location)
		self.size = list(size) if type(size) is list or type(size) is tuple else [size, size]
		self.ramp = ramp if self.size[0] == self.size[1] else 0
	#__INIT__

	#RECT
	@property
	def rect(self):
		'''Returns a pygame.Rect object of the Tile object'''
		return pygame.Rect(self.location[0], self.location[1], self.size[0], self.size[1])
	#RECT
#TILE