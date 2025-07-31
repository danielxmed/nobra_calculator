"""
Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis Router

Endpoint for calculating BWPS for thyroid storm assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.burch_wartofsky_point_scale import (
    BurchWartofskypointScaleRequest,
    BurchWartofskypointScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/burch_wartofsky_point_scale",
    response_model=BurchWartofskypointScaleResponse,
    summary="Calculate Burch-Wartofsky Point Scale",
    description="Predicts likelihood that biochemical thyrotoxicosis is thyroid storm by evaluating clinical symptoms and precipitating factors. This empirically derived scoring system assesses multiple organ decompensation including thermoregulatory dysfunction, cardiovascular symptoms, neurological changes, and gastrointestinal symptoms.",
    response_description="The calculated burch wartofsky point scale with interpretation",
    operation_id="calculate_burch_wartofsky_point_scale"
)
async def calculate_burch_wartofsky_point_scale(request: BurchWartofskypointScaleRequest):
    """
    Calculates Burch-Wartofsky Point Scale (BWPS) for Thyrotoxicosis
    
    Predicts likelihood that biochemical thyrotoxicosis is thyroid storm by 
    evaluating clinical symptoms and precipitating factors. This empirically 
    derived scoring system assesses multiple organ decompensation including:
    
    - Thermoregulatory dysfunction (fever)
    - Central nervous system effects (agitation, delirium, coma)
    - Gastrointestinal-hepatic dysfunction (nausea, vomiting, jaundice)
    - Cardiovascular dysfunction (tachycardia, atrial fibrillation, heart failure)
    - Precipitating factors (infection, surgery, trauma, medication noncompliance)
    
    Score interpretation:
    - <25 points: Thyroid storm unlikely
    - 25-44 points: Impending thyroid storm (high suspicion)
    - ≥45 points: Thyroid storm highly suggestive (life-threatening emergency)
    
    This scale has a positive predictive value of 75% and negative predictive 
    value of 100%, making it a valuable diagnostic tool for this endocrine 
    emergency with 10-30% mortality rate.
    
    Args:
        request: Parameters needed for BWPS calculation
        
    Returns:
        BurchWartofskypointScaleResponse: Result with clinical interpretation and emergency treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("burch_wartofsky_point_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Burch-Wartofsky Point Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BurchWartofskypointScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={  
                "error": "ValidationError",
                "message": "Invalid parameters for Burch-Wartofsky Point Scale",
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