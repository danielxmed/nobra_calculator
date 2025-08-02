"""
Kinetic Estimated Glomerular Filtration Rate (keGFR) Router

Endpoint for calculating keGFR in patients with acutely changing creatinine.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.kinetic_egfr import (
    KineticEgfrRequest,
    KineticEgfrResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kinetic_egfr",
    response_model=KineticEgfrResponse,
    summary="Calculate Kinetic Estimated Glomerular Filtration Rate (keGFR)",
    description="Calculates kinetic eGFR for patients with acutely changing creatinine levels, "
                "enabling earlier detection of acute kidney injury compared to traditional eGFR "
                "equations. This tool is particularly valuable during non-steady-state conditions "
                "where creatinine is rapidly changing, such as in ICU patients, post-operative "
                "settings, or during acute illness. The keGFR accounts for the rate of creatinine "
                "change over time and provides more accurate GFR estimation than static equations. "
                "A keGFR <30 mL/min/1.73 m² has 90% specificity for acute kidney injury and can "
                "detect AKI 8-24 hours earlier than traditional creatinine-based criteria. The "
                "calculation combines baseline eGFR (using MDRD equation) with kinetic factors "
                "including volume of distribution and creatinine production rate.",
    response_description="Kinetic eGFR with baseline comparison, AKI risk assessment, and clinical management recommendations",
    operation_id="kinetic_egfr"
)
async def calculate_kinetic_egfr(request: KineticEgfrRequest):
    """
    Calculates Kinetic Estimated Glomerular Filtration Rate (keGFR)
    
    The keGFR is a dynamic GFR assessment tool designed for non-steady-state 
    conditions when creatinine levels are changing rapidly. Unlike traditional 
    eGFR equations that assume steady-state conditions, keGFR accounts for the 
    kinetics of creatinine change over time.
    
    Clinical Indications:
    - Acute kidney injury detection and monitoring
    - ICU patients with changing kidney function
    - Post-operative kidney function assessment
    - Patients receiving nephrotoxic medications
    - Critically ill patients with hemodynamic instability
    
    Calculation Method:
    - Uses MDRD equation for baseline eGFR calculation
    - Incorporates creatinine change rate over time
    - Accounts for volume of distribution and creatinine production
    - Adjusts for demographic factors (age, sex, race)
    
    Performance Characteristics:
    - Detects AKI 8-24 hours earlier than traditional criteria
    - 90% specificity for AKI when keGFR <30 mL/min/1.73 m²
    - 71% sensitivity for AKI detection
    - Better correlation with measured CrCl during AKI
    
    Clinical Thresholds:
    - keGFR ≥60: Low AKI risk, routine monitoring
    - keGFR 30-59: Intermediate risk, increased monitoring
    - keGFR 15-29: High risk, nephrology consultation
    - keGFR <15: Very high risk, urgent intervention
    
    Advantages:
    - No urine collection required (unlike CrCl)
    - Real-time assessment during acute changes
    - Objective risk stratification
    - Guides intervention timing and intensity
    
    Limitations:
    - Requires two creatinine measurements
    - Assumes normal creatinine production rate
    - Less accurate with changing muscle mass
    - Not validated in pediatric patients
    
    Clinical Applications:
    - Early AKI detection in high-risk patients
    - Monitoring response to interventions
    - Risk stratification for RRT need
    - Guiding nephrology referral timing
    - ICU patient triage and monitoring
    
    Args:
        request: keGFR calculation parameters
        
    Returns:
        KineticEgfrResponse: keGFR result with AKI risk assessment
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kinetic_egfr", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kinetic eGFR",
                    "details": {"parameters": parameters}
                }
            )
        
        return KineticEgfrResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kinetic eGFR calculation",
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