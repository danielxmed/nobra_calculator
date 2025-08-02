"""
Migraine Disability Assessment (MIDAS) Router

Endpoint for calculating MIDAS score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.midas import (
    MidasRequest,
    MidasResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/midas",
    response_model=MidasResponse,
    summary="Calculate Migraine Disability Assessment (MIDAS)",
    description="Quantifies headache-related disability over a 3-month period to guide treatment "
                "decisions. The MIDAS score helps identify patients who need preventive therapy "
                "and tracks treatment response. Scores ≥11 indicate moderate to severe disability "
                "warranting prophylaxis. Assesses impact across work, household, and social domains.",
    response_description="The calculated MIDAS score with disability grade and treatment recommendations",
    operation_id="midas"
)
async def calculate_midas(request: MidasRequest):
    """
    Calculates Migraine Disability Assessment (MIDAS)
    
    Measures functional impact of headaches over the past 3 months to
    determine treatment strategies and monitor therapeutic response.
    
    Args:
        request: Number of days affected in each domain (work, household, social)
        
    Returns:
        MidasResponse: Total score, disability grade, and treatment guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("midas", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MIDAS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MidasResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MIDAS score",
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