"""
Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria Router

Endpoint for calculating BRUE 2.0 Criteria classification and risk prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.brue_2_0 import (
    Brue20Request,
    Brue20Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/brue_2_0",
    response_model=Brue20Response,
    summary="Calculate Brief Resolved Unexplained Events 2.0",
    description="Classifies unexplained events and improves on the original BRUE criteria by providing sophisticated risk prediction models for serious underlying conditions and event recurrence in infants <1 year old. Uses derived models to predict risk of serious diagnosis and recurrent events.",
    response_description="The calculated brue 2 0 with interpretation",
    operation_id="calculate_brue_2_0"
)
async def calculate_brue_2_0(request: Brue20Request):
    """
    Calculates Brief Resolved Unexplained Events 2.0 (BRUE 2.0) Criteria
    
    Classifies unexplained events and improves on the original BRUE criteria by 
    providing sophisticated risk prediction models for serious underlying conditions 
    and event recurrence in infants <1 year old. Uses derived models to predict 
    quantitative risk percentages for clinical decision-making.
    
    Args:
        request: Parameters needed for BRUE 2.0 classification and risk prediction
        
    Returns:
        Brue20Response: Result with classification, quantitative risk predictions, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("brue_2_0", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BRUE 2.0 Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return Brue20Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BRUE 2.0 Criteria",
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