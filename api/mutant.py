from fastapi import APIRouter, HTTPException
from schemas.dna import DnaRequest, DnaResponse
from services.mutant_service import check_if_mutant
from repositories.dna_repository import save_dna
import uuid

router = APIRouter()

@router.post("/mutant", response_model=DnaResponse)
async def is_mutant(dna_request: DnaRequest):
    """
    Endpoint to determine if a given DNA sequence belongs to a mutant.

    Args:
        dna_request (DnaRequest): The DNA sequence data for verification.

    Raises:
        HTTPException: Raised if the DNA sequence is already recorded as mutant or human.
        HTTPException: Raised if the DNA sequence is identified as a new human.

    Returns:
        DnaResponse: The response indicating mutant status if newly identified as mutant.
    """
    # Generate a random ID for the record
    record_id = str(uuid.uuid4())

    # Normalize the DNA sequence as a single string
    dna_sequence_str = "".join(dna_request.dna)

    # Check if the DNA belongs to a mutant
    is_mutant = check_if_mutant(dna_request.dna)

    # Save the record and get the response status
    save_result = save_dna(record_id, dna_sequence_str, is_mutant)
    
    if save_result["exists"] == True:
        # If the sequence already exists, raise a 403 error specifying if it belongs to a human or mutant
        if save_result["is_mutant"]:
            raise HTTPException(status_code=403, detail=f"The DNA sequence '{dna_sequence_str}' is already recorded as mutant.")
        else:
            raise HTTPException(status_code=403, detail=f"The DNA sequence '{dna_sequence_str}' is already recorded as human.")
    
    if is_mutant:
        # If it is a new mutant, save to the database and respond with 200, specifying it as a new mutant
        return DnaResponse(status="mutant", record_id=save_result["record_id"], detail=f"The DNA sequence '{dna_sequence_str}' is identified as a new mutant.")
    else:
        # If it is a new human, save to the database and raise a 403 error specifying it as a new human
        raise HTTPException(status_code=403, detail=f"The DNA sequence '{dna_sequence_str}' is identified as a new human.")