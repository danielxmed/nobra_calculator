"""
BAP-65 Score Router

Endpoint for calculating BAP-65 Score for Acute Exacerbation of COPD.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.bap_65 import (
    Bap65Request,
    Bap65Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/bap_65", response_model=Bap65Response)
async def calculate_bap_65(request: Bap65Request):
    """
    Calculates BAP-65 Score for Acute Exacerbation of COPD
    
    The BAP-65 score is a simple risk stratification tool that predicts in-hospital 
    mortality in patients with acute exacerbations of chronic obstructive pulmonary 
    disease (COPD). It uses four easily obtainable clinical variables:
    
    - **B**UN (Blood Urea Nitrogen) ≥25 mg/dL
    - **A**ltered Mental Status
    - **P**ulse ≥109 beats/min
    - Age ≥**65** years
    
    The score ranges from 0-3 points and stratifies patients into five risk classes
    with mortality rates ranging from 0.3% to 14.1%.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        Bap65Response: Result with clinical interpretation and risk classification
        
    Raises:
        HTTPException: If calculation fails or invalid parameters are provided
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bap_65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BAP-65 score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Bap65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BAP-65 score",
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