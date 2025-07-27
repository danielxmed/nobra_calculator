"""
Four Ts router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology import FourTsRequest, FourTsResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/4ts_hit", response_model=FourTsResponse)
async def calculate_4ts_hit(request: FourTsRequest):
    """
    Calculates the 4Ts Score for HIT probability assessment
    
    Args:
        request: Parameters required for calculation (thrombocytopenia, timing, thrombosis, other causes)
        
    Returns:
        FourTsResponse: Result with probability of heparin-induced thrombocytopenia
    """
    try:
        # Convert request to dictionary
        parameters = {
            "thrombocytopenia_severity": request.thrombocytopenia_severity.value,
            "timing_onset": request.timing_onset.value,
            "thrombosis_sequelae": request.thrombosis_sequelae.value,
            "other_causes": request.other_causes.value
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("4ts_hit", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 4Ts Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FourTsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 4Ts Score",
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