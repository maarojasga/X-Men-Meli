from pydantic import BaseModel
from typing import List

class DnaRequest(BaseModel):
    """
    Represents a request model for DNA analysis.

    Args:
        BaseModel (pydantic.BaseModel): Inherits from Pydantic's BaseModel.

    Attributes:
        dna (List[str]): List of DNA sequence string to be analyzed.
    """
    dna: List[str]

class DnaResponse(BaseModel):
    """
    Represents a response model for DNA analysis results.

    Args:
        BaseModel (pydantic.BaseModel): Inherits from Pydantic's BaseModel.

    Attributes:
        status (str): Indicates the result of the analysis ("mutant" or "human").
        record_id (str): Unique identifier for the DNA record.
        detail (str): Additional details about the result, such as whether it is a new or existing entry.
    """
    status: str  # Mutant" or Human
    record_id: str
    detail: str
