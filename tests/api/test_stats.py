from fastapi.testclient import TestClient
from unittest.mock import patch
from api.stats import router
import pytest

client = TestClient(router)

@patch("api.stats.get_stats")
def test_stats(mock_get_stats):
    """
    Test case for the /stats endpoint, mocking the get_stats function.

    Args:
        mock_get_stats (MagicMock): Mock for the get_stats function to simulate database response.
    """
    # Simulate data returned by get_stats
    mock_get_stats.return_value = {
        "count_mutant_dna": 4,
        "count_human_dna": 7,
        "ratio": 36.36,
        "most_mutants_day": "2024-11-08",
        "most_humans_day": "2024-11-09"
    }

    # Send test request to the /stats endpoint
    response = client.get("/stats")

    # Verify response status code and data
    assert response.status_code == 200
    data = response.json()
    assert data["count_mutant_dna"] == 4
    assert data["count_human_dna"] == 7
    assert data["ratio"] == pytest.approx(36.36, rel=0.01)
    assert data["most_mutants_day"] == "2024-11-08"
    assert data["most_humans_day"] == "2024-11-09"
