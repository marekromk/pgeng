'A Spark class'
import pygame, math
from ..collision import Polygon

def set_spark_attributes(front_length=1, side_length=0.3, back_length=3.5):
	'''Set the attributes for the Spark
	front_length is the length of the front point of the Spark
	side_length is the length of the side points of the Spark
	back_length is the length of the back point of the Spark

	For reference, the length of the front point of the Spark is usually 1'''
	if front_length <= 0 or side_length <= 0 or back_length <= 0:
		raise ValueError('front_length, side_length and back_length can\'t be 0 or less')
	Spark.front_length = front_length
	Spark.side_length = side_length
	Spark.back_length = back_length

class Spark:
	'''A spark to draw and move
	The angle should be in degrees
	A spark is a polygon, so checking collision with it is not possible

	Attributes:

	alive

	angle

	colour

	lengths

	location

	points

	size

	speed'''
	front_length = 1
	side_length = 0.3
	back_length = 3.5

	def __init__(self, location, angle, speed, size, colour):
		'Initialising a Spark object'
		self.location = pygame.Vector2(location)
		self.angle = angle
		self.speed = speed
		self.size = size
		self.colour = tuple(colour)
		self.lengths = (Spark.front_length, Spark.side_length, Spark.back_length)
		self.alive = True
		self.points = None

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Spark({tuple(self.location)})'

	@property
	def polygon(self):
		'''Returns a Polygon object of the Spark if the points are set and it is alive
		The points are set when it has been rendered once

		Returns: Polygon (or NoneType)'''
		if self.alive and self.points is not None:
			return Polygon(self.points, self.colour)

	def angle_towards(self, angle, change_rate, delta_time=1):
		'''A function to change the angle slightly towards another angle
		angle should be given in degrees
		change_rate is how much the angle should change every frame'''
		direction = (angle - self.angle + 180) % 360 - 180
		rotation = abs(direction) / direction if direction else 1
		if abs(direction) < change_rate * delta_time:
			self.angle = angle
		else:
			self.angle += rotation * change_rate * delta_time

	def move(self, speed_change, delta_time=1, angle_change=0):
		'''A function to move the Spark
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive
		angle_change will change the angle by that amount every time this function runs'''
		angle = math.radians(self.angle)
		self.location = pygame.Vector2(self.location)
		self.location.x += math.cos(angle) * self.speed * delta_time
		self.location.y += math.sin(angle) * self.speed * delta_time
		self.speed -= speed_change * delta_time
		self.angle += angle_change * delta_time
		if self.speed <= 0:
			self.alive = False

	def gravity(self, speed_change, change_rate, delta_time=1):
		'''A function to move the Spark, but it also includes gravity
		It will use angle_towards, so that's what change_rate is for
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive'''
		self.move(speed_change, delta_time)
		if self.alive:
			self.angle_towards(90, change_rate, delta_time)

	def render(self, surface, scroll=pygame.Vector2(), lighting_colour=None, lighting_alpha=255, lighting_flag=0):
		'''A function to render the Spark if it is alive
		It will calculate every point for the polygon (there are 4 points) that looks like a rhombus, but the back one is longer
		scroll is position of the camera, it will render it at the location of the Spark minus scroll
		It can also render a bigger spark around the particle with a colour and special flag, set with lighting_flag'''
		if self.alive:
			angle = math.radians(self.angle)
			self.points = [[self.location[0] + math.cos(angle) * self.speed * self.size * self.lengths[0], self.location[1] + math.sin(angle) * self.speed * self.size * self.lengths[0]], #FRONT POINT
			[self.location[0] + math.cos(angle + math.pi * 0.5) * self.speed * self.size * self.lengths[1], self.location[1] + math.sin(angle + math.pi * 0.5) * self.speed * self.size * self.lengths[1]], #RIGHT POINT
			[self.location[0] - math.cos(angle) * self.speed * self.size * self.lengths[2], self.location[1] - math.sin(angle) * self.speed * self.size * self.lengths[2]], #BOTTOM POINT
			[self.location[0] + math.cos(angle - math.pi * 0.5) * self.speed * self.size * self.lengths[1], self.location[1] + math.sin(angle - math.pi * 0.5) * self.speed * self.size * self.lengths[1]]] #LEFT POINT

			pygame.draw.polygon(surface, self.colour, [pygame.Vector2(point) - scroll for point in self.points])
			if lighting_colour:
				lighting_position = [abs(min(point[i] for point in self.points) - self.location[i] + (min(point[i] for point in self.points) - max(point[i] for point in self.points)) * 0.5) for i in range(2)]
				surface.blit(self._lighting(lighting_position, lighting_colour, lighting_alpha), self.location - lighting_position - scroll, special_flags=lighting_flag)

	def _lighting(self, position, colour, alpha=255):
		'A function used by render to render a bigger polygon on top of the normal one'
		#EVERYTHING * 2 FOR MAKING THE POLYGON LARGER
		angle = math.radians(self.angle)
		lengths = [self.lengths[i] * 2 for i in range(3)]
		larger_points = [[position[0] + math.cos(angle) * self.speed * self.size * lengths[0], position[1] + math.sin(angle) * self.speed * self.size * lengths[0]], #FRONT POINT
		[position[0] + math.cos(angle + math.pi * 0.5) * self.speed * self.size * lengths[1], position[1] + math.sin(angle + math.pi * 0.5) * self.speed * self.size * lengths[1]], #RIGHT POINT
		[position[0] - math.cos(angle) * self.speed * self.size * lengths[2], position[1] - math.sin(angle) * self.speed * self.size * lengths[2]], #BOTTOM POINT
		[position[0] + math.cos(angle - math.pi * 0.5) * self.speed * self.size * lengths[1], position[1] + math.sin(angle - math.pi * 0.5) * self.speed * self.size * lengths[1]]] #LEFT POINT

		surface_size = [math.ceil(max(point[i] for point in larger_points) - min(point[i] for point in larger_points)) for i in range(2)] #DIFFERENCE BETWEEN LOWEST AND HIGHTEST POINTS
		surface = pygame.Surface(surface_size)
		surface.set_colorkey((0, 0, 0))
		if alpha != 255:
			surface.set_alpha(alpha)
		pygame.draw.polygon(surface, colour, larger_points)
		return surface