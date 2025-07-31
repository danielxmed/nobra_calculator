"""
Clinical Dementia Rating (CDR) Scale Router

Endpoint for calculating CDR Scale score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.clinical_dementia_rating import (
    ClinicalDementiaRatingRequest,
    ClinicalDementiaRatingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/clinical_dementia_rating",
    response_model=ClinicalDementiaRatingResponse,
    summary="Calculate Clinical Dementia Rating (CDR) Scale",
    description="Stages dementia, including Alzheimer's disease, in elderly patients. The CDR assesses cognitive and functional performance across six domains to provide both a global CDR score (0-3) and a sum of boxes score (0-18).",
    response_description="The calculated clinical dementia rating with interpretation",
    operation_id="clinical_dementia_rating"
)
async def calculate_clinical_dementia_rating(request: ClinicalDementiaRatingRequest):
    """
    Calculates Clinical Dementia Rating (CDR) Scale
    
    Stages dementia, including Alzheimer's disease, in elderly patients by 
    assessing cognitive and functional performance across six domains. Returns 
    both a global CDR score (0-3) using the Washington University algorithm 
    and a CDR Sum of Boxes score (0-18) for additional staging information.
    
    Args:
        request: Parameters containing scores for 6 domains (Memory, Orientation,
                Judgment & Problem Solving, Community Affairs, Home & Hobbies,
                Personal Care)
        
    Returns:
        ClinicalDementiaRatingResponse: Global CDR score, Sum of Boxes, and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("clinical_dementia_rating", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CDR Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ClinicalDementiaRatingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CDR Scale",
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