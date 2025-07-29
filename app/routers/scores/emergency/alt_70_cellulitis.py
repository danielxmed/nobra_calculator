"""
ALT-70 Score for Cellulitis Router

Endpoint for calculating ALT-70 Score for Cellulitis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.alt_70_cellulitis import (
    Alt70CellulitisRequest,
    Alt70CellulitisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/alt_70_cellulitis", response_model=Alt70CellulitisResponse)
async def calculate_alt_70_cellulitis(request: Alt70CellulitisRequest):
    """
    Calculates ALT-70 Score for Cellulitis
    
    A validated clinical prediction rule that helps differentiate lower extremity 
    cellulitis from its mimics (pseudocellulitis) in the emergency department setting.
    Uses four clinical variables (Asymmetric involvement, Leukocytosis, Tachycardia, 
    and age ≥70) to stratify patients into risk categories.
    
    Args:
        request: Clinical parameters for ALT-70 calculation
        
    Returns:
        Alt70CellulitisResponse: Score result with interpretation and likelihood
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("alt_70_cellulitis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ALT-70 Score for Cellulitis",
                    "details": {"parameters": parameters}
                }
            )
        
        return Alt70CellulitisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ALT-70 Score for Cellulitis",
                "details": {"error": str(e)}
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "InternalServerError",
                "message": "Internal error in calculation",
                "details": {"error": str(e)}
            }
        )