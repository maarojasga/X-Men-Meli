import services.mutant_service as mutant_service

def test_detect_mutant_true():
    """
    Test case for detect_mutant when the DNA sequence belongs to a mutant.
    """
    dna_sequence = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
    assert mutant_service.detect_mutant(dna_sequence) == True

def test_detect_mutant_false():
    """
    Test case for detect_mutant when the DNA sequence does not belong to a mutant.
    """
    dna_sequence = [
        "ATGCGA",
        "CAGTGC",
        "TTATTT",
        "AGACGG",
        "GCGTCA",
        "TCACTG"
    ]
    assert mutant_service.detect_mutant(dna_sequence) == False

def test_check_if_mutant():
    """
    Test case for check_if_mutant to ensure that it correctly identifies a mutant sequence.
    """
    dna_sequence = [
        "ATGCGA",
        "CAGTGC",
        "TTATGT",
        "AGAAGG",
        "CCCCTA",
        "TCACTG"
    ]
    assert mutant_service.check_if_mutant(dna_sequence) == True
