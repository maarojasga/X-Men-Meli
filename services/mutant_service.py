def detect_mutant(dna_sequence):
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

def check_if_mutant(dna_sequence):
    """
    Executes the mutant detection logic.

    Args:
        dna_sequence (list of str): A list of strings representing the DNA matrix.

    Returns:
        bool: True if the DNA sequence is identified as mutant, False otherwise.
    """
    is_mutant = detect_mutant(dna_sequence)
    return is_mutant