"""
Abic Score router endpoint
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology import AbicScoreRequest, AbicScoreResponse
from app.services.calculator_service import calculator_service

router = APIRouter()

@router.post("/abic_score", response_model=AbicScoreResponse)
async def calculate_abic_score(request: AbicScoreRequest):
    """
    Calculates ABIC Score for alcoholic hepatitis
    
    Args:
        request: Parameters required for calculation (age, bilirubin, creatinine, INR)
        
    Returns:
        AbicScoreResponse: Result with survival prognosis
    """
    try:
        # Convert request to dictionary
        parameters = {
            "age": request.age,
            "serum_bilirubin": request.serum_bilirubin,
            "serum_creatinine": request.serum_creatinine,
            "inr": request.inr
        }
        
        # Execute calculation
        result = calculator_service.calculate_score("abic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ABIC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AbicScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ABIC Score",
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