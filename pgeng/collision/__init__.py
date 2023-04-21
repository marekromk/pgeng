'Object classes with collision functions'
#import functions with underscore so it doesn't get imported by pgeng itself
from .. import _failed_imports

__all__ = ['Circle', 'Polygon']

try:
	from .circle import Circle
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .polygon import Polygon
except ImportError as e:
	_failed_imports.append(e.name)