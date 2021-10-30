'A Spark class'
#IMPORTS
import pygame, math
#IMPORTS

#SET_SPARK_ATTRIBUTES
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
#SET_SPARK_ATTRIBUTES

#SPARK
class Spark:
	'''A spark to draw and move
	the given angle will be changed to radians, so give it in degrees
	A spark is a polygon, so checking collision with it is not possible

	Attributes:

	alive

	angle

	colour

	lengths

	location

	size

	speed'''
	#VARIABLES
	front_length = 1
	side_length = 0.3
	back_length = 3.5
	#VARIABLES

	#__INIT__
	def __init__(self, location, angle, speed, size, colour):
		'Initialising a Spark object'
		self.location = list(location)
		self.angle = math.radians(angle)
		self.speed = speed
		self.size = size
		self.colour = colour
		self.lengths = [Spark.front_length, Spark.side_length, Spark.back_length]
		self.alive = True
	#__INIT__

	#ANGLE_TOWARDS
	def angle_towards(self, angle, change_rate, delta_time=1):
		'''A function to change the angle slightly towards another angle
		angle should be given in degrees
		change_rate is how much the angle should change every frame'''
		angle = math.radians(angle)
		direction = (angle - self.angle + math.pi) % (math.pi * 2) - math.pi
		rotation = abs(direction) / direction if direction else 1
		if abs(direction) < change_rate * delta_time:
			self.angle = angle
		else:
			self.angle += rotation * change_rate * delta_time
	#ANGLE_TOWARDS

	#MOVE
	def move(self, speed_change, delta_time=1, angle_change=0):
		'''A function to move the Spark
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive
		angle_change will change the angle by that amount every time this function runs'''
		self.location = list(self.location)
		self.location[0] += math.cos(self.angle) * self.speed * delta_time
		self.location[1] += math.sin(self.angle) * self.speed * delta_time
		self.speed -= speed_change * delta_time
		self.angle += angle_change * delta_time
		if self.speed <= 0:
			self.alive = False
	#MOVE

	#GRAVITY
	def gravity(self, speed_change, change_rate, delta_time=1):
		'''A function to move the Spark, but it also includes gravity
		It will use angle_towards, so that's what change_rate is for
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive'''
		self.move(speed_change, delta_time)
		self.angle_towards(90, change_rate, delta_time)
	#GRAVITY

	#RENDER
	def render(self, surface, scroll=(0, 0), lighting_colour=None, lighting_alpha=255, lighting_flag=0):
		'''A function to render the Spark if it is alive
		It will calculate every point for the polygon (there are 4 points) that looks like a rhombus, but the back one is longer
		scroll is position of the camera, it will render it at the location of the Spark minus scroll
		It can also render a bigger spark around the particle with a colour and special flag, set with lighting_flag'''
		if self.alive:
			points = [[self.location[0] + math.cos(self.angle) * self.speed * self.size * self.lengths[0], self.location[1] + math.sin(self.angle) * self.speed * self.size * self.lengths[0]], #FRONT POINT
			[self.location[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * self.lengths[1], self.location[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * self.lengths[1]], #RIGHT POINT
			[self.location[0] - math.cos(self.angle) * self.speed * self.size * self.lengths[2], self.location[1] - math.sin(self.angle) * self.speed * self.size * self.lengths[2]], #BOTTOM POINT
			[self.location[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * self.lengths[1], self.location[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * self.lengths[1]]] #LEFT POINT

			pygame.draw.polygon(surface, self.colour, [[point[i] - scroll[i] for i in range(2)] for point in points])
			if lighting_colour:
				lighting_position = [abs(min(point[i] for point in points) - self.location[i] + (min(point[i] for point in points) - max(point[i] for point in points)) * 0.5) for i in range(2)]
				surface.blit(self.lighting(points, lighting_position, lighting_colour, lighting_alpha), [self.location[i] - lighting_position[i] - scroll[i] for i in range(2)], special_flags=lighting_flag)
	#RENDER

	#LIGHTING
	def lighting(self, points, position, colour, alpha):
		'A function used by render to draw a bigger polygon on top of the normal one'
		#EVERYTHING * 2 FOR MAKING THE POLYGON LARGER
		lengths = [self.lengths[i] * 2 for i in range(3)]
		larger_points = [[position[0] + math.cos(self.angle) * self.speed * self.size * lengths[0], position[1] + math.sin(self.angle) * self.speed * self.size * lengths[0]], #FRONT POINT
		[position[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * lengths[1], position[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * lengths[1]], #RIGHT POINT
		[position[0] - math.cos(self.angle) * self.speed * self.size * lengths[2], position[1] - math.sin(self.angle) * self.speed * self.size * lengths[2]], #BOTTOM POINT
		[position[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * lengths[1], position[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * lengths[1]]] #LEFT POINT

		surface_size = [math.ceil(max(point[i] for point in larger_points) - min(point[i] for point in larger_points)) for i in range(2)] #DIFFERENCE BETWEEN LOWEST AND HIGHTEST POINTS
		surface = pygame.Surface(surface_size)
		surface.set_colorkey((0, 0, 0))
		if alpha != 255:
			surface.set_alpha(alpha)
		pygame.draw.polygon(surface, colour, larger_points)
		return surface
		#LIGHTING
#SPARK