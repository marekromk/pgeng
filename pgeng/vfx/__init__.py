'Visual effects classes and functions for pgeng'
#import functions with underscore so it doesn't get imported by pgeng itself
from .. import _failed_imports

__all__ = ['circle_lighting', 'Particle', 'ShockWave']

try:
    from .core import circle_lighting
except ImportError as e:
    _failed_imports.append(e.name)

try:
    from .flame import *
    __all__ += flame.__all__ #if the __all__ variable ever changes, it will too here
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
    __all__ += spark.__all__ #if the __all__ variable ever changes, it will too here
except ImportError as e:
    _failed_imports.append(e.name)