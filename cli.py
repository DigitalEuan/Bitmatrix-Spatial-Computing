#!/usr/bin/env python3
"""
BitMatrix Spatial Computing CLI

A command-line interface for interacting with the BitMatrix Spatial Computing framework.
This CLI provides a simple way to create, manipulate, and visualize BitMatrix structures.
"""

import argparse
import sys
import numpy as np
from bsc import (
    BitField3D, BitField4D,
    mapTo3D, mapTo4D, extractLinear,
    rotate3D, translate3D, scale3D, mirror3D,
    applyKineticTransform, superposition, entangle,
    findPattern, matchPattern, generatePattern,
    visualize3D, visualize4D, animateTransform
)

def create_bitfield(args):
    """Create a new bitfield with the specified dimensions."""
    dimensions = args.dimensions
    
    if len(dimensions) == 3:
        # Create 3D bitfield
        x_dim, y_dim, z_dim = dimensions
        bitfield = BitField3D(x_dim, y_dim, z_dim)
        print(f"Created 3D bitfield with dimensions {x_dim}×{y_dim}×{z_dim}")
        
        # Initialize with pattern if specified
        if args.pattern:
            pattern_bitfield = generatePattern(args.pattern, dimensions)
            # Copy pattern to bitfield
            for x in range(x_dim):
                for y in range(y_dim):
                    for z in range(z_dim):
                        bitfield.setBit(x, y, z, pattern_bitfield.getBit(x, y, z))
            print(f"Initialized with '{args.pattern}' pattern")
        
        # Visualize if requested
        if args.visualize:
            print("\n" + visualize3D(bitfield))
    
    elif len(dimensions) == 4:
        # Create 4D bitfield
        x_dim, y_dim, z_dim, t_dim = dimensions
        bitfield = BitField4D(x_dim, y_dim, z_dim, t_dim)
        print(f"Created 4D bitfield with dimensions {x_dim}×{y_dim}×{z_dim}×{t_dim}")
        
        # Initialize with pattern if specified
        if args.pattern:
            pattern_bitfield = generatePattern(args.pattern, dimensions)
            # Copy pattern to bitfield
            for t in range(t_dim):
                for x in range(x_dim):
                    for y in range(y_dim):
                        for z in range(z_dim):
                            bitfield.setBit(x, y, z, t, pattern_bitfield.getBit(x, y, z, t))
            print(f"Initialized with '{args.pattern}' pattern")
        
        # Visualize if requested
        if args.visualize:
            print("\n" + visualize4D(bitfield))
    
    else:
        print("Error: Dimensions must be either 3 (x,y,z) or 4 (x,y,z,t)")
        return

def transform_bitfield(args):
    """Apply a transformation to a bitfield."""
    # Create a sample bitfield for demonstration
    if args.dimensions:
        dimensions = args.dimensions
    else:
        dimensions = [4, 4, 4]  # Default dimensions
    
    # Create bitfield with pattern
    if len(dimensions) == 3:
        pattern_bitfield = generatePattern('cube', dimensions)
        bitfield = pattern_bitfield
        print(f"Created 3D bitfield with dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}")
    elif len(dimensions) == 4:
        pattern_bitfield = generatePattern('cube', dimensions)
        bitfield = pattern_bitfield
        print(f"Created 4D bitfield with dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}×{dimensions[3]}")
    else:
        print("Error: Dimensions must be either 3 (x,y,z) or 4 (x,y,z,t)")
        return
    
    # Apply transformation
    if args.transform_type == 'rotate':
        if len(dimensions) != 3:
            print("Error: Rotation is only supported for 3D bitfields")
            return
        
        axis = args.axis if args.axis else 'z'
        angle = args.angle if args.angle else 90
        
        print(f"Original bitfield:")
        print(visualize3D(bitfield))
        
        transformed = rotate3D(bitfield, axis, angle)
        
        print(f"\nRotated bitfield (axis={axis}, angle={angle}):")
        print(visualize3D(transformed))
    
    elif args.transform_type == 'translate':
        if len(dimensions) != 3:
            print("Error: Translation is only supported for 3D bitfields")
            return
        
        vector = args.vector if args.vector else [1, 1, 1]
        
        print(f"Original bitfield:")
        print(visualize3D(bitfield))
        
        transformed = translate3D(bitfield, vector)
        
        print(f"\nTranslated bitfield (vector={vector}):")
        print(visualize3D(transformed))
    
    elif args.transform_type == 'scale':
        if len(dimensions) != 3:
            print("Error: Scaling is only supported for 3D bitfields")
            return
        
        factors = args.factors if args.factors else [1.5, 1.5, 1.5]
        
        print(f"Original bitfield:")
        print(visualize3D(bitfield))
        
        transformed = scale3D(bitfield, factors)
        
        print(f"\nScaled bitfield (factors={factors}):")
        print(visualize3D(transformed))
    
    elif args.transform_type == 'mirror':
        if len(dimensions) != 3:
            print("Error: Mirroring is only supported for 3D bitfields")
            return
        
        plane = args.plane if args.plane else 'xy'
        
        print(f"Original bitfield:")
        print(visualize3D(bitfield))
        
        transformed = mirror3D(bitfield, plane)
        
        print(f"\nMirrored bitfield (plane={plane}):")
        print(visualize3D(transformed))
    
    elif args.transform_type == 'kta':
        kta_type = args.kta_type if args.kta_type else 'wave'
        
        if len(dimensions) == 3:
            print(f"Original bitfield:")
            print(visualize3D(bitfield))
            
            transformed = applyKineticTransform(bitfield, kta_type)
            
            print(f"\nKTA transformed bitfield (type={kta_type}):")
            print(visualize3D(transformed))
        else:
            print(f"Original bitfield:")
            print(visualize4D(bitfield))
            
            transformed = applyKineticTransform(bitfield, kta_type)
            
            print(f"\nKTA transformed bitfield (type={kta_type}):")
            print(visualize4D(transformed))
    
    else:
        print(f"Error: Unknown transformation type '{args.transform_type}'")

def generate_pattern_cmd(args):
    """Generate a pattern with the specified type and dimensions."""
    dimensions = args.dimensions
    pattern_type = args.pattern_type
    
    if len(dimensions) not in (3, 4):
        print("Error: Dimensions must be either 3 (x,y,z) or 4 (x,y,z,t)")
        return
    
    try:
        pattern = generatePattern(pattern_type, dimensions)
        
        if len(dimensions) == 3:
            print(f"Generated '{pattern_type}' pattern with dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}:")
            print(visualize3D(pattern))
        else:
            print(f"Generated '{pattern_type}' pattern with dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}×{dimensions[3]}:")
            print(visualize4D(pattern))
    
    except Exception as e:
        print(f"Error generating pattern: {e}")

def animate_transform(args):
    """Animate a transformation on a bitfield."""
    # Create a sample bitfield for demonstration
    if args.dimensions:
        dimensions = args.dimensions
    else:
        dimensions = [4, 4, 4]  # Default dimensions
    
    # Create bitfield with pattern
    pattern_type = args.pattern_type if args.pattern_type else 'cube'
    
    if len(dimensions) == 3:
        bitfield = generatePattern(pattern_type, dimensions)
        print(f"Created 3D bitfield with '{pattern_type}' pattern and dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}")
    elif len(dimensions) == 4:
        bitfield = generatePattern(pattern_type, dimensions)
        print(f"Created 4D bitfield with '{pattern_type}' pattern and dimensions {dimensions[0]}×{dimensions[1]}×{dimensions[2]}×{dimensions[3]}")
    else:
        print("Error: Dimensions must be either 3 (x,y,z) or 4 (x,y,z,t)")
        return
    
    # Generate animation frames
    frames = args.frames if args.frames else 5
    animation = animateTransform(bitfield, frames)
    
    # Display animation
    print("\nAnimation frames:")
    for i, frame in enumerate(animation):
        print(f"\n--- Frame {i+1}/{len(animation)} ---")
        print(frame)
        
        # Pause between frames in interactive mode
        if not args.no_pause and i < len(animation) - 1:
            input("Press Enter for next frame...")

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(description='BitMatrix Spatial Computing CLI')
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Create command
    create_parser = subparsers.add_parser('create', help='Create a new bitfield')
    create_parser.add_argument('dimensions', type=int, nargs='+', help='Dimensions of the bitfield (3 or 4 values)')
    create_parser.add_argument('--pattern', choices=['cube', 'sphere', 'wave', 'random'], help='Initialize with a pattern')
    create_parser.add_argument('--visualize', action='store_true', help='Visualize the created bitfield')
    
    # Transform command
    transform_parser = subparsers.add_parser('transform', help='Apply a transformation to a bitfield')
    transform_parser.add_argument('transform_type', choices=['rotate', 'translate', 'scale', 'mirror', 'kta'], help='Type of transformation')
    transform_parser.add_argument('--dimensions', type=int, nargs='+', help='Dimensions of the bitfield (3 or 4 values)')
    transform_parser.add_argument('--axis', choices=['x', 'y', 'z'], help='Rotation axis (for rotate)')
    transform_parser.add_argument('--angle', type=float, help='Rotation angle in degrees (for rotate)')
    transform_parser.add_argument('--vector', type=int, nargs=3, help='Translation vector (for translate)')
    transform_parser.add_argument('--factors', type=float, nargs=3, help='Scale factors (for scale)')
    transform_parser.add_argument('--plane', choices=['xy', 'xz', 'yz'], help='Mirror plane (for mirror)')
    transform_parser.add_argument('--kta-type', choices=['wave', 'fractal', 'recursive'], help='KTA transform type (for kta)')
    
    # Pattern command
    pattern_parser = subparsers.add_parser('pattern', help='Generate a pattern')
    pattern_parser.add_argument('pattern_type', choices=['cube', 'sphere', 'wave', 'random'], help='Type of pattern')
    pattern_parser.add_argument('dimensions', type=int, nargs='+', help='Dimensions of the pattern (3 or 4 values)')
    
    # Animate command
    animate_parser = subparsers.add_parser('animate', help='Animate a transformation')
    animate_parser.add_argument('--dimensions', type=int, nargs='+', help='Dimensions of the bitfield (3 or 4 values)')
    animate_parser.add_argument('--pattern-type', choices=['cube', 'sphere', 'wave', 'random'], help='Type of pattern')
    animate_parser.add_argument('--frames', type=int, help='Number of animation frames')
    animate_parser.add_argument('--no-pause', action='store_true', help='Do not pause between frames')
    
    # Parse arguments
    args = parser.parse_args()
    
    # Execute command
    if args.command == 'create':
        create_bitfield(args)
    elif args.command == 'transform':
        transform_bitfield(args)
    elif args.command == 'pattern':
        generate_pattern_cmd(args)
    elif args.command == 'animate':
        animate_transform(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
