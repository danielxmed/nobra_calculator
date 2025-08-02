"""
Hydroxychloroquine (Plaquenil) Dosing Calculator Router

Endpoint for calculating Hydroxychloroquine dosing to minimize retinopathy risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.hydroxychloroquine_dosing import (
    HydroxychloroquineDosingRequest,
    HydroxychloroquineDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/hydroxychloroquine_dosing",
    response_model=HydroxychloroquineDosingResponse,
    summary="Calculate Hydroxychloroquine (Plaquenil) Dosing",
    description="Calculates maximum daily hydroxychloroquine dose to minimize retinopathy risk "
                "based on 2016 American Academy of Ophthalmology guidelines. Uses actual body weight "
                "to determine safe dosing limits with a maximum of 5 mg/kg/day, reduced from the "
                "previous 6.5 mg/kg/day recommendation. The calculator considers clinical indication "
                "(rheumatoid arthritis, lupus, malaria) and risk factors (age >65, renal disease, "
                "liver disease, previous retinal disease) to provide personalized dosing recommendations. "
                "Doses ≤5 mg/kg/day have a 2% 10-year retinopathy risk compared to 10% risk with "
                "higher doses. Includes practical dosing schedules using standard tablet strengths "
                "and monitoring recommendations for ophthalmologic screening.",
    response_description="The calculated maximum daily dose with retinopathy risk assessment, "
                        "practical dosing schedule, and monitoring recommendations",
    operation_id="hydroxychloroquine_dosing"
)
async def calculate_hydroxychloroquine_dosing(request: HydroxychloroquineDosingRequest):
    """
    Calculates Hydroxychloroquine (Plaquenil) Dosing
    
    Determines safe daily dosing limits based on actual body weight and risk factors 
    to minimize hydroxychloroquine-induced retinopathy while maintaining therapeutic efficacy.
    
    Args:
        request: Body weight, clinical indication, and risk factor status
        
    Returns:
        HydroxychloroquineDosingResponse: Maximum dose with risk assessment and monitoring plan
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("hydroxychloroquine_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Hydroxychloroquine dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return HydroxychloroquineDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Hydroxychloroquine dosing calculation",
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