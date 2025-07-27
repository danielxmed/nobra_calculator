"""
Aas router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry import AasRequest, AasResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/aas", response_model=AasResponse)
async def calculate_aas(request: AasRequest):
    """
    Calculates Abuse Assessment Screen (AAS)
    
    Args:
        request: Parameters required for screening (questions about emotional, physical, and sexual abuse)
        
    Returns:
        AasResponse: Result of domestic violence screening
    """
    try:
        # Convert request to dictionary
        parameters = {
            "emotional_physical_abuse": request.emotional_physical_abuse.value,
            "physical_hurt_recently": request.physical_hurt_recently.value,
            "physical_hurt_pregnancy": request.physical_hurt_pregnancy.value,
            "sexual_abuse": request.sexual_abuse.value,
            "afraid_of_partner": request.afraid_of_partner.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("aas", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AAS",
                    "details": {"parameters": parameters}
                }
            )
        
        return AasResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AAS",
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