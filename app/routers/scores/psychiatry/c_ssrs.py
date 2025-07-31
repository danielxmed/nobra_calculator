"""
Columbia Suicide Severity Rating Scale (C-SSRS) Screener Router

Endpoint for calculating C-SSRS suicide risk assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.c_ssrs import (
    CSSRSRequest,
    CSSRSResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/c_ssrs",
    response_model=CSSRSResponse,
    summary="Calculate Columbia Suicide Severity Rating Scale",
    description="Screens for suicidal ideation and behavior to assess suicide risk and guide clinical management. The C-SSRS evaluates both the severity of suicidal ideation and the presence of suicidal behaviors, helping stratify patients into low, moderate, or high risk categories.",
    response_description="The calculated c ssrs with interpretation",
    operation_id="c_ssrs"
)
async def calculate_c_ssrs(request: CSSRSRequest):
    """
    Calculates Columbia Suicide Severity Rating Scale (C-SSRS) Screener
    
    Screens for suicidal ideation and behavior to assess suicide risk and guide 
    clinical management. The C-SSRS evaluates both the severity of suicidal 
    ideation and the presence of suicidal behaviors, helping stratify patients 
    into low, moderate, or high risk categories.
    
    Args:
        request: Parameters including ideation level (0-5), behavior level (0-5),
                and timing of most recent behavior
        
    Returns:
        CSSRSResponse: Risk level (Low/Moderate/High) with clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("c_ssrs", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating C-SSRS score",
                    "details": {"parameters": parameters}
                }
            )
        
        return CSSRSResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for C-SSRS score",
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