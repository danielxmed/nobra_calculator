"""
Index of Severity for Eosinophilic Esophagitis (I-SEE) Router

Endpoint for calculating the I-SEE Severity Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.i_see_score import (
    ISeeScoreRequest,
    ISeeScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/i_see_score",
    response_model=ISeeScoreResponse,
    summary="Calculate Index of Severity for Eosinophilic Esophagitis (I-SEE)",
    description="Calculates the Index of Severity for Eosinophilic Esophagitis (I-SEE) score, "
                "a comprehensive scoring system that evaluates symptoms, complications, inflammatory features, "
                "and fibrostenotic changes in eosinophilic esophagitis (EoE) patients. Developed by a "
                "multidisciplinary international group of EoE experts to standardize disease severity "
                "assessment beyond eosinophil counts alone. The score ranges from 0-45 points and classifies "
                "patients into four severity categories: Inactive (0), Mild (1-6), Moderate (7-14), and "
                "Severe (≥15). Higher scores correlate with lower BMI, longer symptom duration, smaller "
                "esophageal diameter, and increased need for dilation. This validated clinical tool helps "
                "guide EoE management decisions, monitor treatment response, and predict need for interventions.",
    response_description="The calculated I-SEE Severity Score with disease classification and clinical management recommendations",
    operation_id="i_see_score"
)
async def calculate_i_see_score(request: ISeeScoreRequest):
    """
    Calculates Index of Severity for Eosinophilic Esophagitis (I-SEE)
    
    A comprehensive scoring system for evaluating eosinophilic esophagitis severity 
    across multiple clinical domains including symptoms, complications, inflammation, 
    and fibrostenotic features.
    
    Args:
        request: Parameters needed for I-SEE calculation
        
    Returns:
        ISeeScoreResponse: Result with severity classification and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("i_see_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating I-SEE Severity Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return ISeeScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for I-SEE Severity Score",
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