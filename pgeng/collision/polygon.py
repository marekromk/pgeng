'A Polygon class with collision functions'
import pygame, math
from ..core import int_location
from importlib import import_module
cir =  import_module('.circle', __package__)

class Polygon:
	'''A polygon to check collision with and render
	It can check collisions with other Polygon object, pygame.Rect objects and Circle objects
	points must be a list with tuples/lists with coordinates and there must be 3 points minimally

	Attributes:

	colour

	mask

	points

	rotation

	surface

	zero_rotation_center'''
	def __init__(self, points, colour):
		'Initialising a Polygon object'
		if len(points) < 3:
			raise ValueError('Polygon must have 3 or more points')
		self.colour = tuple(colour)
		self.rotation = 0
		self.surface = pygame.Surface((0, 0))
		self.set_points(points)

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Polygon({tuple(self.location)})'

	def __eq__(self, other):
		'''Returns if it is the same as another Polygon object
		colour doesn't get included
		If other is not a Polygon object, it will return False

		Returns: bool'''
		return ([tuple(point) for point in self.points], self.rotation % 360) == ([tuple(point) for point in other.points], other.rotation % 360) if isinstance(other, Polygon) else False

	def __len__(self):
		'''Returns the length of the points variable

		Returns: int'''
		return len(self.points)

	@property
	def location(self):
		'''Returns the topleft location of the Polygon

		Returns: pygame.math.Vector2'''
		return pygame.Vector2([int(min(point[i] for point in self.points)) for i in range(2)])

	@property
	def center(self):
		'''Returns the center location of Polygon
		It doesn't return the middle of the drawn polygon, but of the rectangle the outer points create

		Returns: pygame.math.Vector2'''
		return pygame.Vector2([math.ceil(max(point[i] for point in self.points) + min(point[i] for point in self.points)) // 2 for i in range(2)])

	@property
	def size(self):
		'''Returns the size of the Polygon

		Returns: pygame.math.Vector2'''
		return pygame.Vector2([math.ceil(max([point[i] for point in self.points]) - min(point[i] for point in self.points)) for i in range(2)])

	def _create_mask(self):
		'A function used by the class to create the mask'
		if self.surface.get_size() != tuple([self.size[i] + 1 for i in range(2)]):
			self.surface = pygame.Surface([self.size[i] + 1 for i in range(2)], pygame.SRCALPHA)
		else:
			self.surface.fill((0, 0, 0, 0))
		corrected_points = [[int(point[i]) - min(int(point[i]) for point in self.points) for i in range(2)] for point in self.points]
		pygame.draw.polygon(self.surface, (255, 255, 255), corrected_points)
		self.mask = pygame.mask.from_surface(self.surface)

	def set_points(self, points, index=None, reset_rotation=True):
		'''Used to set the points of the Polygon object or change a single one
		points must be a list with tuples/lists or pygame.math.Vector2 objects
		There must be 3 points minimally
		It will run rotation_as_zero if reset_rotation is True'''
		if index is None and len(points) < 3:
			raise ValueError('Polygon must have 3 or more points')
		if index is not None:
			self.points[index] = pygame.Vector2(points)
		else:
			self.points = [pygame.Vector2(point) for point in points]
		self._create_mask()
		if reset_rotation:
			self.rotation_as_zero()

	def rotation_as_zero(self):
		'This will reset rotation to 0 and zero_rotation_center to the current center of Polygon'
		self.rotation = 0
		self.zero_rotation_center = self.center

	def move(self, momentum, delta_time=1):
		'''Move the entire Polygon
		momentum must be a list/tuple with how much it should move horizontally and vertically'''
		momentum = pygame.Vector2(momentum) * delta_time
		self.points = [point + momentum for point in self.points]
		self.zero_rotation_center += momentum

	def rotate(self, angle):
		'''Rotates the entire Polygon a given amount of degrees clockwise
		The Polygon gets rotated around zero_rotation_center'''
		self.rotation = (self.rotation + angle) % 360
		angle = math.radians(angle)
		for i, point in enumerate(self.points):
			old_distance = point - self.zero_rotation_center
			old_angle = math.radians(pygame.Vector2().angle_to(old_distance))
			length = old_distance.length()
			new_angle = old_angle + angle
			self.points[i] = self.zero_rotation_center + (math.cos(new_angle) * length, math.sin(new_angle) * length)
		self._create_mask()

	def collide(self, polygon):
		'''A function to check if the Polygon collided with another Polygon object

		Returns: bool'''
		if not isinstance(polygon, Polygon):
			raise TypeError('polygon is not a Polygon object')
		offset = int_location(polygon.location - self.location)
		return bool(self.mask.overlap(polygon.mask, offset))

	def collidelist(self, polygons):
		'''A function to check if the Polygon collides with another Polygon object in a list
		It returns the index of the Polygon it collided with
		It returns None if it didn't collide with another Polygon object

		Returns: int (or NoneType)'''
		if not all(isinstance(polygon, Polygon) for polygon in polygons):
			raise TypeError(f'every item in polygons needs to be a Polygon object')
		for i, polygon in enumerate(polygons):
			if self.collide(polygon):
				return i
		return None

	def colliderect(self, Rect):
		'''A function to check if the Polygon collides with a pygame.Rect object

		Returns: bool'''
		if not isinstance(Rect, pygame.Rect):
			raise TypeError('Rect is not a pygame.Rect object')
		offset = int_location(Rect.topleft - self.location)
		rect_mask = pygame.Mask(Rect.size, True)
		return bool(self.mask.overlap(rect_mask, offset))

	def collidecircle(self, circle):
		'''A function to check if the Polgyon collides with a Circle object

		Returns: bool'''
		if not isinstance(circle, cir.Circle):
			raise TypeError('circle is not a Circle object')
		offset = int_location(circle.location - self.location)
		return bool(self.mask.overlap(circle.mask, offset))

	def render(self, surface, scroll=pygame.Vector2(), width=0):
		'A function to render the Polygon, it just uses pygame.draw.polygon()'
		pygame.draw.polygon(surface, self.colour, [point - scroll for point in self.points], width)