"""
Licurse Score for Renal Ultrasound Router

Endpoint for calculating the Licurse Score to predict likelihood of hydronephrosis 
on renal ultrasound requiring urological intervention in adult patients with acute 
kidney injury.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.licurse_score import (
    LicurseScoreRequest,
    LicurseScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/licurse_score",
    response_model=LicurseScoreResponse,
    summary="Calculate Licurse Score for Renal Ultrasound",
    description="Calculates the Licurse Score for Renal Ultrasound, a validated clinical decision tool "
                "that predicts the likelihood of hydronephrosis on renal ultrasonography in adult patients "
                "with acute kidney injury (AKI). This evidence-based risk stratification framework helps "
                "clinicians determine the appropriate use of renal ultrasound by categorizing patients into "
                "low risk (4.0% hydronephrosis rate), medium risk (6.8% rate), or high risk (20.9% rate) "
                "groups. The tool optimizes resource utilization by identifying patients who may safely "
                "defer imaging (low risk) versus those requiring prompt evaluation (high risk), reducing "
                "unnecessary healthcare costs while maintaining diagnostic accuracy for detecting urinary "
                "tract obstruction. Clinical applications include emergency department risk stratification, "
                "inpatient management coordination, and quality improvement initiatives for AKI evaluation "
                "protocols.",
    response_description="The calculated Licurse Score with risk stratification, hydronephrosis probability, intervention likelihood, and evidence-based recommendations for renal ultrasound utilization and clinical management",
    operation_id="licurse_score"
)
async def calculate_licurse_score(request: LicurseScoreRequest):
    """
    Calculates the Licurse Score for Renal Ultrasound risk stratification
    
    The Licurse Score is a validated clinical decision tool developed to predict the 
    likelihood of hydronephrosis on renal ultrasonography in adult patients with acute 
    kidney injury. This risk stratification framework optimizes resource utilization 
    by identifying patients at low, medium, or high risk for urinary tract obstruction, 
    guiding appropriate use of renal ultrasound while maintaining diagnostic accuracy.
    
    Args:
        request: Clinical parameters for Licurse Score calculation including history 
                of hydronephrosis, demographic factors, comorbidities, and AKI etiology
        
    Returns:
        LicurseScoreResponse: Risk stratification score with clinical recommendations 
                             for renal ultrasound utilization and patient management
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("licurse_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Licurse Score for Renal Ultrasound",
                    "details": {"parameters": parameters}
                }
            )
        
        return LicurseScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Licurse Score calculation",
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
                "message": "Internal error in Licurse Score calculation",
                "details": {"error": str(e)}
            }
        )