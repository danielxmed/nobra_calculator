"""
Canadian CT Head Injury/Trauma Rule Router

Endpoint for calculating Canadian CT Head Rule for minor head injury imaging decisions.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.canadian_ct_head_rule import (
    CanadianCtHeadRuleRequest,
    CanadianCtHeadRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/canadian_ct_head_rule", response_model=CanadianCtHeadRuleResponse)
async def calculate_canadian_ct_head_rule(request: CanadianCtHeadRuleRequest):
    """
    Calculates Canadian CT Head Rule for minor head injury imaging decisions
    
    The Canadian CT Head Rule is a validated clinical decision tool that helps 
    determine which patients with minor head injury require CT head imaging. It 
    uses high-risk and medium-risk criteria to identify patients who may have 
    injuries requiring neurosurgical intervention or admission. The rule is 100% 
    sensitive for detecting neurosurgical lesions and can reduce unnecessary CT 
    scans by approximately 30%.
    
    Key features:
    - Applicable to minor head injury patients (GCS 13-15) with LOC, amnesia, or disorientation
    - Age requirement: ≥16 years
    - Excludes anticoagulated patients, seizures, obvious skull fractures
    - 100% sensitive for injuries requiring neurosurgical intervention
    - 98.4% sensitive for clinically important brain injury
    - Reduces CT imaging by 30-50%
    
    High-risk criteria (require CT):
    - GCS <15 at 2 hours after injury
    - Suspected open or depressed skull fracture
    - Any sign of basilar skull fracture
    - Vomiting ≥2 episodes
    - Age ≥65 years
    
    Medium-risk criteria (require CT):
    - Amnesia before impact >30 minutes
    - Dangerous mechanism (pedestrian struck, ejected, fall >3 feet)
    
    Args:
        request: Parameters for Canadian CT Head Rule calculation
        
    Returns:
        CanadianCtHeadRuleResponse: CT imaging recommendation based on the rule
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("canadian_ct_head_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Canadian CT Head Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return CanadianCtHeadRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Canadian CT Head Rule",
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