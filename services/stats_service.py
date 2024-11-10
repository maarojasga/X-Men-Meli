from repositories.dna_repository import get_daily_counts

def get_stats():
    """
    Calculates statistics for mutant and human DNA sequences recorded in the database.

    Retrieves daily counts of mutants and humans, then aggregates total counts, calculates
    the mutant ratio, and identifies the days with the highest number of mutants and humans.

    Returns:
        dict: A dictionary containing:
              - "count_mutant_dna" (int): Total number of mutant DNA sequences recorded.
              - "count_human_dna" (int): Total number of human DNA sequences recorded.
              - "ratio" (float): Percentage of mutant DNA sequences out of the total DNA sequences.
              - "most_mutants_day" (str): Date with the highest recorded mutants, in "YYYY-MM-DD" format.
              - "most_humans_day" (str): Date with the highest recorded humans, in "YYYY-MM-DD" format.
    """
    daily_counts = get_daily_counts()

    # Sum all mutants and humans
    count_mutant_dna = sum(day[1] for day in daily_counts)  # Sum of the 'mutants' column
    count_human_dna = sum(day[2] for day in daily_counts)   # Sum of the 'humans' column
    total_dna = count_mutant_dna + count_human_dna          # Total number of sequences
    ratio = (count_mutant_dna / total_dna * 100) if total_dna > 0 else 0  # Mutant percentage

    # Find the day with the most mutants and the day with the most humans
    most_mutants_day = (
        max(daily_counts, key=lambda x: x[1])[0].strftime("%Y-%m-%d") if daily_counts else None
    )
    most_humans_day = (
        max(daily_counts, key=lambda x: x[2])[0].strftime("%Y-%m-%d") if daily_counts else None
    )

    return {
        "count_mutant_dna": count_mutant_dna,
        "count_human_dna": count_human_dna,
        "ratio": ratio,
        "most_mutants_day": most_mutants_day,
        "most_humans_day": most_humans_day
    }