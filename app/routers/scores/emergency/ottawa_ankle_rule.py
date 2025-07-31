"""
Ottawa Ankle Rule Router

Endpoint for calculating Ottawa Ankle Rule recommendations.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ottawa_ankle_rule import (
    OttawaAnkleRuleRequest,
    OttawaAnkleRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ottawa_ankle_rule",
    response_model=OttawaAnkleRuleResponse,
    summary="Calculate Ottawa Ankle Rule",
    description="Rules out clinically significant foot and ankle fractures to reduce use of x-ray imaging. Provides separate criteria for ankle and foot x-rays based on location of pain and specific clinical findings.",
    response_description="The calculated ottawa ankle rule with interpretation",
    operation_id="ottawa_ankle_rule"
)
async def calculate_ottawa_ankle_rule(request: OttawaAnkleRuleRequest):
    """
    Calculates Ottawa Ankle Rule recommendations
    
    Rules out clinically significant foot and ankle fractures to reduce use of x-ray imaging.
    High sensitivity (98-100%) for detecting fractures, can reduce unnecessary radiographs by 30-40%.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OttawaAnkleRuleResponse: Result with x-ray recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ottawa_ankle_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ottawa Ankle Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return OttawaAnkleRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ottawa Ankle Rule",
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