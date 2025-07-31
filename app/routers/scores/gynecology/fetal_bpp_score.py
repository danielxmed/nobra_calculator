"""
Fetal Biophysical Profile (BPP) Score Router

Endpoint for calculating Fetal BPP Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gynecology.fetal_bpp_score import (
    FetalBppScoreRequest,
    FetalBppScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fetal_bpp_score",
    response_model=FetalBppScoreResponse,
    summary="Calculate Fetal Biophysical Profile (BPP) Score",
    description="Predicts need for urgent delivery based on sonographic and non-stress test. Assesses for fetal distress in high-risk pregnancies.",
    response_description="The calculated fetal bpp score with interpretation",
    operation_id="calculate_fetal_bpp_score"
)
async def calculate_fetal_bpp_score(request: FetalBppScoreRequest):
    """
    Calculates Fetal Biophysical Profile (BPP) Score
    
    The BPP is a prenatal ultrasound evaluation of fetal well-being using five
    criteria: fetal breathing, movement, tone, amniotic fluid volume, and 
    non-stress test. Used to assess need for urgent delivery in high-risk pregnancies.
    
    Args:
        request: BPP parameters (each scored 0 or 2)
        
    Returns:
        FetalBppScoreResponse: BPP score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fetal_bpp_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fetal BPP Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return FetalBppScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fetal BPP Score",
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