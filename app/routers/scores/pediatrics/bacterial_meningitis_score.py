"""
Bacterial Meningitis Score for Children Router

Endpoint for calculating the Bacterial Meningitis Score for Children.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.bacterial_meningitis_score import (
    BacterialMeningitisScoreRequest,
    BacterialMeningitisScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/bacterial_meningitis_score", response_model=BacterialMeningitisScoreResponse)
async def calculate_bacterial_meningitis_score(request: BacterialMeningitisScoreRequest):
    """
    Calculates the Bacterial Meningitis Score for Children
    
    Predicts likelihood of bacterial (versus aseptic) meningitis in children with CSF pleocytosis.
    The score helps clinicians distinguish between bacterial and aseptic meningitis to support safe 
    discharge decisions while maintaining appropriate caution for this serious condition.
    
    Score components (each worth 1 point):
    - Positive CSF Gram stain
    - CSF ANC ≥1,000 cells/µL
    - CSF protein ≥80 mg/dL
    - Peripheral blood ANC ≥10,000 cells/µL
    - Seizure at or prior to presentation
    
    Interpretation:
    - 0 points: Very low risk (~0.1%) - Consider discharge with close follow-up
    - ≥1 point: Not very low risk - Admission recommended
    
    Limitations:
    - Not recommended for patients <2 months old
    - Clinical judgment should always supersede the score
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        BacterialMeningitisScoreResponse: Result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bacterial_meningitis_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bacterial Meningitis Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BacterialMeningitisScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bacterial Meningitis Score",
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