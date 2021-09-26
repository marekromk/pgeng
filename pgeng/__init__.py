'''Useful functions and classes for PyGame'''
#VARIABLES
__version__ = '1.2.2'
failed_imports = []
#VARIABLES

#ANIMATIONS
try:
	from .Animations import *
except ImportError as e:
	failed_imports.append(e.name)
#ANIMATIONS

#COLOUR
try:
	from .Colour import *
except ImportError as e:
	failed_imports.append(e.name)
#COLOUR

#CORE
try:
	from .Core import *
except ImportError as e:
	failed_imports.append(e.name)
#CORE

#ENTITY
try:
	from .Entity import Entity
except ImportError as e:
	failed_imports.append(e.name)
#ENTITY

#FONT
try:
	from .Font import *
except ImportError as e:
	failed_imports.append(e.name)
#FONT

#SCREEN
try:
	from .Screen import Screen
except ImportError as e:
	failed_imports.append(e.name)
#SCREEN

#TILE
try:
	from .Tile import *
except ImportError as e:
	failed_imports.append(e.name)
#TILE

#SOUNDS
try:
	from .Sounds import Sounds
except ImportError as e:
	failed_imports.append(e.name)
#SOUNDS

#VFX
try:
	from .VFX import *
except ImportError as e:
	failed_imports.append(e.name)
#VFX

#MESSAGES
print('''\nDo help(pgeng.<Function>) to get the documentation of the function (or possibly class)
Or do help(pgeng.<Package Content>) to get the documentation of the functions or classes in a file\n''')
print(f'Failed to import {", ".join([failed_import.split(".")[1] for failed_import in failed_imports])} from pgeng') if failed_imports else None
del failed_imports
#MESSAGES