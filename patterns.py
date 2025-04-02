"""
Pattern operations for BitMatrix Spatial Computing.

This module provides functions for finding, matching, and generating patterns
within BitMatrix data structures.
"""

import numpy as np
from .exceptions import PatternError
from .matrix import BitField3D, BitField4D

def findPattern(bitfield, pattern):
    """
    Finds all occurrences of a pattern in a bitfield.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to search in
        pattern (BitField3D or BitField4D): Pattern to find
        
    Returns:
        list: List of positions where the pattern was found
        
    Raises:
        PatternError: If pattern is larger than bitfield or types don't match
        TypeError: If bitfields are not BitField3D or BitField4D instances
    """
    # Validate bitfield types
    if not isinstance(bitfield, (BitField3D, BitField4D)) or not isinstance(pattern, (BitField3D, BitField4D)):
        raise TypeError("Bitfields must be BitField3D or BitField4D instances")
    
    # Validate bitfield compatibility
    if type(bitfield) != type(pattern):
        raise PatternError("Cannot find pattern of different bitfield type")
    
    # Get dimensions
    if isinstance(bitfield, BitField3D):
        bitfield_dims = bitfield.getDimensions()
        pattern_dims = pattern.getDimensions()
        
        # Validate pattern size
        if (pattern_dims[0] > bitfield_dims[0] or
            pattern_dims[1] > bitfield_dims[1] or
            pattern_dims[2] > bitfield_dims[2]):
            raise PatternError("Pattern is larger than bitfield")
        
        # Find pattern occurrences
        positions = []
        
        # Iterate through all possible positions
        for x in range(bitfield_dims[0] - pattern_dims[0] + 1):
            for y in range(bitfield_dims[1] - pattern_dims[1] + 1):
                for z in range(bitfield_dims[2] - pattern_dims[2] + 1):
                    # Check if pattern matches at this position
                    if _check_pattern_match_3d(bitfield, pattern, (x, y, z)):
                        positions.append((x, y, z))
        
        return positions
    
    else:  # BitField4D
        bitfield_dims = bitfield.getDimensions()
        pattern_dims = pattern.getDimensions()
        
        # Validate pattern size
        if (pattern_dims[0] > bitfield_dims[0] or
            pattern_dims[1] > bitfield_dims[1] or
            pattern_dims[2] > bitfield_dims[2] or
            pattern_dims[3] > bitfield_dims[3]):
            raise PatternError("Pattern is larger than bitfield")
        
        # Find pattern occurrences
        positions = []
        
        # Iterate through all possible positions
        for t in range(bitfield_dims[3] - pattern_dims[3] + 1):
            for x in range(bitfield_dims[0] - pattern_dims[0] + 1):
                for y in range(bitfield_dims[1] - pattern_dims[1] + 1):
                    for z in range(bitfield_dims[2] - pattern_dims[2] + 1):
                        # Check if pattern matches at this position
                        if _check_pattern_match_4d(bitfield, pattern, (x, y, z, t)):
                            positions.append((x, y, z, t))
        
        return positions

def _check_pattern_match_3d(bitfield, pattern, position):
    """
    Checks if a pattern matches at the specified position in a 3D bitfield.
    
    Args:
        bitfield (BitField3D): Bitfield to check
        pattern (BitField3D): Pattern to match
        position (tuple): Position (x, y, z) to check
        
    Returns:
        bool: True if pattern matches, False otherwise
    """
    pattern_dims = pattern.getDimensions()
    pos_x, pos_y, pos_z = position
    
    # Check each bit in the pattern
    for x in range(pattern_dims[0]):
        for y in range(pattern_dims[1]):
            for z in range(pattern_dims[2]):
                # Get bit values
                pattern_bit = pattern.getBit(x, y, z)
                bitfield_bit = bitfield.getBit(pos_x + x, pos_y + y, pos_z + z)
                
                # If bits don't match, pattern doesn't match
                if pattern_bit != bitfield_bit:
                    return False
    
    # All bits match
    return True

def _check_pattern_match_4d(bitfield, pattern, position):
    """
    Checks if a pattern matches at the specified position in a 4D bitfield.
    
    Args:
        bitfield (BitField4D): Bitfield to check
        pattern (BitField4D): Pattern to match
        position (tuple): Position (x, y, z, t) to check
        
    Returns:
        bool: True if pattern matches, False otherwise
    """
    pattern_dims = pattern.getDimensions()
    pos_x, pos_y, pos_z, pos_t = position
    
    # Check each bit in the pattern
    for t in range(pattern_dims[3]):
        for x in range(pattern_dims[0]):
            for y in range(pattern_dims[1]):
                for z in range(pattern_dims[2]):
                    # Get bit values
                    pattern_bit = pattern.getBit(x, y, z, t)
                    bitfield_bit = bitfield.getBit(pos_x + x, pos_y + y, pos_z + z, pos_t + t)
                    
                    # If bits don't match, pattern doesn't match
                    if pattern_bit != bitfield_bit:
                        return False
    
    # All bits match
    return True

def matchPattern(bitfield, pattern, threshold=0.8):
    """
    Finds approximate matches of a pattern in a bitfield.
    
    Args:
        bitfield (BitField3D or BitField4D): Bitfield to search in
        pattern (BitField3D or BitField4D): Pattern to match
        threshold (float): Minimum similarity threshold (0.0 to 1.0)
        
    Returns:
        list: List of (position, similarity) tuples where pattern was matched
        
    Raises:
        PatternError: If pattern is larger than bitfield or types don't match
        ValueError: If threshold is not between 0 and 1
        TypeError: If bitfields are not BitField3D or BitField4D instances
    """
    # Validate threshold
    if threshold < 0.0 or threshold > 1.0:
        raise ValueError("Threshold must be between 0.0 and 1.0")
    
    # Validate bitfield types
    if not isinstance(bitfield, (BitField3D, BitField4D)) or not isinstance(pattern, (BitField3D, BitField4D)):
        raise TypeError("Bitfields must be BitField3D or BitField4D instances")
    
    # Validate bitfield compatibility
    if type(bitfield) != type(pattern):
        raise PatternError("Cannot match pattern of different bitfield type")
    
    # Get dimensions
    if isinstance(bitfield, BitField3D):
        bitfield_dims = bitfield.getDimensions()
        pattern_dims = pattern.getDimensions()
        
        # Validate pattern size
        if (pattern_dims[0] > bitfield_dims[0] or
            pattern_dims[1] > bitfield_dims[1] or
            pattern_dims[2] > bitfield_dims[2]):
            raise PatternError("Pattern is larger than bitfield")
        
        # Find pattern matches
        matches = []
        
        # Calculate total bits in pattern
        total_bits = pattern_dims[0] * pattern_dims[1] * pattern_dims[2]
        
        # Iterate through all possible positions
        for x in range(bitfield_dims[0] - pattern_dims[0] + 1):
            for y in range(bitfield_dims[1] - pattern_dims[1] + 1):
                for z in range(bitfield_dims[2] - pattern_dims[2] + 1):
                    # Calculate similarity at this position
                    similarity = _calculate_similarity_3d(bitfield, pattern, (x, y, z), total_bits)
                    
                    # If similarity is above threshold, add to matches
                    if similarity >= threshold:
                        matches.append(((x, y, z), similarity))
        
        # Sort matches by similarity (highest first)
        matches.sort(key=lambda m: m[1], reverse=True)
        return matches
    
    else:  # BitField4D
        bitfield_dims = bitfield.getDimensions()
        pattern_dims = pattern.getDimensions()
        
        # Validate pattern size
        if (pattern_dims[0] > bitfield_dims[0] or
            pattern_dims[1] > bitfield_dims[1] or
            pattern_dims[2] > bitfield_dims[2] or
            pattern_dims[3] > bitfield_dims[3]):
            raise PatternError("Pattern is larger than bitfield")
        
        # Find pattern matches
        matches = []
        
        # Calculate total bits in pattern
        total_bits = pattern_dims[0] * pattern_dims[1] * pattern_dims[2] * pattern_dims[3]
        
        # Iterate through all possible positions
        for t in range(bitfield_dims[3] - pattern_dims[3] + 1):
            for x in range(bitfield_dims[0] - pattern_dims[0] + 1):
                for y in range(bitfield_dims[1] - pattern_dims[1] + 1):
                    for z in range(bitfield_dims[2] - pattern_dims[2] + 1):
                        # Calculate similarity at this position
                        similarity = _calculate_similarity_4d(bitfield, pattern, (x, y, z, t), total_bits)
                        
                        # If similarity is above threshold, add to matches
                        if similarity >= threshold:
                            matches.append(((x, y, z, t), similarity))
        
        # Sort matches by similarity (highest first)
        matches.sort(key=lambda m: m[1], reverse=True)
        return matches

def _calculate_similarity_3d(bitfield, pattern, position, total_bits):
    """
    Calculates the similarity between a pattern and a region in a 3D bitfield.
    
    Args:
        bitfield (BitField3D): Bitfield to check
        pattern (BitField3D): Pattern to match
        position (tuple): Position (x, y, z) to check
        total_bits (int): Total number of bits in the pattern
        
    Returns:
        float: Similarity score (0.0 to 1.0)
    """
    pattern_dims = pattern.getDimensions()
    pos_x, pos_y, pos_z = position
    
    # Count matching bits
    matching_bits = 0
    
    # Check each bit in the pattern
    for x in range(pattern_dims[0]):
        for y in range(pattern_dims[1]):
            for z in range(pattern_dims[2]):
                # Get bit values
                pattern_bit = pattern.getBit(x, y, z)
                bitfield_bit = bitfield.getBit(pos_x + x, pos_y + y, pos_z + z)
                
                # If bits match, increment counter
                if pattern_bit == bitfield_bit:
                    matching_bits += 1
    
    # Calculate similarity
    return matching_bits / total_bits

def _calculate_similarity_4d(bitfield, pattern, position, total_bits):
    """
    Calculates the similarity between a pattern and a region in a 4D bitfield.
    
    Args:
        bitfield (BitField4D): Bitfield to check
        pattern (BitField4D): Pattern to match
        position (tuple): Position (x, y, z, t) to check
        total_bits (int): Total number of bits in the pattern
        
    Returns:
        float: Similarity score (0.0 to 1.0)
    """
    pattern_dims = pattern.getDimensions()
    pos_x, pos_y, pos_z, pos_t = position
    
    # Count matching bits
    matching_bits = 0
    
    # Check each bit in the pattern
    for t in range(pattern_dims[3]):
        for x in range(pattern_dims[0]):
            for y in range(pattern_dims[1]):
                for z in range(pattern_dims[2]):
                    # Get bit values
                    pattern_bit = pattern.getBit(x, y, z, t)
                    bitfield_bit = bitfield.getBit(pos_x + x, pos_y + y, pos_z + z, pos_t + t)
                    
                    # If bits match, increment counter
                    if pattern_bit == bitfield_bit:
                        matching_bits += 1
    
    # Calculate similarity
    return matching_bits / total_bits

def generatePattern(pattern_type, dimensions):
    """
    Generates a pattern of the specified type and dimensions.
    
    Args:
        pattern_type (str): Type of pattern ('cube', 'sphere', 'wave', 'random')
        dimensions (tuple): Dimensions of the pattern (x, y, z) or (x, y, z, t)
        
    Returns:
        BitField3D or BitField4D: Generated pattern
        
    Raises:
        PatternError: If pattern_type is invalid
        ValueError: If dimensions are invalid
    """
    # Validate dimensions
    if len(dimensions) not in (3, 4):
        raise ValueError("Dimensions must be a tuple of length 3 or 4")
    
    if len(dimensions) == 3:
        x_dim, y_dim, z_dim = dimensions
        
        # Create bitfield
        pattern = BitField3D(x_dim, y_dim, z_dim)
        
        # Generate pattern based on type
        if pattern_type == 'cube':
            _generate_cube_pattern(pattern)
        elif pattern_type == 'sphere':
            _generate_sphere_pattern(pattern)
        elif pattern_type == 'wave':
            _generate_wave_pattern(pattern)
        elif pattern_type == 'random':
            _generate_random_pattern(pattern)
        else:
            raise PatternError(f"Invalid pattern type: {pattern_type}")
        
        return pattern
    
    else:  # 4D
        x_dim, y_dim, z_dim, t_dim = dimensions
        
        # Create bitfield
        pattern = BitField4D(x_dim, y_dim, z_dim, t_dim)
        
        # Generate pattern based on type
        if pattern_type == 'cube':
            _generate_cube_pattern_4d(pattern)
        elif pattern_type == 'sphere':
            _generate_sphere_pattern_4d(pattern)
        elif pattern_type == 'wave':
            _generate_wave_pattern_4d(pattern)
        elif pattern_type == 'random':
            _generate_random_pattern_4d(pattern)
        else:
            raise PatternError(f"Invalid pattern type: {pattern_type}")
        
        return pattern

def _generate_cube_pattern(pattern):
    """
    Generates a cube pattern in a 3D bitfield.
    
    Args:
        pattern (BitField3D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim = pattern.getDimensions()
    
    # Set bits on the edges of the cube
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Check if bit is on the edge of the cube
                if (x == 0 or x == x_dim - 1 or
                    y == 0 or y == y_dim - 1 or
                    z == 0 or z == z_dim - 1):
                    pattern.setBit(x, y, z, 1)

def _generate_cube_pattern_4d(pattern):
    """
    Generates a cube pattern in a 4D bitfield.
    
    Args:
        pattern (BitField4D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim, t_dim = pattern.getDimensions()
    
    # Set bits on the edges of the hypercube
    for t in range(t_dim):
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Check if bit is on the edge of the hypercube
                    if (x == 0 or x == x_dim - 1 or
                        y == 0 or y == y_dim - 1 or
                        z == 0 or z == z_dim - 1 or
                        t == 0 or t == t_dim - 1):
                        pattern.setBit(x, y, z, t, 1)

def _generate_sphere_pattern(pattern):
    """
    Generates a sphere pattern in a 3D bitfield.
    
    Args:
        pattern (BitField3D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim = pattern.getDimensions()
    
    # Calculate center of the sphere
    center_x = (x_dim - 1) / 2
    center_y = (y_dim - 1) / 2
    center_z = (z_dim - 1) / 2
    
    # Calculate radius (half of the smallest dimension)
    radius = min(x_dim, y_dim, z_dim) / 2
    
    # Set bits on the surface of the sphere
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Calculate distance from center
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2 + (z - center_z)**2)
                
                # Check if bit is on the surface of the sphere
                if abs(distance - radius) < 0.5:
                    pattern.setBit(x, y, z, 1)

def _generate_sphere_pattern_4d(pattern):
    """
    Generates a hypersphere pattern in a 4D bitfield.
    
    Args:
        pattern (BitField4D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim, t_dim = pattern.getDimensions()
    
    # Calculate center of the hypersphere
    center_x = (x_dim - 1) / 2
    center_y = (y_dim - 1) / 2
    center_z = (z_dim - 1) / 2
    center_t = (t_dim - 1) / 2
    
    # Calculate radius (half of the smallest dimension)
    radius = min(x_dim, y_dim, z_dim, t_dim) / 2
    
    # Set bits on the surface of the hypersphere
    for t in range(t_dim):
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Calculate distance from center
                    distance = np.sqrt((x - center_x)**2 + (y - center_y)**2 + 
                                      (z - center_z)**2 + (t - center_t)**2)
                    
                    # Check if bit is on the surface of the hypersphere
                    if abs(distance - radius) < 0.5:
                        pattern.setBit(x, y, z, t, 1)

def _generate_wave_pattern(pattern):
    """
    Generates a wave pattern in a 3D bitfield.
    
    Args:
        pattern (BitField3D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim = pattern.getDimensions()
    
    # Set bits in a wave pattern
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Calculate wave value
                wave_val = np.sin(x/2) * np.cos(y/2) * np.sin(z/2)
                
                # Set bit if wave value is positive
                if wave_val > 0:
                    pattern.setBit(x, y, z, 1)

def _generate_wave_pattern_4d(pattern):
    """
    Generates a wave pattern in a 4D bitfield.
    
    Args:
        pattern (BitField4D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim, t_dim = pattern.getDimensions()
    
    # Set bits in a wave pattern
    for t in range(t_dim):
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Calculate wave value with temporal component
                    wave_val = np.sin(x/2) * np.cos(y/2) * np.sin(z/2) * np.cos(t/2)
                    
                    # Set bit if wave value is positive
                    if wave_val > 0:
                        pattern.setBit(x, y, z, t, 1)

def _generate_random_pattern(pattern):
    """
    Generates a random pattern in a 3D bitfield.
    
    Args:
        pattern (BitField3D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim = pattern.getDimensions()
    
    # Set bits randomly
    for x in range(x_dim):
        for y in range(y_dim):
            for z in range(z_dim):
                # Set bit with 50% probability
                if np.random.random() > 0.5:
                    pattern.setBit(x, y, z, 1)

def _generate_random_pattern_4d(pattern):
    """
    Generates a random pattern in a 4D bitfield.
    
    Args:
        pattern (BitField4D): Bitfield to generate pattern in
    """
    x_dim, y_dim, z_dim, t_dim = pattern.getDimensions()
    
    # Set bits randomly
    for t in range(t_dim):
        for x in range(x_dim):
            for y in range(y_dim):
                for z in range(z_dim):
                    # Set bit with 50% probability
                    if np.random.random() > 0.5:
                        pattern.setBit(x, y, z, t, 1)
