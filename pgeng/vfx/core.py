'Core functions for pgeng.vfx'
import pygame

def circle_lighting(radius, colour, alpha=255):
	'''Creates a surface twice as big as the given radius
	It draws a circle with the radius on it
	The surface can have an alpha

	Returns: pygame.Surface'''
	lighting_surface = pygame.Surface((int(radius) * 2, int(radius) * 2))
	lighting_surface.set_colorkey((0, 0, 0))
	if alpha != 255:
		lighting_surface.set_alpha(alpha)
	pygame.draw.circle(lighting_surface, colour, (radius, radius), radius)
	return lighting_surface