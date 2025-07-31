"""
ARISCAT Score Router

Endpoint for calculating ARISCAT Score for Postoperative Pulmonary Complications.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.anesthesiology.ariscat_score import (
    AriscatScoreRequest,
    AriscatScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/ariscat_score", response_model=AriscatScoreResponse, summary="Calculate ARISCAT Score", description="Calculates ARISCAT Score for Postoperative Pulmonary Complications", response_description="ARISCAT score with risk stratification and clinical interpretation", operation_id="calculate_ariscat_score")
async def calculate_ariscat_score(request: AriscatScoreRequest):
    """
    Calculates ARISCAT Score for Postoperative Pulmonary Complications
    
    The ARISCAT score predicts the risk of postoperative pulmonary complications 
    including respiratory failure, respiratory infection, pleural effusion, 
    atelectasis, pneumothorax, bronchospasm, or aspiration pneumonitis after 
    surgery with general, neuraxial or regional anesthesia.
    
    Args:
        request: Parameters needed for ARISCAT calculation including age, 
                preoperative SpO2, respiratory infection history, anemia status,
                surgical incision type, surgery duration, and emergency status
        
    Returns:
        AriscatScoreResponse: ARISCAT score with risk stratification and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ariscat_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ARISCAT Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return AriscatScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ARISCAT Score",
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
