# BitMatrix Spatial Computing API Reference

This document provides a comprehensive reference for the BitMatrix Spatial Computing (BSC) API.

## Table of Contents

1. [Core Classes](#core-classes)
   - [BitField3D](#bitfield3d)
   - [BitField4D](#bitfield4d)
2. [Spatial Operations](#spatial-operations)
3. [Pattern Operations](#pattern-operations)
4. [KTA Operations](#kta-operations)
5. [Visualization Functions](#visualization-functions)
6. [Exceptions](#exceptions)

## Core Classes

### BitField3D

A three-dimensional bit field that forms the foundation of BitMatrix Spatial Computing.

#### Constructor

```python
BitField3D(x_dim, y_dim, z_dim)
```

Creates a new 3D bit field with the specified dimensions.

**Parameters:**
- `x_dim` (int): Size in the x dimension
- `y_dim` (int): Size in the y dimension
- `z_dim` (int): Size in the z dimension

**Returns:**
- A new BitField3D instance

#### Methods

##### `getBit(x, y, z)`

Gets the value of the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate

**Returns:**
- `int`: Bit value (0 or 1)

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `setBit(x, y, z, value)`

Sets the value of the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `value` (int): Bit value (0 or 1)

**Raises:**
- `DimensionError`: If coordinates are out of bounds
- `ValueError`: If value is not 0 or 1

##### `getDimensions()`

Gets the dimensions of the bit field.

**Returns:**
- `tuple`: (x_dim, y_dim, z_dim)

##### `setProperty(x, y, z, property_name, property_value)`

Sets a property for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `property_name` (str): Name of the property
- `property_value` (any): Value of the property

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `getProperty(x, y, z, property_name)`

Gets a property for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `property_name` (str): Name of the property

**Returns:**
- Property value, or None if the property is not set

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `getPropertyNames(x, y, z)`

Gets all property names for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate

**Returns:**
- `list`: List of property names

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `copy()`

Creates a deep copy of the bit field.

**Returns:**
- `BitField3D`: A new BitField3D instance with the same bits and properties

### BitField4D

A four-dimensional bit field that extends the 3D bit field with a temporal or fourth dimension.

#### Constructor

```python
BitField4D(x_dim, y_dim, z_dim, t_dim)
```

Creates a new 4D bit field with the specified dimensions.

**Parameters:**
- `x_dim` (int): Size in the x dimension
- `y_dim` (int): Size in the y dimension
- `z_dim` (int): Size in the z dimension
- `t_dim` (int): Size in the t dimension (time or fourth dimension)

**Returns:**
- A new BitField4D instance

#### Methods

##### `getBit(x, y, z, t)`

Gets the value of the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `t` (int): T coordinate (time or fourth dimension)

**Returns:**
- `int`: Bit value (0 or 1)

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `setBit(x, y, z, t, value)`

Sets the value of the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `t` (int): T coordinate (time or fourth dimension)
- `value` (int): Bit value (0 or 1)

**Raises:**
- `DimensionError`: If coordinates are out of bounds
- `ValueError`: If value is not 0 or 1

##### `getDimensions()`

Gets the dimensions of the bit field.

**Returns:**
- `tuple`: (x_dim, y_dim, z_dim, t_dim)

##### `setProperty(x, y, z, t, property_name, property_value)`

Sets a property for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `t` (int): T coordinate (time or fourth dimension)
- `property_name` (str): Name of the property
- `property_value` (any): Value of the property

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `getProperty(x, y, z, t, property_name)`

Gets a property for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `t` (int): T coordinate (time or fourth dimension)
- `property_name` (str): Name of the property

**Returns:**
- Property value, or None if the property is not set

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `getPropertyNames(x, y, z, t)`

Gets all property names for the bit at the specified coordinates.

**Parameters:**
- `x` (int): X coordinate
- `y` (int): Y coordinate
- `z` (int): Z coordinate
- `t` (int): T coordinate (time or fourth dimension)

**Returns:**
- `list`: List of property names

**Raises:**
- `DimensionError`: If coordinates are out of bounds

##### `copy()`

Creates a deep copy of the bit field.

**Returns:**
- `BitField4D`: A new BitField4D instance with the same bits and properties

## Spatial Operations

### `mapTo3D(linear_data, x_dim, y_dim, z_dim)`

Maps linear data to a 3D bit field.

**Parameters:**
- `linear_data` (list or array): Linear data to map
- `x_dim` (int): Size in the x dimension
- `y_dim` (int): Size in the y dimension
- `z_dim` (int): Size in the z dimension

**Returns:**
- `BitField3D`: A new BitField3D instance with the mapped data

**Raises:**
- `ValueError`: If linear_data length doesn't match the product of dimensions

### `mapTo4D(linear_data, x_dim, y_dim, z_dim, t_dim)`

Maps linear data to a 4D bit field.

**Parameters:**
- `linear_data` (list or array): Linear data to map
- `x_dim` (int): Size in the x dimension
- `y_dim` (int): Size in the y dimension
- `z_dim` (int): Size in the z dimension
- `t_dim` (int): Size in the t dimension

**Returns:**
- `BitField4D`: A new BitField4D instance with the mapped data

**Raises:**
- `ValueError`: If linear_data length doesn't match the product of dimensions

### `extractLinear(bitfield)`

Extracts linear data from a bit field.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to extract data from

**Returns:**
- `list`: Linear representation of the bit field data

**Raises:**
- `TypeError`: If bitfield is not a BitField3D or BitField4D instance

### `rotate3D(bitfield, axis, angle)`

Rotates a 3D bit field around the specified axis.

**Parameters:**
- `bitfield` (BitField3D): Bit field to rotate
- `axis` (str): Rotation axis ('x', 'y', or 'z')
- `angle` (float): Rotation angle in degrees

**Returns:**
- `BitField3D`: A new BitField3D instance with the rotated data

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance
- `ValueError`: If axis is not 'x', 'y', or 'z'

### `translate3D(bitfield, vector)`

Translates a 3D bit field by the specified vector.

**Parameters:**
- `bitfield` (BitField3D): Bit field to translate
- `vector` (list or tuple): Translation vector [dx, dy, dz]

**Returns:**
- `BitField3D`: A new BitField3D instance with the translated data

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance
- `ValueError`: If vector is not a list or tuple of length 3

### `scale3D(bitfield, factors)`

Scales a 3D bit field by the specified factors.

**Parameters:**
- `bitfield` (BitField3D): Bit field to scale
- `factors` (list or tuple): Scale factors [sx, sy, sz]

**Returns:**
- `BitField3D`: A new BitField3D instance with the scaled data

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance
- `ValueError`: If factors is not a list or tuple of length 3

### `mirror3D(bitfield, plane)`

Mirrors a 3D bit field across the specified plane.

**Parameters:**
- `bitfield` (BitField3D): Bit field to mirror
- `plane` (str): Mirror plane ('xy', 'xz', or 'yz')

**Returns:**
- `BitField3D`: A new BitField3D instance with the mirrored data

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance
- `ValueError`: If plane is not 'xy', 'xz', or 'yz'

## Pattern Operations

### `findPattern(bitfield, pattern)`

Finds all occurrences of a pattern in a bit field.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to search in
- `pattern` (BitField3D or BitField4D): Pattern to find

**Returns:**
- `list`: List of positions where the pattern was found

**Raises:**
- `TypeError`: If bitfield or pattern is not a BitField3D or BitField4D instance
- `PatternError`: If pattern is larger than bitfield or types don't match

### `matchPattern(bitfield, pattern, threshold=0.8)`

Finds approximate matches of a pattern in a bit field.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to search in
- `pattern` (BitField3D or BitField4D): Pattern to match
- `threshold` (float, optional): Minimum similarity threshold (0.0 to 1.0)

**Returns:**
- `list`: List of (position, similarity) tuples where pattern was matched

**Raises:**
- `TypeError`: If bitfield or pattern is not a BitField3D or BitField4D instance
- `PatternError`: If pattern is larger than bitfield or types don't match
- `ValueError`: If threshold is not between 0 and 1

### `generatePattern(pattern_type, dimensions)`

Generates a pattern of the specified type and dimensions.

**Parameters:**
- `pattern_type` (str): Type of pattern ('cube', 'sphere', 'wave', 'random')
- `dimensions` (tuple): Dimensions of the pattern (x, y, z) or (x, y, z, t)

**Returns:**
- `BitField3D` or `BitField4D`: Generated pattern

**Raises:**
- `PatternError`: If pattern_type is invalid
- `ValueError`: If dimensions are invalid

## KTA Operations

### `applyKineticTransform(bitfield, transform_type)`

Applies a kinetic transform to a bit field.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to transform
- `transform_type` (str): Type of transform ('wave', 'fractal', 'recursive')

**Returns:**
- `BitField3D` or `BitField4D`: Transformed bit field

**Raises:**
- `TypeError`: If bitfield is not a BitField3D or BitField4D instance
- `KTAError`: If transform_type is invalid

### `superposition(bitfield_a, bitfield_b)`

Creates a superposition of two bit fields.

**Parameters:**
- `bitfield_a` (BitField3D or BitField4D): First bit field
- `bitfield_b` (BitField3D or BitField4D): Second bit field

**Returns:**
- `BitField3D` or `BitField4D`: Superposition of the two bit fields

**Raises:**
- `TypeError`: If bitfields are not BitField3D or BitField4D instances
- `KTAError`: If bitfields have different dimensions or types

### `entangle(bitfield_a, bitfield_b)`

Creates an entanglement between two bit fields.

**Parameters:**
- `bitfield_a` (BitField3D or BitField4D): First bit field
- `bitfield_b` (BitField3D or BitField4D): Second bit field

**Returns:**
- `tuple`: Tuple containing (entangled_a, entangled_b)

**Raises:**
- `TypeError`: If bitfields are not BitField3D or BitField4D instances
- `KTAError`: If bitfields have different dimensions or types

## Visualization Functions

### `visualize3D(bitfield, layer=None)`

Visualizes a 3D bit field using ASCII representation.

**Parameters:**
- `bitfield` (BitField3D): Bit field to visualize
- `layer` (int, optional): Specific z-layer to visualize. If None, visualizes all layers.

**Returns:**
- `str`: ASCII visualization of the bit field

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance
- `DimensionError`: If layer is out of bounds

### `visualize4D(bitfield, time_point=None, layer=None)`

Visualizes a 4D bit field using ASCII representation.

**Parameters:**
- `bitfield` (BitField4D): Bit field to visualize
- `time_point` (int, optional): Specific t-coordinate to visualize. If None, visualizes all time points.
- `layer` (int, optional): Specific z-layer to visualize. If None, visualizes all layers.

**Returns:**
- `str`: ASCII visualization of the bit field

**Raises:**
- `TypeError`: If bitfield is not a BitField4D instance
- `DimensionError`: If time_point or layer is out of bounds

### `animateTransform(bitfield, frames=5)`

Creates an ASCII animation of a bit field transformation.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to animate
- `frames` (int): Number of frames to generate

**Returns:**
- `list`: List of ASCII frames

**Raises:**
- `TypeError`: If bitfield is not a BitField3D or BitField4D instance
- `ValueError`: If frames is less than 1

### `visualize3D_compact(bitfield)`

Creates a compact ASCII visualization of a 3D bit field.

**Parameters:**
- `bitfield` (BitField3D): Bit field to visualize

**Returns:**
- `str`: Compact ASCII visualization of the bit field

**Raises:**
- `TypeError`: If bitfield is not a BitField3D instance

### `visualize4D_compact(bitfield)`

Creates a compact ASCII visualization of a 4D bit field.

**Parameters:**
- `bitfield` (BitField4D): Bit field to visualize

**Returns:**
- `str`: Compact ASCII visualization of the bit field

**Raises:**
- `TypeError`: If bitfield is not a BitField4D instance

### `visualize_properties(bitfield, position)`

Visualizes the properties of a bit at the specified position.

**Parameters:**
- `bitfield` (BitField3D or BitField4D): Bit field to visualize
- `position` (tuple): Position of the bit (x, y, z) or (x, y, z, t)

**Returns:**
- `str`: ASCII visualization of the bit properties

**Raises:**
- `TypeError`: If bitfield is not a BitField3D or BitField4D instance
- `ValueError`: If position length doesn't match bitfield dimensions

## Exceptions

### `DimensionError`

Raised when an operation is attempted with invalid dimensions.

### `PatternError`

Raised when an operation on patterns fails.

### `KTAError`

Raised when a KTA operation fails.
