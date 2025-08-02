"""
Medication Regimen Complexity-Intensive Care Unit (MRC-ICU) Score Router

Endpoint for calculating MRC-ICU Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.mrc_icu_score import (
    MrcIcuScoreRequest,
    MrcIcuScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mrc_icu_score",
    response_model=MrcIcuScoreResponse,
    summary="Calculate Medication Regimen Complexity-ICU (MRC-ICU) Score",
    description="Calculates the Medication Regimen Complexity-Intensive Care Unit (MRC-ICU) "
                "Score to predict patient outcomes (mortality, length of stay), ICU complications "
                "(fluid overload), and pharmacist workload (amount and intensity of intervention) "
                "in the ICU. The MRC-ICU is an objective, quantitative scoring tool that describes "
                "the relative complexity of medication regimens in critically ill patients. It "
                "consists of 39 discrete medication items (simplified version presented here), "
                "each assigned a weighted value (1-3 points) that is summed to create a total "
                "MRC-ICU score. Every 1-point increase is associated with 7% increased odds of "
                "mortality and 0.25 day increase in ICU length of stay. The score has been "
                "validated in multiple large multicenter studies and correlates with pharmacist "
                "workload metrics. Scores <10 indicate low complexity, 10-19 moderate complexity "
                "(mean ~10.3), and ≥20 high complexity requiring intensive pharmacist intervention.",
    response_description="The calculated MRC-ICU score with complexity classification and clinical implications",
    operation_id="mrc_icu_score"
)
async def calculate_mrc_icu_score(request: MrcIcuScoreRequest):
    """
    Calculates Medication Regimen Complexity-ICU (MRC-ICU) Score
    
    The MRC-ICU quantifies medication regimen complexity in ICU patients to predict
    outcomes and guide pharmacist resource allocation. Higher scores indicate greater
    complexity and are associated with worse outcomes.
    
    Args:
        request: Medication categories and counts for MRC-ICU calculation
        
    Returns:
        MrcIcuScoreResponse: Calculated score with complexity level and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mrc_icu_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MRC-ICU Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MrcIcuScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MRC-ICU Score calculation",
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