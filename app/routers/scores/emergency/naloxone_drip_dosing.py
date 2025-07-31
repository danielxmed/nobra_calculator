"""
Naloxone Drip Dosing Router

Endpoint for calculating Naloxone Drip Dosing.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.naloxone_drip_dosing import (
    NaloxoneDripDosingRequest,
    NaloxoneDripDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/naloxone_drip_dosing",
    response_model=NaloxoneDripDosingResponse,
    summary="Calculate Naloxone Drip Dosing",
    description="Doses naloxone for acute opioid overdose. Calculates continuous IV infusion rate based on the initial effective bolus dose, with goal of maintaining same level of opioid reversal.",
    response_description="The calculated naloxone drip dosing with interpretation",
    operation_id="calculate_naloxone_drip_dosing"
)
async def calculate_naloxone_drip_dosing(request: NaloxoneDripDosingRequest):
    """
    Calculates Naloxone Drip Dosing
    
    Doses naloxone for acute opioid overdose by calculating the appropriate 
    continuous IV infusion rate based on the initial effective bolus dose.
    
    The formula uses two-thirds of the initial effective bolus dose per hour 
    to maintain the same level of opioid reversal, accounting for naloxone's 
    shorter half-life (30-100 minutes) compared to most opioids.
    
    Clinical Context:
    - Indicated for long-acting opioid overdoses (methadone, sustained-release)
    - Required when multiple bolus doses needed for initial reversal
    - Essential for synthetic opioid overdoses (fentanyl, carfentanil)
    - Prevents recurrent respiratory depression
    
    Args:
        request: Parameters needed for calculation (bolus dose in mg)
        
    Returns:
        NaloxoneDripDosingResponse: Infusion rate in mg/hr with clinical guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("naloxone_drip_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Naloxone Drip Dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return NaloxoneDripDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Naloxone Drip Dosing",
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