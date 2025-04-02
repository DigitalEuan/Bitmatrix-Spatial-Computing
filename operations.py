"""
Core operations for BitMatrix Spatial Computing.

This module provides functions for manipulating and transforming BitMatrix
data structures, including dimensional mapping, spatial transformations,
and block operations.
"""

import numpy as np
import math
from .exceptions import DimensionError, CoordinateError
from .matrix import BitField3D, BitField4D

# Dimensional Mapping Functions

def mapTo3D(data, dimensions):
    """
    Maps linear data to a 3D bitfield structure according to specified dimensions.
    
    Args:
        data (list): Linear array of binary data
        dimensions (tuple): (x, y, z) dimensions of the target 3D structure
        
    Returns:
        BitField3D: 3D bitfield containing the mapped data
        
    Raises:
        DimensionError: If data length doesn't match dimensions product
    """
    x_dim, y_dim, z_dim = dimensions
    total_size = x_dim * y_dim * z_dim
    
    # Validate data length
    if len(data) > total_size:
        raise DimensionError(f"Data length ({len(data)}) exceeds capacity of target dimensions ({total_size})")
    
    # Create new bitfield
    bitfield = BitField3D(x_dim, y_dim, z_dim)
    
    # Map data to 3D structure
    index = 0
    for z in range(z_dim):
        for y in range(y_dim):
            for x in range(x_dim):
                if index < len(data):
                    bitfield.setBit(x, y, z, 1 if data[index] else 0)
                    index += 1
                else:
                    bitfield.setBit(x, y, z, 0)
    
    return bitfield

def mapTo4D(data, dimensions, temporal_length):
    """
    Maps linear data to a 4D bitfield structure with a temporal dimension.
    
    Args:
        data (list): Linear array of binary data
        dimensions (tuple): (x, y, z) dimensions of the spatial structure
        temporal_length (int): Length of the temporal dimension
        
    Returns:
        BitField4D: 4D bitfield containing the mapped data
        
    Raises:
        DimensionError: If data length doesn't match dimensions product
    """
    x_dim, y_dim, z_dim = dimensions
    total_size = x_dim * y_dim * z_dim * temporal_length
    
    # Validate data length
    if len(data) > total_size:
        raise DimensionError(f"Data length ({len(data)}) exceeds capacity of target dimensions ({total_size})")
    
    # Create new bitfield
    bitfield = BitField4D(x_dim, y_dim, z_dim, temporal_length)
    
    # Map data to 4D structure
    index = 0
    for t in range(temporal_length):
        for z in range(z_dim):
            for y in range(y_dim):
                for x in range(x_dim):
                    if index < len(data):
                        bitfield.setBit(x, y, z, t, 1 if data[index] else 0)
                        index += 1
                    else:
                        bitfield.setBit(x, y, z, t, 0)
    
    return bitfield

def extractLinear(bitfield):
    """
    Extracts data from a multidimensional bitfield into a linear representation.
    
    Args:
        bitfield (BitField3D or BitField4D): Multidimensional bitfield
        
    Returns:
        list: Linear array of binary data
        
    Raises:
        TypeError: If bitfield is not a BitField3D or BitField4D instance
    """
    dimensions = bitfield.getDimensions()
    linear_data = []
    
    if isinstance(bitfield, BitField3D):
        x_dim, y_dim, z_dim = dimensions
        for z in range(z_dim):
            for y in range(y_dim):
                for x in range(x_dim):
                    linear_data.append(bitfield.getBit(x, y, z))
    
    elif isinstance(bitfield, BitField4D):
        x_dim, y_dim, z_dim, t_dim = dimensions
        for t in range(t_dim):
            for z in range(z_dim):
                for y in range(y_dim):
                    for x in range(x_dim):
                        linear_data.append(bitfield.getBit(x, y, z, t))
    
    else:
        raise TypeError("Bitfield must be a BitField3D or BitField4D instance")
    
    return linear_data

def dimensionalReshape(bitfield, new_dimensions):
    """
    Reshapes a bitfield to new dimensions while preserving data.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to reshape
        new_dimensions (tuple): New dimensions (x, y, z) or (x, y, z, t)
        
    Returns:
        BitField3D or BitField4D: Reshaped bitfield
        
    Raises:
        DimensionError: If new dimensions don't match total bit count
        TypeError: If bitfield is not a BitField3D or BitField4D instance
    """
    # Extract linear data
    linear_data = extractLinear(bitfield)
    
    # Create new bitfield with new dimensions
    if isinstance(bitfield, BitField3D) and len(new_dimensions) == 3:
        x_dim, y_dim, z_dim = new_dimensions
        total_size = x_dim * y_dim * z_dim
        
        if len(linear_data) != total_size:
            raise DimensionError(f"Data length ({len(linear_data)}) doesn't match new dimensions product ({total_size})")
        
        return mapTo3D(linear_data, new_dimensions)
    
    elif isinstance(bitfield, BitField4D) and len(new_dimensions) == 4:
        x_dim, y_dim, z_dim, t_dim = new_dimensions
        total_size = x_dim * y_dim * z_dim * t_dim
        
        if len(linear_data) != total_size:
            raise DimensionError(f"Data length ({len(linear_data)}) doesn't match new dimensions product ({total_size})")
        
        return mapTo4D(linear_data, (x_dim, y_dim, z_dim), t_dim)
    
    else:
        raise TypeError("Incompatible bitfield type and dimensions")

# Spatial Transformation Functions

def rotate3D(bitfield, axis, angle_degrees):
    """
    Rotates a 3D bitfield around the specified axis.
    
    Args:
        bitfield (BitField3D): BitField3D instance to rotate
        axis (str): Rotation axis ('x', 'y', or 'z')
        angle_degrees (float): Rotation angle in degrees
        
    Returns:
        BitField3D: New BitField3D instance with rotated data
        
    Raises:
        ValueError: If axis is not 'x', 'y', or 'z'
        TypeError: If bitfield is not a BitField3D instance
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    # Convert angle to radians
    angle_radians = math.radians(angle_degrees)
    
    # Get dimensions
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    
    # Create rotation matrix
    cos_angle = math.cos(angle_radians)
    sin_angle = math.sin(angle_radians)
    
    if axis == 'x':
        # Rotation around x-axis
        rotation_matrix = np.array([
            [1, 0, 0],
            [0, cos_angle, -sin_angle],
            [0, sin_angle, cos_angle]
        ])
    elif axis == 'y':
        # Rotation around y-axis
        rotation_matrix = np.array([
            [cos_angle, 0, sin_angle],
            [0, 1, 0],
            [-sin_angle, 0, cos_angle]
        ])
    elif axis == 'z':
        # Rotation around z-axis
        rotation_matrix = np.array([
            [cos_angle, -sin_angle, 0],
            [sin_angle, cos_angle, 0],
            [0, 0, 1]
        ])
    else:
        raise ValueError("Axis must be 'x', 'y', or 'z'")
    
    # Create new bitfield
    new_bitfield = BitField3D(x_dim, y_dim, z_dim)
    
    # Calculate center of rotation
    center_x = (x_dim - 1) / 2
    center_y = (y_dim - 1) / 2
    center_z = (z_dim - 1) / 2
    
    # Apply rotation to each bit
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Translate to origin
                tx = x - center_x
                ty = y - center_y
                tz = z - center_z
                
                # Apply rotation
                coords = np.array([tx, ty, tz])
                rotated_coords = np.dot(rotation_matrix, coords)
                
                # Translate back and round to nearest integer
                rx = round(rotated_coords[0] + center_x)
                ry = round(rotated_coords[1] + center_y)
                rz = round(rotated_coords[2] + center_z)
                
                # Check if rotated coordinates are within bounds
                if (0 <= rx < x_dim and 0 <= ry < y_dim and 0 <= rz < z_dim):
                    # Copy bit value
                    new_bitfield.setBit(rx, ry, rz, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(rx, ry, rz, prop_name, prop_value)
    
    return new_bitfield

def translate3D(bitfield, vector):
    """
    Translates a 3D bitfield by the specified vector.
    
    Args:
        bitfield (BitField3D): BitField3D instance to translate
        vector (tuple): Translation vector (dx, dy, dz)
        
    Returns:
        BitField3D: New BitField3D instance with translated data
        
    Raises:
        TypeError: If bitfield is not a BitField3D instance
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    # Get dimensions
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    
    # Get translation vector
    dx, dy, dz = vector
    
    # Create new bitfield
    new_bitfield = BitField3D(x_dim, y_dim, z_dim)
    
    # Apply translation to each bit
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Calculate new coordinates
                nx = x + dx
                ny = y + dy
                nz = z + dz
                
                # Check if new coordinates are within bounds
                if (0 <= nx < x_dim and 0 <= ny < y_dim and 0 <= nz < z_dim):
                    # Copy bit value
                    new_bitfield.setBit(nx, ny, nz, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(nx, ny, nz, prop_name, prop_value)
    
    return new_bitfield

def scale3D(bitfield, scale_factors):
    """
    Scales a 3D bitfield by the specified factors.
    
    Args:
        bitfield (BitField3D): BitField3D instance to scale
        scale_factors (tuple): Scale factors (sx, sy, sz)
        
    Returns:
        BitField3D: New BitField3D instance with scaled data
        
    Raises:
        TypeError: If bitfield is not a BitField3D instance
        ValueError: If any scale factor is less than or equal to 0
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    # Get dimensions
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    
    # Get scale factors
    sx, sy, sz = scale_factors
    
    # Validate scale factors
    if sx <= 0 or sy <= 0 or sz <= 0:
        raise ValueError("Scale factors must be greater than 0")
    
    # Calculate new dimensions
    new_x_dim = round(x_dim * sx)
    new_y_dim = round(y_dim * sy)
    new_z_dim = round(z_dim * sz)
    
    # Create new bitfield
    new_bitfield = BitField3D(new_x_dim, new_y_dim, new_z_dim)
    
    # Apply scaling to each bit in the new bitfield
    for nx in range(new_x_dim):
        for ny in range(new_y_dim):
            for nz in range(new_z_dim):
                # Calculate original coordinates
                x = round(nx / sx)
                y = round(ny / sy)
                z = round(nz / sz)
                
                # Check if original coordinates are within bounds
                if (0 <= x < x_dim and 0 <= y < y_dim and 0 <= z < z_dim):
                    # Copy bit value
                    new_bitfield.setBit(nx, ny, nz, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(nx, ny, nz, prop_name, prop_value)
    
    return new_bitfield

def mirror3D(bitfield, plane):
    """
    Mirrors a 3D bitfield across the specified plane.
    
    Args:
        bitfield (BitField3D): BitField3D instance to mirror
        plane (str): Mirror plane ('xy', 'xz', or 'yz')
        
    Returns:
        BitField3D: New BitField3D instance with mirrored data
        
    Raises:
        ValueError: If plane is not 'xy', 'xz', or 'yz'
        TypeError: If bitfield is not a BitField3D instance
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    # Get dimensions
    x_dim, y_dim, z_dim = bitfield.getDimensions()
    
    # Create new bitfield
    new_bitfield = BitField3D(x_dim, y_dim, z_dim)
    
    # Apply mirroring based on plane
    if plane == 'xy':
        # Mirror across xy-plane (flip z)
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    mz = z_dim - 1 - z
                    new_bitfield.setBit(x, y, mz, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(x, y, mz, prop_name, prop_value)
    
    elif plane == 'xz':
        # Mirror across xz-plane (flip y)
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    my = y_dim - 1 - y
                    new_bitfield.setBit(x, my, z, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(x, my, z, prop_name, prop_value)
    
    elif plane == 'yz':
        # Mirror across yz-plane (flip x)
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    mx = x_dim - 1 - x
                    new_bitfield.setBit(mx, y, z, bitfield.getBit(x, y, z))
                    
                    # Copy properties if any
                    for prop_name in bitfield.getPropertyNames(x, y, z):
                        prop_value = bitfield.getProperty(x, y, z, prop_name)
                        new_bitfield.setProperty(mx, y, z, prop_name, prop_value)
    
    else:
        raise ValueError("Plane must be 'xy', 'xz', or 'yz'")
    
    return new_bitfield

# Block Operations

def insertBlock(target_bitfield, source_block, position):
    """
    Inserts a block at the specified position in the target bitfield.
    
    Args:
        target_bitfield (BitField3D): Target bitfield to insert into
        source_block (BitField3D): Source block to insert
        position (tuple): Position (x, y, z) to insert at
        
    Returns:
        BitField3D: New BitField3D instance with the block inserted
        
    Raises:
        TypeError: If bitfields are not BitField3D instances
        CoordinateError: If position is invalid or block doesn't fit
    """
    if not isinstance(target_bitfield, BitField3D) or not isinstance(source_block, BitField3D):
        raise TypeError("Bitfields must be BitField3D instances")
    
    # Get dimensions
    target_dims = target_bitfield.getDimensions()
    source_dims = source_block.getDimensions()
    
    # Get position
    pos_x, pos_y, pos_z = position
    
    # Check if block fits
    if (pos_x < 0 or pos_y < 0 or pos_z < 0 or
        pos_x + source_dims[0] > target_dims[0] or
        pos_y + source_dims[1] > target_dims[1] or
        pos_z + source_dims[2] > target_dims[2]):
        raise CoordinateError("Block doesn't fit at the specified position")
    
    # Create new bitfield as a copy of the target
    new_bitfield = target_bitfield.copy()
    
    # Insert block
    for x in range(source_dims[0]):
        for y in range(source_dims[1]):
            for z in range(source_dims[2]):
                # Calculate target position
                tx = pos_x + x
                ty = pos_y + y
                tz = pos_z + z
                
                # Copy bit value
                new_bitfield.setBit(tx, ty, tz, source_block.getBit(x, y, z))
                
                # Copy properties if any
                for prop_name in source_block.getPropertyNames(x, y, z):
                    prop_value = source_block.getProperty(x, y, z, prop_name)
                    new_bitfield.setProperty(tx, ty, tz, prop_name, prop_value)
    
    return new_bitfield

def extractBlock(bitfield, start_position, dimensions):
    """
    Extracts a block from the bitfield.
    
    Args:
        bitfield (BitField3D): Bitfield to extract from
        start_position (tuple): Start position (x, y, z) of the block
        dimensions (tuple): Dimensions (x_dim, y_dim, z_dim) of the block
        
    Returns:
        BitField3D: New BitField3D instance containing the extracted block
        
    Raises:
        TypeError: If bitfield is not a BitField3D instance
        CoordinateError: If position or dimensions are invalid
    """
    if not isinstance(bitfield, BitField3D):
        raise TypeError("Bitfield must be a BitField3D instance")
    
    # Get bitfield dimensions
    bitfield_dims = bitfield.getDimensions()
    
    # Get start position and block dimensions
    start_x, start_y, start_z = start_position
    block_x_dim, block_y_dim, block_z_dim = dimensions
    
    # Check if block is within bounds
    if (start_x < 0 or start_y < 0 or start_z < 0 or
        start_x + block_x_dim > bitfield_dims[0] or
        start_y + block_y_dim > bitfield_dims[1] or
        start_z + block_z_dim > bitfield_dims[2]):
        raise CoordinateError("Block is not within the bitfield bounds")
    
    # Create new bitfield for the block
    block = BitField3D(block_x_dim, block_y_dim, block_z_dim)
    
    # Extract block
    for x in range(block_x_dim):
        for y in range(block_y_dim):
            for z in range(block_z_dim):
                # Calculate source position
                sx = start_x + x
                sy = start_y + y
                sz = start_z + z
                
                # Copy bit value
                block.setBit(x, y, z, bitfield.getBit(sx, sy, sz))
                
                # Copy properties if any
                for prop_name in bitfield.getPropertyNames(sx, sy, sz):
                    prop_value = bitfield.getProperty(sx, sy, sz, prop_name)
                    block.setProperty(x, y, z, prop_name, prop_value)
    
    return block

def replaceBlock(target_bitfield, replacement_block, position):
    """
    Replaces a block at the specified position in the target bitfield.
    
    Args:
        target_bitfield (BitField3D): Target bitfield to replace in
        replacement_block (BitField3D): Replacement block
        position (tuple): Position (x, y, z) to replace at
        
    Returns:
        BitField3D: New BitField3D instance with the block replaced
        
    Raises:
        TypeError: If bitfields are not BitField3D instances
        CoordinateError: If position is invalid or block doesn't fit
    """
    # This is essentially the same as insertBlock, but included for API completeness
    return insertBlock(target_bitfield, replacement_block, position)
