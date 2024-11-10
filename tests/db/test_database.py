from unittest.mock import patch
import db.database as db

@patch('db.database.psycopg2.connect')
def test_get_db_connection(mock_connect):
    """
    Test case for get_db_connection to ensure that it calls psycopg2.connect once
    and returns the simulated database connection.

    Args:
        mock_connect (MagicMock): Mock for the psycopg2.connect function.
    """
    # Simulate the database connection
    conn = db.get_db_connection()
    mock_connect.assert_called_once()  # Ensure psycopg2.connect was called exactly once
    assert conn == mock_connect.return_value  # Verify that it returns the mocked connection

@patch('db.database.get_db_connection')
def test_initialize_db(mock_get_db_connection):
    """
    Test case for initialize_db to verify that it creates the dna_records table
    if it does not already exist.

    Args:
        mock_get_db_connection (MagicMock): Mock for the get_db_connection function.
    """
    # Simulate the database connection and cursor
    mock_conn = mock_get_db_connection.return_value
    mock_cursor = mock_conn.cursor.return_value

    # Execute initialize_db
    db.initialize_db()

    # Verify that cursor and commit were called with the correct SQL statement
    mock_cursor.execute.assert_called_once_with('''
    CREATE TABLE IF NOT EXISTS dna_records (
        id TEXT PRIMARY KEY,
        dna_sequence TEXT,
        is_mutant BOOLEAN,
        date TIMESTAMP DEFAULT CURRENT_DATE
    )''')
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()
