"""
Brief Resolved Unexplained Events (BRUE) Criteria Router

Endpoint for calculating BRUE Criteria classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.brue import (
    BrueRequest,
    BrueResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/brue",
    response_model=BrueResponse,
    summary="Calculate Brief Resolved Unexplained Events",
    description="Classifies unexplained events in infants <1 year old and replaces the Apparent Life-Threatening Events (ALTE) classification. Determines risk stratification and management recommendations for infants who have experienced brief, resolved episodes of concerning symptoms.",
    response_description="The calculated brue with interpretation",
    operation_id="brue"
)
async def calculate_brue(request: BrueRequest):
    """
    Calculates Brief Resolved Unexplained Events (BRUE) Criteria
    
    Classifies unexplained events in infants <1 year old and replaces the Apparent 
    Life-Threatening Events (ALTE) classification. Determines risk stratification 
    and management recommendations for infants who have experienced brief, resolved 
    episodes of concerning symptoms.
    
    Args:
        request: Parameters needed for BRUE classification
        
    Returns:
        BrueResponse: Result with classification, risk stratification, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("brue", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BRUE Criteria",
                    "details": {"parameters": parameters}
                }
            )
        
        return BrueResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BRUE Criteria",
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