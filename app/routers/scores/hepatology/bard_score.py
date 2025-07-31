"""
BARD Score for NAFLD Fibrosis Router

Endpoint for calculating BARD score for NAFLD fibrosis risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hepatology.bard_score import (
    BardScoreRequest,
    BardScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bard_score",
    response_model=BardScoreResponse,
    summary="Calculate BARD Score for NAFLD Fibrosis",
    description="Predicts risk of advanced fibrosis in patients with non-alcoholic fatty liver disease (NAFLD). The BARD score uses three simple clinical parameters (BMI, AST/ALT ratio, and diabetes) to identify patients at low risk of advanced fibrosis who may not require liver biopsy.",
    response_description="The calculated bard score with interpretation",
    operation_id="bard_score"
)
async def calculate_bard_score(request: BardScoreRequest):
    """
    Calculates BARD Score for NAFLD Fibrosis
    
    The BARD score is a simple non-invasive scoring system that uses BMI, 
    AST/ALT ratio, and diabetes status to predict the risk of advanced 
    fibrosis (F3-F4) in patients with non-alcoholic fatty liver disease (NAFLD).
    
    Args:
        request: Parameters including BMI, AST, ALT, and diabetes status
        
    Returns:
        BardScoreResponse: BARD score with risk assessment and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bard_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating BARD score",
                    "details": {"parameters": parameters}
                }
            )
        
        return BardScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for BARD score",
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