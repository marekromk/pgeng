'''Functions and classes for tiles and physics objects'''
#IMPORTS
import pygame
#IMPORTS

#VARIABLES
__all__ = ['TileSize', 'Tile']
TileSize = 0
#VARIABLES

#TILE
class Tile:
	'''A tile used by the Entity object to check collision
	It also supports ramps (45 degrees)
	Ramp 0 = No ramp
	Ramp 1 = top left
	Ramp 2 = top right
	Ramp 3 = bottom right
	Ramp 4 = bottom left'''
	#__INIT__
	def __init__(self, Location, Size, Ramp=0):
		'''Initialising a tile'''
		self.Location = Location
		self.Size = Size
		self.Ramp = Ramp
	#__INIT__

	#RECT
	@property
	def rect(self):
		'''Return a pygame.Rect object of the tile
		Used by the PhysicsObject class

		Returns: pygame.Rect'''
		return pygame.Rect(self.Location[0], self.Location[1], self.Size, self.Size)
	#RECT
#TILE