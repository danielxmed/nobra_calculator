"""
Abbey Pain router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.geriatrics import AbbeyPainRequest, AbbeyPainResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/abbey_pain_scale", response_model=AbbeyPainResponse)
async def calculate_abbey_pain_scale(request: AbbeyPainRequest):
    """
    Calculates Abbey Pain Scale for pain assessment in dementia
    
    Args:
        request: Parameters required for calculation (vocalization, facial expression, body language, etc.)
        
    Returns:
        AbbeyPainResponse: Result with pain intensity and recommendations
    """
    try:
        # Convert request to dictionary
        parameters = {
            "vocalization": request.vocalization,
            "facial_expression": request.facial_expression,
            "body_language": request.body_language,
            "behavioral_change": request.behavioral_change,
            "physiological_change": request.physiological_change,
            "physical_change": request.physical_change
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abbey_pain_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Abbey Pain Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbbeyPainResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Abbey Pain Scale",
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