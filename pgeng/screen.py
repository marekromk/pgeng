'''A class to make the dipslay/screen
It also has functions to enter and exit fullscreen'''
import pygame
from pygame._sdl2.video import Window

class Screen:
	'''A class for the display
	It can also toggle the display fullscreen on all platforms
	The default flag is pygame.SCALED
	Use get_display to get the display from the class

	For more information about the parameters, go to https://www.pygame.org/docs/ref/display.html#pygame.display.set_mode

	Attributes:

	depth

	display

	flags

	fullscreen_size

	pygame_display

	size

	vsync

	window'''
	def __init__(self, size, flags=pygame.SCALED, depth=0, display=0, vsync=1, fullscreen=False):
		'Initialising the class, it should only be done once'
		self.fullscreen_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
		self.size = size
		self.flags = flags
		self.depth = depth
		self.display = display
		self.vsync = vsync
		self.fullscreen = fullscreen
		if fullscreen:
			self.toggle_fullscreen(manual=fullscreen)
		else:
			self.pygame_display = pygame.display.set_mode(size, flags, depth, display, vsync)
		self.window = Window.from_display_module()

	def __repr__(self):
		'''Returns a string representation of the object

		Returns: str'''
		return f'pgeng.Screen({tuple(self.size)}, fullscreen={self.fullscreen})'

	def toggle_fullscreen(self, manual=None):
		'''Toggle the display to fullscreen or from fullscreen
		manual can be used if you don't want to toggle it, but set it to fullscreen or exit fullscreen manually
		Than manual has to be True (enter fullscreen) or False (exit Fullscreen)

		Returns: pygame.Surface'''
		self.fullscreen = not self.fullscreen
		if manual is not None:
			self.fullscreen = bool(manual)
		if self.fullscreen:
			self.pygame_display = pygame.display.set_mode(self.size, pygame.SCALED | pygame.NOFRAME | pygame.FULLSCREEN, self.depth, self.display, self.vsync)
		else:
			pygame.display.toggle_fullscreen()
			self.pygame_display = pygame.display.set_mode(self.size, self.flags, self.depth, self.display, self.vsync)
			self.center()
		return self.pygame_display

	def center(self):
		'''Centers the window and returns the position

		Returns: tuple'''
		self.window.position = [(self.fullscreen_size[i] - self.window.size[i]) * 0.5 for i in range(2)]
		return self.window.position

	def get_display(self):
		'''Used to return the pygame display

		Returns: pygame.Surface'''
		return self.pygame_display