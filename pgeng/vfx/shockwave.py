'A Shockwave class'
import pygame

class ShockWave:
	'''A shockwave that gets smaller or bigger

	Attributes:

	alive

	center

	colour

	radius

	width'''
	def __init__(self, center, radius, width, colour):
		'Initialising a Shockwave object'
		self.center = pygame.Vector2(center)
		self.radius = radius
		self.width = width
		self.colour = tuple(colour)
		self.alive = True

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.ShockWave({tuple(self.center)})'

	def move(self, radius_change, width_change, delta_time=1):
		'''The move function of the Shockwave
		If the width is smaller or the same as 1, it will no longer be alive
		The radius will become bigger and the width will become smaller (by default)'''
		self.center = pygame.Vector2(self.center)
		self.radius += radius_change * delta_time
		self.width -= width_change * delta_time
		if round(self.width) <= 1:
			self.alive = False

	def render(self, surface, scroll=pygame.Vector2()):
		'''It will only render it if it is still alive
		scroll is position of the camera, it will render it at the center of the Shockwave minus the scroll'''
		if self.alive:
			pygame.draw.circle(surface, self.colour, self.center - scroll, self.radius, round(self.width))