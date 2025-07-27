"""
Six Minute Walk router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology import SixMinuteWalkRequest, SixMinuteWalkResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/6_minute_walk_distance", response_model=SixMinuteWalkResponse)
async def calculate_6_minute_walk_distance(request: SixMinuteWalkRequest):
    """
    Calculates reference values for 6-minute walk distance
    
    Args:
        request: Parameters required for calculation (age, sex, height, weight, optional observed distance)
        
    Returns:
        SixMinuteWalkResponse: Result with predicted distance and functional capacity analysis
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "sex": request.sex.value,
            "height": request.height,
            "weight": request.weight
        }
        
        # Add observed distance if provided
        if request.observed_distance is not None:
            parameters["observed_distance"] = request.observed_distance
        
        # Execute calculation
        result = calculator_service.calculate_score("6_minute_walk_distance", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating 6 Minute Walk Distance",
                    "details": {"parameters": parameters}
                }
            )
        
        return SixMinuteWalkResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for 6 Minute Walk Distance",
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