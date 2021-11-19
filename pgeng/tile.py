'A class and variable for Tile objects'
from pygame import Vector2, Rect

tile_size = 0

class Tile:
	'''A tile used by the Entity object to check collision
	size can be a single number and it will be the width and the height, or it can be a tuple/list
	It also supports ramps (45 degrees)
	If the width and height are not the same, ramp will be 0
	ramp 0 = no ramp
	ramp 1 = top left
	ramp 2 = top right
	ramp 3 = bottom right
	ramp 4 = bottom left


	Attributes:

	location

	ramp

	size'''
	def __init__(self, location, size, ramp=0):
		'Initialising a Tile object'
		if not 0 <= ramp <= 4:
			raise ValueError('ramp must be between 0 and 4')
		self.location = Vector2(location)
		self.size = Vector2(size)
		self.ramp = ramp if self.size[0] == self.size[1] else 0

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Tile{tuple(self.location), tuple(self.size), self.ramp}'

	@property
	def rect(self):
		'''Returns a pygame.Rect object of the Tile object

		Returns: pygame.Rect'''
		return Rect(self.location, self.size)