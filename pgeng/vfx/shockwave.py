'''A Shockwave class'''
#IMPORTS
import pygame
#IMPORTS

#SHOCKWAVE
class ShockWave:
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
		if round(self.width) <= 1:
			self.alive = False
		else:
			pygame.draw.circle(surface, self.colour, [self.location[i] - scroll[i] for i in range(2)], self.radius, round(self.width))
	#UPDATE
#SHOCKWAVE