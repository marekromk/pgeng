'''A class to make the dipslay/screen
It also has functions to enter and exit fullscreen'''
#IMPORTS
import pygame
from pygame._sdl2.video import Window
#IMPORTS

#SCREEN
class Screen:
	'''A class for the display/screen
	It can also set the display fullscreen on all platforms
	The default flag is pygame.SCALED
	Use GetDisplay to get the display from the class

	For more information about the parameters, go to https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode'''
	#__INIT__
	def __init__(self, Size, Flags=pygame.SCALED, Depth=0, Display=0, VSync=1, Fullscreen=False):
		'''Initialising the class, it should only be done once'''
		self.FullscreenSize = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.Size = Size
		self.Flags = Flags
		self.Depth = Depth
		self.Display = Display
		self.VSync = VSync
		self.Fullscreen = Fullscreen
		if Fullscreen:
			self.ToggleFullscreen(ManualSet=Fullscreen)
		else:
			self.PygameDisplay = pygame.display.set_mode(Size, Flags, Depth, Display, VSync)
		self.Window = Window.from_display_module()
	#__INIT__

	#TOGGLEFULLSCREEN
	def ToggleFullscreen(self, ManualSet=None):
		'''Toggle the display to fullscreen or from fullscreen
		ManualSet can be used if you don't want to toggle it, but set it to fullscreen or exit fullscreen manually
		Then ManualSet has to be True (set fullscreen) or False (exit Fullscreen)

		Returns: pygame.Surface'''
		self.Fullscreen = not self.Fullscreen
		if type(ManualSet) == bool:
			self.Fullscreen = ManualSet
		if self.Fullscreen:
			self.PygameDisplay = pygame.display.set_mode(self.Size, pygame.SCALED | pygame.NOFRAME | pygame.FULLSCREEN, self.Depth, self.Display, self.VSync)
		else:
			pygame.display.toggle_fullscreen()
			self.PygameDisplay = pygame.display.set_mode(self.Size, self.Flags, self.Depth, self.Display, self.VSync)
			self.Window = Window.from_display_module()
			self.Window.position = (self.FullscreenSize[i] / 2 - self.Window.size[i] / 2 for i in range(2))
		return self.PygameDisplay
	#TOGGLEFULLSCREEN

	#SCREENSHOT
	def ScreenShot(self, Alpha=None):
		'''Making a screenshot of the pygame display
		Only works if this class is used as the main display/screen

		Return: pygame.Surface'''
		ScreenShot = self.PygameDisplay.copy()
		ScreenShot.set_alpha(Alpha)
		return ScreenShot
	#SCREENSHOT

	#GETDISPLAY
	def GetDisplay(self):
		'''Used to return the display/screen

		Return: pygame.Surface'''
		return self.PygameDisplay
	#GETDISPLAY
#SCREEN