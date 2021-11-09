'Object classes with collision functions'
from .. import failed_imports as _failed_imports #UNDERSCORE SO IT IS NOT VISIBLE AS A VARIABLE

try:
	from .circle import Circle
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .polygon import Polygon
except ImportError as e:
	_failed_imports.append(e.name)