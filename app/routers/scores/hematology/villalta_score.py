"""
Villalta Score for Post-thrombotic Syndrome (PTS) Router

Endpoint for calculating Villalta Score for post-thrombotic syndrome assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology.villalta_score import (
    VillaltaScoreRequest,
    VillaltaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/villalta_score",
    response_model=VillaltaScoreResponse,
    summary="Calculate Villalta Score for Post-thrombotic Syndrome",
    description="Calculates the Villalta Score to diagnose and grade post-thrombotic syndrome (PTS) severity "
                "following deep venous thrombosis (DVT). This validated clinical assessment tool combines "
                "5 patient-reported symptoms (pain, cramps, heaviness, paresthesia, pruritus) with "
                "6 physician-assessed clinical signs (pretibial edema, skin induration, hyperpigmentation, "
                "redness, venous ectasia, calf compression pain). Each component is rated 0-3 for severity. "
                "The Villalta score is the most widely used and recommended tool for PTS assessment, with "
                "good inter-observer reliability. Presence of venous ulcer automatically classifies PTS as "
                "severe. Score interpretation guides treatment decisions from conservative management for "
                "mild PTS to intensive interventions for severe disease. Assessment should be performed "
                "at least 6 months post-DVT when post-thrombotic changes have stabilized.",
    response_description="Villalta score with PTS severity classification, detailed clinical interpretation, and component breakdown",
    operation_id="villalta_score"
)
async def calculate_villalta_score(request: VillaltaScoreRequest):
    """
    Calculates Villalta Score for Post-thrombotic Syndrome
    
    Diagnoses and grades post-thrombotic syndrome severity using a standardized 
    assessment of patient symptoms and clinical signs.
    
    Args:
        request: Symptom and clinical sign assessments plus venous ulcer status
        
    Returns:
        VillaltaScoreResponse: Villalta score with PTS severity and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("villalta_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Villalta Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return VillaltaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Villalta Score",
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