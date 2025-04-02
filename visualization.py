"""
Visualization functions for BitMatrix Spatial Computing.

This module provides functions for visualizing BitMatrix data structures
using ASCII representations for maximum compatibility and performance.
"""

from .exceptions import DimensionError
from .matrix import BitField3D, BitField4D

def visualize3D(bitfield, layer=None):
    """
    Visualizes a 3D bitfield using ASCII representation.
    
    Args:
        bitfield (BitField3D): Bitfield to visualize
        layer (int, optional): Specific z-layer to visualize. If None, visualizes all layers.
        
    Returns:
        str: ASCII visualization of the bitfield
        
    Raises:
        TypeError: If bitfield is not a BitField3D instance
        DimensionError: If layer is out of bounds
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    result = []
    
    # Header
    result.append(f"BitField3D({x_dim}×{y_dim}×{z_dim})")
    
    # Visualize specific layer or all layers
    if layer is not None:
        if layer < 0 or layer >= z_dim:
            raise DimensionError(f"Layer {layer} is out of bounds (0-{z_dim-1})")
        
        result.append(f"\nLayer z={layer}:")
        result.append("+{}+".format("-" * x_dim))
        
        for y in range(y_dim):
            row = "|"
            for x in range(x_dim):
                row += str(bitfield.getBit(x, y, layer))
            row += "|"
            result.append(row)
        
        result.append("+{}+".format("-" * x_dim))
    
    else:
        # Visualize all layers
        for z in range(z_dim):
            result.append(f"\nLayer z={z}:")
            result.append("+{}+".format("-" * x_dim))
            
            for y in range(y_dim):
                row = "|"
                for x in range(x_dim):
                    row += str(bitfield.getBit(x, y, z))
                row += "|"
                result.append(row)
            
            result.append("+{}+".format("-" * x_dim))
    
    return "\n".join(result)

def visualize4D(bitfield, time_point=None, layer=None):
    """
    Visualizes a 4D bitfield using ASCII representation.
    
    Args:
        bitfield (BitField4D): Bitfield to visualize
        time_point (int, optional): Specific t-coordinate to visualize. If None, visualizes all time points.
        layer (int, optional): Specific z-layer to visualize. If None, visualizes all layers.
        
    Returns:
        str: ASCII visualization of the bitfield
        
    Raises:
        TypeError: If bitfield is not a BitField4D instance
        DimensionError: If time_point or layer is out of bounds
    """
    if not isinstance(bitfield, BitField4D):
        raise TypeError("Bitfield must be a BitField4D instance")
    
    x_dim, y_dim, z_dim, t_dim = bitfield.getDimensions()
    result = []
    
    # Header
    result.append(f"BitField4D({x_dim}×{y_dim}×{z_dim}×{t_dim})")
    
    # Validate time_point if specified
    if time_point is not None and (time_point < 0 or time_point >= t_dim):
        raise DimensionError(f"Time point {time_point} is out of bounds (0-{t_dim-1})")
    
    # Validate layer if specified
    if layer is not None and (layer < 0 or layer >= z_dim):
        raise DimensionError(f"Layer {layer} is out of bounds (0-{z_dim-1})")
    
    # Determine time points to visualize
    t_range = range(t_dim) if time_point is None else [time_point]
    
    # Determine layers to visualize
    z_range = range(z_dim) if layer is None else [layer]
    
    # Visualize specified time points and layers
    for t in t_range:
        result.append(f"\nTime t={t}:")
        
        for z in z_range:
            result.append(f"  Layer z={z}:")
            result.append("  +{}+".format("-" * x_dim))
            
            for y in range(y_dim):
                row = "  |"
                for x in range(x_dim):
                    row += str(bitfield.getBit(x, y, z, t))
                row += "|"
                result.append(row)
            
            result.append("  +{}+".format("-" * x_dim))
    
    return "\n".join(result)

def animateTransform(bitfield, frames=5):
    """
    Creates an ASCII animation of a bitfield transformation.
    
    This function generates a series of ASCII frames that can be displayed
    sequentially to visualize a transformation over time.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to animate
        frames (int): Number of frames to generate
        
    Returns:
        list: List of ASCII frames
        
    Raises:
        TypeError: If bitfield is not a BitField3D or BitField4D instance
        ValueError: If frames is less than 1
    """
    if not isinstance(bitfield, (BitField3D, BitField4D)):
        raise TypeError("Bitfield must be a BitField3D or BitField4D instance")
    
    if frames < 1:
        raise ValueError("Frames must be at least 1")
    
    # Generate animation frames
    animation_frames = []
    
    if isinstance(bitfield, BitField3D):
        # For 3D bitfield, animate by showing different layers in sequence
        x_dim, y_dim, z_dim = bitfield.getDimensions()
        
        # If z_dim is less than frames, repeat layers
        for frame in range(frames):
            z = frame % z_dim
            animation_frames.append(visualize3D(bitfield, layer=z))
    
    else:  # BitField4D
        # For 4D bitfield, animate by showing different time points
        x_dim, y_dim, z_dim, t_dim = bitfield.getDimensions()
        
        # If t_dim is less than frames, repeat time points
        for frame in range(frames):
            t = frame % t_dim
            animation_frames.append(visualize4D(bitfield, time_point=t))
    
    return animation_frames

def visualize3D_compact(bitfield):
    """
    Creates a compact ASCII visualization of a 3D bitfield.
    
    This function generates a more space-efficient representation
    suitable for larger bitfields.
    
    Args:
        bitfield (BitField3D): Bitfield to visualize
        
    Returns:
        str: Compact ASCII visualization of the bitfield
        
    Raises:
        TypeError: If bitfield is not a BitField3D instance
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    result = []
    
    # Header
    result.append(f"BitField3D({x_dim}×{y_dim}×{z_dim}) [Compact View]")
    
    # Generate compact visualization
    for z in range(z_dim):
        result.append(f"\nz={z}:")
        
        for y in range(y_dim):
            row = ""
            for x in range(x_dim):
                row += str(bitfield.getBit(x, y, z))
            result.append(row)
    
    return "\n".join(result)

def visualize4D_compact(bitfield):
    """
    Creates a compact ASCII visualization of a 4D bitfield.
    
    This function generates a more space-efficient representation
    suitable for larger bitfields.
    
    Args:
        bitfield (BitField4D): Bitfield to visualize
        
    Returns:
        str: Compact ASCII visualization of the bitfield
        
    Raises:
        TypeError: If bitfield is not a BitField4D instance
    """
    if not isinstance(bitfield, BitField4D):
        raise TypeError("Bitfield must be a BitField4D instance")
    
    x_dim, y_dim, z_dim, t_dim = bitfield.getDimensions()
    result = []
    
    # Header
    result.append(f"BitField4D({x_dim}×{y_dim}×{z_dim}×{t_dim}) [Compact View]")
    
    # Generate compact visualization
    for t in range(t_dim):
        result.append(f"\nt={t}:")
        
        for z in range(z_dim):
            result.append(f"  z={z}:")
            
            for y in range(y_dim):
                row = "  "
                for x in range(x_dim):
                    row += str(bitfield.getBit(x, y, z, t))
                result.append(row)
    
    return "\n".join(result)

def visualize_properties(bitfield, position):
    """
    Visualizes the properties of a bit at the specified position.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to visualize
        position (tuple): Position of the bit (x, y, z) or (x, y, z, t)
        
    Returns:
        str: ASCII visualization of the bit properties
        
    Raises:
        TypeError: If bitfield is not a BitField3D or BitField4D instance
        ValueError: If position length doesn't match bitfield dimensions
    """
    if not isinstance(bitfield, (BitField3D, BitField4D)):
        raise TypeError("Bitfield must be a BitField3D or BitField4D instance")
    
    # Validate position
    if isinstance(bitfield, BitField3D) and len(position) != 3:
        raise ValueError("Position must be a tuple of length 3 for BitField3D")
    elif isinstance(bitfield, BitField4D) and len(position) != 4:
        raise ValueError("Position must be a tuple of length 4 for BitField4D")
    
    result = []
    
    # Get bit value and properties
    if isinstance(bitfield, BitField3D):
        x, y, z = position
        bit_value = bitfield.getBit(x, y, z)
        property_names = bitfield.getPropertyNames(x, y, z)
        
        # Header
        result.append(f"Bit at position ({x}, {y}, {z}):")
        result.append(f"Value: {bit_value}")
        
        # Properties
        if property_names:
            result.append("\nProperties:")
            for prop_name in property_names:
                prop_value = bitfield.getProperty(x, y, z, prop_name)
                result.append(f"  {prop_name}: {prop_value}")
        else:
            result.append("\nNo properties set.")
    
    else:  # BitField4D
        x, y, z, t = position
        bit_value = bitfield.getBit(x, y, z, t)
        property_names = bitfield.getPropertyNames(x, y, z, t)
        
        # Header
        result.append(f"Bit at position ({x}, {y}, {z}, {t}):")
        result.append(f"Value: {bit_value}")
        
        # Properties
        if property_names:
            result.append("\nProperties:")
            for prop_name in property_names:
                prop_value = bitfield.getProperty(x, y, z, t, prop_name)
                result.append(f"  {prop_name}: {prop_value}")
        else:
            result.append("\nNo properties set.")
    
    return "\n".join(result)
