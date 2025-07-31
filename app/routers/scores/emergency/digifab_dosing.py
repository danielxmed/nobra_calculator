"""
DigiFab (Digibind) Dosing for Digoxin Poisoning Router

Endpoint for calculating DigiFab dosing in digoxin toxicity.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.digifab_dosing import (
    DigifabDosingRequest,
    DigifabDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/digifab_dosing",
    response_model=DigifabDosingResponse,
    summary="Calculate DigiFab (Digibind) Dosing for Digoxin Poisoning",
    description="Doses DigiFab in patients with confirmed digoxin poisoning or overdose",
    response_description="The calculated digifab dosing with interpretation",
    operation_id="calculate_digifab_dosing"
)
async def calculate_digifab_dosing(request: DigifabDosingRequest):
    """
    Calculates DigiFab (Digibind) Dosing for Digoxin Poisoning
    
    Doses DigiFab in patients with confirmed digoxin poisoning or overdose.
    Two methods available:
    - Serum level method: Uses patient weight and serum digoxin level
    - Amount ingested method: Uses total amount of digoxin ingested
    
    Each vial contains approximately 40 mg of digoxin-specific antibody fragments.
    
    Args:
        request: Parameters needed for calculation
        
    Returns:
        DigifabDosingResponse: Number of vials with clinical interpretation
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("digifab_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating DigiFab dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return DigifabDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for DigiFab dosing",
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