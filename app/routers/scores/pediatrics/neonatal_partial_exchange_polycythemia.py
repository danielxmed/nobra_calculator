"""
Neonatal Partial Exchange for Polycythemia Router

Endpoint for calculating Neonatal Partial Exchange for Polycythemia.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.pediatrics.neonatal_partial_exchange_polycythemia import (
    NeonatalPartialExchangePolycythemiaRequest,
    NeonatalPartialExchangePolycythemiaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/neonatal_partial_exchange_polycythemia",
    response_model=NeonatalPartialExchangePolycythemiaResponse,
    summary="Calculate Neonatal Partial Exchange for Polycythemia",
    description="Estimates total blood volume to remove and crystalloid volume to infuse in neonatal polycythemia",
    response_description="The calculated neonatal partial exchange polycythemia with interpretation",
    operation_id="neonatal_partial_exchange_polycythemia"
)
async def calculate_neonatal_partial_exchange_polycythemia(request: NeonatalPartialExchangePolycythemiaRequest):
    """
    Calculates Neonatal Partial Exchange for Polycythemia
    
    Estimates the total blood volume to remove and crystalloid volume to infuse
    in neonatal polycythemia. This calculator helps determine the appropriate 
    exchange volume for partial exchange transfusion in polycythemic neonates.
    
    Args:
        request: Parameters needed for calculation including weight, gestational age,
                initial hematocrit, and goal hematocrit
        
    Returns:
        NeonatalPartialExchangePolycythemiaResponse: Exchange volume with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("neonatal_partial_exchange_polycythemia", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Neonatal Partial Exchange for Polycythemia",
                    "details": {"parameters": parameters}
                }
            )
        
        return NeonatalPartialExchangePolycythemiaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Neonatal Partial Exchange for Polycythemia",
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