"""
Bova Score for Pulmonary Embolism Complications Router

Endpoint for calculating Bova Score for PE complications.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.bova_score import (
    BovaScoreRequest,
    BovaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bova_score",
    response_model=BovaScoreResponse,
    summary="Calculate Bova Score for Pulmonary Embolism Complications",
    description="Predicts 30-day risk of PE-related complications (death, hemodynamic collapse, or recurrent PE) in hemodynamically stable patients with confirmed pulmonary embolism",
    response_description="The calculated bova score with interpretation",
    operation_id="bova_score"
)
async def calculate_bova_score(request: BovaScoreRequest):
    """
    Calculates Bova Score for Pulmonary Embolism Complications
    
    Predicts 30-day risk of PE-related complications (death, hemodynamic collapse, 
    or recurrent PE) in hemodynamically stable patients with confirmed pulmonary embolism.
    
    The score stratifies patients into three risk categories:
    - Stage I (0-2 points): Low risk - 4.4% complications
    - Stage II (3-4 points): Intermediate risk - 18% complications  
    - Stage III (>4 points): High risk - 42% complications
    
    Args:
        request: Parameters needed for calculation including systolic BP, 
                troponin status, RV dysfunction, and heart rate
        
    Returns:
        BovaScoreResponse: Score result with risk stage and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bova_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Bova Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BovaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Bova Score",
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