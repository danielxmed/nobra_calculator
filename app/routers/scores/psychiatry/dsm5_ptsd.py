"""
DSM-5 Criteria for Posttraumatic Stress Disorder Router

Endpoint for calculating DSM-5 PTSD diagnostic criteria.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dsm5_ptsd import (
    Dsm5PtsdRequest,
    Dsm5PtsdResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/dsm5_ptsd",
    response_model=Dsm5PtsdResponse,
    summary="Calculate DSM-5 Criteria for Posttraumatic Stress Disorder",
    description="Diagnostic criteria for posttraumatic stress disorder (PTSD) based on DSM-5. Evaluates trauma exposure and four symptom clusters: intrusion, avoidance, negative alterations in cognitions/mood, and alterations in arousal/reactivity.",
    response_description="The calculated dsm5 ptsd with interpretation",
    operation_id="calculate_dsm5_ptsd"
)
async def calculate_dsm5_ptsd(request: Dsm5PtsdRequest):
    """
    Calculates DSM-5 Criteria for Posttraumatic Stress Disorder
    
    Diagnostic criteria checker for PTSD based on DSM-5. Evaluates trauma exposure
    and four symptom clusters: intrusion, avoidance, negative alterations in 
    cognitions/mood, and alterations in arousal/reactivity.
    
    Args:
        request: DSM-5 PTSD diagnostic parameters
        
    Returns:
        Dsm5PtsdResponse: Diagnostic result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dsm5_ptsd", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DSM-5 PTSD criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return Dsm5PtsdResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DSM-5 PTSD criteria",
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