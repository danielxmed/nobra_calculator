"""
Drug Abuse Screening Test-10 (DAST-10) Router

Endpoint for calculating DAST-10 scores.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.dast_10 import (
    Dast10Request,
    Dast10Response
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/dast_10", response_model=Dast10Response)
async def calculate_dast_10(request: Dast10Request):
    """
    Calculates Drug Abuse Screening Test-10 (DAST-10) Score
    
    The DAST-10 is a brief, 10-item assessment tool designed to measure, evaluate, 
    and identify drug use problems, excluding alcohol or tobacco. It assesses drug 
    use in the past 12 months and provides a quantitative index of the degree of 
    consequences related to drug abuse.
    
    Scoring:
    - Questions 1, 2, 4-10: 1 point for each "yes" answer
    - Question 3: 1 point for "no" answer (reverse scored)
    - Total score range: 0-10 points
    
    Interpretation:
    - 0: No problems reported
    - 1-2: Low level problems (monitoring recommended)
    - 3-5: Moderate level problems (further investigation needed)
    - 6-8: Substantial problems (intensive assessment and treatment required)
    - 9-10: Severe problems (immediate specialized treatment warranted)
    
    Args:
        request: DAST-10 parameters (10 yes/no questions about drug use)
        
    Returns:
        Dast10Response: DAST-10 score with risk level interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("dast_10", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Drug Abuse Screening Test-10 (DAST-10)",
                    "details": {"parameters": parameters}
                }
            )
        
        return Dast10Response(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Drug Abuse Screening Test-10 (DAST-10)",
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