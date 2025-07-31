"""
ABC/2 Formula for Intracerebral Hemorrhage Volume Router

Endpoint for calculating ABC/2 ICH Volume.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.abc2_ich_volume import (
    Abc2IchVolumeRequest,
    Abc2IchVolumeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/abc2_ich_volume",
    response_model=Abc2IchVolumeResponse,
    summary="Calculate ABC/2 Formula for Intracerebral Hemorrhage Volume",
    description="Predicts volume of intracranial hemorrhage from CT measurements using a simplified ellipsoid formula. Widely used bedside method for rapid ICH volume estimation.",
    response_description="The calculated abc2 ich volume with interpretation",
    operation_id="abc2_ich_volume"
)
async def calculate_abc2_ich_volume(request: Abc2IchVolumeRequest):
    """
    Calculates ABC/2 Formula for Intracerebral Hemorrhage Volume
    
    Predicts volume of intracranial hemorrhage from CT measurements using the
    Kothari ABC/2 method, a simplified ellipsoid formula widely used for bedside
    ICH volume estimation.
    
    The ABC/2 formula is derived from the ellipsoid volume equation where:
    - A = greatest hemorrhage diameter on CT slice with largest area  
    - B = diameter 90 degrees to A on the same CT slice
    - C = weighted number of CT slices × slice thickness (converted to cm)
    
    Volume = (A × B × C) / 2
    
    This method correlates well with planimetric measurements (R² = 0.96) and
    can be performed in less than 1 minute at the bedside.
    
    Args:
        request: Parameters needed for ABC/2 volume calculation
        
    Returns:
        Abc2IchVolumeResponse: Volume result with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("abc2_ich_volume", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABC/2 ICH Volume",
                    "details": {"parameters": parameters}
                }
            )
        
        return Abc2IchVolumeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABC/2 ICH Volume calculation",
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
                "message": "Internal error in ABC/2 ICH Volume calculation",
                "details": {"error": str(e)}
            }
        )
