'A Particle class'
#IMPORTS
import pygame
from .core import circle_lighting
#IMPORTS

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

	size'''
	#__INIT__
	def __init__(self, location, momentum, size, colour, width=0):
		'Initialising a Particle object'
		self.location = list(location)
		self.momentum = list(momentum)
		self.size = size
		self.colour = colour
		self.width = 0
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
	def render(self, surface, scroll=(0, 0), lighting_colour=None, lighting_alpha=255, lighting_flag=0):
		'''Render the Particle if it is alive
		scroll is position of the camera, it will render it at the location of the Particle minus the scroll
		It can also render a lighting circle around the particle with a colour and special flag, set with lighting_flag'''
		if self.alive:
			pygame.draw.circle(surface, self.colour, [self.location[i] - scroll[i] for i in range(2)], self.size, self.width)
			if lighting_colour:
				lighting_radius = self.size * 2
				surface.blit(circle_lighting(lighting_radius, lighting_colour, lighting_alpha), [self.location[i] - lighting_radius - scroll[i] for i in range(2)], special_flags=lighting_flag)
	#RENDER
#PARTICLE