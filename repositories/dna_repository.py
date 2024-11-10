from datetime import datetime
from db.database import get_db_connection

def save_dna(record_id, dna_sequence, is_mutant):
    """
    Saves the DNA sequence and mutant status in the database with a ID.
    If the sequence already exists, it does not save it again and returns an "exists" status.

    Args:
        record_id (str): Unique identifier for the DNA record.
        dna_sequence (list): List of strings representing the DNA sequence.
        is_mutant (bool): Boolean indicating if the DNA belongs to a mutant.

    Returns:
        dict: A dictionary containing:
              - "exists" (bool): Whether the DNA sequence was already in the database.
              - "is_mutant" (bool): Mutant status of the DNA (True if mutant, False if human).
              - "record_id" (str): The unique ID of the record.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    # Normalize the DNA sequence into a single string (if not already normalized)
    dna_sequence_str = "".join(dna_sequence)

    # Check if the DNA sequence already exists in the database
    cursor.execute("SELECT is_mutant, id FROM dna_records WHERE dna_sequence = %s", (dna_sequence_str,))
    result = cursor.fetchone()
    
    if result:
        # If it already exists, return the "exists" status and whether it is mutant or human
        existing_is_mutant = result[0]
        conn.close()
        return {"exists": True, "is_mutant": existing_is_mutant, "record_id": result[1]}

    # If it does not exist, insert the new record into the database
    cursor.execute(
        "INSERT INTO dna_records (id, dna_sequence, is_mutant, date) VALUES (%s, %s, %s, %s)",
        (record_id, dna_sequence_str, is_mutant, datetime.now().date())
    )
    conn.commit()
    conn.close()
    return {"exists": False, "is_mutant": is_mutant, "record_id": record_id}

def get_daily_counts():
    """
    Retrieves the daily counts of mutants and humans from the database.

    Returns:
        list: A list of tuples, each containing:
              - date (datetime): The date of the record.
              - mutants (int): The count of mutant DNA sequences for that date.
              - humans (int): The count of human DNA sequences for that date.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''  
        SELECT date, 
               SUM(CASE WHEN is_mutant THEN 1 ELSE 0 END) AS mutants, 
               SUM(CASE WHEN NOT is_mutant THEN 1 ELSE 0 END) AS humans
        FROM dna_records
        GROUP BY date
    ''')
    results = cursor.fetchall()
    conn.close()
    return results
