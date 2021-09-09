'''Functions used for changing colours of surfaces'''
#IMPORTS
import pygame
from .Core import Nearest
#IMPORT

#PALETTESWAP
def PaletteSwap(Surface, Colours):
	'''Swaps the Colours of a pygame.Surface
	Colours = {OldColour: NewColour, OldColour: NewColour}

	Returns: pygame.Surface'''
	NewSurface = Surface.copy()
	for Y in range(NewSurface.get_height()):
		for X in range(NewSurface.get_width()):
			ColourValue = NewSurface.get_at((X, Y))
			if ColourValue[:-1] in Colours:
				NewSurface.set_at((X, Y), Colours[ColourValue[:-1]])
	return NewSurface
#PALETTESWAP

#GRAYSCALE
def GrayScale(Surface):
	'''A basic algorithm for grayscaling a surface (Luma ITU-R Recommendation BT. 709)
	Formula: Red * 0.2126 + Green * 0.7152 + Blue * 0.0722

	Returns: pygame.Surface'''
	NewSurface = Surface.copy()
	for Y in range(NewSurface.get_height()):
		for X in range(NewSurface.get_width()):
			ColourValue = NewSurface.get_at((X, Y))
			NewSurface.set_at((X, Y), [ColourValue[0] * 0.2126 + ColourValue[1] * 0.7152 + ColourValue[2] * 0.0722 for i in range(3)])
	return NewSurface
#GRAYSCALE

#GRAYSHADE
def GrayShade(Surface, Shades=16):
	'''A basic algorithm for grayscaling a surface with shades
	It will change the colour to one of the shades
	The amount of shades must be between 2 and 256

	Returns: pygame.Surface'''
	if not 2 < Shades < 256:
		raise ValueError(f'{Shades} Shades not supported, the amount must be between 2 and 256')
	Conversion = 255 / (Shades - 1)
	NewSurface = Surface.copy()
	for Y in range(NewSurface.get_height()):
		for X in range(NewSurface.get_width()):
			ColourValue = NewSurface.get_at((X, Y))
			NewSurface.set_at((X, Y), [Nearest((ColourValue[0] + ColourValue[1] + ColourValue[2]) / 3, Conversion) for i in range(3)])
	return NewSurface
#GRAYSHADE