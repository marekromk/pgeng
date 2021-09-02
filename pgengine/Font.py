'''A classes and functions for creating fonts and text buttons '''
#IMPORTS
import pygame
from .Core import ClipSurface, LoadImage
from .Colour import PaletteSwap
#IMPORTS

#VARIALBES
__all__ = ['CreateFont', 'TextButton']
#VARIABLES

#PATH
from pathlib import Path
Path = Path( __file__ ).parent.resolve()
#PATH

#CREATEFONT
def CreateFont(Colour):
	'''A function to create a large and small Font object
	Colour will be the colour of the text
	First value in the tuple is the SmallFont and the second value is the LargeFont

	Returns: Tuple'''
	SmallFontImage = PaletteSwap(LoadImage(f'{Path}/Font/SmallFont.png'), {(255, 0, 0): Colour})
	LargeFontImage = PaletteSwap(LoadImage(f'{Path}/Font/LargeFont.png'), {(255, 0, 0): Colour})
	return Font(SmallFontImage), Font(LargeFontImage)
#CREATEFONT

#FONT
class Font:
	'''A class to create a pixel art font
	It will get all the letters out of the image and render them'''
	#__INIT__
	def __init__(self, FontImage, BorderColour=127):
		'''Initialising a font object'''
		self.FontImage = FontImage
		self.TextXOffset = 0 #TO GET WIDTH OF TEXT
		self.Texts = {}
		self.Characters = {}
		CurrentWidth = 0
		CharacterCount = 0
		CharacterOrder = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','.','-',',',':','+','\'','!','?','0','1','2','3','4','5','6','7','8','9','(',')','/','_','=','\\','[',']','*','"','<','>',';']
		for X in range(self.FontImage.get_width()):
			Colour = self.FontImage.get_at((X, 0))
			if Colour[0] == BorderColour: #IF THE TEXT COLOR[0] = 127, CHANGE BORDERCOLOR
				CharacterImage = ClipSurface(self.FontImage, X - CurrentWidth, 0, CurrentWidth, self.FontImage.get_height()) #CLIP EVERY CHARACTER OUT OF THE FONT IMAGE
				self.Characters[CharacterOrder[CharacterCount]] = CharacterImage
				CharacterCount += 1
				CurrentWidth = 0
			else:
				CurrentWidth += 1
		self.SpaceWidth = self.Characters['A'].get_width()
	#__INIT__

	#RENDERTEXT
	def RenderText(self, Surface, Text, Location):
		'''Render a string on a surface at a location
		Print self.TextXOffset to get the width of the text'''
		self.TextXOffset = 0
		for Character in Text:
			if Character != ' ':
				Surface.blit(self.Characters[Character], (Location[0] + self.TextXOffset, Location[1]))
				self.TextXOffset += self.Characters[Character].get_width() + 1 #+ 1 FOR SPACING
			else:
				self.TextXOffset += self.SpaceWidth + 1 #+ 1 FOR SPACING
	#RENDERTEXT
#FONT

#TEXTBUTTON
class TextButton:
	'''A string of text that is also a button
	The collide function is to collide with the mouse and clicks
	It also needs a font size, it has to be either 'Small'  or 'Large\''''
	#__INIT__
	def __init__(self, Text, Location, FontSize):
		if FontSize != 'Small' and FontSize != 'Large':
			raise ValueError(f'{FontSize} is not \'Small\' or \'Large\'')
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