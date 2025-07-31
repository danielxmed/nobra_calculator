"""
Ottawa Knee Rule Router

Endpoint for calculating Ottawa Knee Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ottawa_knee_rule import (
    OttawaKneeRuleRequest,
    OttawaKneeRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ottawa_knee_rule",
    response_model=OttawaKneeRuleResponse,
    summary="Calculate Ottawa Knee Rule",
    description="Describes criteria for low-risk knee trauma patients, not warranting imaging. Rules out clinically significant knee fractures to reduce unnecessary x-rays with high sensitivity (98-100%).",
    response_description="The calculated ottawa knee rule with interpretation",
    operation_id="calculate_ottawa_knee_rule"
)
async def calculate_ottawa_knee_rule(request: OttawaKneeRuleRequest):
    """
    Calculates Ottawa Knee Rule
    
    Clinical decision rule for determining when knee radiography is required
    in patients with acute knee trauma. High sensitivity (98-100%) for 
    clinically significant fractures and can reduce unnecessary x-rays by 20-30%.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        OttawaKneeRuleResponse: Result with imaging recommendation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ottawa_knee_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ottawa Knee Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return OttawaKneeRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ottawa Knee Rule",
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