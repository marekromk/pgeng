'''Functions used for changing colours of surfaces'''
#IMPORTS
import pygame
from .Core import nearest
#IMPORT

#PALETTE_SWAP
def palette_swap(surface, colours):
	'''Swaps the colours of a pygame.Surface
	colours = {old_colour: new_colour, old_colour: new_colour}

	Returns: pygame.Surface'''
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			if colour_value[:-1] in colours:
				new_surface.set_at((x, y), colours[colour_value[:-1]])
	return new_surface
#PALETTE_SWAP

#GRAY_SCALE
def gray_scale(surface):
	'''A basic algorithm for grayscaling a surface (Luma ITU-R Recommendation BT. 709)
	Formula: Red * 0.2126 + Green * 0.7152 + Blue * 0.0722

	Returns: pygame.Surface'''
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			new_surface.set_at((x, y), [colour_value[0] * 0.2126 + colour_value[1] * 0.7152 + colour_value[2] * 0.0722 for i in range(3)])
	return new_surface
#GRAY_SCALE

#GRAY_SHADE
def gray_shade(surface, shades=16):
	'''A basic algorithm for grayscaling a surface with shades
	It will change the colour to one of the shades
	The amount of shades must be between 2 and 256

	Returns: pygame.Surface'''
	if not 2 < shades < 256:
		raise ValueError(f'{shades} Shades not supported, the amount must be between 2 and 256')
	conversion = 255 / (shades - 1)
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			new_surface.set_at((x, y), [nearest((colour_value[0] + colour_value[1] + colour_value[2]) / 3, conversion) for i in range(3)])
	return new_surface
#GRAY_SHADE