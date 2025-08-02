"""
McMahon Score for Rhabdomyolysis Router

Endpoint for calculating McMahon Score for Rhabdomyolysis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.mcmahon_score import (
    McMahonScoreRequest,
    McMahonScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mcmahon_score",
    response_model=McMahonScoreResponse,
    summary="Calculate McMahon Score for Rhabdomyolysis",
    description="Calculates the McMahon Score to predict mortality or acute kidney injury (AKI) requiring "
                "renal replacement therapy in hospitalized rhabdomyolysis patients. This validated clinical "
                "prediction tool uses 8 variables available on admission to identify low-risk patients (score <6) "
                "who have only a 3% risk of death or AKI requiring RRT. Patients with scores ≥6 are not low risk "
                "and should receive aggressive renal protective therapy including high-volume fluid resuscitation. "
                "The score was developed for patients with CPK >5,000 U/L and is 68% specific and 86% sensitive "
                "for predicting need for RRT when the score is ≥6.",
    response_description="The calculated McMahon Score with risk stratification and clinical management recommendations",
    operation_id="mcmahon_score"
)
async def calculate_mcmahon_score(request: McMahonScoreRequest):
    """
    Calculates McMahon Score for Rhabdomyolysis
    
    The McMahon Score helps risk-stratify patients with rhabdomyolysis to guide early 
    management decisions and identify those who may benefit from aggressive fluid 
    resuscitation and close monitoring.
    
    Args:
        request: Clinical and laboratory parameters needed for calculation
        
    Returns:
        McMahonScoreResponse: Calculated score with risk category and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mcmahon_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating McMahon Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return McMahonScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for McMahon Score",
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