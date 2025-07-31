"""
4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) Router

Endpoint for calculating the 4PEPS score to assess pulmonary embolism probability
and guide diagnostic testing decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.four_peps import (
    FourPepsRequest,
    FourPepsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/four_peps",
    response_model=FourPepsResponse,
    summary="Calculate 4-Level Pulmonary Embolism Clinical Probability...",
    description="Clinical probability score for suspected pulmonary embolism using 13 clinical variables to safely decrease imaging testing needs",
    response_description="The calculated four peps with interpretation",
    operation_id="calculate_four_peps"
)
async def calculate_four_peps(request: FourPepsRequest):
    """
    Calculates 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)
    
    The 4PEPS uses 13 clinical variables to stratify patients with suspected 
    pulmonary embolism into four probability categories:
    
    - Very Low (<0 points): PE ruled out, no testing needed
    - Low (0-5 points): Use D-dimer with 1000 μg/L cut-off  
    - Moderate (6-12 points): Use age-adjusted D-dimer cut-off
    - High (>12 points): Proceed directly to imaging
    
    This score can safely reduce imaging studies in 58% of patients with 
    suspected PE while maintaining a low failure rate of 1.3%.
    
    Args:
        request: Clinical parameters for 4PEPS calculation including age category,
                chronic respiratory disease, vital signs, symptoms, risk factors,
                and clinical assessment
        
    Returns:
        FourPepsResponse: 4PEPS score with clinical probability category and 
                         recommended diagnostic approach
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("four_peps", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4-Level Pulmonary Embolism Clinical Probability Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourPepsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4PEPS calculation",
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
                "message": "Internal error in 4PEPS calculation",
                "details": {"error": str(e)}
            }
        )