"""
Fomepizole Dosing Router

Endpoint for calculating fomepizole dosing for methanol and ethylene glycol poisoning.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.fomepizole_dosing import (
    FomepizoleDosingRequest,
    FomepizoleDosingResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/fomepizole_dosing",
    response_model=FomepizoleDosingResponse,
    summary="Calculate Fomepizole Dosing Calculator",
    description="Calculates fomepizole (4-methylpyrazole) dosing for treatment of methanol and ethylene glycol poisoning. Provides initial loading dose, maintenance doses, and special hemodialysis considerations.",
    response_description="The calculated fomepizole dosing with interpretation",
    operation_id="calculate_fomepizole_dosing"
)
async def calculate_fomepizole_dosing(request: FomepizoleDosingRequest):
    """
    Calculates Fomepizole Dosing for Methanol and Ethylene Glycol Poisoning
    
    Fomepizole (4-methylpyrazole) is the antidote of choice for methanol and ethylene glycol 
    poisoning. It competitively inhibits alcohol dehydrogenase, preventing the formation of 
    toxic metabolites (formic acid from methanol, oxalic acid from ethylene glycol).
    
    **Clinical Indications:**
    - Methanol poisoning (blood level >20 mg/dL or suspected significant ingestion)
    - Ethylene glycol poisoning (blood level >20 mg/dL or suspected significant ingestion)
    - Diethylene glycol poisoning
    
    **Dosing Protocols:**
    - Initial loading: 15 mg/kg IV
    - Maintenance (no dialysis): 10 mg/kg q12h × 4 doses, then 15 mg/kg q12h
    - During hemodialysis: 10 mg/kg q4h or continuous infusion 1-1.5 mg/kg/h
    - Post-hemodialysis: Dose depends on timing since last dose
    
    **Administration:**
    - IV over 30 minutes in ≥100 mL diluent (NS or D5W)
    - Treatment endpoint: ethylene glycol/methanol <20 mg/dL with normal pH and asymptomatic
    
    Args:
        request: Fomepizole dosing parameters (weight, clinical scenario, hours since last dose)
        
    Returns:
        FomepizoleDosingResponse: Calculated dose with clinical interpretation and administration guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("fomepizole_dosing", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Fomepizole Dosing",
                    "details": {"parameters": parameters}
                }
            )
        
        return FomepizoleDosingResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Fomepizole Dosing",
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
                "message": "Internal error in fomepizole dosing calculation",
                "details": {"error": str(e)}
            }
        )