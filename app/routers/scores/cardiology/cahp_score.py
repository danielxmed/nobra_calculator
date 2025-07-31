"""
CAHP (Cardiac Arrest Hospital Prognosis) Score Router

Endpoint for calculating CAHP Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.cahp_score import (
    CahpScoreRequest,
    CahpScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/cahp_score",
    response_model=CahpScoreResponse,
    summary="Calculate CAHP (Cardiac Arrest Hospital Prognos...",
    description="Predicts poor prognosis after out-of-hospital cardiac arrest and guides utility of cardiac catheterization",
    response_description="The calculated cahp score with interpretation",
    operation_id="cahp_score"
)
async def calculate_cahp_score(request: CahpScoreRequest):
    """
    Calculates CAHP (Cardiac Arrest Hospital Prognosis) Score
    
    Predicts poor prognosis after out-of-hospital cardiac arrest and guides 
    utility of cardiac catheterization. The score incorporates seven variables:
    age, setting, initial rhythm, time from collapse to CPR, time from CPR to 
    ROSC, admission pH, and epinephrine dose.
    
    The CAHP score stratifies patients into three risk categories:
    - Low risk (<150): 39% risk of poor neurological outcome
    - Moderate risk (150-200): 81% risk of poor neurological outcome
    - High risk (>200): 100% risk of poor neurological outcome
    
    Important: This score is validated only for medical/cardiac arrests, not 
    for traumatic arrests, drowning, hanging, or overdose. High scores do not 
    automatically warrant withdrawal of care.
    
    Args:
        request: CAHP Score parameters including age, arrest details, and labs
        
    Returns:
        CahpScoreResponse: Score with risk stratification and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cahp_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CAHP Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CahpScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CAHP Score",
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