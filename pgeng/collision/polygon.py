#IMPORTS
import pygame, math
from importlib import import_module
#IMPORTS

#VARIABLES
cir =  import_module('.circle', __package__)
#VARIABLES

#POLYGON
class Polygon:
	'''A polygon to check collision with and render
	It can check collisions with other Polygon object, pygame.Rect objects and Circle objects
	points must be a list with tuples/lists with coordinates and there must be 3 points minimally

	Attributes:

	colour

	points

	rotation

	surface

	zero_rotation_center'''
	#__INIT__
	def __init__(self, points, colour):
		'Initialising a Polygon object'
		if len(points) < 3:
			raise ValueError('Polygon must have 3 or more points')
		self.colour = tuple(colour)
		self.rotation = 0
		self.surface = pygame.Surface((0, 0))
		self.set_points(points)
	#__INIT__

	#LOCATION
	@property
	def location(self):
		'''Returns the topleft location of the Polygon

		Returns: List'''
		return [int(min(point[i] for point in self.points)) for i in range(2)]
	#LOCATION

	#CENTER
	@property
	def center(self):
		'''Returns the center location of Polygon
		It doesn't return the middle of the drawn polygon, but of the rectangle the outer points create

		Returns: List'''
		return [math.ceil(max(point[i] for point in self.points) + min(point[i] for point in self.points)) // 2 for i in range(2)]
	#CENTER

	#SIZE
	@property
	def size(self):
		'''Returns the size of the Polygon

		Returns: List'''
		return [math.ceil(max([point[i] for point in self.points]) - min(point[i] for point in self.points)) for i in range(2)]
	#SIZE

	#MASK
	@property
	def mask(self):
		'''A function used by the collision functions
		the polygon gets drawn on a surface and a mask gets created from that surface

		Returns: pygame.mask.Mask'''
		if self.surface.get_size() != tuple([self.size[i] + 1 for i in range(2)]):
			self._create_surface()
		else:
			self.surface.fill((0, 0, 0))
		corrected_points = [[int(point[i]) - min(int(point[i]) for point in self.points) for i in range(2)] for point in self.points]
		pygame.draw.polygon(self.surface, (255, 255, 255), corrected_points)
		return pygame.mask.from_surface(self.surface)
	#MASK

	#_CREATE_SURFACE
	def _create_surface(self):
		'A function used by the class to create the surface variable'
		self.surface = pygame.Surface([self.size[i] + 1 for i in range(2)])
		self.surface.set_colorkey((0, 0, 0))
	#_CREATE_SURFACE

	#SET_POINTS
	def set_points(self, points, index=None):
		'''Used to set the points of the Polygon object or change a single one
		points must be a list with tuples/lists with coordinates and there must be 3 points minimally'''
		if index is None and len(points) < 3:
			raise ValueError('Polygon must have 3 or more points')
		if index is not None:
			self.points[index] = list(points)
		else:
			self.points = [list(point) for point in points]
		self.zero_rotation_center = self.center
	#SET_POINTS

	#MOVE
	def move(self, momentum, delta_time=1):
		'''Move the entire polygon
		momentum must be a list/tuple with how much it should move horizontally and vertically'''
		momentum = [momentum[i] * delta_time for i in range(2)]
		self.points = [[point[i] + momentum[i] for i in range(2)] for point in self.points]
		self.zero_rotation_center = [self.zero_rotation_center[i] + momentum[i] for i in range(2)]
	#MOVE

	#ROTATE
	def rotate(self, angle):
		'''Rotates the entire polygon a given amount of degrees clockwise
		The Polygon gets rotated around its center'''
		self.rotation = (self.rotation + angle) % 360
		angle = math.radians(angle)
		for i, point in enumerate(self.points):
			old_distance = [point[i] - self.zero_rotation_center[i] for i in range(2)]
			old_angle = math.atan2(old_distance[1], old_distance[0])
			length = math.hypot(old_distance[0], old_distance[1])
			new_angle = old_angle + angle
			self.points[i] = (self.zero_rotation_center[0] + math.cos(new_angle) * length, self.zero_rotation_center[1] + math.sin(new_angle) * length)
	#ROTATE

	#COLLIDE
	def collide(self, polygon):
		'''A function to check if the Polygon collided with another Polygon object

		Returns: Boolean'''
		if not isinstance(polygon, Polygon):
			raise TypeError('polygon is not a Polygon object')
		offset = [polygon.location[i] - self.location[i] for i in range(2)]
		return bool(self.mask.overlap(polygon.mask, offset))
	#COLLIDE

	#COLLIDELIST
	def collidelist(self, polygons):
		'''A function to check if the Polygon collides with another Polygon object in a list
		It returns the index of the Polygon it collided with
		It returns None if it didn't collide with another Polygon object

		Returns: Integer (or NoneType)'''
		if not all(isinstance(polygon, Polygon) for polygon in polygons):
			raise TypeError(f'every item in polygons needs to be a Polygon object')
		for i, polygon in enumerate(polygons):
			if self.collide(polygon):
				return i
		return None
	#COLLIDELIST

	#COLLIDERECT
	def colliderect(self, Rect):
		'''A function to check if the Polygon collides with a pygame.Rect object

		Returns: Boolean'''
		if not isinstance(Rect, pygame.Rect):
			raise TypeError('Rect is not a pygame.Rect object')
		offset = [Rect.topleft[i] - self.location[i] for i in range(2)]
		rect_mask = pygame.Mask(Rect.size, True)
		return bool(self.mask.overlap(rect_mask, offset))
	#COLLIDERECT

	#COLLIDECIRCLE
	def collidecircle(self, circle):
		'''A function to check if the Polgyon collides with a Circle object

		Returns: Boolean'''
		if not isinstance(circle, cir.Circle):
			raise TypeError('circle is not a Circle object')
		offset = [circle.location[i] - self.location[i] for i in range(2)]
		return bool(self.mask.overlap(circle.mask, offset))
	#COLLIDECIRCLE

	#RENDER
	def render(self, surface, scroll=(0, 0), width=0):
		'A function to render the Polygon, it just uses pygame.draw.polygon()'
		pygame.draw.polygon(surface, self.colour, [[point[i] - scroll[i] for i in range(2)] for point in self.points], width)
	#RENDER
#POLYGON