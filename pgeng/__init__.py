'Useful functions and classes for pygame'
__version__ = '1.7'
_failed_imports = []

try:
	from .collision import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .vfx import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .animations import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .colour import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .core import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .entity import Entity
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .font import *
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .screen import Screen
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .sounds import Sounds
except ImportError as e:
	_failed_imports.append(e.name)

try:
	from .tile import *
except ImportError as e:
	_failed_imports.append(e.name)

print('''\nRun help(pgeng.<Function>) to get the documentation of the function (or possibly class)
Or run help(pgeng.<Package Content>) to get the documentation of the functions or classes in a file\n''')
print(f'Failed to import: {", ".join([failed_import.split(".")[-1] + " from " + ".".join(failed_import.split(".")[:-1]) if "pgeng" in failed_import else failed_import for failed_import in set(_failed_imports)])}') if _failed_imports else None
del _failed_imports