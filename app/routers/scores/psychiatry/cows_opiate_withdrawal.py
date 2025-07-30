"""
Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal Router

Endpoint for calculating COWS score for opiate withdrawal assessment.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.psychiatry.cows_opiate_withdrawal import (
    CowsOpiateWithdrawalRequest,
    CowsOpiateWithdrawalResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post("/cows_opiate_withdrawal", response_model=CowsOpiateWithdrawalResponse)
async def calculate_cows_opiate_withdrawal(request: CowsOpiateWithdrawalRequest):
    """
    Calculates Clinical Opiate Withdrawal Scale (COWS) for Opiate Withdrawal
    
    Quantifies severity of opiate withdrawal symptoms using 11 clinical criteria 
    to guide treatment decisions and assess withdrawal progression. The COWS scale 
    is a standardized, clinician-administered assessment tool developed in 2003 
    and validated in 2009 for evaluating withdrawal severity.
    
    **Clinical Assessment Areas:**
    - **Physiological:** Pulse rate, sweating, pupil size, tremor
    - **Behavioral:** Restlessness, anxiety/irritability
    - **Physical:** Bone/joint aches, GI upset, runny nose/tearing, gooseflesh, yawning
    
    **Score Interpretation:**
    - **0-4 points:** None to minimal withdrawal - No treatment necessary
    - **5-12 points:** Mild withdrawal - Supportive care and comfort medications
    - **13-24 points:** Moderate withdrawal - Pharmacologic treatment indicated, consider buprenorphine
    - **25-36 points:** Moderately severe withdrawal - Medication-assisted treatment strongly recommended
    - **37-48 points:** Severe withdrawal - Immediate medical intervention required
    
    **Clinical Applications:**
    - **MAT Decision-Making:** Guides medication-assisted treatment initiation
    - **Buprenorphine Induction:** Determines appropriate timing to prevent precipitated withdrawal
    - **Treatment Monitoring:** Tracks withdrawal progression during detoxification
    - **Resource Allocation:** Determines appropriate level of care and monitoring intensity
    
    **Administration Guidelines:**
    - Should be performed by trained healthcare professionals
    - Assessment should be repeated regularly during withdrawal management
    - Clinical judgment should always accompany numerical scores
    - Consider patient safety and comfort throughout assessment
    
    **Evidence Base:**
    The COWS has been validated against naloxone challenges and shows good 
    reliability for assessing withdrawal severity. It is widely used in addiction 
    medicine and recommended by professional organizations including ASAM.
    
    **References:**
    - Wesson DR, Ling W. The Clinical Opiate Withdrawal Scale (COWS). J Psychoactive Drugs. 2003;35(2):253-259.
    - Tompkins DA, et al. Concurrent validation of COWS and single-item indices. Drug Alcohol Depend. 2009;105(1-2):154-159.
    
    Args:
        request: Parameters for 11 withdrawal symptoms assessment
        
    Returns:
        CowsOpiateWithdrawalResponse: Total score with clinical interpretation and treatment recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("cows_opiate_withdrawal", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating COWS Score for Opiate Withdrawal",
                    "details": {"parameters": parameters}
                }
            )
        
        return CowsOpiateWithdrawalResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for COWS Score for Opiate Withdrawal",
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