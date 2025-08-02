"""
Modified Fatigue Impact Scale (MFIS) Router

Endpoint for calculating MFIS fatigue impact assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.modified_fatigue_impact_scale import (
    ModifiedFatigueImpactScaleRequest,
    ModifiedFatigueImpactScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/modified_fatigue_impact_scale",
    response_model=ModifiedFatigueImpactScaleResponse,
    summary="Calculate Modified Fatigue Impact Scale (MFIS)",
    description="Calculates the Modified Fatigue Impact Scale (MFIS) for assessing fatigue impact on daily "
                "functioning. This 21-item questionnaire measures fatigue effects across physical, cognitive, "
                "and psychosocial domains using a 5-point Likert scale (0-4). Originally developed for multiple "
                "sclerosis patients, it is now used across various conditions causing fatigue. The scale provides "
                "a total score (0-84) and subscale scores for physical (0-36), cognitive (0-40), and psychosocial "
                "(0-8) functioning. A cutoff of 38 points indicates clinically significant fatigue impact requiring "
                "intervention. Changes ≥4 points predict significant effects on quality of life. Takes 5-10 minutes "
                "to complete and provides valuable insights for fatigue management strategies.",
    response_description="The calculated MFIS total score with subscale scores, clinical interpretation, and management recommendations",
    operation_id="modified_fatigue_impact_scale"
)
async def calculate_modified_fatigue_impact_scale(request: ModifiedFatigueImpactScaleRequest):
    """
    Calculates Modified Fatigue Impact Scale (MFIS)
    
    The MFIS is a validated tool for assessing the impact of fatigue on daily 
    functioning across physical, cognitive, and psychosocial domains. It helps 
    clinicians understand fatigue severity and develop targeted management strategies.
    
    Args:
        request: Twenty-one MFIS items each scored 0-4 (Never to Almost Always)
        
    Returns:
        ModifiedFatigueImpactScaleResponse: Total and subscale scores with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("modified_fatigue_impact_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Modified Fatigue Impact Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return ModifiedFatigueImpactScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Modified Fatigue Impact Scale",
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