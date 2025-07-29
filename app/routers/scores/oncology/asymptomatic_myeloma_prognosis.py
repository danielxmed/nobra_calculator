"""
Asymptomatic Myeloma Prognosis Router

Endpoint for calculating Asymptomatic Myeloma Prognosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.asymptomatic_myeloma_prognosis import (
    AsymptomaticMyelomaPrognosisRequest,
    AsymptomaticMyelomaPrognosisResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/asymptomatic_myeloma_prognosis", response_model=AsymptomaticMyelomaPrognosisResponse)
async def calculate_asymptomatic_myeloma_prognosis(request: AsymptomaticMyelomaPrognosisRequest):
    """
    Calculates Asymptomatic Myeloma Prognosis
    
    Predicts risk of progression of asymptomatic (smoldering) multiple myeloma 
    to active myeloma or amyloidosis based on bone marrow plasmacytosis 
    percentage and serum monoclonal protein level.
    
    This score stratifies patients into three risk groups:
    - Low Risk: Both factors low (bone marrow <10% AND serum M-protein <3 g/dL)
    - Intermediate Risk: One factor high 
    - High Risk: Both factors high (bone marrow ≥10% AND serum M-protein ≥3 g/dL)
    
    Args:
        request: Parameters including bone marrow plasmacytosis and serum M-protein level
        
    Returns:
        AsymptomaticMyelomaPrognosisResponse: Risk group with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("asymptomatic_myeloma_prognosis", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Asymptomatic Myeloma Prognosis",
                    "details": {"parameters": parameters}
                }
            )
        
        return AsymptomaticMyelomaPrognosisResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Asymptomatic Myeloma Prognosis",
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
