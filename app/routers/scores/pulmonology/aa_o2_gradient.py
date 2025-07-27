"""
Aa O2 Gradient router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology import AAO2GradientRequest, AAO2GradientResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/a_a_o2_gradient", response_model=AAO2GradientResponse)
async def calculate_a_a_o2_gradient(request: AAO2GradientRequest):
    """
    Calculates the alveolar-arterial oxygen gradient (A-a O₂)
    
    Args:
        request: Parameters required for calculation (age, FiO₂, PaCO₂, PaO₂, atmospheric pressure, respiratory quotient)
        
    Returns:
        AAO2GradientResponse: Result with A-a gradient and interpretation of lung function
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "fio2": request.fio2,
            "paco2": request.paco2,
            "pao2": request.pao2,
            "patm": request.patm,
            "respiratory_quotient": request.respiratory_quotient
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("a_a_o2_gradient", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating A-a O₂ Gradient",
                    "details": {"parameters": parameters}
                }
            )
        
        return AAO2GradientResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for A-a O₂ Gradient",
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