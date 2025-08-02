"""
Pulmonary Embolism Severity Index (PESI) Router

Endpoint for calculating PESI.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.pesi import (
    PesiRequest,
    PesiResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/pesi",
    response_model=PesiResponse,
    summary="Calculate Pulmonary Embolism Severity Index (PESI)",
    description="Predicts 30-day outcome of patients with pulmonary embolism using 11 clinical "
                "criteria to guide critical disposition and treatment decisions. This extensively "
                "validated prognostic tool, developed from over 15,000 patients, stratifies "
                "mortality risk into five classes: Class I (≤65 points, 0.0-1.6% mortality), "
                "Class II (66-85 points, 1.7-3.5%), Class III (86-105 points, 3.2-7.1%), "
                "Class IV (106-125 points, 4.0-11.4%), and Class V (≥126 points, 10.0-24.5%). "
                "The score incorporates age (absolute value), male sex (+10), cancer history "
                "(+30), heart failure (+10), chronic lung disease (+10), heart rate ≥110 (+20), "
                "systolic BP <100 (+30), respiratory rate ≥30 (+20), temperature <36°C (+20), "
                "altered mental status (+60), and oxygen saturation <90% (+20). Classes I and II "
                "may be suitable for outpatient management with appropriate anticoagulation and "
                "close follow-up, while higher classes require inpatient care with increasing "
                "intensity of monitoring and advanced therapies. Strong evidence supports PESI "
                "use for safely identifying low-risk patients appropriate for outpatient treatment, "
                "reducing healthcare costs while maintaining excellent outcomes. The tool has "
                "demonstrated consistent performance across diverse populations with area under "
                "ROC curve of 0.78 and is recommended in multiple clinical guidelines for PE "
                "risk stratification and disposition planning.",
    response_description="The calculated PESI score with risk class and comprehensive management recommendations",
    operation_id="pesi"
)
async def calculate_pesi(request: PesiRequest):
    """
    Calculates Pulmonary Embolism Severity Index (PESI)
    
    This prognostic tool stratifies 30-day mortality risk in acute PE patients
    to guide disposition decisions and treatment intensity.
    
    Args:
        request: Clinical parameters including demographics, comorbidities,
                and physiological findings for PESI calculation
        
    Returns:
        PesiResponse: Result with risk class and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("pesi", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating PESI",
                    "details": {"parameters": parameters}
                }
            )
        
        return PesiResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for PESI",
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