'''Functions and classes for visual effects in PyGame'''
#IMPORTS
import pygame, math
#IMPORTS

#CIRCLE_LIGHTING
def circle_lighting(radius, colour, alpha=255):
	'''Creates a surface twice as big as the given radius
	It draws a circle with the radius on it
	Recommended to blit with a special flag

	Returns: pygame.Surface'''
	lighting_surface = pygame.Surface((radius * 2, radius * 2))
	lighting_surface.set_colorkey((0, 0, 0))
	if alpha != 255:
		lighting_surface.set_alpha(alpha)
	pygame.draw.circle(lighting_surface, colour, (radius, radius), radius)
	return lighting_surface
#CIRCLE_LIGHTING

#PARITCLE
class Particle:
	'''A particle to move and render
	momentum has to be a list with how much the particle should move every frame [x, y]
	It can also have gravity and a 'lighting' for the rendering

	Attributes:

	alive

	colour

	location

	momentum

	size
	'''
	#__INIT__
	def __init__(self, location, momentum, size, colour):
		'''Initialising a Particle object'''
		self.location = list(location)
		self.momentum = list(momentum)
		self.size = size
		self.colour = colour
		self.alive = True
	#__INIT__

	#MOVE
	def move(self, size_change, y_momentum=0, delta_time=1):
		'''Move the location of the Particle and change the size
		If the size is smaller or equal to 0, it will no longer be alive
		It also has gravity (y_momentum)'''
		self.location = list(self.location)
		self.momentum = list(self.momentum)
		self.momentum[1] += y_momentum * delta_time
		self.location[0] += self.momentum[0] * delta_time
		self.location[1] += self.momentum[1] * delta_time
		self.size -= size_change * delta_time
		if self.size < 1:
			self.alive = False
	#MOVE

	#RENDER
	def render(self, surface, scroll=(0, 0), lighting_colour=None):
		'''Render the Particle if it is alive
		scroll is position of the camera, it will render it at the location of the Particle minus the scroll
		It can also render a lighting circle around the particle with the pygame.BLEND_RGBA_ADD flag'''
		if self.alive:
			pygame.draw.circle(surface, self.colour, (self.location[0] - scroll[0], self.location[1] - scroll[1]), self.size)
			if lighting_colour:
				lighting_radius = self.size * 2
				surface.blit(circle_lighting(lighting_radius, lighting_colour), (self.location[0] - lighting_radius - scroll[0], self.location[1] - lighting_radius - scroll[1]), special_flags=pygame.BLEND_RGBA_ADD)
	#RENDER
#PARTICLE

#SHOCKWAVE
class Shockwave:
	'''A shockwave that gets smaller or bigger

	Attributes:

	alive

	colour

	location

	radius

	width'''
	#__INIT__
	def __init__(self, location, radius, width, colour):
		'''Initialising a Shockwave object'''
		self.location = list(location)
		self.radius = radius
		self.width = width
		self.colour = colour
		self.alive = True
	#__INIT__

	#UPDATE
	def update(self, surface, radius_change, width_change, scroll=(0, 0), delta_time=1):
		'''The move and render function of the Shockwave (it will only render it if it is still alive)
		If the width is smaller or the same as 1, it will no longer be alive
		scroll is position of the camera, it will render it at the location of the Shockwave minus the scroll'''
		self.radius += radius_change * delta_time
		self.width -= width_change * delta_time
		if self.width <= 1:
			self.alive = False
		else:
			pygame.draw.circle(surface, self.colour, (self.location[0] - scroll[0], self.location[1] - scroll[1]), self.radius, int(self.width))
	#UPDATE
#SHOCKWAVE

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
	def render(self, surface, scroll=(0, 0), lighting_colour=None):
		'''A function to render the Spark if it is alive
		It will calculate every point for the polygon (there are 4 points) that looks like a rhombus, but the back one is longer
		scroll is position of the camera, it will render it at the location of the Spark minus scroll
		If lighting_colour is turned on, it will blit a bigger polygon with a specific colour on top of it with BLEND_RGBA_ADD'''
		if self.alive:
			points = [[self.location[0] + math.cos(self.angle) * self.speed * self.size, self.location[1] + math.sin(self.angle) * self.speed * self.size], #FRONT POINT
			[self.location[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * 0.4, self.location[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * 0.4], #RIGHT POINT
			[self.location[0] - math.cos(self.angle) * self.speed * self.size * 2.5, self.location[1] - math.sin(self.angle) * self.speed * self.size * 2.5], #BOTTOM POINT
			[self.location[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * 0.4, self.location[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * 0.4]] #LEFT POINT

			pygame.draw.polygon(surface, self.colour, [[point[0] - scroll[0], point[1] - scroll[1]] for point in points])
			if lighting_colour:
				lighting_position = [abs(min([point[0] for point in points]) - self.location[0] + (min([point[0] for point in points]) - max([point[0] for point in points])) * 0.5),
				abs(min([point[1] for point in points]) - self.location[1] + (min([point[1] for point in points]) - max([point[1] for point in points])) * 0.5)]
				surface.blit(self.lighting(points, lighting_position, lighting_colour), (self.location[0] - lighting_position[0] - scroll[0], self.location[1] - lighting_position[1] - scroll[1]), special_flags=pygame.BLEND_RGBA_ADD)
	#RENDER

	#LIGHTING
	def lighting(self, points, lighting_position, colour):
		'''A function used by render to draw a bigger polygon on top of the normal one'''
		lighting_surface_width = (max([point[0] for point in points]) - min([point[0] for point in points])) * 2
		lighting_surface_height = (max([point[1] for point in points]) - min([point[1] for point in points])) * 2
		lighting_surface = pygame.Surface((lighting_surface_width, lighting_surface_height)) #DIFFERENCE BETWEEN LOWEST AND HIGHTEST POINTS
		lighting_surface.set_colorkey((0, 0, 0))

		#EVERYTHING * 2 FOR MAKING THE POLYGON LARGER
		larger_points = [[lighting_position[0] + math.cos(self.angle) * self.speed * self.size * 2, lighting_position[1] + math.sin(self.angle) * self.speed * self.size * 2], #FRONT POINT
		[lighting_position[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.size * 0.8, lighting_position[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.size * 0.8], #RIGHT POINT
		[lighting_position[0] - math.cos(self.angle) * self.speed * self.size * 5, lighting_position[1] - math.sin(self.angle) * self.speed * self.size * 5], #BOTTOM POINT
		[lighting_position[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.size * 0.8, lighting_position[1] + math.sin(self.angle - math.pi / 2) * self.speed * self.size * 0.8]] #LEFT POINT
		pygame.draw.polygon(lighting_surface, colour, larger_points)
		return lighting_surface
		#LIGHTING
#SPARK