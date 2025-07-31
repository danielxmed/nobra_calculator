"""
Acute Gout Diagnosis Rule Router

Endpoint for calculating Acute Gout Diagnosis Rule for acute gout risk stratification.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.rheumatology.acute_gout_diagnosis_rule import (
    AcuteGoutDiagnosisRuleRequest,
    AcuteGoutDiagnosisRuleResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/acute_gout_diagnosis_rule",
    response_model=AcuteGoutDiagnosisRuleResponse,
    summary="Calculate Acute Gout Diagnosis Rule",
    description="Risk stratifies for gout vs non-gout arthritis and helps determine which patients benefit most from joint aspiration. A diagnostic rule for acute gouty arthritis in primary care without joint fluid analysis.",
    response_description="The calculated acute gout diagnosis rule with interpretation",
    operation_id="calculate_acute_gout_diagnosis_rule"
)
async def calculate_acute_gout_diagnosis_rule(request: AcuteGoutDiagnosisRuleRequest):
    """
    Calculates Acute Gout Diagnosis Rule
    
    The Acute Gout Diagnosis Rule is a clinical decision tool developed for primary 
    care settings to help diagnose acute gout without joint fluid analysis. This 
    evidence-based rule uses seven readily available clinical parameters to risk 
    stratify patients for gout vs non-gout arthritis and helps determine which 
    patients benefit most from joint aspiration.
    
    The rule was derived from a study of 328 patients with monoarthritis in primary 
    care and validated in secondary care (rheumatology clinic) settings. It provides 
    excellent diagnostic utility with scores ≤4 having a negative predictive value 
    of 95% and scores ≥8 having a positive predictive value of 87%.
    
    Clinical Applications:
    - Primary care diagnosis of acute gout when joint aspiration is not available
    - Risk stratification for patients with monoarthritis
    - Decision support for empirical anti-inflammatory treatment
    - Guidance for specialty referral and further diagnostic testing
    - Resource allocation in clinical settings with limited access to joint aspiration
    
    Key Clinical Parameters:
    - Male sex (classic demographic risk factor)
    - Previous arthritis attacks (recurrent nature of gout)
    - Acute onset within 1 day (typical gout presentation)
    - Joint redness (inflammatory response)
    - First MTP joint involvement (podagra - pathognomonic for gout)
    - Hypertension/cardiovascular disease (metabolic syndrome association)
    - Elevated serum uric acid >5.88 mg/dL (biochemical marker)
    
    Score Interpretation and Management:
    - Low Risk (≤4 points, 2.2% prevalence): Gout unlikely, consider alternative diagnoses
    - Intermediate Risk (4.5-7.5 points, 31.2% prevalence): Joint aspiration recommended
    - High Risk (≥8 points, 80.4-82.5% prevalence): Gout highly likely, consider empirical treatment
    
    Important Clinical Considerations:
    - Designed for monoarticular presentations only
    - Should not be used in polyarticular disease
    - Joint aspiration remains gold standard for definitive diagnosis
    - Useful when synovial fluid analysis is not readily available or feasible
    - Can guide initial management decisions in acute settings
    - Serum uric acid should ideally be measured when not on urate-lowering therapy
    
    Limitations:
    - Not validated for polyarticular gout or chronic presentations
    - Should not replace clinical judgment in complex cases
    - May not apply to all patient populations (validation primarily in Caucasian populations)
    - Septic arthritis should always be excluded in appropriate clinical contexts
    
    Args:
        request: Clinical parameters including demographics, symptoms, physical findings, 
                and laboratory values needed for gout risk assessment
        
    Returns:
        AcuteGoutDiagnosisRuleResponse: Risk score with clinical interpretation and 
                                       recommended management approach
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("acute_gout_diagnosis_rule", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Acute Gout Diagnosis Rule",
                    "details": {"parameters": parameters}
                }
            )
        
        return AcuteGoutDiagnosisRuleResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Acute Gout Diagnosis Rule",
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