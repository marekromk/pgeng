'''A classes and functions for creating fonts and text buttons'''
#IMPORTS
import pygame
from pathlib import Path
from .Core import ClipSurface, LoadImage
from .Colour import PaletteSwap
#IMPORTS

#VARIALBES
__all__ = ['CreateFont', 'TextButton']
Path = Path( __file__ ).parent.resolve()
#VARIABLES

#CREATEFONT
def CreateFont(Colour):
	'''A function to create a large and small Font object
	Colour will be the colour of the text
	First value in the returned tuple is the SmallFont and the second value is the LargeFont

	Returns: Tuple'''
	if tuple(Colour) == (0, 0, 0):
		SmallFontImage = PaletteSwap(LoadImage(f'{Path}/Font/SmallFont.png'), {(255, 0, 0): Colour, tuple(Colour): (255, 255, 255)})
		LargeFontImage = PaletteSwap(LoadImage(f'{Path}/Font/LargeFont.png'), {(255, 0, 0): Colour, tuple(Colour): (255, 255, 255)})
		return Font(SmallFontImage, BackGroundColour=255), Font(LargeFontImage, BackGroundColour=255)
	if tuple(Colour) == (127, 127, 127):
		SmallFontImage = PaletteSwap(LoadImage(f'{Path}/Font/SmallFont.png'), {(255, 0, 0): Colour, tuple(Colour): (128, 128, 128)})
		LargeFontImage = PaletteSwap(LoadImage(f'{Path}/Font/LargeFont.png'), {(255, 0, 0): Colour, tuple(Colour): (128, 128, 128)})
		return Font(SmallFontImage, 128), Font(LargeFontImage, 128)
	SmallFontImage = PaletteSwap(LoadImage(f'{Path}/Font/SmallFont.png'), {(255, 0, 0): Colour})
	LargeFontImage = PaletteSwap(LoadImage(f'{Path}/Font/LargeFont.png'), {(255, 0, 0): Colour})
	return Font(SmallFontImage), Font(LargeFontImage)
#CREATEFONT

#FONT
class Font:
	'''A class to create a pixel art font
	It will get all the letters out of the image and render them
	The border between letters is usually (127, 127, 127) and the background is usually (0, 0, 0) change them if it is necessary

	Attributes:

	Characters

	FontImage

	SpaceWidth

	Width'''
	#__INIT__
	def __init__(self, FontImage, BorderColour=127, BackGroundColour=0):
		'''Initialising a font object'''
		self.FontImage = FontImage
		self.Width = 0
		self.Characters = {}
		CurrentWidth = 0
		CharacterCount = 0
		CharacterOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
		for X in range(self.FontImage.get_width()):
			Colour = self.FontImage.get_at((X, 0))
			if Colour[:-1] == (BorderColour, BorderColour, BorderColour): #IF THE TEXT COLOR[0] = 127, CHANGE BORDERCOLOR
				CharacterImage = ClipSurface(self.FontImage, (X - CurrentWidth, 0), (CurrentWidth, self.FontImage.get_height())) #CLIP EVERY CHARACTER OUT OF THE FONT IMAGE
				CharacterImage.set_colorkey((0, 0, 0) if not BackGroundColour else [BackGroundColour for i in range(3)])
				self.Characters[CharacterOrder[CharacterCount]] = CharacterImage
				CharacterCount += 1
				CurrentWidth = 0
			else:
				CurrentWidth += 1
		self.SpaceWidth = self.Characters['A'].get_width()
	#__INIT__

	#RENDER
	def Render(self, Surface, Text, Location):
		'''Render a string on a surface at a location'''
		if type(Text) is not str:
			raise TypeError(f'{Text} is not a string')
		self.Width = 0
		for Character in Text:
			if Character != ' ':
				Surface.blit(self.Characters[Character], (Location[0] + self.Width, Location[1]))
				self.Width += self.Characters[Character].get_width() + 1 #+ 1 FOR SPACING
			else:
				self.Width += self.SpaceWidth + 1 #+ 1 FOR SPACING
	#RENDER
#FONT

#TEXTBUTTON
class TextButton:
	'''A string of text that is also a button
	The collide function is to collide with the mouse and clicks
	It also needs a font size, it has to be either 'Small'  or 'Large\

	Attributes:

	rect

	TestFont

	Text

	Width'''
	#__INIT__
	def __init__(self, Text, Location, FontSize):
		if FontSize != 'Small' and FontSize != 'Large':
			raise ValueError(f'{FontSize} is not \'Small\' or \'Large\'')
		if type(Text) is not str:
			raise TypeError(f'{Text} is not a string')
		self.Text = Text
		self.Width = 0
		self.TestFont = Font(LoadImage(f'{Path}/Font/{FontSize}Font.png'))
		for Character in Text:
			if Character != ' ':
				self.Width += self.TestFont.Characters[Character].get_width() + 1 #+ 1 FOR SPACING
			else:
				self.Width += self.TestFont.SpaceWidth + 1 #+ 1 FOR SPACING
		self.rect = pygame.Rect(Location, (self.Width, self.TestFont.FontImage.get_height()))
	#__INIT__

	#SETTEXT
	def SetText(self, Text):
		'''Sets a new string as the text
		All the variables will be updated, so the functions can be used the same'''
		self.Text = Text
		self.Width = 0
		for Character in Text:
			if Character != ' ':
				self.Width += self.TestFont.Characters[Character].get_width() + 1 #+ 1 FOR SPACING
			else:
				self.Width += self.TestFont.SpaceWidth + 1 #+ 1 FOR SPACING
		Location = self.rect.topleft
		self.rect = pygame.Rect(Location, (self.Width, self.TestFont.FontImage.get_height()))
	#SETTEXT

	#COLLIDE
	def Collide(self, Click):
		'''This will check collision with the mouse location and also if Click is True
		The first value returns True if it has collided with the button, the second one is if the mouse clicked on it

		Returns: Tuple'''
		if self.rect.collidepoint(pygame.mouse.get_pos()):
			if Click:
				return True, True
			return True, False
		return False, False
	#COLLIDE

	#RENDER
	def Render(self, Surface, Font):
		'''Renders the text from the button'''
		Font.RenderText(Surface, self.Text, self.rect.topleft)
	#RENDER
#TEXTBUTTON