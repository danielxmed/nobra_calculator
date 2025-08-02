"""
Immunization Schedule Calculator Router

Endpoint for immunization schedule calculation based on CDC vaccination guidelines.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.immunization_schedule_calculator import (
    ImmunizationScheduleCalculatorRequest,
    ImmunizationScheduleCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/immunization_schedule_calculator",
    response_model=ImmunizationScheduleCalculatorResponse,
    summary="Calculate Immunization Schedule",
    description="Determines what immunizations/vaccinations are due based on patient's age according to CDC vaccination guidelines. This clinical decision support tool helps healthcare providers identify appropriate vaccinations for pediatric and adult patients based on standardized immunization schedules. The calculator provides general vaccination recommendations for infants (0-23 months), children and adolescents (2-17 years), and adults (18+ years) following CDC immunization schedules. Key features include age-appropriate vaccine recommendations, catch-up schedule guidance, and consideration of routine, risk-based, and occupational vaccines. The tool requires clinical judgment and knowledge of patient's vaccination history for optimal use, including assessment of contraindications such as immunocompromised state or pregnancy for live vaccines.",
    response_description="Vaccination recommendations based on patient age with clinical guidance and CDC schedule category",
    operation_id="immunization_schedule_calculator"
)
async def calculate_immunization_schedule_calculator(request: ImmunizationScheduleCalculatorRequest):
    """
    Calculates Immunization Schedule based on CDC guidelines
    
    Provides vaccination recommendations for pediatric and adult patients based on 
    CDC immunization schedules and patient age.
    
    Args:
        request: Patient age information for immunization schedule determination
        
    Returns:
        ImmunizationScheduleCalculatorResponse: Vaccination recommendations with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("immunization_schedule_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Immunization Schedule",
                    "details": {"parameters": parameters}
                }
            )
        
        return ImmunizationScheduleCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Immunization Schedule Calculator",
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
                "message": "Internal error in immunization schedule calculation",
                "details": {"error": str(e)}
            }
        )