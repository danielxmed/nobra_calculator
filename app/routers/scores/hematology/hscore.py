"""
HScore for Reactive Hemophagocytic Syndrome Router

Endpoint for calculating HScore for Reactive Hemophagocytic Syndrome.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.hscore import (
    HScoreRequest,
    HScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hscore",
    response_model=HScoreResponse,
    summary="Calculate HScore for Reactive Hemophagocytic Syndrome",
    description="Estimates the risk of having reactive hemophagocytic syndrome (RHS) using a validated "
                "9-variable scoring system. The HScore includes 3 clinical variables (immunosuppression, "
                "temperature, organomegaly), 5 laboratory variables (cytopenias, triglycerides, fibrinogen, "
                "ferritin, AST), and 1 histologic variable (bone marrow hemophagocytosis). Scores range from "
                "0-337 points with probability stratification: ≤90 (<1%), 91-168 (1-25%), 169-250 (25-99%), "
                "and >250 (>99%) for reactive hemophagocytic syndrome. This life-threatening condition requires "
                "urgent recognition and treatment, making the HScore a critical diagnostic tool for clinicians "
                "evaluating patients with fever, cytopenias, and hyperinflammation.",
    response_description="The calculated HScore with probability percentage and risk stratification for "
                        "reactive hemophagocytic syndrome diagnosis",
    operation_id="hscore"
)
async def calculate_hscore(request: HScoreRequest):
    """
    Calculates HScore for Reactive Hemophagocytic Syndrome
    
    Uses a validated 9-variable model to estimate the probability of reactive 
    hemophagocytic syndrome, helping clinicians distinguish this life-threatening 
    condition from sepsis and hematologic malignancies.
    
    Args:
        request: Nine clinical, laboratory, and histologic parameters
        
    Returns:
        HScoreResponse: Score (0-337) with probability percentage and risk category
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hscore", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating HScore",
                    "details": {"parameters": parameters}
                }
            )
        
        return HScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HScore calculation",
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