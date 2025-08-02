"""
Local Anesthetic Dosing Calculator Router

Endpoint for calculating maximum safe doses of local anesthetics to prevent 
Local Anesthetic Systemic Toxicity (LAST).
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.local_anesthetic_dosing_calculator import (
    LocalAnestheticDosingCalculatorRequest,
    LocalAnestheticDosingCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/local_anesthetic_dosing_calculator",
    response_model=LocalAnestheticDosingCalculatorResponse,
    summary="Calculate Local Anesthetic Maximum Safe Dosing",
    description="Calculates maximum safe doses of local anesthetics to prevent Local Anesthetic Systemic "
                "Toxicity (LAST). This essential clinical safety tool determines appropriate dosing limits for "
                "bupivacaine (2 mg/kg), lidocaine (4.5 mg/kg), mepivacaine (4.4 mg/kg), and ropivacaine (3 mg/kg) "
                "based on patient weight and drug concentration. The calculator provides maximum doses in both mg "
                "and mL to guide safe administration during regional anesthesia, nerve blocks, and local infiltration "
                "procedures. LAST is a rare but potentially fatal complication occurring in 0.03-0.3% of procedures, "
                "manifesting as CNS symptoms (seizures, altered mental status) followed by cardiovascular toxicity "
                "(arrhythmias, cardiac arrest). Clinical applications include pre-procedure dose planning, procedural "
                "safety verification, emergency dose calculations, and staff education on toxicity prevention. The "
                "tool emphasizes critical safety measures including aspiration before injection, slow administration "
                "with frequent aspiration, continuous monitoring for 30 minutes post-injection, and immediate "
                "availability of lipid emulsion therapy for LAST treatment.",
    response_description="Maximum safe doses in mg and mL with comprehensive clinical interpretation, drug properties, safety considerations, and emergency management guidance",
    operation_id="local_anesthetic_dosing_calculator"
)
async def calculate_local_anesthetic_dosing_calculator(request: LocalAnestheticDosingCalculatorRequest):
    """
    Calculates maximum safe doses of local anesthetics to prevent LAST
    
    The Local Anesthetic Dosing Calculator is an essential clinical safety tool 
    that determines maximum safe doses of commonly used local anesthetic agents 
    to prevent Local Anesthetic Systemic Toxicity (LAST). This evidence-based 
    calculator helps clinicians avoid potentially life-threatening complications 
    during regional anesthesia and local infiltration procedures.
    
    Args:
        request: Parameters including drug type, patient weight, and concentration 
                for maximum safe dose calculation
        
    Returns:
        LocalAnestheticDosingCalculatorResponse: Maximum doses with comprehensive 
                                               safety guidance and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("local_anesthetic_dosing_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Local Anesthetic Dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return LocalAnestheticDosingCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Local Anesthetic Dosing calculation",
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
                "message": "Internal error in Local Anesthetic Dosing calculation",
                "details": {"error": str(e)}
            }
        )