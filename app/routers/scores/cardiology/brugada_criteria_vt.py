"""
Brugada Criteria for Ventricular Tachycardia Router

Endpoint for calculating Brugada Criteria for VT diagnosis.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.brugada_criteria_vt import (
    BrugadaCriteriaVtRequest,
    BrugadaCriteriaVtResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/brugada_criteria_vt",
    response_model=BrugadaCriteriaVtResponse,
    summary="Calculate Brugada Criteria for Ventricular Tach...",
    description="Distinguishes ventricular tachycardia from supraventricular tachycardia with aberrancy using ECG morphology criteria",
    response_description="The calculated brugada criteria vt with interpretation",
    operation_id="brugada_criteria_vt"
)
async def calculate_brugada_criteria_vt(request: BrugadaCriteriaVtRequest):
    """
    Calculates Brugada Criteria for Ventricular Tachycardia
    
    Distinguishes ventricular tachycardia from supraventricular tachycardia with 
    aberrancy using a four-step sequential ECG morphology algorithm. This is a 
    critical diagnostic tool as treatments for SVT (adenosine, calcium channel 
    blockers) can be detrimental to patients with VT.
    
    The algorithm follows four sequential steps:
    1. Absence of RS complex in all precordial leads (V1-V6)
    2. R to S interval >100 ms in any precordial lead (Brugada's sign)
    3. Atrioventricular dissociation
    4. Morphology criteria for VT in leads V1-V2 and V6
    
    Any positive step indicates VT diagnosis. All steps must be negative to suggest 
    SVT with aberrancy. When in doubt, treat as VT.
    
    Args:
        request: Parameters needed for Brugada Criteria assessment
        
    Returns:
        BrugadaCriteriaVtResponse: Result with diagnosis, step-by-step analysis, and clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("brugada_criteria_vt", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Brugada Criteria for VT",
                    "details": {"parameters": parameters}
                }
            )
        
        return BrugadaCriteriaVtResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Brugada Criteria for VT",
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