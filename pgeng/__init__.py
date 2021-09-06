'''Useful functions and classes for PyGame'''
#COLOR
try:
	from .Colour import *
except ImportError:
	pass
#COLOR

#CORE
try:
	from .Core import *
except ImportError:
	pass
#CORE

#ENTITY
try:
	from .Entity import Entity
except ImportError:
	pass
#ENTITY

#FONT
try:
	from .Font import *
except ImportError:
	pass
#FONT

#SCREEN
try:
	from .Screen import Screen
except ImportError:
	pass
#SCREEN

#TILE
try:
	from .Tile import *
except ImportError:
	pass
#TILE

#SOUNDS
try:
	from .Sounds import Sounds
except ImportError:
	pass
#SOUNDS

#VISUALEFFECTS
try:
	from .VisualEffects import *
except ImportError:
	pass
#VISUALEFFECTS

#MESSAGE
print('''\nDo help(pgeng.<Function>) to get the documentation of the function (or possibly class)
Or do help(pgeng.<Package Content>) to get the documentation of the functions or classes in a file\n''')
#MESSAGE