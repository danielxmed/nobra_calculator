"""
Brief Addiction Monitor (BAM) Router

Endpoint for calculating Brief Addiction Monitor.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.bam import (
    BamRequest,
    BamResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/bam",
    response_model=BamResponse,
    summary="Calculate Brief Addiction Monitor (BAM)",
    description="Assesses substance use-related behaviors, risk factors, and protective factors over the past 30 days",
    response_description="The calculated bam with interpretation",
    operation_id="calculate_bam"
)
async def calculate_bam(request: BamRequest):
    """
    Calculates Brief Addiction Monitor (BAM)
    
    Assesses substance use-related behaviors, risk factors, and protective 
    factors over the past 30 days in individuals with substance use disorders.
    
    Args:
        request: Parameters needed for BAM calculation
        
    Returns:
        BamResponse: Result with total score, subscale scores, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("bam", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Brief Addiction Monitor",
                    "details": {"parameters": parameters}
                }
            )
        
        return BamResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Brief Addiction Monitor",
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