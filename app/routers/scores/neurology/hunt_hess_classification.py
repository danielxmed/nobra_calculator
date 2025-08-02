"""
Hunt & Hess Classification of Subarachnoid Hemorrhage Router

Endpoint for calculating Hunt-Hess Classification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.hunt_hess_classification import (
    HuntHessClassificationRequest,
    HuntHessClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hunt_hess_classification",
    response_model=HuntHessClassificationResponse,
    summary="Calculate Hunt & Hess Classification of Subarachnoid Hemorrhage",
    description="Classifies severity of aneurysmal subarachnoid hemorrhage based on clinical "
                "presentation to predict mortality and guide surgical risk assessment. The "
                "Hunt-Hess scale, developed in 1968 and modified in 1974, grades patients "
                "from I to V based on neurological symptoms and level of consciousness. "
                "Grade I (asymptomatic/minimal headache) has ~70% survival with low surgical "
                "risk, while Grade V (deep coma/decerebrate rigidity) has ~10% survival with "
                "very high surgical risk. The presence of serious systemic disease increases "
                "the grade by one level. This widely-used classification system helps clinicians "
                "make treatment decisions, assess prognosis, and provide prognostic information "
                "to patients and families.",
    response_description="The calculated Hunt-Hess grade with survival rates, mortality rates, "
                        "and surgical risk assessment",
    operation_id="hunt_hess_classification"
)
async def calculate_hunt_hess_classification(request: HuntHessClassificationRequest):
    """
    Calculates Hunt & Hess Classification of Subarachnoid Hemorrhage
    
    Uses clinical presentation and presence of systemic disease to assign 
    grades I-V with corresponding mortality prediction and surgical risk assessment.
    
    Args:
        request: Clinical presentation and serious systemic disease status
        
    Returns:
        HuntHessClassificationResponse: Grade (I-V) with prognosis and surgical risk
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hunt_hess_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hunt-Hess Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return HuntHessClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hunt-Hess Classification",
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