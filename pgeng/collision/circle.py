#IMPORTS
import pygame
from importlib import import_module
#IMPORTS

#VARIABLES
poly =  import_module('.polygon', __package__)
#VARIABLES

#CIRCLE
class Circle:
	'''A circle to check collisions with and render
	It can check collisions with other Circle object, pygame.Rect objects and Polygon objects

	Attributes:

	center

	colour

	mask

	radius

	surface'''
	#__INIT__
	def __init__(self, center, radius, colour):
		'Initialising a Circle object'
		if type(center) is not list and type(center) is not tuple:
			raise TypeError('center must be a list or tuple')
		self.center = list(center)
		self.colour = tuple(colour)
		self.surface = pygame.Surface((0, 0))
		self.set_radius(radius)
	#__INIT__

	#LOCATION
	@property
	def location(self):
		'''Returns the topleft location of the Circle

		Returns: List'''
		return [int(self.center[i]) - int(self.radius) for i in range(2)]
	#LOCATION

	#SIZE
	@property
	def size(self):
		'''Returns the size of the Circle

		Returns: List'''
		return [int(self.radius) * 2 for i in range(2)]
	#SIZE

	#_CREATE_MASK
	def _create_mask(self):
		'A function used by the class to create the mask variable'
		self.surface = pygame.Surface(self.size)
		self.surface.set_colorkey((0, 0, 0))
		pygame.draw.circle(self.surface, (255, 255, 255), (self.radius, self.radius), self.radius)
		self.mask = pygame.mask.from_surface(self.surface)
	#_CREATE_MASK

	#SET_RADIUS
	def set_radius(self, radius):
		'''Used to set the radius and correct the mask
		radius must be 1 or bigger'''
		if radius < 1:
			raise ValueError('radius can\'t be lower than 1')
		self.radius = radius
		if self.surface.get_size() != tuple(self.size):
			self._create_mask()
	#SET_RADIUS

	#COLLIDE
	def collide(self, circle):
		'''A function to check if the Circle collided with another Circle object

		Returns: Boolean'''
		if not isinstance(circle, Circle):
			raise TypeError('circle is not a Circle object')
		offset = [circle.location[i] - self.location[i] for i in range(2)]
		return bool(self.mask.overlap(circle.mask, offset))
	#COLLIDE

	#COLLIDELIST
	def collidelist(self, circles):
		'''A function to check if the Circle collides with another Circle object in a list
		It returns the index of the Circle it collided with
		It returns None if it didn't collide with another Circle object

		Returns: Integer (or NoneType)'''
		if not all(isinstance(circle, Circle) for circle in circles):
			raise TypeError(f'every item in circles needs to be a Circle object')
		for i, circle in enumerate(circles):
			if self.collide(circle):
				return i
		return None
	#COLLIDELIST

	#COLLIDERECT
	def colliderect(self, Rect):
		'''A function to check if the Circle collides with a pygame.Rect object

		Returns: Boolean'''
		if not isinstance(Rect, pygame.Rect):
			raise TypeError('Rect is not a pygame.Rect object')
		offset = [Rect.topleft[i] - self.location[i] for i in range(2)]
		rect_mask = pygame.Mask(Rect.size, True)
		return bool(self.mask.overlap(rect_mask, offset))
	#COLLIDERECT

	#COLLIDEPOLYGON
	def collidepolygon(self, polygon):
		'''A function to check if the Circle collides with a Polygon object

		Returns: Boolean'''
		if not isinstance(polygon, poly.Polygon):
			raise TypeError('polygon is not a Polygon object')
		offset = [polygon.location[i] - self.location[i] for i in range(2)]
		return bool(self.mask.overlap(polygon.mask, offset))
	#COLLIDEPOLYGON

	#RENDER
	def render(self, surface, scroll=(0, 0), width=0):
		'A function to render the Circle, it just uses pygame.draw.circle()'
		pygame.draw.circle(surface, self.colour, [self.center[i] - scroll[i] for i in range(2)], self.radius, width)
	#RENDER
#CIRCLE