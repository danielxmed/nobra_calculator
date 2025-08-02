"""
Trunk Impairment Scale Router

Endpoint for calculating Trunk Impairment Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.trunk_impairment_scale import (
    TrunkImpairmentScaleRequest,
    TrunkImpairmentScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/trunk_impairment_scale",
    response_model=TrunkImpairmentScaleResponse,
    summary="Calculate Trunk Impairment Scale",
    description="Calculates the Trunk Impairment Scale (TIS) for quantifying trunk motor impairment after stroke. "
                "This validated assessment tool evaluates three domains of trunk function: static sitting balance "
                "(3 items, 0-7 points), dynamic sitting balance (10 items, 0-10 points), and coordination "
                "(4 items, 0-6 points) for a total possible score of 23 points. The TIS has also been validated "
                "in Parkinson's disease patients. Higher scores indicate better trunk function, while lower scores "
                "suggest greater impairment and higher rehabilitation needs. A special rule applies: if the patient "
                "cannot maintain the basic sitting position without support for 10 seconds, the total score is 0.",
    response_description="The calculated Trunk Impairment Scale score with impairment classification and rehabilitation recommendations",
    operation_id="trunk_impairment_scale"
)
async def calculate_trunk_impairment_scale(request: TrunkImpairmentScaleRequest):
    """
    Calculates Trunk Impairment Scale
    
    The Trunk Impairment Scale (TIS) is a clinical assessment tool that quantifies trunk motor 
    impairment after stroke and has been validated in Parkinson's disease. It evaluates trunk 
    function through 17 specific items across three domains:
    
    - Static sitting balance (3 items): Basic sitting position maintenance, therapist-assisted 
      leg crossing, and patient-performed leg crossing (0-7 points)
    - Dynamic sitting balance (10 items): Elbow movements and pelvis lifts with assessments 
      of shortening/lengthening and compensation patterns (0-10 points)  
    - Coordination (4 items): Upper and lower trunk rotation movements with speed assessment 
      (0-6 points)
    
    The assessment requires specific positioning: patient sits on edge of bed/table without 
    back or arm support, thighs fully in contact with surface, knees bent at 90°, feet 
    hip-width apart and flat on floor, arms resting on legs, head and trunk in midline position.
    
    Scores range from 0-23 points with established cut-off values for impairment classification. 
    The tool includes dependency rules where failing certain items automatically results in 
    zero scores for related follow-up assessments.
    
    Args:
        request: Parameters for all 17 TIS assessment items
        
    Returns:
        TrunkImpairmentScaleResponse: Result with impairment classification and recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("trunk_impairment_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Trunk Impairment Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return TrunkImpairmentScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Trunk Impairment Scale",
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