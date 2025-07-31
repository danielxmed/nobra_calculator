"""
Glasgow Modified Alcohol Withdrawal Scale (GMAWS) Router

Endpoint for calculating Glasgow Modified Alcohol Withdrawal Scale.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.glasgow_modified_alcohol_withdrawal_scale import (
    GlasgowModifiedAlcoholWithdrawalScaleRequest,
    GlasgowModifiedAlcoholWithdrawalScaleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/glasgow_modified_alcohol_withdrawal_scale",
    response_model=GlasgowModifiedAlcoholWithdrawalScaleResponse,
    summary="Calculate Glasgow Modified Alcohol Withdrawal Scale (GMAWS)",
    description="Clinical scale used to assess and monitor the severity of alcohol withdrawal symptoms. Evaluates five clinical characteristics (tremor, sweating, hallucinations, orientation, agitation) with scores from 0-2 each, for a total score ranging from 0-10 points. Used to guide benzodiazepine treatment dosing and monitoring intervals.",
    response_description="The calculated glasgow modified alcohol withdrawal scale with interpretation",
    operation_id="glasgow_modified_alcohol_withdrawal_scale"
)
async def calculate_glasgow_modified_alcohol_withdrawal_scale(request: GlasgowModifiedAlcoholWithdrawalScaleRequest):
    """
    Calculates Glasgow Modified Alcohol Withdrawal Scale (GMAWS)
    
    The Glasgow Modified Alcohol Withdrawal Scale is a clinical assessment tool 
    designed to evaluate and monitor the severity of alcohol withdrawal symptoms 
    in hospitalized patients. It evaluates five clinical characteristics: tremor, 
    sweating, hallucinations, orientation, and agitation, each scored from 0-2 
    points. The scale is used to guide benzodiazepine treatment dosing and 
    monitoring intervals as part of the Glasgow Assessment and Management of 
    Alcohol (GAMA) protocol.
    
    Args:
        request: Parameters including tremor (0-2), sweating (0-2), hallucinations (0-2),
                orientation (0-2), and agitation (0-2)
        
    Returns:
        GlasgowModifiedAlcoholWithdrawalScaleResponse: Total GMAWS score with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("glasgow_modified_alcohol_withdrawal_scale", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Glasgow Modified Alcohol Withdrawal Scale",
                    "details": {"parameters": parameters}
                }
            )
        
        return GlasgowModifiedAlcoholWithdrawalScaleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Glasgow Modified Alcohol Withdrawal Scale",
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