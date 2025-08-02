"""
Injury Severity Score (ISS) Router

Endpoint for calculating Injury Severity Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.injury_severity_score import (
    InjurySeverityScoreRequest,
    InjurySeverityScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/injury_severity_score",
    response_model=InjurySeverityScoreResponse,
    summary="Calculate Injury Severity Score (ISS)",
    description="Calculates the Injury Severity Score (ISS) for standardizing traumatic injury severity based on the worst injuries from 6 body systems. "
                "Developed by Baker and colleagues in 1974, the ISS uses the Abbreviated Injury Scale (AIS) to score each body region from 0-6 "
                "(0=No injury, 1=Minor, 2=Moderate, 3=Serious, 4=Severe, 5=Critical, 6=Unsurvivable). The six body regions are: head/neck, face, "
                "chest, abdomen, extremity, and external. The ISS is calculated by taking the three highest AIS scores, squaring each, and summing "
                "them (ISS = A² + B² + C²). If any region has an AIS of 6 (unsurvivable), the ISS automatically becomes 75. The score ranges from "
                "0-75 and correlates linearly with mortality, morbidity, and hospitalization time. Scores ≥16 traditionally define major trauma. "
                "This tool is used primarily for research and trauma system evaluation rather than immediate clinical decision-making.",
    response_description="The calculated Injury Severity Score with trauma severity classification and clinical management recommendations",
    operation_id="injury_severity_score"
)
async def calculate_injury_severity_score(request: InjurySeverityScoreRequest):
    """
    Calculates Injury Severity Score for trauma severity assessment
    
    Standardizes traumatic injury severity using AIS scores from 6 body systems.
    Provides trauma classification to guide resource allocation and prognosis.
    
    Args:
        request: AIS scores for all 6 body regions (head/neck, face, chest, abdomen, extremity, external)
        
    Returns:
        InjurySeverityScoreResponse: ISS score with trauma severity category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("injury_severity_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Injury Severity Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return InjurySeverityScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Injury Severity Score",
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