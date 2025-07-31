"""
Acetaminophen Overdose and NAC Dosing Router

Endpoint for calculating N-acetylcysteine dosing for acetaminophen overdose.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.acetaminophen_overdose_nac import (
    AcetaminophenOverdoseNacRequest,
    AcetaminophenOverdoseNacResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/acetaminophen_overdose_nac",
    response_model=AcetaminophenOverdoseNacResponse,
    summary="Calculate Acetaminophen Overdose and NAC Dosing",
    description="Calculates PO/IV N-acetylcysteine (NAC) dosing for acetaminophen overdose and determines toxicity based on the Rumack-Matthew nomogram",
    response_description="The calculated acetaminophen overdose nac with interpretation",
    operation_id="calculate_acetaminophen_overdose_nac"
)
async def calculate_acetaminophen_overdose_nac(request: AcetaminophenOverdoseNacRequest):
    """
    Calculates N-acetylcysteine (NAC) dosing for acetaminophen overdose
    
    This calculator provides complete NAC dosing regimens for both IV (21-hour protocol) 
    and oral (72-hour protocol) routes. It can also assess toxicity risk using the 
    Rumack-Matthew nomogram when time of ingestion and acetaminophen level are provided.
    
    Key features:
    - IV protocol: 21-hour regimen with loading, second, and third doses
    - Oral protocol: 72-hour regimen with loading and 17 maintenance doses
    - Optional toxicity assessment using Rumack-Matthew nomogram
    - Maximum dose safety limits applied automatically
    
    Args:
        request: Parameters including route, weight, and optional nomogram data
        
    Returns:
        AcetaminophenOverdoseNacResponse: Complete dosing regimen and toxicity assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("acetaminophen_overdose_nac", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating NAC dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return AcetaminophenOverdoseNacResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for NAC dosing calculation",
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