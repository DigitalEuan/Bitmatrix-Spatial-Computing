"""
Core BitMatrix classes for 3D and 4D spatial computing.

These classes implement the foundational data structures for the BitMatrix
Spatial Computing framework, enabling representation of data in three or
four dimensions with extended properties beyond simple binary values.
"""

import numpy as np
from .exceptions import CoordinateError, PropertyError

class BitField3D:
    """
    Implementation of a 3D bitfield for the BitMatrix architecture.
    
    This class provides a three-dimensional data structure where each "bit"
    can have associated properties beyond its binary value, enabling complex
    spatial representations and operations.
    """
    def __init__(self, x_dim, y_dim, z_dim):
        """
        Initialize a 3D bitfield with the specified dimensions.
        
        Args:
            x_dim (int): Number of bits in the x dimension
            y_dim (int): Number of bits in the y dimension
            z_dim (int): Number of bits in the z dimension
        """
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        
        # Initialize bit storage (using a 3D numpy array for efficiency)
        self.bits = np.zeros((x_dim, y_dim, z_dim), dtype=np.uint8)
        
        # Initialize property storage (using a dictionary for flexibility)
        self.properties = {}
    
    def getBit(self, x, y, z):
        """
        Get the bit value at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            
        Returns:
            int: Bit value (0 or 1)
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        return int(self.bits[x, y, z])
    
    def setBit(self, x, y, z, value):
        """
        Set the bit value at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            value (int): Bit value (0 or 1)
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        self.bits[x, y, z] = 1 if value else 0
    
    def setProperty(self, x, y, z, property_name, property_value):
        """
        Set a property for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            property_name (str): Name of the property
            property_value: Value of the property
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z)
        
        # Initialize property dictionary for this position if it doesn't exist
        if pos_key not in self.properties:
            self.properties[pos_key] = {}
        
        # Set the property
        self.properties[pos_key][property_name] = property_value
    
    def getProperty(self, x, y, z, property_name):
        """
        Get a property for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            property_name (str): Name of the property
            
        Returns:
            The value of the property
            
        Raises:
            CoordinateError: If coordinates are out of bounds
            PropertyError: If property doesn't exist
        """
        if not self._validate_coordinates(x, y, z):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z)
        
        # Check if property exists
        if pos_key not in self.properties or property_name not in self.properties[pos_key]:
            raise PropertyError(f"Property '{property_name}' not found at coordinates ({x}, {y}, {z})")
        
        return self.properties[pos_key][property_name]
    
    def getPropertyNames(self, x, y, z):
        """
        Get all property names for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            
        Returns:
            list: List of property names
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z)
        
        # Return property names or empty list if none exist
        if pos_key in self.properties:
            return list(self.properties[pos_key].keys())
        else:
            return []
    
    def getDimensions(self):
        """
        Get the dimensions of the bitfield.
        
        Returns:
            tuple: Tuple containing (x_dim, y_dim, z_dim)
        """
        return (self.x_dim, self.y_dim, self.z_dim)
    
    def copy(self):
        """
        Create a deep copy of this bitfield.
        
        Returns:
            BitField3D: New BitField3D instance with the same data
        """
        new_bitfield = BitField3D(self.x_dim, self.y_dim, self.z_dim)
        new_bitfield.bits = np.copy(self.bits)
        
        # Deep copy properties
        for pos_key, props in self.properties.items():
            new_bitfield.properties[pos_key] = props.copy()
        
        return new_bitfield
    
    def _validate_coordinates(self, x, y, z):
        """
        Validate that the given coordinates are within bounds.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            
        Returns:
            bool: True if coordinates are valid, False otherwise
        """
        return (0 <= x < self.x_dim and 
                0 <= y < self.y_dim and 
                0 <= z < self.z_dim)
    
    def __str__(self):
        """
        Return a string representation of the bitfield.
        
        Returns:
            str: ASCII representation of the bitfield
        """
        result = f"BitField3D({self.x_dim}×{self.y_dim}×{self.z_dim})\n"
        
        for z in range(self.z_dim):
            result += f"Layer z={z}:\n"
            result += "+{}+\n".format("-" * self.x_dim)
            
            for y in range(self.y_dim):
                row = "|"
                for x in range(self.x_dim):
                    row += str(self.bits[x, y, z])
                row += "|\n"
                result += row
            
            result += "+{}+\n".format("-" * self.x_dim)
        
        return result


class BitField4D:
    """
    Implementation of a 4D bitfield for the BitMatrix architecture.
    
    This class extends the 3D bitfield to include a temporal dimension,
    enabling representation of time-varying data within the BitMatrix framework.
    """
    def __init__(self, x_dim, y_dim, z_dim, t_dim):
        """
        Initialize a 4D bitfield with the specified dimensions.
        
        Args:
            x_dim (int): Number of bits in the x dimension
            y_dim (int): Number of bits in the y dimension
            z_dim (int): Number of bits in the z dimension
            t_dim (int): Number of bits in the t (time) dimension
        """
        self.x_dim = x_dim
        self.y_dim = y_dim
        self.z_dim = z_dim
        self.t_dim = t_dim
        
        # Initialize bit storage (using a 4D numpy array for efficiency)
        self.bits = np.zeros((x_dim, y_dim, z_dim, t_dim), dtype=np.uint8)
        
        # Initialize property storage (using a dictionary for flexibility)
        self.properties = {}
    
    def getBit(self, x, y, z, t):
        """
        Get the bit value at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            
        Returns:
            int: Bit value (0 or 1)
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z, t):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}, {t}) out of bounds")
        
        return int(self.bits[x, y, z, t])
    
    def setBit(self, x, y, z, t, value):
        """
        Set the bit value at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            value (int): Bit value (0 or 1)
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z, t):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}, {t}) out of bounds")
        
        self.bits[x, y, z, t] = 1 if value else 0
    
    def setProperty(self, x, y, z, t, property_name, property_value):
        """
        Set a property for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            property_name (str): Name of the property
            property_value: Value of the property
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z, t):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}, {t}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z, t)
        
        # Initialize property dictionary for this position if it doesn't exist
        if pos_key not in self.properties:
            self.properties[pos_key] = {}
        
        # Set the property
        self.properties[pos_key][property_name] = property_value
    
    def getProperty(self, x, y, z, t, property_name):
        """
        Get a property for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            property_name (str): Name of the property
            
        Returns:
            The value of the property
            
        Raises:
            CoordinateError: If coordinates are out of bounds
            PropertyError: If property doesn't exist
        """
        if not self._validate_coordinates(x, y, z, t):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}, {t}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z, t)
        
        # Check if property exists
        if pos_key not in self.properties or property_name not in self.properties[pos_key]:
            raise PropertyError(f"Property '{property_name}' not found at coordinates ({x}, {y}, {z}, {t})")
        
        return self.properties[pos_key][property_name]
    
    def getPropertyNames(self, x, y, z, t):
        """
        Get all property names for the bit at the specified coordinates.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            
        Returns:
            list: List of property names
            
        Raises:
            CoordinateError: If coordinates are out of bounds
        """
        if not self._validate_coordinates(x, y, z, t):
            raise CoordinateError(f"Coordinates ({x}, {y}, {z}, {t}) out of bounds")
        
        # Create position key
        pos_key = (x, y, z, t)
        
        # Return property names or empty list if none exist
        if pos_key in self.properties:
            return list(self.properties[pos_key].keys())
        else:
            return []
    
    def getDimensions(self):
        """
        Get the dimensions of the bitfield.
        
        Returns:
            tuple: Tuple containing (x_dim, y_dim, z_dim, t_dim)
        """
        return (self.x_dim, self.y_dim, self.z_dim, self.t_dim)
    
    def copy(self):
        """
        Create a deep copy of this bitfield.
        
        Returns:
            BitField4D: New BitField4D instance with the same data
        """
        new_bitfield = BitField4D(self.x_dim, self.y_dim, self.z_dim, self.t_dim)
        new_bitfield.bits = np.copy(self.bits)
        
        # Deep copy properties
        for pos_key, props in self.properties.items():
            new_bitfield.properties[pos_key] = props.copy()
        
        return new_bitfield
    
    def _validate_coordinates(self, x, y, z, t):
        """
        Validate that the given coordinates are within bounds.
        
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            z (int): Z coordinate
            t (int): T (time) coordinate
            
        Returns:
            bool: True if coordinates are valid, False otherwise
        """
        return (0 <= x < self.x_dim and 
                0 <= y < self.y_dim and 
                0 <= z < self.z_dim and
                0 <= t < self.t_dim)
    
    def __str__(self):
        """
        Return a string representation of the bitfield.
        
        Returns:
            str: ASCII representation of the bitfield
        """
        result = f"BitField4D({self.x_dim}×{self.y_dim}×{self.z_dim}×{self.t_dim})\n"
        
        for t in range(self.t_dim):
            result += f"Time t={t}:\n"
            
            for z in range(self.z_dim):
                result += f"  Layer z={z}:\n"
                result += "  +{}+\n".format("-" * self.x_dim)
                
                for y in range(self.y_dim):
                    row = "  |"
                    for x in range(self.x_dim):
                        row += str(self.bits[x, y, z, t])
                    row += "|\n"
                    result += row
                
                result += "  +{}+\n".format("-" * self.x_dim)
        
        return result
