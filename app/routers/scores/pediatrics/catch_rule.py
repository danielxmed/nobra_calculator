"""
CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule Router

Endpoint for calculating CATCH Rule for pediatric head injury assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.catch_rule import (
    CatchRuleRequest,
    CatchRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/catch_rule", response_model=CatchRuleResponse)
async def calculate_catch_rule(request: CatchRuleRequest):
    """
    Calculates CATCH Rule for pediatric head injury assessment
    
    The CATCH (Canadian Assessment of Tomography for Childhood Head injury) Rule
    predicts clinically significant head injuries in children aged 0-16 years to
    guide CT imaging decisions in the emergency department.
    
    The rule stratifies patients into risk categories based on:
    
    HIGH-RISK FACTORS (need for neurologic intervention):
    - GCS <15 at two hours after injury
    - Suspected open or depressed skull fracture
    - History of worsening headache
    - Irritability on examination
    
    MEDIUM-RISK FACTORS (brain injury on CT):
    - Signs of basal skull fracture
    - Large, boggy scalp hematoma
    - Dangerous mechanism of injury
    
    Clinical Performance:
    - High-risk factors: 100% sensitive for neurologic intervention, 70.2% specific
    - Medium-risk factors: 98.1% sensitive for brain injury on CT, 50.1% specific
    - Developed from study of 3,866 children with minor head injury
    
    Inclusion Criteria:
    - Age 0-16 years with minor head injury
    - Initial GCS ≥13, injury within 24 hours
    - Must have witnessed LOC, amnesia, disorientation, vomiting ≥2x, or irritability
    
    Note: PECARN rule is often preferred due to more extensive validation,
    especially for children under 2 years.
    
    Args:
        request: Parameters needed for CATCH Rule assessment
        
    Returns:
        CatchRuleResponse: Risk stratification and CT imaging recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("catch_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CATCH Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return CatchRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CATCH Rule",
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