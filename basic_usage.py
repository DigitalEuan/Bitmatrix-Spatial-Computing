#!/usr/bin/env python3
"""
Basic Usage Examples for BitMatrix Spatial Computing

This script demonstrates the basic usage of the BitMatrix Spatial Computing framework,
including creating bitfields, manipulating bits, and applying transformations.
"""

import sys
import numpy as np
from bsc import (
    BitField3D, BitField4D,
    rotate3D, translate3D, scale3D, mirror3D,
    visualize3D, visualize4D
)

def example_create_bitfields():
    """Example of creating 3D and 4D bitfields."""
    print("=== Creating BitFields ===")
    
    # Create a 3D bitfield
    print("\nCreating a 3D bitfield (4×4×2):")
    bitfield3d = BitField3D(4, 4, 2)
    print(visualize3D(bitfield3d))
    
    # Create a 4D bitfield
    print("\nCreating a 4D bitfield (4×4×2×2):")
    bitfield4d = BitField4D(4, 4, 2, 2)
    print(visualize4D(bitfield4d))
    
    return bitfield3d, bitfield4d

def example_set_get_bits(bitfield3d, bitfield4d):
    """Example of setting and getting bits in bitfields."""
    print("\n=== Setting and Getting Bits ===")
    
    # Set bits in 3D bitfield
    print("\nSetting bits in 3D bitfield:")
    bitfield3d.setBit(0, 0, 0, 1)
    bitfield3d.setBit(3, 3, 1, 1)
    bitfield3d.setBit(1, 2, 0, 1)
    print(visualize3D(bitfield3d))
    
    # Get bits from 3D bitfield
    print("\nGetting bits from 3D bitfield:")
    print(f"Bit at (0,0,0): {bitfield3d.getBit(0, 0, 0)}")
    print(f"Bit at (1,1,0): {bitfield3d.getBit(1, 1, 0)}")
    print(f"Bit at (3,3,1): {bitfield3d.getBit(3, 3, 1)}")
    
    # Set bits in 4D bitfield
    print("\nSetting bits in 4D bitfield:")
    bitfield4d.setBit(0, 0, 0, 0, 1)
    bitfield4d.setBit(3, 3, 1, 1, 1)
    bitfield4d.setBit(1, 2, 0, 1, 1)
    print(visualize4D(bitfield4d))
    
    # Get bits from 4D bitfield
    print("\nGetting bits from 4D bitfield:")
    print(f"Bit at (0,0,0,0): {bitfield4d.getBit(0, 0, 0, 0)}")
    print(f"Bit at (1,2,0,1): {bitfield4d.getBit(1, 2, 0, 1)}")
    print(f"Bit at (3,3,1,1): {bitfield4d.getBit(3, 3, 1, 1)}")

def example_properties(bitfield3d, bitfield4d):
    """Example of setting and getting properties in bitfields."""
    print("\n=== Working with Properties ===")
    
    # Set properties in 3D bitfield
    print("\nSetting properties in 3D bitfield:")
    bitfield3d.setProperty(0, 0, 0, "color", "red")
    bitfield3d.setProperty(3, 3, 1, "weight", 0.75)
    bitfield3d.setProperty(1, 2, 0, "label", "important")
    
    # Get properties from 3D bitfield
    print("\nGetting properties from 3D bitfield:")
    print(f"Property 'color' at (0,0,0): {bitfield3d.getProperty(0, 0, 0, 'color')}")
    print(f"Property 'weight' at (3,3,1): {bitfield3d.getProperty(3, 3, 1, 'weight')}")
    print(f"Property 'label' at (1,2,0): {bitfield3d.getProperty(1, 2, 0, 'label')}")
    
    # Get all property names
    print("\nAll property names at (0,0,0):", bitfield3d.getPropertyNames(0, 0, 0))
    
    # Set properties in 4D bitfield
    print("\nSetting properties in 4D bitfield:")
    bitfield4d.setProperty(0, 0, 0, 0, "color", "blue")
    bitfield4d.setProperty(3, 3, 1, 1, "weight", 0.5)
    bitfield4d.setProperty(1, 2, 0, 1, "label", "critical")
    
    # Get properties from 4D bitfield
    print("\nGetting properties from 4D bitfield:")
    print(f"Property 'color' at (0,0,0,0): {bitfield4d.getProperty(0, 0, 0, 0, 'color')}")
    print(f"Property 'weight' at (3,3,1,1): {bitfield4d.getProperty(3, 3, 1, 1, 'weight')}")
    print(f"Property 'label' at (1,2,0,1): {bitfield4d.getProperty(1, 2, 0, 1, 'label')}")

def example_spatial_transformations():
    """Example of applying spatial transformations to bitfields."""
    print("\n=== Spatial Transformations ===")
    
    # Create a 3D bitfield with a simple pattern
    print("\nCreating a 3D bitfield with a pattern:")
    bitfield = BitField3D(4, 4, 2)
    
    # Set bits to create a simple pattern
    for x in range(4):
        bitfield.setBit(x, 0, 0, 1)  # Bottom edge
        bitfield.setBit(0, x, 0, 1)  # Left edge
        bitfield.setBit(3, x, 0, 1)  # Right edge
        bitfield.setBit(x, 3, 0, 1)  # Top edge
    
    print(visualize3D(bitfield))
    
    # Rotate the bitfield
    print("\nRotating the bitfield 90 degrees around the z-axis:")
    rotated = rotate3D(bitfield, 'z', 90)
    print(visualize3D(rotated))
    
    # Translate the bitfield
    print("\nTranslating the bitfield by vector [1, 1, 0]:")
    translated = translate3D(bitfield, [1, 1, 0])
    print(visualize3D(translated))
    
    # Scale the bitfield
    print("\nScaling the bitfield by factors [1.5, 1.5, 1.0]:")
    scaled = scale3D(bitfield, [1.5, 1.5, 1.0])
    print(visualize3D(scaled))
    
    # Mirror the bitfield
    print("\nMirroring the bitfield across the xy plane:")
    mirrored = mirror3D(bitfield, 'xy')
    print(visualize3D(mirrored))

def example_copy_bitfields(bitfield3d, bitfield4d):
    """Example of copying bitfields."""
    print("\n=== Copying BitFields ===")
    
    # Copy 3D bitfield
    print("\nCopying 3D bitfield:")
    copy3d = bitfield3d.copy()
    print("Original 3D bitfield:")
    print(visualize3D(bitfield3d))
    print("Copied 3D bitfield:")
    print(visualize3D(copy3d))
    
    # Modify the copy and show both are independent
    print("\nModifying the copy (setting bit at (2,2,1) to 1):")
    copy3d.setBit(2, 2, 1, 1)
    print("Original 3D bitfield (unchanged):")
    print(visualize3D(bitfield3d))
    print("Modified copy:")
    print(visualize3D(copy3d))
    
    # Copy 4D bitfield
    print("\nCopying 4D bitfield:")
    copy4d = bitfield4d.copy()
    print("Original 4D bitfield:")
    print(visualize4D(bitfield4d))
    print("Copied 4D bitfield:")
    print(visualize4D(copy4d))

def main():
    """Main function to run all examples."""
    print("BitMatrix Spatial Computing - Basic Usage Examples")
    print("=" * 50)
    
    # Run examples
    bitfield3d, bitfield4d = example_create_bitfields()
    example_set_get_bits(bitfield3d, bitfield4d)
    example_properties(bitfield3d, bitfield4d)
    example_spatial_transformations()
    example_copy_bitfields(bitfield3d, bitfield4d)
    
    print("\nAll examples completed successfully!")

if __name__ == "__main__":
    main()
