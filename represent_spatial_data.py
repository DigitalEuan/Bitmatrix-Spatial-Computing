#!/usr/bin/env python3
"""
Spatial Data Representation Examples for BitMatrix Spatial Computing

This script demonstrates how to represent various types of spatial data
using the BitMatrix Spatial Computing framework.
"""

import sys
import numpy as np
import math
from bsc import (
    BitField3D, BitField4D,
    mapTo3D, mapTo4D, extractLinear,
    rotate3D, translate3D, scale3D,
    generatePattern,
    visualize3D, visualize4D
)

def example_represent_3d_object():
    """Example of representing a 3D object (cube) in a BitField3D."""
    print("=== Representing a 3D Object (Cube) ===")
    
    # Create a 3D bitfield for a cube
    size = 8
    cube = BitField3D(size, size, size)
    
    # Set bits to represent the cube's faces
    for i in range(size):
        for j in range(size):
            # Front face (z=0)
            cube.setBit(i, j, 0, 1)
            # Back face (z=size-1)
            cube.setBit(i, j, size-1, 1)
            # Left face (x=0)
            cube.setBit(0, i, j, 1)
            # Right face (x=size-1)
            cube.setBit(size-1, i, j, 1)
            # Bottom face (y=0)
            cube.setBit(i, 0, j, 1)
            # Top face (y=size-1)
            cube.setBit(i, size-1, j, 1)
    
    # Visualize the cube
    print("\nCube representation:")
    print(visualize3D(cube))
    
    # Add properties to specific vertices
    cube.setProperty(0, 0, 0, "vertex", "front-bottom-left")
    cube.setProperty(size-1, 0, 0, "vertex", "front-bottom-right")
    cube.setProperty(0, size-1, 0, "vertex", "front-top-left")
    cube.setProperty(size-1, size-1, 0, "vertex", "front-top-right")
    cube.setProperty(0, 0, size-1, "vertex", "back-bottom-left")
    cube.setProperty(size-1, 0, size-1, "vertex", "back-bottom-right")
    cube.setProperty(0, size-1, size-1, "vertex", "back-top-left")
    cube.setProperty(size-1, size-1, size-1, "vertex", "back-top-right")
    
    # Print vertex properties
    print("\nVertex properties:")
    for x, y, z in [(0,0,0), (size-1,0,0), (0,size-1,0), (size-1,size-1,0),
                    (0,0,size-1), (size-1,0,size-1), (0,size-1,size-1), (size-1,size-1,size-1)]:
        print(f"Vertex at ({x},{y},{z}): {cube.getProperty(x, y, z, 'vertex')}")
    
    return cube

def example_represent_terrain():
    """Example of representing terrain elevation data in a BitField3D."""
    print("\n=== Representing Terrain Elevation Data ===")
    
    # Create a 3D bitfield for terrain
    width, length = 10, 10
    max_height = 5
    terrain = BitField3D(width, length, max_height)
    
    # Generate a simple terrain with a hill in the middle
    print("\nGenerating terrain with a hill in the middle:")
    center_x, center_y = width // 2, length // 2
    
    for x in range(width):
        for y in range(length):
            # Calculate distance from center
            distance = math.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # Calculate height based on distance (creating a hill)
            height = max(0, int(max_height - distance))
            
            # Set bits from ground up to the calculated height
            for z in range(height):
                terrain.setBit(x, y, z, 1)
            
            # Store the elevation as a property
            terrain.setProperty(x, y, 0, "elevation", height)
    
    # Visualize the terrain
    print(visualize3D(terrain))
    
    # Print elevation data for a few points
    print("\nElevation data:")
    for x, y in [(0,0), (center_x, center_y), (width-1, length-1)]:
        print(f"Elevation at ({x},{y}): {terrain.getProperty(x, y, 0, 'elevation')}")
    
    return terrain

def example_represent_voxel_data():
    """Example of representing voxel data in a BitField3D."""
    print("\n=== Representing Voxel Data ===")
    
    # Create a 3D bitfield for voxel data
    size = 6
    voxel_model = BitField3D(size, size, size)
    
    # Create a simple voxel model (a sphere)
    print("\nCreating a sphere voxel model:")
    center = size // 2
    radius = size // 2 - 1
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # Calculate distance from center
                distance = math.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
                
                # Set bit if point is within the sphere
                if distance <= radius:
                    voxel_model.setBit(x, y, z, 1)
                    
                    # Add material property based on position
                    if distance < radius / 2:
                        voxel_model.setProperty(x, y, z, "material", "core")
                    else:
                        voxel_model.setProperty(x, y, z, "material", "shell")
    
    # Visualize the voxel model
    print(visualize3D(voxel_model))
    
    # Count voxels by material
    core_count = 0
    shell_count = 0
    
    for x in range(size):
        for y in range(size):
            for z in range(size):
                if voxel_model.getBit(x, y, z) == 1:
                    material = voxel_model.getProperty(x, y, z, "material")
                    if material == "core":
                        core_count += 1
                    elif material == "shell":
                        shell_count += 1
    
    print(f"\nVoxel counts by material:")
    print(f"Core: {core_count}")
    print(f"Shell: {shell_count}")
    print(f"Total: {core_count + shell_count}")
    
    return voxel_model

def example_represent_4d_spacetime():
    """Example of representing 4D spacetime data in a BitField4D."""
    print("\n=== Representing 4D Spacetime Data ===")
    
    # Create a 4D bitfield for spacetime data
    size_x, size_y, size_z = 6, 6, 6
    time_steps = 4
    spacetime = BitField4D(size_x, size_y, size_z, time_steps)
    
    # Create a simple moving object through time
    print("\nCreating a moving object through time:")
    
    # Define object positions at each time step
    positions = [
        (1, 1, 1),  # Starting position at t=0
        (2, 2, 2),  # Position at t=1
        (3, 3, 3),  # Position at t=2
        (4, 4, 4)   # Position at t=3
    ]
    
    # Set bits to represent the object at each time step
    for t, (center_x, center_y, center_z) in enumerate(positions):
        # Create a small cube at each position
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                for dz in range(-1, 2):
                    x, y, z = center_x + dx, center_y + dy, center_z + dz
                    
                    # Check bounds
                    if (0 <= x < size_x and 0 <= y < size_y and 0 <= z < size_z):
                        spacetime.setBit(x, y, z, t, 1)
                        
                        # Add velocity property
                        if t < time_steps - 1:
                            next_x, next_y, next_z = positions[t+1]
                            velocity = math.sqrt((next_x - center_x)**2 + 
                                                (next_y - center_y)**2 + 
                                                (next_z - center_z)**2)
                            spacetime.setProperty(x, y, z, t, "velocity", velocity)
    
    # Visualize the spacetime data
    print(visualize4D(spacetime))
    
    # Print velocity at each time step
    print("\nVelocity at each time step:")
    for t, (center_x, center_y, center_z) in enumerate(positions):
        if t < time_steps - 1:
            velocity = spacetime.getProperty(center_x, center_y, center_z, t, "velocity")
            print(f"Time t={t}: Velocity = {velocity}")
    
    return spacetime

def example_map_linear_data():
    """Example of mapping linear data to BitMatrix structures."""
    print("\n=== Mapping Linear Data to BitMatrix Structures ===")
    
    # Create linear data (1D array)
    print("\nCreating linear data (1D array):")
    linear_data = [0] * 27  # 3x3x3 cube
    
    # Set some values in the linear data
    linear_data[0] = 1   # (0,0,0)
    linear_data[4] = 1   # (1,1,0)
    linear_data[26] = 1  # (2,2,2)
    
    print(f"Linear data: {linear_data}")
    
    # Map to 3D bitfield
    print("\nMapping to 3D bitfield (3x3x3):")
    bitfield3d = mapTo3D(linear_data, 3, 3, 3)
    print(visualize3D(bitfield3d))
    
    # Verify the mapping
    print("\nVerifying the mapping:")
    print(f"Bit at (0,0,0): {bitfield3d.getBit(0, 0, 0)} (should be 1)")
    print(f"Bit at (1,1,0): {bitfield3d.getBit(1, 1, 0)} (should be 1)")
    print(f"Bit at (2,2,2): {bitfield3d.getBit(2, 2, 2)} (should be 1)")
    
    # Extract back to linear data
    print("\nExtracting back to linear data:")
    extracted_data = extractLinear(bitfield3d)
    print(f"Extracted data: {extracted_data}")
    print(f"Original data:  {linear_data}")
    print(f"Match: {extracted_data == linear_data}")
    
    return bitfield3d

def main():
    """Main function to run all examples."""
    print("BitMatrix Spatial Computing - Spatial Data Representation Examples")
    print("=" * 70)
    
    # Run examples
    cube = example_represent_3d_object()
    terrain = example_represent_terrain()
    voxel_model = example_represent_voxel_data()
    spacetime = example_represent_4d_spacetime()
    mapped_data = example_map_linear_data()
    
    print("\nAll spatial data representation examples completed successfully!")

if __name__ == "__main__":
    main()
