"""
Direct-Acting Oral Anticoagulants (DOAC) Score Router

Endpoint for calculating DOAC Score for bleeding risk assessment in AF patients on DOACs.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.doac_score import (
    DoacScoreRequest,
    DoacScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/doac_score",
    response_model=DoacScoreResponse,
    summary="Calculate Direct-Acting Oral Anticoagulants (DO...",
    description="Predicts bleeding risk in patients with atrial fibrillation on direct-acting oral anticoagulants",
    response_description="The calculated doac score with interpretation",
    operation_id="doac_score"
)
async def calculate_doac_score(request: DoacScoreRequest):
    """
    Calculates Direct-Acting Oral Anticoagulants (DOAC) Score
    
    Predicts bleeding risk in patients with atrial fibrillation on direct-acting 
    oral anticoagulants (DOACs) using 10 clinical parameters. The score 
    demonstrates superior performance compared to HAS-BLED in DOAC-treated 
    patients and provides five bleeding risk categories with annual bleeding 
    rate estimates.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        DoacScoreResponse: Bleeding risk assessment with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("doac_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DOAC Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return DoacScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DOAC Score",
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