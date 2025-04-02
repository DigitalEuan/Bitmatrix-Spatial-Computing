"""
BitMatrix Spatial Computing (BSC) - A framework for multidimensional data representation and processing.

This package provides a complete implementation of BitMatrix Spatial Computing,
which redefines traditional computational paradigms by introducing multidimensional
data representation and processing.
"""

from .matrix import BitField3D, BitField4D
from .operations import (
    mapTo3D, mapTo4D, extractLinear,
    rotate3D, translate3D, scale3D, mirror3D
)
from .kta import (
    applyKineticTransform, superposition, entangle
)
from .patterns import (
    findPattern, matchPattern, generatePattern
)
from .visualization import (
    visualize3D, visualize4D, animateTransform,
    visualize3D_compact, visualize4D_compact, visualize_properties
)
from .exceptions import (
    DimensionError, PatternError, KTAError
)

__version__ = "1.0.0"
__author__ = "Euan Craig (DigitalEuan.com)"
__all__ = [
    # Core classes
    'BitField3D', 'BitField4D',
    
    # Spatial operations
    'mapTo3D', 'mapTo4D', 'extractLinear',
    'rotate3D', 'translate3D', 'scale3D', 'mirror3D',
    
    # KTA operations
    'applyKineticTransform', 'superposition', 'entangle',
    
    # Pattern operations
    'findPattern', 'matchPattern', 'generatePattern',
    
    # Visualization functions
    'visualize3D', 'visualize4D', 'animateTransform',
    'visualize3D_compact', 'visualize4D_compact', 'visualize_properties',
    
    # Exceptions
    'DimensionError', 'PatternError', 'KTAError'
]
