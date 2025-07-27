"""
Anc router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.hematology import AncRequest, AncResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/anc", response_model=AncResponse)
async def calculate_anc(request: AncRequest):
    """
    Calculates ANC (Absolute Neutrophil Count)
    
    Args:
        request: Parameters required for calculation (white blood cells, neutrophil percentage, bands)
        
    Returns:
        AncResponse: Result with absolute neutrophil count and infection risk
    """
    try:
        # Convert request to dictionary
        parameters = {
            "wbc_count": request.white_blood_cells,
            "segmented_neutrophils": request.neutrophil_percentage,
            "band_neutrophils": request.band_percentage
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("anc", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ANC",
                    "details": {"parameters": parameters}
                }
            )
        
        return AncResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ANC",
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