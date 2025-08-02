"""
Intracerebral Hemorrhage (ICH) Score Router

Endpoint for calculating ICH Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.neurology.ich_score import (
    IchScoreRequest,
    IchScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ich_score",
    response_model=IchScoreResponse,
    summary="Calculate Intracerebral Hemorrhage (ICH) Score",
    description="Calculates the Intracerebral Hemorrhage (ICH) Score to predict 30-day mortality risk in patients with spontaneous intracerebral hemorrhage based on clinical and radiographic findings at presentation. This validated prognostic tool uses five independent risk factors identified through multivariate analysis: Glasgow Coma Scale score (3-4 scores 2 points, 5-12 scores 1 point, 13-15 scores 0 points), age ≥80 years (1 point), infratentorial hemorrhage location (1 point), ICH volume ≥30 cm³ calculated using ABC/2 method (1 point), and presence of intraventricular hemorrhage (1 point). The ICH Score ranges from 0-6 points with excellent discrimination for 30-day mortality prediction: Score 0 (0-5% mortality), Score 1 (~16% mortality), Score 2 (~33% mortality), Score 3 (~54% mortality), Score 4 (~93% mortality), and Score 5-6 (95-100% mortality). Developed in 2001 by Hemphill et al., this simple clinical grading scale standardizes clinical assessment, facilitates treatment protocol development, improves research study design, and enables evidence-based prognostic discussions with patients and families. The tool is particularly valuable for early risk stratification, clinical decision-making in acute intracerebral hemorrhage management, and goals of care discussions for high-risk patients.",
    response_description="The calculated ICH score with 30-day mortality prediction and clinical management recommendations",
    operation_id="ich_score"
)
async def calculate_ich_score(request: IchScoreRequest):
    """
    Calculates ICH Score for 30-day mortality prediction in intracerebral hemorrhage
    
    Predicts mortality risk using five independent clinical and radiographic factors 
    to guide clinical decision-making and prognostic discussions.
    
    Args:
        request: Clinical and radiographic parameters for ICH Score calculation (5 factors)
        
    Returns:
        IchScoreResponse: ICH score with mortality risk prediction and management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ich_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating ICH Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return IchScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for ICH Score",
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