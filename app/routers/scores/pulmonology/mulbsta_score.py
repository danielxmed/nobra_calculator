"""
MuLBSTA Score for Viral Pneumonia Mortality Router

Endpoint for calculating MuLBSTA Score for predicting 90-day mortality risk
in patients with viral pneumonia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pulmonology.mulbsta_score import (
    MulbstaScoreRequest,
    MulbstaScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/mulbsta_score",
    response_model=MulbstaScoreResponse,
    summary="Calculate MuLBSTA Score for Viral Pneumonia Mortality",
    description="Calculates the MuLBSTA Score to predict 90-day mortality risk in patients with viral pneumonia. "
                "This validated clinical prediction tool uses six clinical and laboratory parameters "
                "(Multilobar infiltrates, Lymphopenia, Bacterial coinfection, Smoking history, Hypertension, Age ≥60) "
                "to stratify patients into low (0-5 points), moderate (6-11 points), or high risk (12+ points) categories. "
                "The score has been validated for influenza, COVID-19, and other viral pneumonias, helping clinicians "
                "guide treatment intensity, resource allocation, and ICU admission decisions.",
    response_description="The calculated MuLBSTA score with mortality risk stratification and clinical management recommendations",
    operation_id="mulbsta_score"
)
async def calculate_mulbsta_score(request: MulbstaScoreRequest):
    """
    Calculates MuLBSTA Score for Viral Pneumonia Mortality
    
    The MuLBSTA Score is a clinical prediction tool that uses six clinical and laboratory
    parameters to predict 90-day mortality risk in patients with viral pneumonia. It has
    been validated for influenza, COVID-19, and other viral pneumonias.
    
    Args:
        request: Parameters including multilobar infiltrates, lymphopenia, bacterial 
                coinfection, smoking history, hypertension, and age ≥60 years
        
    Returns:
        MulbstaScoreResponse: Score with mortality risk assessment and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("mulbsta_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MuLBSTA Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MulbstaScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MuLBSTA Score",
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