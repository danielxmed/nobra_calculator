"""
Curb 65 router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology import Curb65Request, Curb65Response
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post(
    "/curb_65",
    response_model=Curb65Response,
    summary="Calculate CURB-65 Score for Pneumonia Severity",
    description="Assesses the severity of community-acquired pneumonia (CAP) to determine the need for hospital admission",
    response_description="The calculated curb 65 with interpretation",
    operation_id="curb_65"
)
async def calculate_curb_65(request: Curb65Request):
    """
    Calculates the CURB-65 Score for pneumonia severity assessment
    
    Args:
        request: Parameters required for calculation
        
    Returns:
        Curb65Response: Result with clinical interpretation and treatment recommendation
    """
    try:
        # Convert request to dictionary
        parameters = {
            "confusion": request.confusion,
            "urea": request.urea,
            "respiratory_rate": request.respiratory_rate,
            "systolic_bp": request.systolic_bp,
            "diastolic_bp": request.diastolic_bp,
            "age": request.age
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("curb_65", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CURB-65",
                    "details": {"parameters": parameters}
                }
            )
        
        return Curb65Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CURB-65",
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