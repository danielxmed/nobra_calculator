"""
NIH Stroke Scale/Score (NIHSS) Router

Endpoint for calculating NIH Stroke Scale/Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.nihss import (
    NihssRequest,
    NihssResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/nihss",
    response_model=NihssResponse,
    summary="Calculate NIH Stroke Scale/Score (NIHSS)",
    description="Quantifies stroke severity based on weighted evaluation findings. The NIHSS is a 15-item "
                "neurological examination stroke scale used to evaluate the effect of acute cerebral infarction "
                "on consciousness, language, neglect, visual-field loss, extraocular movement, motor strength, "
                "ataxia, dysarthria, and sensory loss. Scores range from 0-42, with higher scores indicating "
                "greater stroke severity.",
    response_description="The calculated NIHSS score with stroke severity classification and clinical interpretation",
    operation_id="nihss"
)
async def calculate_nihss(request: NihssRequest):
    """
    Calculates NIH Stroke Scale/Score (NIHSS)
    
    The NIHSS is used to:
    - Quantify stroke severity at initial assessment
    - Monitor neurological status over time
    - Determine eligibility for thrombolytic therapy
    - Predict stroke outcomes
    - Standardize assessments in clinical trials
    
    Args:
        request: NIHSS parameters including all 15 items
        
    Returns:
        NihssResponse: Total score with severity classification and interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("nihss", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NIH Stroke Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return NihssResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NIH Stroke Scale",
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