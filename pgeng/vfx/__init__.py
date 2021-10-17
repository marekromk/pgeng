'''Visual effects classes and functions for pgeng'''
#IMPORTS
from .. import failed_imports as _failed_imports #UNDERSCORE SO IT IS NOT VISIBLE AS A VARIABLE
#IMPORTS

#CORE
try:
    from .core import circle_lighting
except ImportError as e:
    _failed_imports.append(e.name)
#CORE

#FLAME
try:
    from .flame import *
except ImportError as e:
    _failed_imports.append(e.name)
#FLAME

#PARTICLE
try:
    from .particle import Particle
except ImportError as e:
    _failed_imports.append(e.name)
#PARTICLE

#SHOCKWAVE
try:
    from .shockwave import ShockWave
except ImportError as e:
    _failed_imports.append(e.name)
#SHOCKWAVE

#SPARK
try:
    from .spark import Spark
except ImportError as e:
    _failed_imports.append(e.name)
#SPARK