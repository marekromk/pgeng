'Functions used for changing colours of surfaces'
import pygame
from .core import nearest

def palette_swap(surface, colours):
	'''Swaps the colours of a pygame.Surface
	colours = {old_colour: new_colour, old_colour: new_colour}

	Returns: pygame.Surface'''
	if type(colours) is not dict:
		raise TypeError('colours must be a dictionary')
	length_colour = max([len(colour) for colour in colours]) #check if colour format is (r, g, b) or (r, g, b, a)
	for colour in colours.copy():
		if len(colour) != length_colour:
			colours[colour + (255,)] = colours.pop(colour) #if length_colour is 4, add standard alpha value to every key
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			if colour_value[:length_colour] in colours: #check if pixel's colour is in the dictionary, shorten it to 3 with length_colour if necessary
				new_surface.set_at((x, y), colours[colour_value[:length_colour]])
	return new_surface

def gray_scale(surface):
	'''A basic algorithm for grayscaling a surface (Luma ITU-R Recommendation BT. 709)
	Formula: Red * 0.2126 + Green * 0.7152 + Blue * 0.0722

	Returns: pygame.Surface'''
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			new_surface.set_at((x, y), [colour_value.r * 0.2126 + colour_value.g * 0.7152 + colour_value.b * 0.0722 for i in range(3)] + [colour_value[3]]) #for i in range(3) as in (r, g, b), + colour_value[3],because alpha does not change
	return new_surface

def gray_shade(surface, shades=16):
	'''A basic algorithm for grayscaling a surface with shades
	It will change the colour to one of the shades
	The amount of shades must be between 2 and 256

	Returns: pygame.Surface'''
	if not 2 < shades < 256:
		raise ValueError(f'{shades} shades not supported, the amount must be between 2 and 256')
	conversion = 255 / (shades - 1)
	new_surface = surface.copy()
	for y in range(new_surface.get_height()):
		for x in range(new_surface.get_width()):
			colour_value = new_surface.get_at((x, y))
			new_surface.set_at((x, y), [nearest(sum(colour_value[:3]) / 3, conversion) for i in range(3)] + [colour_value[3]]) #for i in range(3) as in (r, g, b), + colour_value[3],because alpha does not change
	return new_surface

def outline(surface, line_colour, draw_surface=True):
	'''Create a coloured outline around a given surface with a given colour and width
	If draw_surface is True, than it will draw te original surface on top of the outline, otherwise it will only return the outline

	Returns: pygame.Surface'''
	outline_surface = pygame.Surface([surface.get_size()[i] + 2 for i in range(2)], pygame.SRCALPHA) #add 2 to width and height, because an outline uses 2 extra pixels on both dimensions
	mask_surface = pygame.mask.from_surface(surface).to_surface() #get the mask from the image, only the coloured and non coloured pixels
	if tuple(line_colour[:3]) == (0, 0, 0):
		mask_surface = palette_swap(mask_surface, {(0, 0, 0): (1, 0, 0)}) #change mask_surface backround to not be the same as the line
	if tuple(line_colour[:3]) != (255, 255, 255):
		mask_surface = palette_swap(mask_surface, {(255, 255, 255): tuple(line_colour)}) #change the mask_surface pixels to be the outline
	mask_surface.set_colorkey((0, 0, 0) if tuple(line_colour[:3]) != (0, 0, 0) else (1, 0, 0))
	for i in (0, 2):
		outline_surface.blit(mask_surface, (i, 1)) #blit mask_surface one pixel to the left or right of the middle
		outline_surface.blit(mask_surface, (1, i)) #blit mask_surface surface one pixel to the top or bottom of the middle
	if draw_surface:
		outline_surface.blit(surface, (1, 1)) #blit the original surface in the middle
	else:
		colourkey = (0, 0, 0) if tuple(line_colour[:3]) != (0, 0, 0) else (1, 0, 0) #colourkey needs to be the original mask so an empty mask get blitted in the middle of the outlines, then only the line is left
		mask_surface = palette_swap(mask_surface, {tuple(line_colour): colourkey})
		outline_surface.set_colorkey(colourkey)
		outline_surface.blit(mask_surface, (1, 1)) #blit the empty mask in the middle
	return outline_surface