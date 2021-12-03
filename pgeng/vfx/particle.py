'A Particle class'
import pygame
from ..collision import Circle
from .core import circle_lighting

class Particle:
	'''A particle to move and render
	momentum has to be a list with how much the particle should move every frame [x, y]
	It can also have gravity and a 'lighting' for the rendering

	Attributes:

	alive

	colour

	location

	momentum

	size'''
	def __init__(self, location, momentum, size, colour, width=0):
		'Initialising a Particle object'
		self.location = pygame.Vector2(location)
		self.momentum = pygame.Vector2(momentum)
		self.size = size
		self.colour = tuple(colour)
		self.width = width
		self.alive = True

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Particle{tuple(self.location), tuple(self.momentum)}'

	@property
	def circle(self):
		'''Returns a Circle object of the Particle if it is alive

		Returns: Circle (or NoneType)'''
		if self.alive:
			return Circle(self.location, self.size, self.colour)

	def move(self, size_change, y_momentum=0, delta_time=1):
		'''Move the location of the Particle and change the size
		If the size is smaller or equal to 0, it will no longer be alive
		It also has gravity (y_momentum)'''
		self.location = pygame.Vector2(self.location)
		self.momentum = pygame.Vector2(self.momentum)
		self.momentum.y += y_momentum * delta_time
		self.location += self.momentum * delta_time
		self.size -= size_change * delta_time
		if self.size < 1:
			self.alive = False

	def render(self, surface, scroll=pygame.Vector2(), lighting_colour=None, lighting_alpha=255, lighting_flag=0):
		'''Render the Particle if it is alive
		scroll is position of the camera, it will render it at the location of the Particle minus the scroll
		It can also render a lighting circle around the particle with a colour and special flag, set with lighting_flag'''
		if self.alive:
			pygame.draw.circle(surface, self.colour, self.location - scroll, self.size, self.width if lighting_colour is None else 0)
			if lighting_colour:
				lighting_radius = self.size * 2
				surface.blit(circle_lighting(lighting_radius, lighting_colour, lighting_alpha), [self.location[i] - lighting_radius - scroll[i] for i in range(2)], special_flags=lighting_flag)