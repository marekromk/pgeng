'''Useful functions and classes for PyGame'''
#VARIABLES
FailedImports = []
#VARIABLES

#COLOR
try:
	from .Colour import *
except ImportError as e:
	FailedImports.append(e.name)
#COLOR

#CORE
try:
	from .Core import *
except ImportError as e:
	FailedImports.append(e.name)
#CORE

#ENTITY
try:
	from .Entity import Entity
except ImportError as e:
	FailedImports.append(e.name)
#ENTITY

#FONT
try:
	from .Font import *
except ImportError as e:
	FailedImports.append(e.name)
#FONT

#SCREEN
try:
	from .Screen import Screen
except ImportError as e:
	FailedImports.append(e.name)
#SCREEN

#TILE
try:
	from .Tile import *
except ImportError as e:
	FailedImports.append(e.name)
#TILE

#SOUNDS
try:
	from .Sounds import Sounds
except ImportError as e:
	FailedImports.append(e.name)
#SOUNDS

#VISUALEFFECTS
try:
	from .VisualEffects import *
except ImportError as e:
	FailedImports.append(e.name)
#VISUALEFFECTS

#MESSAGES
print('''\nDo help(pgeng.<Function>) to get the documentation of the function (or possibly class)
Or do help(pgeng.<Package Content>) to get the documentation of the functions or classes in a file\n''')
print(f'Failed to import {", ".join([Import.split(".")[1] for Import in FailedImports])} from pgeng') if FailedImports else None
del FailedImports
#MESSAGES