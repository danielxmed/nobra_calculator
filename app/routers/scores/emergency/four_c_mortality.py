"""
Four C Mortality router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency import FourCMortalityRequest, FourCMortalityResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/4c_mortality_covid19", response_model=FourCMortalityResponse)
async def calculate_4c_mortality_covid19(request: FourCMortalityRequest):
    """
    Calculates the 4C Mortality Score for COVID-19
    
    Args:
        request: Parameters required for calculation (age, sex, comorbidities, vital signs, lab tests)
        
    Returns:
        FourCMortalityResponse: Result with hospital mortality risk stratification
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "comorbidities": request.comorbidities,
            "respiratory_rate": request.respiratory_rate,
            "oxygen_saturation": request.oxygen_saturation,
            "glasgow_coma_scale": request.glasgow_coma_scale,
            "urea_unit": request.urea_unit.value,
            "urea_value": request.urea_value,
            "crp": request.crp
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("4c_mortality_covid19", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4C Mortality Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourCMortalityResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4C Mortality Score",
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