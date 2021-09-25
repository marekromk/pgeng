'''A classes and functions for creating fonts and text buttons'''
#IMPORTS
import pygame
from pathlib import Path
from .Core import clip_surface, load_image
from .Colour import palette_swap
#IMPORTS

#VARIALBES
__all__ = ['create_font', 'TextButton']
path = Path(__file__).parent.resolve()
#VARIABLES

#CREATE_FONT
def create_font(colour):
	'''A function to create small and large Font objects
	colour will be the colour of the text
	The first value in the returned tuple is the small font and the second value is the large font

	Returns: Tuple'''
	if tuple(colour) == (0, 0, 0):
		small_font_image = palette_swap(load_image(f'{path}/Font/Small.png'), {(255, 0, 0): colour, tuple(colour): (255, 255, 255)})
		large_font_image = palette_swap(load_image(f'{path}/Font/Large.png'), {(255, 0, 0): colour, tuple(colour): (255, 255, 255)})
		return Font(small_font_image, background_colour=255), Font(large_font_image, background_colour=255)
	if tuple(colour) == (127, 127, 127):
		small_font_image = palette_swap(load_image(f'{path}/Font/Small.png'), {(255, 0, 0): colour, tuple(colour): (128, 128, 128)})
		large_font_image = palette_swap(load_image(f'{path}/Font/Large.png'), {(255, 0, 0): colour, tuple(colour): (128, 128, 128)})
		return Font(small_font_image, 128), Font(large_font_image, 128)
	small_font_image = palette_swap(load_image(f'{path}/Font/Small.png'), {(255, 0, 0): colour})
	large_font_image = palette_swap(load_image(f'{path}/Font/Large.png'), {(255, 0, 0): colour})
	return Font(small_font_image), Font(large_font_image)
#CREATE_FONT

#FONT
class Font:
	'''A class to create a pixel art font
	It will get all the letters out of the image and render them
	The border between letters is usually (127, 127, 127) and the background is usually (0, 0, 0) change them if it is necessary

	The font is made by DaFluffyPotato

	Attributes:

	character_height

	characters

	font_image

	space_width'''
	#__INIT__
	def __init__(self, font_image, border_colour=127, background_colour=0):
		'''Initialising a font object'''
		self.font_image = font_image
		self.font_image.set_colorkey((0, 0, 0) if not background_colour else [background_colour for i in range(3)])
		self.characters = {}
		current_width, character_count = 0, 0
		character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
		for x in range(self.font_image.get_width()):
			colour = self.font_image.get_at((x, 0))
			if colour[:-1] == (border_colour, border_colour, border_colour): #IF THE TEXT COLOR IS (127, 127, 127), CHANGE BORDER_COLOR
				character_image = clip_surface(self.font_image, (x - current_width, 0), (current_width, self.font_image.get_height())) #CLIP EVERY CHARACTER OUT OF THE FONT IMAGE
				self.characters[character_order[character_count]] = character_image
				character_count += 1
				current_width = 0
			else:
				current_width += 1
		self.space_width, self.character_height = self.characters['A'].get_size()
	#__INIT__

	#GET_SIZE
	def get_size(self, text):
		'''Get the size that that a rendered string would use
		It will return the width and height

		Returns: Tuple'''
		if type(text) is not str:
			raise TypeError(f'{text} is not a string')
		width, height = 0, 0
		for character in text:
			if character not in ('\n', ' ') and character in self.characters:
				width += self.characters[character].get_width() + 1 #+ 1 FOR SPACING
			elif character == ' ' or character not in ['\n']:
				width += self.space_width + 1 #+ 1 FOR SPACING
			else:
				width = 0
				height += self.character_height + 1 #+ 1 FOR SPACING
		return width, height
	#GET_SIZE

	#RENDER
	def render(self, surface, text, location):
		'''Render a string on a surface at a location'''
		if type(text) is not str:
			raise TypeError(f'{text} is not a string')
		x_offset, y_offset = 0, 0
		for character in text:
			if character not in ('\n', ' ') and character in self.characters:
				surface.blit(self.characters[character], (location[0] + x_offset, location[1] + y_offset))
				x_offset += self.characters[character].get_width() + 1 #+ 1 FOR SPACING
			elif character == ' ' or character not in ['\n']:
				x_offset += self.space_width + 1 #+ 1 FOR SPACING
			else:
				x_offset = 0
				y_offset += self.character_height + 1 #+ 1 FOR SPACING
	#RENDER
#FONT

#TEXTBUTTON
class TextButton:
	'''A string of text that is also a button
	The collide function is to collide with the mouse and clicks
	It also needs a font size, it has to be either 'small' or 'large'

	Attributes:

	rect

	size

	test_font

	text'''
	#__INIT__
	def __init__(self, text, location, font_size):
		if font_size != 'small' and font_size != 'large':
			raise ValueError(f'{font_size} is not \'small\' or \'large\'')
		if type(text) is not str:
			raise TypeError(f'{text} is not a string')
		self.text = text
		self.test_font = Font(load_image(f'{path}/Font/{font_size.title()}_Font.png'))
		self.size = self.test_font.get_size(text)
		self.rect = pygame.Rect(location, (self.size[0] - 1, self.size[1] + self.test_font.character_height)) #- 1 FOR THE EXTRA SPACING
	#__INIT__

	#SET_TEXT
	def set_text(self, text):
		'''Sets a new string as the text
		All the variables will be updated, so the functions can be used the same'''
		if type(text) is not str:
			raise TypeError(f'{text} is not a string')
		self.text = text
		self.size = self.test_font.get_size(text)
		self.rect = pygame.Rect(self.rect.topleft, (self.size[0] - 1, self.size[1] + self.test_font.character_height))
	#SET_TEXT

	#COLLIDE
	def collide(self, click):
		'''This will check collision with the mouse location and also if click is True with it
		The first value returns True if the mouse has collided with the button, the second one is if the mouse clicked on it

		Returns: Tuple'''
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			if click:
				return True, True
			return True, False
		return False, False
	#COLLIDE

	#RENDER
	def render(self, surface, font):
		'''Renders the text from the button'''
		if not isinstance(font, Font):
			raise TypeError(f'{font} is not a Font object')
		font.render(surface, self.text, self.rect.topleft)
	#RENDER
#TEXTBUTTON