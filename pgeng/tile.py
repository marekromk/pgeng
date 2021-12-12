'A class and variable for Tile objects'
from pygame import Vector2, Rect
from json import loads, dumps

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

	def __eq__(self, other):
		'''Returns if it is the same as another Tile object
		If other is not a Tile object, it will return False

		Returns: bool'''
		return (tuple(self.location), tuple(self.size), self.ramp) == (tuple(other.location), tuple(other.size), other.ramp) if isinstance(other, Tile) else False

	@property
	def rect(self):
		'''Returns a pygame.Rect object of the Tile object

		Returns: pygame.Rect'''
		return Rect(self.location, self.size)

	@property
	def left(self):
		'''Returns the x position of the left side of the Tile object

		Returns: float'''
		return float(self.location[0])

	@property
	def right(self):
		'''Returns the x position of the right side of the Tile object

		Returns: float'''
		return float(self.location[0] + self.size[0])

	@property
	def top(self):
		'''Returns the y position of the top side of the Tile object

		Returns: float'''
		return float(self.location[1])

	@property
	def bottom(self):
		'''Returns the y position of the bottom side of the Tile object

		Returns: float'''
		return float(self.location[1] + self.size[1])

	@classmethod
	def from_json(cls, json_string):
		'''Returns a Tile object from a json string
		The string should be from the to_json() function

		Returns: Tile'''
		json_string = loads(json_string)
		return Tile(json_string['location'], json_string['size'], json_string['ramp'])

	def to_json(self):
		'''Returns the object as a json formatted string

		Returns: str'''
		return dumps({'location': tuple(self.location), 'size': tuple(self.size), 'ramp': self.ramp})