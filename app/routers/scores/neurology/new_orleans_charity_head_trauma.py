"""
New Orleans/Charity Head Trauma/Injury Rule Router

Endpoint for calculating New Orleans/Charity Head Trauma Rule.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.new_orleans_charity_head_trauma import (
    NewOrleansCharityHeadTraumaRequest,
    NewOrleansCharityHeadTraumaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/new_orleans_charity_head_trauma",
    response_model=NewOrleansCharityHeadTraumaResponse,
    summary="Calculate New Orleans/Charity Head Trauma/Injury Rule",
    description="Offers criteria for which patients are unlikely to require imaging after head trauma. Use ONLY in patients with head injury and loss of consciousness who are neurologically normal (GCS 15).",
    response_description="The calculated new orleans charity head trauma with interpretation",
    operation_id="new_orleans_charity_head_trauma"
)
async def calculate_new_orleans_charity_head_trauma(request: NewOrleansCharityHeadTraumaRequest):
    """
    Calculates New Orleans/Charity Head Trauma/Injury Rule
    
    Determines need for CT imaging in patients with minor head injury and loss 
    of consciousness who are neurologically normal (GCS 15). The rule is 100% 
    sensitive for detecting intracranial injuries requiring neurosurgical 
    intervention.
    
    Args:
        request: Parameters including 7 clinical criteria
        
    Returns:
        NewOrleansCharityHeadTraumaResponse: CT scan recommendation based on criteria
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("new_orleans_charity_head_trauma", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating New Orleans/Charity Head Trauma Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return NewOrleansCharityHeadTraumaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for New Orleans/Charity Head Trauma Rule",
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