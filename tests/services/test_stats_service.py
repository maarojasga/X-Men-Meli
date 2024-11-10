from unittest.mock import patch
from datetime import datetime
import services.stats_service as stats_service
import pytest

@patch('services.stats_service.get_daily_counts')
def test_get_stats(mock_get_daily_counts):
    """
    Test case for get_stats to verify the correct aggregation and processing
    of daily counts of mutant and human DNA records.

    Args:
        mock_get_daily_counts (MagicMock): Mock for the get_daily_counts function to simulate database response.
    """
    # Simulate the data returned by get_daily_counts
    mock_get_daily_counts.return_value = [
        (datetime(2024, 11, 8), 3, 2),
        (datetime(2024, 11, 9), 1, 5)
    ]

    # Call get_stats
    result = stats_service.get_stats()

    # Verify each field in the result
    assert result["count_mutant_dna"] == 4
    assert result["count_human_dna"] == 7
    assert result["ratio"] == pytest.approx(36.36, rel=0.01)
    assert result["most_mutants_day"] == "2024-11-08"
    assert result["most_humans_day"] == "2024-11-09"
    