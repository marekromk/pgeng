'''Functions and classes for tiles and physics objects'''
#IMPORTS
import pygame
#IMPORTS

#VARIABLES
__all__ = ['tile_size', 'Tile']
tile_size = 0
#VARIABLES

#TILE
class Tile:
	'''A tile used by the Entity object to check collision
	It also supports ramps (45 degrees)
	Ramp 0 = No ramp
	Ramp 1 = top left
	Ramp 2 = top right
	Ramp 3 = bottom right
	Ramp 4 = bottom left

	Attributes:

	location

	size

	ramp'''
	#__INIT__
	def __init__(self, location, size, ramp=0):
		'''Initialising a tile'''
		self.location = list(location)
		self.size = size
		self.ramp = ramp
	#__INIT__

	#RECT
	@property
	def rect(self):
		'''Returns a pygame.Rect object of the tile'''
		return pygame.Rect(self.location[0], self.location[1], self.size, self.size)
	#RECT
#TILE