'A Circle class with collision functions'
import pygame
from ..core import int_location
from importlib import import_module
poly =  import_module('.polygon', __package__)

class Circle:
	'''A circle to check collisions with and render
	It can check collisions with other Circle object, pygame.Rect objects and Polygon objects

	Attributes:

	center

	colour

	mask

	radius

	surface'''
	def __init__(self, center, radius, colour):
		'Initialising a Circle object'
		self.center = pygame.Vector2(center)
		self.colour = tuple(colour)
		self.surface = pygame.Surface((0, 0))
		self.set_radius(radius)

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Circle{tuple(self.center), self.radius}'

	def __eq__(self, other):
		'''Returns if it is the same as another Circle object
		colour doesn't get included
		If other is not a Circle object, it will return False

		Returns: bool'''
		return (tuple(self.center), self.radius) == (tuple(other.center), other.radius) if isinstance(other, Circle) else False

	@property
	def location(self):
		'''Returns the topleft location of the Circle

		Returns: pygame.math.Vector2'''
		return pygame.Vector2([int(self.center[i]) - int(self.radius) for i in range(2)])

	@property
	def size(self):
		'''Returns the size of the Circle

		Returns: pygame.math.Vector2'''
		return pygame.Vector2(int(self.radius) * 2)

	def _create_mask(self):
		'A function used by the class to create the mask variable'
		self.surface = pygame.Surface(self.size, pygame.SRCALPHA)
		pygame.draw.circle(self.surface, (255, 255, 255), (self.radius, self.radius), self.radius)
		self.mask = pygame.mask.from_surface(self.surface)

	def set_radius(self, radius):
		'''Used to set the radius and correct the mask
		radius must be 1 or bigger'''
		if radius < 1:
			raise ValueError('radius can\'t be lower than 1')
		self.radius = radius
		if self.surface.get_size() != tuple(self.size):
			self._create_mask()

	def collide(self, circle):
		'''A function to check if the Circle collided with another Circle object

		Returns: bool'''
		if not isinstance(circle, Circle):
			raise TypeError('circle is not a Circle object')
		offset = int_location(circle.location - self.location)
		return bool(self.mask.overlap(circle.mask, offset))

	def collidelist(self, circles):
		'''A function to check if the Circle collides with another Circle object in a list
		It returns the index of the Circle it collided with
		It returns None if it didn't collide with another Circle object

		Returns: int (or NoneType)'''
		if not all(isinstance(circle, Circle) for circle in circles):
			raise TypeError(f'every item in circles needs to be a Circle object')
		for i, circle in enumerate(circles):
			if self.collide(circle):
				return i
		return None

	def colliderect(self, Rect):
		'''A function to check if the Circle collides with a pygame.Rect object

		Returns: bool'''
		if not isinstance(Rect, pygame.Rect):
			raise TypeError('Rect is not a pygame.Rect object')
		offset = int_location(Rect.topleft - self.location)
		rect_mask = pygame.Mask(Rect.size, True)
		return bool(self.mask.overlap(rect_mask, offset))

	def collidepolygon(self, polygon):
		'''A function to check if the Circle collides with a Polygon object

		Returns: bool'''
		if not isinstance(polygon, poly.Polygon):
			raise TypeError('polygon is not a Polygon object')
		offset = int_location(polygon.location - self.location)
		return bool(self.mask.overlap(polygon.mask, offset))

	def render(self, surface, scroll=pygame.Vector2(), width=0):
		'A function to render the Circle, it just uses pygame.draw.circle()'
		pygame.draw.circle(surface, self.colour, self.center - scroll, self.radius, width)