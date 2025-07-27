"""
Abcd2 router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology import Abcd2Request, Abcd2Response
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/abcd2_score", response_model=Abcd2Response)
async def calculate_abcd2_score(request: Abcd2Request):
    """
    Calculates the ABCD² Score to estimate stroke risk after TIA
    
    Args:
        request: Parameters required for calculation (age, BP, clinical features, duration, diabetes)
        
    Returns:
        Abcd2Response: Result with stroke risk stratification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "blood_pressure": request.blood_pressure.value,
            "clinical_features": request.clinical_features.value,
            "duration": request.duration.value,
            "diabetes": request.diabetes.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abcd2_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABCD² Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return Abcd2Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABCD² Score",
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