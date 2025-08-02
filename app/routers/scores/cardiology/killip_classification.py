"""
Killip Classification for Heart Failure Router

Endpoint for calculating Killip Classification for heart failure severity in ACS.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.killip_classification import (
    KillipClassificationRequest,
    KillipClassificationResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/killip_classification",
    response_model=KillipClassificationResponse,
    summary="Calculate Killip Classification for Heart Failure",
    description="Quantifies heart failure severity in acute coronary syndrome (STEMI or NSTEMI) "
                "and predicts 30-day mortality based on physical examination findings. This simple "
                "bedside tool stratifies patients into four risk categories using only clinical "
                "assessment: Class I (no heart failure), Class II (S3/rales), Class III (pulmonary "
                "edema), and Class IV (cardiogenic shock). Originally developed in 1967, it remains "
                "one of the most powerful predictors of mortality in ACS patients, even in the modern "
                "era of reperfusion therapy. Higher Killip classes are associated with increased "
                "mortality and guide treatment decisions including urgency of revascularization, "
                "need for mechanical circulatory support, and intensity of monitoring.",
    response_description="Killip classification with mortality risk estimates and clinical management recommendations",
    operation_id="killip_classification"
)
async def calculate_killip_classification(request: KillipClassificationRequest):
    """
    Calculates Killip Classification for Heart Failure
    
    The Killip Classification is a simple yet powerful bedside tool for risk 
    stratification in acute coronary syndrome patients based on physical 
    examination findings of heart failure.
    
    Clinical Assessment:
    - Class I: No clinical signs of heart failure (clear lungs, no S3 gallop)
    - Class II: S3 gallop and/or basal lung rales on auscultation
    - Class III: Frank acute pulmonary edema with rales throughout lung fields
    - Class IV: Cardiogenic shock (SBP <90 mmHg with signs of hypoperfusion)
    
    Risk Stratification:
    - Class I: Low risk (30-day mortality 2-3%)
    - Class II: Moderate risk (30-day mortality 5-12%)
    - Class III: High risk (30-day mortality 10-20%)
    - Class IV: Very high risk (30-day mortality 10-20%, in-hospital 81%)
    
    Clinical Applications:
    - Emergency department triage and risk assessment
    - Guide urgency of cardiac catheterization
    - Determine need for ICU vs. step-down unit
    - Consider mechanical circulatory support (Classes III-IV)
    - Predict response to medical therapy
    
    Historical Context:
    - Developed in 1967 by Killip and Kimball
    - Based on 250 patients with acute MI
    - Remains valid despite advances in therapy
    - Mortality rates have decreased but relative risk persists
    
    Limitations:
    - Based on clinical examination, which may vary between examiners
    - May change during hospitalization as patient condition evolves
    - Should be interpreted in context of overall clinical picture
    - Not validated for use in non-ACS heart failure
    
    Args:
        request: Killip Classification parameters
        
    Returns:
        KillipClassificationResponse: Classification result with risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("killip_classification", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Killip Classification",
                    "details": {"parameters": parameters}
                }
            )
        
        return KillipClassificationResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Killip Classification",
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