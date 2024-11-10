import uuid
from fastapi.testclient import TestClient
from unittest.mock import patch
from api.mutant import router
from fastapi import HTTPException
import pytest

client = TestClient(router)

@patch("api.mutant.save_dna")
@patch("api.mutant.check_if_mutant")
def test_is_mutant_new_mutant(mock_check_if_mutant, mock_save_dna):
    """
    Test case for a new mutant DNA sequence.

    Args:
        mock_check_if_mutant (MagicMock): Mock for the check_if_mutant function.
        mock_save_dna (MagicMock): Mock for the save_dna function.
    """
    # Mock the response to indicate it is a mutant
    mock_check_if_mutant.return_value = True
    mock_save_dna.return_value = {"exists": False, "is_mutant": True, "record_id": str(uuid.uuid4())}
    
    # Send test request
    dna_request = {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
    response = client.post("/mutant", json=dna_request)

    # Verify response
    assert response.status_code == 200
    assert response.json()["status"] == "mutant"

@patch("api.mutant.save_dna")
@patch("api.mutant.check_if_mutant")
def test_is_mutant_existing_mutant(mock_check_if_mutant, mock_save_dna):
    """
    Test case for an existing mutant DNA sequence.

    Args:
        mock_check_if_mutant (MagicMock): Mock for the check_if_mutant function.
        mock_save_dna (MagicMock): Mock for the save_dna function.
    """
    # Mock the response to indicate the DNA sequence already exists as mutant
    mock_check_if_mutant.return_value = True
    mock_save_dna.return_value = {"exists": True, "is_mutant": True, "record_id": str(uuid.uuid4())}
    
    dna_request = {"dna": ["ATGCGA", "CAGTGC", "TTATGT", "AGAAGG", "CCCCTA", "TCACTG"]}
    
    # Use pytest.raises to check for HTTP 403 exception
    with pytest.raises(HTTPException) as exc_info:
        response = client.post("/mutant", json=dna_request)
        
    # Verify that the HTTP 403 exception contains the expected message
    assert exc_info.value.status_code == 403
    assert "already recorded as mutant" in str(exc_info.value.detail)
    
@patch("api.mutant.save_dna")
@patch("api.mutant.check_if_mutant")
def test_is_mutant_new_human(mock_check_if_mutant, mock_save_dna):
    """
    Test case for a new human DNA sequence.

    Args:
        mock_check_if_mutant (MagicMock): Mock for the check_if_mutant function.
        mock_save_dna (MagicMock): Mock for the save_dna function.
    """
    # Mock the response to indicate it is a new human
    mock_check_if_mutant.return_value = False
    mock_save_dna.return_value = {"exists": False, "is_mutant": False, "record_id": str(uuid.uuid4())}

    dna_request = {"dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]}
    
    # Capture the expected exception for a new human
    with pytest.raises(HTTPException) as exc_info:
        client.post("/mutant", json=dna_request)

    # Verify that the exception is HTTP 403 with the correct message
    assert exc_info.value.status_code == 403
    assert "identified as a new human" in str(exc_info.value.detail)

@patch("api.mutant.save_dna")
@patch("api.mutant.check_if_mutant")
def test_is_mutant_existing_human(mock_check_if_mutant, mock_save_dna):
    """
    Test case for an existing human DNA sequence.

    Args:
        mock_check_if_mutant (MagicMock): Mock for the check_if_mutant function.
        mock_save_dna (MagicMock): Mock for the save_dna function.
    """
    # Mock the response to indicate the DNA sequence already exists as human
    mock_check_if_mutant.return_value = False
    mock_save_dna.return_value = {"exists": True, "is_mutant": False, "record_id": str(uuid.uuid4())}

    dna_request = {"dna": ["ATGCGA", "CAGTGC", "TTATTT", "AGACGG", "GCGTCA", "TCACTG"]}

    # Capture the expected exception for an existing human
    with pytest.raises(HTTPException) as exc_info:
        client.post("/mutant", json=dna_request)

    # Verify that the exception is HTTP 403 with the correct message
    assert exc_info.value.status_code == 403
    assert "already recorded as human" in str(exc_info.value.detail)