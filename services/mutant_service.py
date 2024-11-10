from repositories.dna_repository import save_dna

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
    print(n)
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
            print('checking position', i, j, dna_sequence[i][j])
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