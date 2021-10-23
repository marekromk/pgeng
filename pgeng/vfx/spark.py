'''A Spark class'''
#IMPORTS
import pygame, math
#IMPORTS

#SPARK
class Spark:
	'''A spark to draw and move
	A spark is a polygon so checking collision with it is not possible'''
	#__INIT__
	def __init__(self, location, angle, speed, size, colour):
		'''Initialising a Spark object
		It will change the angle to radians

		Attributes:

		alive

		angle

		colour

		location

		size

		speed'''
		self.location = list(location)
		self.angle = math.radians(angle) #ANGLE IS IN RADIANS
		self.speed = speed
		self.size = size
		self.colour = colour
		self.alive = True
	#__INIT__

	#NORMAL_MOVEMENT
	def normal_movement(self, speed_change, delta_time=1, angle_change=0):
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
	#NORMAL_MOVEMENT

	#GRAVITY_MOVEMENT
	def gravity_movement(self, speed_change, y_momentum, maximum_y_momentum, delta_time=1):
		'''A function to move the Spark, but it also includes gravity
		It will change the angle a small amount down every frame, that will be set with y_momentum
		It will decrease the speed and if it is lower or equal to 0, it is no longer alive'''
		self.location = list(self.location)
		momentum = [math.cos(self.angle) * self.speed * delta_time, math.sin(self.angle) * self.speed * delta_time]
		self.location[0] += momentum[0]
		self.location[1] += momentum[1]
		momentum[1] = min(momentum[1] + y_momentum * delta_time, maximum_y_momentum)
		self.angle = math.atan2(momentum[1], momentum[0])
		self.speed -= speed_change * delta_time
		if self.speed <= 0:
			self.alive = False
	#GRAVITY_MOVEMENT

	#RENDER
	def render(self, surface, scroll=(0, 0), lighting_colour=None, lighting_alpha=255, lighting_flag=0):
		'''A function to render the Spark if it is alive
		It will calculate every point for the polygon (there are 4 points) that looks like a rhombus, but the back one is longer
		scroll is position of the camera, it will render it at the location of the Spark minus scroll
		It can also render a bigger spark around the particle with a colour and special flag, set with lighting_flag'''
		if self.alive:
			points = [[self.location[0] + math.cos(self.angle) * self.speed * self.size, self.location[1] + math.sin(self.angle) * self.speed * self.size], #FRONT POINT
			[self.location[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * 0.4, self.location[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * 0.4], #RIGHT POINT
			[self.location[0] - math.cos(self.angle) * self.speed * self.size * 2.5, self.location[1] - math.sin(self.angle) * self.speed * self.size * 2.5], #BOTTOM POINT
			[self.location[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * 0.4, self.location[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * 0.4]] #LEFT POINT

			pygame.draw.polygon(surface, self.colour, [[point[i] - scroll[i] for i in range(2)] for point in points])
			if lighting_colour:
				lighting_position = [abs(min(point[i] for point in points) - self.location[i] + (min(point[i] for point in points) - max(point[i] for point in points)) * 0.5) for i in range(2)]
				surface.blit(self.lighting(points, lighting_position, lighting_colour, lighting_alpha), [self.location[i] - lighting_position[i] - scroll[i] for i in range(2)], special_flags=lighting_flag)
	#RENDER

	#LIGHTING
	def lighting(self, points, position, colour, alpha):
		'''A function used by render to draw a bigger polygon on top of the normal one'''
		#EVERYTHING * 2 FOR MAKING THE POLYGON LARGER
		larger_points = [[position[0] + math.cos(self.angle) * self.speed * self.size * 2, position[1] + math.sin(self.angle) * self.speed * self.size * 2], #FRONT POINT
		[position[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * 0.8, position[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * 0.8], #RIGHT POINT
		[position[0] - math.cos(self.angle) * self.speed * self.size * 5, position[1] - math.sin(self.angle) * self.speed * self.size * 5], #BOTTOM POINT
		[position[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * 0.8, position[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * 0.8]] #LEFT POINT

		surface_size = [(math.ceil(max(point[i] for point in larger_points)) - int(min(point[i] for point in larger_points))) for i in range(2)] #DIFFERENCE BETWEEN LOWEST AND HIGHTEST POINTS
		surface = pygame.Surface(surface_size)
		surface.set_colorkey((0, 0, 0))
		if alpha != 255:
			surface.set_alpha(alpha)
		pygame.draw.polygon(surface, colour, larger_points)
		return surface
		#LIGHTING
#SPARK