'Core functions for pgeng.vfx'
import pygame

def circle_lighting(radius, colour, alpha=255):
	'''Creates a surface twice as big as the given radius
	It draws a circle with the radius on it
	The surface can have an alpha

	Returns: pygame.Surface'''
	tuple_colour = tuple(colour[:3])
	surface = pygame.Surface((int(radius) * 2, int(radius) * 2))
	surface.set_colorkey((0, 0, 0) if tuple_colour != (0, 0, 0) else (1, 0, 0)) #there should be no background
	if tuple_colour == (0, 0, 0):
		surface.fill((1, 0, 0))
	if alpha != 255:
		surface.set_alpha(alpha)
	pygame.draw.circle(surface, colour, (radius, radius), radius)
	return surface