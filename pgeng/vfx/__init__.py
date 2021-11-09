'Visual effects classes and functions for pgeng'
from .. import failed_imports as _failed_imports #UNDERSCORE SO IT IS NOT VISIBLE AS A VARIABLE

try:
    from .core import circle_lighting
except ImportError as e:
    _failed_imports.append(e.name)

try:
    from .flame import *
except ImportError as e:
    _failed_imports.append(e.name)

try:
    from .particle import Particle
except ImportError as e:
    _failed_imports.append(e.name)

try:
    from .shockwave import ShockWave
except ImportError as e:
    _failed_imports.append(e.name)

try:
    from .spark import *
except ImportError as e:
    _failed_imports.append(e.name)