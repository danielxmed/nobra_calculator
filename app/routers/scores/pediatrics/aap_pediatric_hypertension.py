"""
Aap Pediatric Hypertension router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics import AapPediatricHypertensionRequest, AapPediatricHypertensionResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/aap_pediatric_hypertension", response_model=AapPediatricHypertensionResponse)
async def calculate_aap_pediatric_hypertension(request: AapPediatricHypertensionRequest):
    """
    Calculates AAP 2017 pediatric blood pressure classification
    
    Args:
        request: Parameters required for calculation (age, sex, height, systolic BP, diastolic BP)
        
    Returns:
        AapPediatricHypertensionResponse: Result with pediatric BP classification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "height": request.height,
            "systolic_bp": request.systolic_bp,
            "diastolic_bp": request.diastolic_bp
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aap_pediatric_hypertension", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AAP Pediatric Hypertension",
                    "details": {"parameters": parameters}
                }
            )
        
        return AapPediatricHypertensionResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AAP Pediatric Hypertension",
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