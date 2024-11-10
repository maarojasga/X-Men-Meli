import time
import random
import statistics
from typing import List, Callable
import matplotlib.pyplot as plt

# First version
def detect_mutant(dna_sequence):
    """
    Detects if a DNA sequence belongs to a mutant.
    Searches for sequences of four identical letters in horizontal, vertical, and diagonal directions.
    A DNA sequence is considered mutant if at least two such sequences are found.

    Args:
        dna_sequence (list of str): A list of strings representing the DNA matrix.

    Returns:
        bool: True if the DNA sequence is identified as mutant, False otherwise.
    """
    n = len(dna_sequence)
    if n < 4:
        return False  # Cannot detect mutants in matrices smaller than 4x4

    count = 0  # Counter for found sequences

    # Helper function to check for sequences in a specific direction
    def has_sequence(x_step, y_step, x_start, y_start):
        char = dna_sequence[x_start][y_start]
        for i in range(1, 4):
            x = x_start + i * x_step
            y = y_start + i * y_step
            if x < 0 or x >= n or y < 0 or y >= n or dna_sequence[x][y] != char:
                return False
        return True

    # Search for sequences in all possible positions and directions
    for i in range(n):
        for j in range(n):
            if dna_sequence[i][j] in {'A', 'T', 'C', 'G'}:
                # Check horizontally (right)
                if j <= n - 4 and has_sequence(0, 1, i, j):
                    count += 1
                # Check vertically (down)
                if i <= n - 4 and has_sequence(1, 0, i, j):
                    count += 1
                # Check diagonal descending
                if i <= n - 4 and j <= n - 4 and has_sequence(1, 1, i, j):
                    count += 1
                # Check diagonal ascending
                if i >= 3 and j <= n - 4 and has_sequence(-1, 1, i, j):
                    count += 1
            # If at least two sequences are found, the DNA belongs to a mutant
            if count >= 2:
                return True

    return False

# Optimized version
def detect_mutant_optimized(dna_sequence):
    """
    Detects if a DNA sequence belongs to a mutant.
    Optimized version that uses early termination and efficient direction checking.

    Args:
        dna_sequence (list of str): A list of strings representing the DNA matrix.

    Returns:
        bool: True if the DNA sequence is identified as mutant, False otherwise.
    """
    n = len(dna_sequence)
    if n < 4:
        return False

    # Directions: right, down-right, down, down-left
    directions = [(0, 1), (1, 1), (1, 0), (1, -1)]
    sequences_found = 0

    def check_sequence(row, col, direction):
        """Check sequence in given direction from starting position."""
        char = dna_sequence[row][col]
        dr, dc = direction
        
        # Validate if we can make a sequence of 4 in this direction
        if (0 <= row + 3*dr < n and 0 <= col + 3*dc < n):
            # Check all 4 positions at once
            if (char == dna_sequence[row + dr][col + dc] and
                char == dna_sequence[row + 2*dr][col + 2*dc] and
                char == dna_sequence[row + 3*dr][col + 3*dc]):
                return True
        return False

    # Process each cell only once
    for i in range(n):
        for j in range(n):
            # Skip invalid characters
            if dna_sequence[i][j] not in {'A', 'T', 'C', 'G'}:
                continue
                
            # Check each direction
            for direction in directions:
                if check_sequence(i, j, direction):
                    sequences_found += 1
                    if sequences_found >= 2:
                        return True

    return False

# Test
def generate_dna_sequence(size: int) -> List[str]:
    """Generate a random DNA sequence of given size."""
    return [''.join(random.choices(['A', 'T', 'C', 'G'], k=size)) for _ in range(size)]

def generate_mutant_sequence(size: int) -> List[str]:
    """Generate a DNA sequence that is guaranteed to be mutant."""
    sequence = generate_dna_sequence(size)
    # Insert two horizontal sequences of 'AAAA'
    if size >= 4:
        sequence[0] = 'A' * 4 + ''.join(random.choices(['A', 'T', 'C', 'G'], k=size-4))
        sequence[1] = 'A' * 4 + ''.join(random.choices(['A', 'T', 'C', 'G'], k=size-4))
    return sequence

def measure_performance(func: Callable, sequence: List[str], iterations: int = 100) -> dict:
    """Measure execution time statistics for a given function."""
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        func(sequence)
        end = time.perf_counter()
        times.append(end - start)
    
    return {
        'min': min(times),
        'max': max(times),
        'mean': statistics.mean(times),
        'median': statistics.median(times),
        'std_dev': statistics.stdev(times)
    }

def compare_algorithms(sizes=[4, 6, 8, 10, 12, 15, 20]):
    """Compare both algorithms with different matrix sizes."""
    results_original = []
    results_optimized = []
    results_mutant_original = []
    results_mutant_optimized = []

    for size in sizes:
        # Test with random sequence
        random_sequence = generate_dna_sequence(size)
        original_stats = measure_performance(detect_mutant, random_sequence)
        optimized_stats = measure_performance(detect_mutant_optimized, random_sequence)
        
        results_original.append(original_stats['mean'])
        results_optimized.append(optimized_stats['mean'])

        # Test with mutant sequence
        mutant_sequence = generate_mutant_sequence(size)
        original_mutant_stats = measure_performance(detect_mutant, mutant_sequence)
        optimized_mutant_stats = measure_performance(detect_mutant_optimized, mutant_sequence)
        
        results_mutant_original.append(original_mutant_stats['mean'])
        results_mutant_optimized.append(optimized_mutant_stats['mean'])

        print(f"\nMatrix size: {size}x{size}")
        print("Random Sequence:")
        print(f"Original algorithm: {original_stats['mean']*1000:.3f} ms")
        print(f"Optimized algorithm: {optimized_stats['mean']*1000:.3f} ms")
        print(f"Improvement: {((original_stats['mean'] - optimized_stats['mean'])/original_stats['mean'])*100:.1f}%")
        print("\nMutant Sequence:")
        print(f"Original algorithm: {original_mutant_stats['mean']*1000:.3f} ms")
        print(f"Optimized algorithm: {optimized_mutant_stats['mean']*1000:.3f} ms")
        print(f"Improvement: {((original_mutant_stats['mean'] - optimized_mutant_stats['mean'])/original_mutant_stats['mean'])*100:.1f}%")

    # Plot results
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.plot(sizes, results_original, 'o-', label='Original')
    plt.plot(sizes, results_optimized, 'o-', label='Optimized')
    plt.title('Performance Comparison (Random Sequences)')
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.plot(sizes, results_mutant_original, 'o-', label='Original')
    plt.plot(sizes, results_mutant_optimized, 'o-', label='Optimized')
    plt.title('Performance Comparison (Mutant Sequences)')
    plt.xlabel('Matrix Size')
    plt.ylabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Testing
def run_example_tests():
    """Run example tests to demonstrate functionality."""
    # Human
    normal_dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATTT",
        "AGACGG",
        "GCGTCA",
        "TCACTG"
    ]
    
    # Mutant
    mutant_dna = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
    
    print("\nExample Test Results:")
    print("Normal DNA:")
    print("Original algorithm:", detect_mutant(normal_dna))
    print("Optimized algorithm:", detect_mutant_optimized(normal_dna))
    
    print("\nMutant DNA:")
    print("Original algorithm:", detect_mutant(mutant_dna))
    print("Optimized algorithm:", detect_mutant_optimized(mutant_dna))
    
    print("\nPerformance Comparison:")
    compare_algorithms()

if __name__ == "__main__":
    run_example_tests()