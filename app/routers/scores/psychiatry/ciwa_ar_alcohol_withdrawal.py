"""
CIWA-Ar for Alcohol Withdrawal Router

Endpoint for calculating CIWA-Ar (Clinical Institute Withdrawal Assessment for Alcohol, Revised).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.ciwa_ar_alcohol_withdrawal import (
    CiwaArAlcoholWithdrawalRequest,
    CiwaArAlcoholWithdrawalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ciwa_ar_alcohol_withdrawal", response_model=CiwaArAlcoholWithdrawalResponse)
async def calculate_ciwa_ar_alcohol_withdrawal(request: CiwaArAlcoholWithdrawalRequest):
    """
    Calculates CIWA-Ar for Alcohol Withdrawal Assessment
    
    The Clinical Institute Withdrawal Assessment for Alcohol, Revised (CIWA-Ar) is a 
    validated 10-component assessment tool that quantifies alcohol withdrawal severity 
    and guides evidence-based treatment decisions. This scale takes less than 5 minutes 
    to complete and should be performed every 1-2 hours during active withdrawal management.
    
    The assessment evaluates:
    - Nausea and vomiting (0-7 points)
    - Tremor (0-7 points) 
    - Paroxysmal sweats (0-7 points)
    - Anxiety (0-7 points)
    - Agitation (0-7 points)
    - Tactile disturbances (0-7 points)
    - Auditory disturbances (0-7 points)
    - Visual disturbances (0-7 points)
    - Headache and fullness in head (0-7 points)
    - Orientation and clouding of sensorium (0-4 points)
    
    Total scores range from 0-67 points with three severity categories:
    - Minimal (0-8): Usually no treatment required
    - Mild to Moderate (9-19): Consider benzodiazepines
    - Severe (≥20): Aggressive treatment required, high risk for delirium tremens
    
    Args:
        request: CIWA-Ar assessment parameters with all 10 component scores
        
    Returns:
        CiwaArAlcoholWithdrawalResponse: Comprehensive withdrawal assessment with 
        severity category, treatment recommendations, and detailed clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ciwa_ar_alcohol_withdrawal", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CIWA-Ar for Alcohol Withdrawal",
                    "details": {"parameters": parameters}
                }
            )
        
        return CiwaArAlcoholWithdrawalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CIWA-Ar Alcohol Withdrawal assessment",
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
                "message": "Internal error in CIWA-Ar calculation",
                "details": {"error": str(e)}
            }
        )