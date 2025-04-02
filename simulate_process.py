#!/usr/bin/env python3
"""
Process Simulation Examples for BitMatrix Spatial Computing

This script demonstrates how to simulate various processes using the
BitMatrix Spatial Computing framework, including cellular automata,
diffusion processes, and wave propagation.
"""

import sys
import numpy as np
import time
from bsc import (
    BitField3D, BitField4D,
    applyKineticTransform, superposition, entangle,
    generatePattern,
    visualize3D, visualize4D, animateTransform
)

def example_cellular_automaton():
    """Example of simulating a 3D cellular automaton."""
    print("=== Simulating a 3D Cellular Automaton ===")
    
    # Create a 3D bitfield for the cellular automaton
    size = 8
    automaton = BitField3D(size, size, size)
    
    # Initialize with a simple pattern (a small cube in the center)
    print("\nInitializing with a small cube in the center:")
    center = size // 2
    for x in range(center-1, center+2):
        for y in range(center-1, center+2):
            for z in range(center-1, center+2):
                automaton.setBit(x, y, z, 1)
    
    print(visualize3D(automaton))
    
    # Define the cellular automaton rules
    # Rule: A cell is alive if it has 4-6 alive neighbors
    # Rule: A dead cell becomes alive if it has exactly 3 alive neighbors
    
    # Run the simulation for several generations
    generations = 3
    print(f"\nRunning simulation for {generations} generations:")
    
    for generation in range(generations):
        # Create a new bitfield for the next generation
        next_gen = automaton.copy()
        
        # Apply the rules to each cell
        for x in range(1, size-1):  # Skip border cells for simplicity
            for y in range(1, size-1):
                for z in range(1, size-1):
                    # Count alive neighbors
                    alive_neighbors = 0
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            for dz in [-1, 0, 1]:
                                if dx == 0 and dy == 0 and dz == 0:
                                    continue  # Skip the cell itself
                                if automaton.getBit(x+dx, y+dy, z+dz) == 1:
                                    alive_neighbors += 1
                    
                    # Apply rules
                    current_state = automaton.getBit(x, y, z)
                    if current_state == 1:
                        # Cell is alive
                        if alive_neighbors < 4 or alive_neighbors > 6:
                            next_gen.setBit(x, y, z, 0)  # Cell dies
                    else:
                        # Cell is dead
                        if alive_neighbors == 3:
                            next_gen.setBit(x, y, z, 1)  # Cell becomes alive
        
        # Update the automaton for the next generation
        automaton = next_gen
        
        # Visualize the current generation
        print(f"\nGeneration {generation+1}:")
        print(visualize3D(automaton))
    
    return automaton

def example_diffusion_process():
    """Example of simulating a diffusion process."""
    print("\n=== Simulating a Diffusion Process ===")
    
    # Create a 3D bitfield for the diffusion process
    size = 10
    diffusion = BitField3D(size, size, size)
    
    # Initialize with a concentration at the center
    print("\nInitializing with a concentration at the center:")
    center = size // 2
    
    # Set the concentration as a property
    for x in range(size):
        for y in range(size):
            for z in range(size):
                # Calculate distance from center
                distance = np.sqrt((x - center)**2 + (y - center)**2 + (z - center)**2)
                
                # Set initial concentration based on distance (higher at center)
                if distance < 2:
                    concentration = 1.0
                    diffusion.setBit(x, y, z, 1)  # Visible concentration
                else:
                    concentration = 0.0
                
                diffusion.setProperty(x, y, z, "concentration", concentration)
    
    print(visualize3D(diffusion))
    
    # Run the diffusion simulation for several steps
    steps = 3
    diffusion_rate = 0.2
    
    print(f"\nRunning diffusion simulation for {steps} steps (diffusion rate = {diffusion_rate}):")
    
    for step in range(steps):
        # Create a new bitfield for the next step
        next_step = diffusion.copy()
        
        # Apply diffusion to each cell
        for x in range(1, size-1):  # Skip border cells for simplicity
            for y in range(1, size-1):
                for z in range(1, size-1):
                    # Get current concentration
                    current_conc = diffusion.getProperty(x, y, z, "concentration")
                    
                    # Calculate diffusion from neighbors
                    neighbor_conc = 0.0
                    for dx, dy, dz in [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]:
                        neighbor_conc += diffusion.getProperty(x+dx, y+dy, z+dz, "concentration")
                    
                    # Calculate new concentration
                    new_conc = current_conc + diffusion_rate * (neighbor_conc / 6 - current_conc)
                    next_step.setProperty(x, y, z, "concentration", new_conc)
                    
                    # Update visibility based on concentration threshold
                    if new_conc > 0.2:
                        next_step.setBit(x, y, z, 1)
                    else:
                        next_step.setBit(x, y, z, 0)
        
        # Update the diffusion for the next step
        diffusion = next_step
        
        # Visualize the current step
        print(f"\nStep {step+1}:")
        print(visualize3D(diffusion))
        
        # Print concentration at a few points
        print("\nConcentration values:")
        for pos in [(center, center, center), (center+2, center, center), (center+4, center, center)]:
            x, y, z = pos
            conc = diffusion.getProperty(x, y, z, "concentration")
            print(f"Position ({x},{y},{z}): {conc:.4f}")
    
    return diffusion

def example_wave_propagation():
    """Example of simulating wave propagation."""
    print("\n=== Simulating Wave Propagation ===")
    
    # Create a 4D bitfield for the wave propagation (3D space + time)
    size_x, size_y, size_z = 10, 10, 1  # 2D space for simplicity (z=1)
    time_steps = 5
    wave = BitField4D(size_x, size_y, size_z, time_steps)
    
    # Initialize with a point source at the center at t=0
    print("\nInitializing with a point source at the center:")
    center_x, center_y = size_x // 2, size_y // 2
    
    # Set the initial amplitude at t=0
    for x in range(size_x):
        for y in range(size_y):
            # Calculate distance from center
            distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
            
            # Set initial amplitude (only at center)
            if distance < 1:
                amplitude = 1.0
                wave.setBit(x, y, 0, 0, 1)  # Visible amplitude
            else:
                amplitude = 0.0
            
            wave.setProperty(x, y, 0, 0, "amplitude", amplitude)
    
    # Simulate wave propagation over time
    print("\nSimulating wave propagation over time:")
    wave_speed = 1.0
    damping = 0.9
    
    for t in range(1, time_steps):
        # For each point in space
        for x in range(1, size_x-1):  # Skip border cells
            for y in range(1, size_y-1):  # Skip border cells
                # Calculate new amplitude based on wave equation
                prev_amplitude = wave.getProperty(x, y, 0, t-1, "amplitude")
                
                # Simple wave propagation from neighbors at previous time step
                neighbor_sum = 0.0
                for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
                    neighbor_sum += wave.getProperty(x+dx, y+dy, 0, t-1, "amplitude")
                
                # Calculate new amplitude
                new_amplitude = damping * (neighbor_sum / 4)
                
                # Add source term if at center and t=1
                if x == center_x and y == center_y and t == 1:
                    new_amplitude = 1.0
                
                # Set new amplitude
                wave.setProperty(x, y, 0, t, "amplitude", new_amplitude)
                
                # Update visibility based on amplitude threshold
                if new_amplitude > 0.2:
                    wave.setBit(x, y, 0, t, 1)
                else:
                    wave.setBit(x, y, 0, t, 0)
    
    # Visualize the wave propagation
    print("\nWave propagation visualization:")
    print(visualize4D(wave))
    
    # Print amplitude at the center for each time step
    print("\nAmplitude at center over time:")
    for t in range(time_steps):
        amplitude = wave.getProperty(center_x, center_y, 0, t, "amplitude")
        print(f"Time t={t}: {amplitude:.4f}")
    
    return wave

def example_kta_simulation():
    """Example of using KTA operations for simulation."""
    print("\n=== Using KTA Operations for Simulation ===")
    
    # Create two 3D bitfields with different patterns
    size = 6
    print("\nCreating two bitfields with different patterns:")
    
    # Create a cube pattern
    cube = generatePattern('cube', (size, size, size))
    print("\nCube pattern:")
    print(visualize3D(cube))
    
    # Create a sphere pattern
    sphere = generatePattern('sphere', (size, size, size))
    print("\nSphere pattern:")
    print(visualize3D(sphere))
    
    # Apply KTA operations
    print("\nApplying KTA operations:")
    
    # Create a superposition of the two patterns
    print("\n1. Creating a superposition of cube and sphere:")
    superposed = superposition(cube, sphere)
    print(visualize3D(superposed))
    
    # Apply a wave transform
    print("\n2. Applying a wave transform to the cube:")
    wave_transformed = applyKineticTransform(cube, 'wave')
    print(visualize3D(wave_transformed))
    
    # Apply a fractal transform
    print("\n3. Applying a fractal transform to the sphere:")
    fractal_transformed = applyKineticTransform(sphere, 'fractal')
    print(visualize3D(fractal_transformed))
    
    # Create entangled bitfields
    print("\n4. Creating entangled bitfields:")
    entangled_a, entangled_b = entangle(cube, sphere)
    
    # Modify one entangled bitfield and observe the effect on the other
    print("\nBefore modification:")
    print("Entangled A:")
    print(visualize3D(entangled_a))
    print("Entangled B:")
    print(visualize3D(entangled_b))
    
    # Modify entangled_a
    print("\nModifying Entangled A at position (1,1,1):")
    current_value = entangled_a.getBit(1, 1, 1)
    entangled_a.setBit(1, 1, 1, 1 - current_value)  # Flip the bit
    
    print("\nAfter modification:")
    print("Entangled A:")
    print(visualize3D(entangled_a))
    print("Entangled B (should reflect the change due to entanglement):")
    print(visualize3D(entangled_b))
    
    return superposed, wave_transformed, fractal_transformed, entangled_a, entangled_b

def example_animation():
    """Example of creating animations of simulated processes."""
    print("\n=== Creating Animations of Simulated Processes ===")
    
    # Create a 3D bitfield with a pattern
    size = 6
    bitfield = generatePattern('sphere', (size, size, size))
    
    # Create an animation of a transformation
    print("\nCreating an animation of a rotating sphere:")
    frames = 4
    
    # Generate animation frames manually
    animation_frames = []
    
    for i in range(frames):
        # Rotate the sphere around the z-axis
        angle = i * 90  # 0, 90, 180, 270 degrees
        rotated = bitfield.copy()  # In a real implementation, this would be rotate3D(bitfield, 'z', angle)
        
        # For demonstration, we'll just modify some bits to simulate rotation
        if i > 0:
            # Flip some bits to simulate movement
            for x in range(1, size-1):
                for y in range(1, size-1):
                    for z in range(1, size-1):
                        if (x + y + z + i) % 4 == 0:
                            current_value = rotated.getBit(x, y, z)
                            rotated.setBit(x, y, z, 1 - current_value)
        
        # Add frame to animation
        animation_frames.append(rotated)
    
    # Display animation frames
    print("\nAnimation frames:")
    for i, frame in enumerate(animation_frames):
        print(f"\n--- Frame {i+1}/{frames} ---")
        print(visualize3D(frame))
        
        # In a real application, you might add a delay between frames
        # time.sleep(0.5)
    
    # Use the built-in animation function
    print("\nUsing the built-in animation function:")
    built_in_frames = animateTransform(bitfield, frames=frames)
    
    print(f"\nGenerated {len(built_in_frames)} animation frames")
    
    return animation_frames

def main():
    """Main function to run all examples."""
    print("BitMatrix Spatial Computing - Process Simulation Examples")
    print("=" * 60)
    
    # Run examples
    automaton = example_cellular_automaton()
    diffusion = example_diffusion_process()
    wave = example_wave_propagation()
    kta_results = example_kta_simulation()
    animation_frames = example_animation()
    
    print("\nAll process simulation examples completed successfully!")

if __name__ == "__main__":
    main()
