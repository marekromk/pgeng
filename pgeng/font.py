'Classes and functions for creating fonts and text buttons'
import pygame
from pathlib import Path
from .colour import palette_swap
from .core import clip_surface, load_image

__all__ = ['create_font', 'TextButton']
path = Path(__file__).resolve().parent

def create_font(colour):
	'''A function to create small and large Font objects
	colour will be the colour of the text
	The first value in the returned tuple is the small font and the second value is the large font

	For help on a Font object, do help(pgeng.font.Font)

	Returns: tuple'''
	if tuple(colour[:3]) == (0, 0, 0):
		small_font_image = palette_swap(load_image(path.joinpath('font/small.png')), {(255, 0, 0): colour[:3], tuple(colour[:3]): (255, 255, 255)})
		large_font_image = palette_swap(load_image(path.joinpath('font/large.png')), {(255, 0, 0): colour[:3], tuple(colour[:3]): (255, 255, 255)})
		return Font(small_font_image, background_colour=255), Font(large_font_image, background_colour=255)
	if tuple(colour[:3]) == (127, 127, 127):
		small_font_image = palette_swap(load_image(path.joinpath('font/small.png')), {(255, 0, 0): colour[:3], tuple(colour[:3]): (128, 128, 128)})
		large_font_image = palette_swap(load_image(path.joinpath('font/large.png')), {(255, 0, 0): colour[:3], tuple(colour[:3]): (128, 128, 128)})
		return Font(small_font_image, 128), Font(large_font_image, 128)
	small_font_image = palette_swap(load_image(path.joinpath('font/small.png')), {(255, 0, 0): colour[:3]})
	large_font_image = palette_swap(load_image(path.joinpath('font/large.png')), {(255, 0, 0): colour[:3]})
	return Font(small_font_image), Font(large_font_image)

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
	def __init__(self, font_image, border_colour=127, background_colour=0):
		'Initialising a font object'
		self.font_image = font_image
		self.font_image.set_colorkey((0, 0, 0) if not background_colour else [background_colour for i in range(3)])
		self.characters = {}
		current_width, character_count = 0, 0
		character_order = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
		for x in range(self.font_image.get_width()):
			colour = self.font_image.get_at((x, 0))
			if colour[:3] == (border_colour, border_colour, border_colour): #IF THE TEXT COLOR IS (127, 127, 127), CHANGE BORDER_COLOR
				character_image = clip_surface(self.font_image, (x - current_width, 0), (current_width, self.font_image.get_height())) #CLIP EVERY CHARACTER OUT OF THE FONT IMAGE
				self.characters[character_order[character_count]] = character_image
				character_count += 1
				current_width = 0
			else:
				current_width += 1
		self.space_width, self.character_height = self.characters['A'].get_size()

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return 'pgeng.Font'

	def get_size(self, text):
		'''Get the size that that a rendered string would use
		It will return the width and height

		Returns: tuple'''
		if type(text) is not str:
			raise TypeError('text has to be a string')
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

	def render(self, surface, text, location, scroll=pygame.Vector2()):
		'Render a string on a surface at a location'
		if type(text) is not str:
			raise TypeError('text has to be a string')
		x_offset, y_offset = 0, 0
		for character in text:
			if character not in ('\n', ' ') and character in self.characters:
				surface.blit(self.characters[character], (location[0] + x_offset - scroll[0], location[1] + y_offset - scroll[1]))
				x_offset += self.characters[character].get_width() + 1 #+ 1 FOR SPACING
			elif character == ' ' or character not in ['\n']:
				x_offset += self.space_width + 1 #+ 1 FOR SPACING
			else:
				x_offset = 0
				y_offset += self.character_height + 1 #+ 1 FOR SPACING

class TextButton:
	'''A string of text that is also a button
	The collide function is to collide with the mouse and clicks
	It also needs a font size, it has to be either 'small' or 'large'
	Use the location variable instead of the rect values

	Attributes:

	location

	rect

	size

	test_font

	text'''
	def __init__(self, text, location, font_size):
		'Initialising a TextButton object'
		if font_size != 'small' and font_size != 'large':
			raise ValueError('font_size is not \'small\' or \'large\'')
		if type(text) is not str:
			raise TypeError('text is not a string')
		self.text = text
		self.location = pygame.Vector2(location)
		self.test_font = Font(load_image(path.joinpath(f'font/{font_size}.png')))
		self.size = self.test_font.get_size(text)

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.TextButton{tuple(self.location), self.text}'

	@property
	def rect(self):
		'''Returns the pygame.Rect object of the TextButton

		Returns: pygame.Rect'''
		self.location = pygame.Vector2(self.location)
		return pygame.Rect(self.location, (self.size[0] - 1, self.size[1] + self.test_font.character_height)) #- 1 FOR THE EXTRA SPACING

	def set_text(self, text):
		'''Sets a new string as the text
		All the variables will be updated, so the functions can be used the same'''
		if type(text) is not str:
			raise TypeError('text is not a string')
		self.text = text
		self.size = self.test_font.get_size(text)

	def collide(self, click, check_location=None):
		'''This will check collision with the mouse location and also if click is True with it
		A custom location can be set with location if pygame.mouse.get_pos() is not wished to be used
		It returns a dictionary like this:
			{'collided': False, 'clicked': False}

		Returns: dict'''
		collides = {'collided': False, 'clicked': False}
		check_location = pygame.mouse.get_pos() if check_location is None else check_location
		if self.rect.collidepoint(check_location):
			collides['collided'] = True
			if click:
				collides['clicked'] = True
		return collides

	def render(self, surface, font, scroll=pygame.Vector2()):
		'Renders the text from the button'
		if not isinstance(font, Font):
			raise TypeError('font is not a Font object')
		font.render(surface, self.text, self.location, scroll)