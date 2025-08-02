"""
Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation Router

Endpoint for calculating Ottawa SAH Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ottawa_sah_rule import (
    OttawaSahRuleRequest,
    OttawaSahRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ottawa_sah_rule",
    response_model=OttawaSahRuleResponse,
    summary="Calculate Ottawa SAH Rule",
    description="Calculates the Ottawa Subarachnoid Hemorrhage (SAH) Rule for Headache Evaluation, "
                "a validated clinical decision tool to identify alert patients with acute headache who "
                "are at risk for subarachnoid hemorrhage. This rule demonstrates 100% sensitivity for "
                "detecting SAH, making it an excellent rule-out tool for emergency physicians. The rule "
                "evaluates six clinical criteria: age ≥40 years, neck pain/stiffness, witnessed loss of "
                "consciousness, onset during exertion, thunderclap headache, and limited neck flexion. "
                "If all criteria are negative, SAH can be safely ruled out. If any criterion is positive, "
                "further investigation with CT scan or lumbar puncture is recommended. The rule has low "
                "specificity (15.3%) but maintains perfect sensitivity across multiple validation studies.",
    response_description="The Ottawa SAH Rule result with detailed clinical management recommendations and emergency protocols",
    operation_id="ottawa_sah_rule"
)
async def calculate_ottawa_sah_rule(request: OttawaSahRuleRequest):
    """
    Calculates Ottawa Subarachnoid Hemorrhage (SAH) Rule
    
    This validated rule helps emergency physicians safely rule out SAH in patients
    with acute headache while guiding appropriate imaging decisions.
    
    Args:
        request: Clinical criteria including age, neck symptoms, consciousness,
                exertion association, thunderclap characteristics, and neck flexion
        
    Returns:
        OttawaSahRuleResponse: Result with emergency management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ottawa_sah_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Ottawa SAH Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return OttawaSahRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Ottawa SAH Rule",
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