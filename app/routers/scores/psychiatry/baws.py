"""
Brief Alcohol Withdrawal Scale (BAWS) Router

Endpoint for calculating Brief Alcohol Withdrawal Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.baws import (
    BawsRequest,
    BawsResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/baws",
    response_model=BawsResponse,
    summary="Calculate Brief Alcohol Withdrawal Scale (BAWS)",
    description="Assesses alcohol withdrawal symptoms using 5 simple criteria: agitation, sweats, tremor, orientation, and hallucinations. A simplified alternative to CIWA-Ar that provides rapid assessment in clinical settings.",
    response_description="The calculated baws with interpretation",
    operation_id="calculate_baws"
)
async def calculate_baws(request: BawsRequest):
    """
    Calculates Brief Alcohol Withdrawal Scale (BAWS)
    
    Assesses alcohol withdrawal symptoms using 5 simple criteria: agitation, sweats, 
    tremor, orientation, and hallucinations. A simplified alternative to CIWA-Ar 
    that provides rapid assessment in clinical settings.
    
    Args:
        request: Parameters needed for BAWS calculation
        
    Returns:
        BawsResponse: Result with total score, component scores, and clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("baws", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Brief Alcohol Withdrawal Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return BawsResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Brief Alcohol Withdrawal Scale",
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