"""
tPA (Alteplase) Dosing for Ischemic Stroke Calculator Router

Endpoint for calculating tPA alteplase dosing for acute ischemic stroke.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.tpa_alteplase_dosing_stroke import (
    TpaAlteplaseDosingStrokeRequest,
    TpaAlteplaseDosingStrokeResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/tpa_alteplase_dosing_stroke",
    response_model=TpaAlteplaseDosingStrokeResponse,
    summary="Calculate tPA (Alteplase) Dosing for Ischemic Stroke",
    description="Calculates precise alteplase dosing for acute ischemic stroke treatment using "
                "weight-based protocol (0.9 mg/kg, maximum 90 mg). Provides complete administration "
                "regimen including 10% IV bolus over 1 minute followed by 90% continuous infusion "
                "over 60 minutes. Essential for time-sensitive thrombolytic therapy within 3-4.5 hours "
                "of symptom onset. Includes safety monitoring guidelines and contraindication considerations.",
    response_description="Complete tPA dosing regimen with bolus and infusion calculations, administration timing, and clinical safety guidance",
    operation_id="tpa_alteplase_dosing_stroke"
)
async def calculate_tpa_alteplase_dosing_stroke(request: TpaAlteplaseDosingStrokeRequest):
    """
    Calculates tPA (Alteplase) dosing for acute ischemic stroke
    
    Determines the appropriate dose of tissue plasminogen activator (alteplase) 
    for acute ischemic stroke treatment based on patient weight. The calculation 
    follows evidence-based protocols established through landmark clinical trials 
    including NINDS rt-PA Stroke Study and ECASS III.
    
    The dosing algorithm applies the standard 0.9 mg/kg protocol with a safety 
    maximum of 90 mg, ensuring optimal therapeutic benefit while minimizing 
    bleeding risk. Critical for time-sensitive stroke treatment within the 
    therapeutic window.
    
    Args:
        request: Patient weight for dose calculation
        
    Returns:
        TpaAlteplaseDosingStrokeResponse: Complete dosing regimen with administration instructions
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("tpa_alteplase_dosing_stroke", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating tPA (Alteplase) dosing for ischemic stroke",
                    "details": {"parameters": parameters}
                }
            )
        
        return TpaAlteplaseDosingStrokeResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for tPA (Alteplase) dosing calculation",
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