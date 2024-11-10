from unittest.mock import patch
from datetime import datetime
import repositories.dna_repository as repo

@patch('repositories.dna_repository.get_db_connection')
def test_save_dna_existing(mock_get_db_connection):
    """
    Test case for save_dna when the DNA sequence already exists in the database.

    Args:
        mock_get_db_connection (MagicMock): Mock for the get_db_connection function.
    """
    # Simulate database connection and cursor
    mock_conn = mock_get_db_connection.return_value
    mock_cursor = mock_conn.cursor.return_value

    # Simulate that the DNA sequence already exists in the database
    mock_cursor.fetchone.return_value = (True, 'existing_id')

    # Call save_dna
    result = repo.save_dna('new_id', ['A', 'T', 'G', 'C'], True)

    # Verify the result and ensure that no insert operation is performed
    assert result == {"exists": True, "is_mutant": True, "record_id": 'existing_id'}
    mock_cursor.execute.assert_called_once_with("SELECT is_mutant, id FROM dna_records WHERE dna_sequence = %s", ('ATGC',))

@patch('repositories.dna_repository.get_db_connection')
def test_save_dna_new(mock_get_db_connection):
    """
    Test case for save_dna when the DNA sequence does not exist in the database.

    Args:
        mock_get_db_connection (MagicMock): Mock for the get_db_connection function.
    """
    # Simulate database connection and cursor
    mock_conn = mock_get_db_connection.return_value
    mock_cursor = mock_conn.cursor.return_value

    # Simulate that the DNA sequence does not exist in the database
    mock_cursor.fetchone.return_value = None

    # Call save_dna
    result = repo.save_dna('new_id', ['A', 'T', 'G', 'C'], True)

    # Verify that the sequence is inserted and returns the expected result
    assert result == {"exists": False, "is_mutant": True, "record_id": 'new_id'}
    mock_cursor.execute.assert_any_call("INSERT INTO dna_records (id, dna_sequence, is_mutant, date) VALUES (%s, %s, %s, %s)",
                                        ('new_id', 'ATGC', True, datetime.now().date()))
    mock_conn.commit.assert_called_once()

@patch('repositories.dna_repository.get_db_connection')
def test_get_daily_counts(mock_get_db_connection):
    """
    Test case for get_daily_counts to verify that it retrieves the daily counts
    of mutants and humans correctly.

    Args:
        mock_get_db_connection (MagicMock): Mock for the get_db_connection function.
    """
    # Simulate database connection and cursor
    mock_conn = mock_get_db_connection.return_value
    mock_cursor = mock_conn.cursor.return_value

    # Simulate database results
    mock_cursor.fetchall.return_value = [(datetime(2024, 11, 8), 3, 2)]

    # Call get_daily_counts
    results = repo.get_daily_counts()

    # Verify the results and that the query was executed correctly
    assert results == [(datetime(2024, 11, 8), 3, 2)]
    mock_cursor.execute.assert_called_once_with('''  
        SELECT date, 
               SUM(CASE WHEN is_mutant THEN 1 ELSE 0 END) AS mutants, 
               SUM(CASE WHEN NOT is_mutant THEN 1 ELSE 0 END) AS humans
        FROM dna_records
        GROUP BY date
    ''')
