"""
Endotracheal Tube (ETT) Depth and Tidal Volume Calculator Router

Endpoint for calculating ETT depth and tidal volume recommendations.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.ett_depth_tidal_volume import (
    EttDepthTidalVolumeRequest,
    EttDepthTidalVolumeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ett_depth_tidal_volume", response_model=EttDepthTidalVolumeResponse)
async def calculate_ett_depth_tidal_volume(request: EttDepthTidalVolumeRequest):
    """
    Calculates Endotracheal Tube (ETT) Depth and Tidal Volume
    
    Estimates optimal ETT placement depth using the Chula formula and calculates 
    target tidal volume based on ideal body weight for lung-protective ventilation. 
    Provides immediate guidance for safe ETT positioning and evidence-based 
    mechanical ventilation settings.
    
    Args:
        request: Parameters including patient height and biological sex
        
    Returns:
        EttDepthTidalVolumeResponse: Calculated ETT depth and tidal volume recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ett_depth_tidal_volume", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ETT depth and tidal volume",
                    "details": {"parameters": parameters}
                }
            )
        
        return EttDepthTidalVolumeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ETT depth and tidal volume calculation",
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