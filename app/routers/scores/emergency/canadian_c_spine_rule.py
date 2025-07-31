"""
Canadian C-Spine Rule Router

Endpoint for calculating Canadian C-Spine Rule for cervical spine imaging decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.canadian_c_spine_rule import (
    CanadianCSpineRuleRequest,
    CanadianCSpineRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/canadian_c_spine_rule",
    response_model=CanadianCSpineRuleResponse,
    summary="Calculate Canadian C-Spine Rule",
    description="The Canadian C-Spine Rule is a clinical decision tool that helps determine whether cervical spine imaging can be safely avoided in alert and stable trauma patients. It uses high-risk factors, low-risk factors, and range of motion assessment to rule out clinically significant cervical spine injury (CSI) with 100% sensitivity.",
    response_description="The calculated canadian c spine rule with interpretation",
    operation_id="canadian_c_spine_rule"
)
async def calculate_canadian_c_spine_rule(request: CanadianCSpineRuleRequest):
    """
    Calculates Canadian C-Spine Rule for cervical spine imaging decisions
    
    The Canadian C-Spine Rule is a validated clinical decision tool that helps 
    determine whether cervical spine imaging can be safely avoided in alert and 
    stable trauma patients. It uses high-risk factors, low-risk factors, and 
    range of motion assessment to rule out clinically significant cervical spine 
    injury with 100% sensitivity.
    
    Key features:
    - Applicable to alert (GCS 15) and stable trauma patients aged ≥16 years
    - Injury must be <48 hours old
    - Excludes penetrating trauma, known vertebral disease, pregnancy
    - Three-step approach: high-risk factors → low-risk factors → ROM assessment
    - 100% sensitivity for clinically significant cervical spine injuries
    - Reduces unnecessary imaging by approximately 42.5%
    
    High-risk factors (mandate imaging):
    - Age ≥65 years
    - Dangerous mechanism of injury
    - Paresthesias in extremities
    
    Low-risk factors (allow ROM testing):
    - Simple rear-end MVC
    - Sitting position in ED
    - Ambulatory at any time
    - Delayed onset of neck pain
    - Absence of midline C-spine tenderness
    
    Args:
        request: Parameters for Canadian C-Spine Rule calculation
        
    Returns:
        CanadianCSpineRuleResponse: Imaging recommendation based on the rule
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("canadian_c_spine_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Canadian C-Spine Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return CanadianCSpineRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Canadian C-Spine Rule",
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