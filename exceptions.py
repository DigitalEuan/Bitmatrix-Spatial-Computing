"""
Custom exceptions for the BitMatrix Spatial Computing framework.
"""

class BitMatrixError(Exception):
    """Base exception class for all BitMatrix errors."""
    pass

class DimensionError(BitMatrixError):
    """Exception raised for errors in dimension specifications."""
    pass

class CoordinateError(BitMatrixError):
    """Exception raised for errors in coordinate specifications."""
    pass

class PropertyError(BitMatrixError):
    """Exception raised for errors in property operations."""
    pass

class TransformError(BitMatrixError):
    """Exception raised for errors in transformation operations."""
    pass

class PatternError(BitMatrixError):
    """Exception raised for errors in pattern operations."""
    pass

class KTAError(BitMatrixError):
    """Exception raised for errors in KTA operations."""
    pass
