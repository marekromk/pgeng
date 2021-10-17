'''Useful functions and classes for PyGame'''
#VARIABLES
__version__ = '1.3.1'
failed_imports = []
#VARIABLES

#VFX
try:
	from .vfx import *
except ImportError as e:
	failed_imports.append(e.name)
#VFX

#ANIMATIONS
try:
	from .animations import *
except ImportError as e:
	failed_imports.append(e.name)
#ANIMATIONS

#COLOUR
try:
	from .colour import *
except ImportError as e:
	failed_imports.append(e.name)
#COLOUR

#CORE
try:
	from .core import *
except ImportError as e:
	failed_imports.append(e.name)
#CORE

#ENTITY
try:
	from .entity import Entity
except ImportError as e:
	failed_imports.append(e.name)
#ENTITY

#FONT
try:
	from .font import *
except ImportError as e:
	failed_imports.append(e.name)
#FONT

#SCREEN
try:
	from .screen import Screen
except ImportError as e:
	failed_imports.append(e.name)
#SCREEN

#SOUNDS
try:
	from .sounds import Sounds
except ImportError as e:
	failed_imports.append(e.name)
#SOUNDS

#TILE
try:
	from .tile import *
except ImportError as e:
	failed_imports.append(e.name)
#TILE

#MESSAGES
print('''\nDo help(pgeng.<Function>) to get the documentation of the function (or possibly class)
Or do help(pgeng.<Package Content>) to get the documentation of the functions or classes in a file\n''')
print(f'Failed to import: {", ".join([failed_import.split(".")[-1] + " from " + ".".join(failed_import.split(".")[:-1]) for failed_import in failed_imports])}') if failed_imports else None
del failed_imports
#MESSAGES