"""
Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score Router

Endpoint for calculating CRASH score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.oncology.crash_score import (
    CrashScoreRequest,
    CrashScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/crash_score",
    response_model=CrashScoreResponse,
    summary="Calculate Chemotherapy Risk Assessment Scale for High-Age...",
    description="Assesses the risk of severe chemotherapy toxicity in older cancer patients (≥70 years). Predicts both hematologic (grade 4) and nonhematologic (grade 3/4) toxicities based on patient characteristics and chemotherapy regimen.",
    response_description="The calculated crash score with interpretation",
    operation_id="crash_score"
)
async def calculate_crash_score(request: CrashScoreRequest):
    """
    Calculates Chemotherapy Risk Assessment Scale for High-Age Patients (CRASH) Score
    
    Predicts risk of severe chemotherapy toxicity in older cancer patients (≥70 years).
    Separately assesses hematologic (grade 4) and nonhematologic (grade 3/4) toxicities
    based on patient characteristics and chemotherapy regimen toxicity profile.
    
    Args:
        request: Parameters needed for calculation including patient characteristics,
                functional assessments, and chemotherapy risk scores
        
    Returns:
        CrashScoreResponse: Result with combined score, subscores, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("crash_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating CRASH score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CrashScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for CRASH score",
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