"""
Modified SOAR Score for Stroke Router

Endpoint for predicting short-term mortality in acute stroke patients.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_soar_score import (
    ModifiedSoarScoreRequest,
    ModifiedSoarScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_soar_score",
    response_model=ModifiedSoarScoreResponse,
    summary="Calculate Modified SOAR Score for Stroke",
    description="Predicts short-term mortality in acute stroke patients using the Modified SOAR "
                "criteria, which improves upon the original SOAR score by incorporating stroke "
                "severity (NIHSS). The mSOAR score evaluates five clinical variables: age category, "
                "stroke subtype (ischemic vs hemorrhagic), Oxfordshire Community Stroke Project "
                "classification, pre-stroke modified Rankin Scale, and admission NIHSS score. "
                "This bedside tool provides prognostic stratification with area under ROC curve "
                "of 0.83, significantly improved from the original SOAR score (0.79). The score "
                "ranges from 0-9 points with four risk categories: Low Risk (0-2 points, 3-7% "
                "mortality), Moderate Risk (3-4 points, 8-20% mortality), High Risk (5-6 points, "
                "21-35% mortality), and Very High Risk (7-9 points, >35% mortality). Essential for "
                "clinical decision-making, family discussions, and resource allocation in acute "
                "stroke care.",
    response_description="The calculated Modified SOAR score with mortality risk stratification and clinical management recommendations",
    operation_id="modified_soar_score"
)
async def calculate_modified_soar_score(request: ModifiedSoarScoreRequest):
    """
    Calculates Modified SOAR Score for predicting short-term mortality in acute stroke
    
    Provides prognostic assessment using five easily available clinical variables 
    to stratify mortality risk and guide clinical decision-making in acute stroke care.
    
    Args:
        request: Clinical parameters including age category, stroke subtype, Oxfordshire 
                classification, pre-stroke functional status, and NIHSS score
        
    Returns:
        ModifiedSoarScoreResponse: mSOAR score with risk category and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_soar_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified SOAR Score for Stroke",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedSoarScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified SOAR Score for Stroke",
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