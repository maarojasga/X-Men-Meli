from pydantic import BaseModel

class StatsResponse(BaseModel):
    """
    Represents the response model for DNA statistics.

    Attributes:
        count_mutant_dna (int): Total count of mutant DNA sequences recorded.
        count_human_dna (int): Total count of human DNA sequences recorded.
        ratio (float): Ratio of mutant DNA sequences to total DNA sequences.
        most_mutants_day (str): Date with the highest number of recorded mutants.
        most_humans_day (str): Date with the highest number of recorded humans.
    """
    count_mutant_dna: int
    count_human_dna: int
    ratio: float
    most_mutants_day: str
    most_humans_day: str
