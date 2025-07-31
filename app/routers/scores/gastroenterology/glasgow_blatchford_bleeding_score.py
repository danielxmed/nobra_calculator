"""
Glasgow-Blatchford Bleeding Score (GBS) Router

Endpoint for calculating Glasgow-Blatchford Bleeding Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.gastroenterology.glasgow_blatchford_bleeding_score import (
    GlasgowBlatchfordBleedingScoreRequest,
    GlasgowBlatchfordBleedingScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_blatchford_bleeding_score",
    response_model=GlasgowBlatchfordBleedingScoreResponse,
    summary="Calculate Glasgow-Blatchford Bleeding Score (GBS)",
    description="Clinical scoring system to assess the risk of upper gastrointestinal bleeding and identify patients who may need medical intervention such as blood transfusion or endoscopic intervention. Used to stratify patients for safe outpatient management versus hospital admission.",
    response_description="The calculated glasgow blatchford bleeding score with interpretation",
    operation_id="calculate_glasgow_blatchford_bleeding_score"
)
async def calculate_glasgow_blatchford_bleeding_score(request: GlasgowBlatchfordBleedingScoreRequest):
    """
    Calculates Glasgow-Blatchford Bleeding Score (GBS)
    
    The Glasgow-Blatchford Bleeding Score is a clinical scoring system used to 
    assess the risk of upper gastrointestinal bleeding and identify patients who 
    may need medical intervention such as blood transfusion or endoscopic intervention. 
    It helps stratify patients for safe outpatient management versus hospital admission 
    and is particularly valuable for identifying low-risk patients who can be managed 
    as outpatients, reducing healthcare costs and hospital burden.
    
    Args:
        request: Parameters including BUN, hemoglobin, gender, vital signs, and clinical factors
        
    Returns:
        GlasgowBlatchfordBleedingScoreResponse: Total GBS score with risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_blatchford_bleeding_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow-Blatchford Bleeding Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowBlatchfordBleedingScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow-Blatchford Bleeding Score",
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