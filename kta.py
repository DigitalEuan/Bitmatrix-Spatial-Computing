"""
5D Kinetic Transform Arithmetic (KTA) operations for BitMatrix Spatial Computing.

This module provides functions for quantum-inspired operations that extend
the mathematical framework of BitMatrix beyond conventional computational approaches.
"""

import numpy as np
import random
from .exceptions import KTAError
from .matrix import BitField3D, BitField4D

def applyKineticTransform(bitfield, transform_type):
    """
    Applies a kinetic transform to a bitfield.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to transform
        transform_type (str): Type of transform ('wave', 'fractal', 'recursive')
        
    Returns:
        BitField3D or BitField4D: Transformed bitfield
        
    Raises:
        KTAError: If transform_type is invalid
        TypeError: If bitfield is not a BitField3D or BitField4D instance
    """
    if not isinstance(bitfield, (BitField3D, BitField4D)):
        raise TypeError("Bitfield must be a BitField3D or BitField4D instance")
    
    # Create a copy of the bitfield
    result = bitfield.copy()
    
    if transform_type == 'wave':
        # Apply wave transform (sinusoidal pattern)
        _apply_wave_transform(result)
    elif transform_type == 'fractal':
        # Apply fractal transform (self-similar pattern)
        _apply_fractal_transform(result)
    elif transform_type == 'recursive':
        # Apply recursive transform (nested pattern)
        _apply_recursive_transform(result)
    else:
        raise KTAError(f"Invalid transform type: {transform_type}")
    
    return result

def _apply_wave_transform(bitfield):
    """
    Applies a wave transform to a bitfield (internal helper).
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to transform
    """
    dimensions = bitfield.getDimensions()
    
    if isinstance(bitfield, BitField3D):
        x_dim, y_dim, z_dim = dimensions
        
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Calculate wave function
                    wave_val = np.sin(x/2) * np.cos(y/2) * np.sin(z/2)
                    
                    # Apply transform based on wave value
                    if wave_val > 0:
                        # Flip bit if wave value is positive
                        current_val = bitfield.getBit(x, y, z)
                        bitfield.setBit(x, y, z, 1 - current_val)
    
    elif isinstance(bitfield, BitField4D):
        x_dim, y_dim, z_dim, t_dim = dimensions
        
        for t in range(t_dim):
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        # Calculate wave function with temporal component
                        wave_val = np.sin(x/2) * np.cos(y/2) * np.sin(z/2) * np.cos(t/2)
                        
                        # Apply transform based on wave value
                        if wave_val > 0:
                            # Flip bit if wave value is positive
                            current_val = bitfield.getBit(x, y, z, t)
                            bitfield.setBit(x, y, z, t, 1 - current_val)

def _apply_fractal_transform(bitfield):
    """
    Applies a fractal transform to a bitfield (internal helper).
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to transform
    """
    dimensions = bitfield.getDimensions()
    
    if isinstance(bitfield, BitField3D):
        x_dim, y_dim, z_dim = dimensions
        
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Simple fractal pattern based on coordinates
                    if (x & y) == (y & z):  # Bitwise AND creates fractal-like pattern
                        current_val = bitfield.getBit(x, y, z)
                        bitfield.setBit(x, y, z, 1 - current_val)
    
    elif isinstance(bitfield, BitField4D):
        x_dim, y_dim, z_dim, t_dim = dimensions
        
        for t in range(t_dim):
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        # Extended fractal pattern with temporal dimension
                        if (x & y) == (z & t):  # Bitwise AND creates fractal-like pattern
                            current_val = bitfield.getBit(x, y, z, t)
                            bitfield.setBit(x, y, z, t, 1 - current_val)

def _apply_recursive_transform(bitfield):
    """
    Applies a recursive transform to a bitfield (internal helper).
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to transform
    """
    dimensions = bitfield.getDimensions()
    
    if isinstance(bitfield, BitField3D):
        x_dim, y_dim, z_dim = dimensions
        
        # Apply recursive pattern (simplified implementation)
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Recursive pattern based on coordinate sum modulo
                    if (x + y + z) % 3 == 0:
                        current_val = bitfield.getBit(x, y, z)
                        bitfield.setBit(x, y, z, 1 - current_val)
    
    elif isinstance(bitfield, BitField4D):
        x_dim, y_dim, z_dim, t_dim = dimensions
        
        # Apply recursive pattern with temporal dimension
        for t in range(t_dim):
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        # Recursive pattern based on coordinate sum modulo
                        if (x + y + z + t) % 4 == 0:
                            current_val = bitfield.getBit(x, y, z, t)
                            bitfield.setBit(x, y, z, t, 1 - current_val)

def superposition(bitfield_a, bitfield_b):
    """
    Creates a superposition of two bitfields.
    
    This function implements a virtual representation of quantum superposition,
    where each bit exists in a probabilistic state derived from both input bitfields.
    
    Args:
        bitfield_a (BitField3D or BitField4D): First bitfield
        bitfield_b (BitField3D or BitField4D): Second bitfield
        
    Returns:
        BitField3D or BitField4D: Superposition of the two bitfields
        
    Raises:
        KTAError: If bitfields have different dimensions or types
        TypeError: If bitfields are not BitField3D or BitField4D instances
    """
    # Validate bitfield types
    if not isinstance(bitfield_a, (BitField3D, BitField4D)) or not isinstance(bitfield_b, (BitField3D, BitField4D)):
        raise TypeError("Bitfields must be BitField3D or BitField4D instances")
    
    # Validate bitfield compatibility
    if type(bitfield_a) != type(bitfield_b):
        raise KTAError("Cannot create superposition of different bitfield types")
    
    # Get dimensions
    dims_a = bitfield_a.getDimensions()
    dims_b = bitfield_b.getDimensions()
    
    # Validate dimensions
    if dims_a != dims_b:
        raise KTAError("Cannot create superposition of bitfields with different dimensions")
    
    # Create result bitfield
    if isinstance(bitfield_a, BitField3D):
        x_dim, y_dim, z_dim = dims_a
        result = BitField3D(x_dim, y_dim, z_dim)
        
        # Apply superposition
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Get bit values
                    bit_a = bitfield_a.getBit(x, y, z)
                    bit_b = bitfield_b.getBit(x, y, z)
                    
                    # Calculate superposition value (probabilistic)
                    if bit_a == bit_b:
                        # If bits are the same, keep the value
                        result.setBit(x, y, z, bit_a)
                    else:
                        # If bits differ, set based on probability
                        prob = random.random()
                        result.setBit(x, y, z, 1 if prob > 0.5 else 0)
                    
                    # Set superposition property
                    result.setProperty(x, y, z, "superposition", (bit_a, bit_b))
    
    else:  # BitField4D
        x_dim, y_dim, z_dim, t_dim = dims_a
        result = BitField4D(x_dim, y_dim, z_dim, t_dim)
        
        # Apply superposition
        for t in range(t_dim):
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        # Get bit values
                        bit_a = bitfield_a.getBit(x, y, z, t)
                        bit_b = bitfield_b.getBit(x, y, z, t)
                        
                        # Calculate superposition value (probabilistic)
                        if bit_a == bit_b:
                            # If bits are the same, keep the value
                            result.setBit(x, y, z, t, bit_a)
                        else:
                            # If bits differ, set based on probability
                            prob = random.random()
                            result.setBit(x, y, z, t, 1 if prob > 0.5 else 0)
                        
                        # Set superposition property
                        result.setProperty(x, y, z, t, "superposition", (bit_a, bit_b))
    
    return result

def entangle(bitfield_a, bitfield_b):
    """
    Creates an entanglement between two bitfields.
    
    This function implements a virtual representation of quantum entanglement,
    where changes in one bitfield affect the other.
    
    Args:
        bitfield_a (BitField3D or BitField4D): First bitfield
        bitfield_b (BitField3D or BitField4D): Second bitfield
        
    Returns:
        tuple: Tuple containing (entangled_a, entangled_b)
        
    Raises:
        KTAError: If bitfields have different dimensions or types
        TypeError: If bitfields are not BitField3D or BitField4D instances
    """
    # Validate bitfield types
    if not isinstance(bitfield_a, (BitField3D, BitField4D)) or not isinstance(bitfield_b, (BitField3D, BitField4D)):
        raise TypeError("Bitfields must be BitField3D or BitField4D instances")
    
    # Validate bitfield compatibility
    if type(bitfield_a) != type(bitfield_b):
        raise KTAError("Cannot entangle different bitfield types")
    
    # Get dimensions
    dims_a = bitfield_a.getDimensions()
    dims_b = bitfield_b.getDimensions()
    
    # Validate dimensions
    if dims_a != dims_b:
        raise KTAError("Cannot entangle bitfields with different dimensions")
    
    # Create copies of the bitfields
    entangled_a = bitfield_a.copy()
    entangled_b = bitfield_b.copy()
    
    # Create entanglement mapping
    entanglement_map = {}
    
    if isinstance(bitfield_a, BitField3D):
        x_dim, y_dim, z_dim = dims_a
        
        # Create entanglement between bits
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Create entanglement key
                    key = (x, y, z)
                    
                    # Store entanglement information
                    entangled_a.setProperty(x, y, z, "entangled", True)
                    entangled_b.setProperty(x, y, z, "entangled", True)
                    
                    # Store entanglement mapping
                    entanglement_map[key] = key
    
    else:  # BitField4D
        x_dim, y_dim, z_dim, t_dim = dims_a
        
        # Create entanglement between bits
        for t in range(t_dim):
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        # Create entanglement key
                        key = (x, y, z, t)
                        
                        # Store entanglement information
                        entangled_a.setProperty(x, y, z, t, "entangled", True)
                        entangled_b.setProperty(x, y, z, t, "entangled", True)
                        
                        # Store entanglement mapping
                        entanglement_map[key] = key
    
    # Store entanglement map in both bitfields
    entangled_a.entanglement_map = entanglement_map
    entangled_b.entanglement_map = entanglement_map
    
    # Store reference to the other bitfield
    entangled_a.entangled_with = entangled_b
    entangled_b.entangled_with = entangled_a
    
    return (entangled_a, entangled_b)
