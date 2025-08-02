"""
HINTS for Stroke in Acute Vestibular Syndrome Router

Endpoint for evaluating HINTS examination.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.hints import (
    HintsRequest,
    HintsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hints",
    response_model=HintsResponse,
    summary="Evaluate HINTS for Stroke in Acute Vestibular Syndrome",
    description="Evaluates the HINTS (Head Impulse, Nystagmus, Test of Skew) examination to "
                "differentiate between peripheral and central causes of acute vestibular syndrome, "
                "particularly to identify posterior circulation strokes. This three-step bedside "
                "oculomotor examination has been shown to be more sensitive than early MRI "
                "diffusion-weighted imaging for detecting posterior circulation strokes. The exam "
                "is only applicable for patients with continuous vertigo lasting >24 hours. A "
                "'Benign HINTS' pattern (abnormal head impulse test, direction-fixed nystagmus, "
                "absent skew deviation) suggests peripheral cause, while a 'Dangerous HINTS' "
                "pattern (any central finding) requires urgent neuroimaging and stroke evaluation.",
    response_description="HINTS examination interpretation with clinical recommendations",
    operation_id="hints"
)
async def calculate_hints(request: HintsRequest):
    """
    Evaluates HINTS examination for stroke in acute vestibular syndrome
    
    The HINTS exam helps emergency physicians and neurologists quickly assess
    whether acute continuous vertigo is due to a benign peripheral cause or
    a dangerous central cause like stroke.
    
    Args:
        request: Three components of the HINTS examination
        
    Returns:
        HintsResponse: Pattern interpretation and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hints", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error evaluating HINTS examination",
                    "details": {"parameters": parameters}
                }
            )
        
        return HintsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for HINTS examination",
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
                "message": "Internal error in HINTS evaluation",
                "details": {"error": str(e)}
            }
        )