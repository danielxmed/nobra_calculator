"""
Myxedema Coma Diagnostic Score Router

Endpoint for calculating Myxedema Coma Diagnostic Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.endocrinology.myxedema_coma_diagnostic_score import (
    MyxedemaComatDiagnosticScoreRequest,
    MyxedemaComatDiagnosticScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/myxedema_coma_diagnostic_score",
    response_model=MyxedemaComatDiagnosticScoreResponse,
    summary="Calculate Myxedema Coma Diagnostic Score",
    description="Calculates the Myxedema Coma Diagnostic Score, a validated clinical tool for early recognition "
                "and diagnosis of myxedema coma, a rare but life-threatening decompensated state of extreme "
                "hypothyroidism. This scoring system evaluates thermoregulatory, central nervous, cardiovascular, "
                "gastrointestinal, and metabolic dysfunction along with precipitating events to facilitate prompt "
                "diagnosis and life-saving treatment. The score ranges from 0-100 points with specific thresholds: "
                "<25 (unlikely), 25-44 (possible), 45-59 (at risk), ≥60 (diagnostic requiring immediate treatment). "
                "The system demonstrates 100% sensitivity and 85.7% specificity at the diagnostic threshold.",
    response_description="The calculated Myxedema Coma Diagnostic Score with clinical interpretation and emergency management recommendations",
    operation_id="myxedema_coma_diagnostic_score"
)
async def calculate_myxedema_coma_diagnostic_score(request: MyxedemaComatDiagnosticScoreRequest):
    """
    Calculates Myxedema Coma Diagnostic Score
    
    This validated scoring system facilitates early recognition of myxedema coma,
    a life-threatening endocrine emergency with 25-50% mortality if untreated.
    
    Args:
        request: Parameters including thermoregulatory, CNS, cardiovascular,
                GI, metabolic dysfunction, and precipitating events
        
    Returns:
        MyxedemaComatDiagnosticScoreResponse: Result with emergency intervention guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("myxedema_coma_diagnostic_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Myxedema Coma Diagnostic Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MyxedemaComatDiagnosticScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Myxedema Coma Diagnostic Score",
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