"""
Acute Interstitial Nephritis (AIN) Risk Calculator Router

Endpoint for calculating AIN Risk probability in patients being considered for kidney biopsy.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.ain_risk_calculator import (
    AinRiskCalculatorRequest,
    AinRiskCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/ain_risk_calculator",
    response_model=AinRiskCalculatorResponse,
    summary="Calculate Acute Interstitial Nephritis (AIN) Risk Calculator",
    description="Identifies the likelihood of acute interstitial nephritis in at-risk patients undergoing kidney biopsy evaluation. Uses commonly available clinical and laboratory parameters to predict AIN probability.",
    response_description="The calculated ain risk calculator with interpretation",
    operation_id="ain_risk_calculator"
)
async def calculate_ain_risk_calculator(request: AinRiskCalculatorRequest):
    """
    Calculates Acute Interstitial Nephritis (AIN) Risk probability
    
    The AIN Risk Calculator is a clinical decision tool developed by Dr. Dennis G. Moledina 
    at Yale School of Medicine to identify the likelihood of acute interstitial nephritis 
    in patients being considered for kidney biopsy. This evidence-based tool addresses a 
    critical clinical challenge: distinguishing AIN from other causes of acute kidney injury 
    using readily available clinical and laboratory parameters.
    
    Clinical Background:
    Acute interstitial nephritis is an important cause of acute kidney injury that requires 
    diagnosis-specific management including discontinuation of culprit medications and 
    administration of corticosteroids. However, distinguishing AIN from other AKI causes 
    is challenging, as traditional non-invasive tests have poor diagnostic accuracy.
    
    Model Development and Validation:
    The calculator was developed using data from patients with biopsy-confirmed diagnoses 
    from three major academic centers (Yale University, Indiana University, and Johns 
    Hopkins University). The model demonstrated excellent performance in external validation 
    with an AUC of 0.73-0.74 and a very high negative predictive value (>90%).
    
    Key Clinical Parameters:
    - Serum creatinine (mg/dL): Marker of AKI severity and kidney function
    - Blood urea nitrogen (mg/dL): Reflects kidney function and volume status  
    - Urine specific gravity: Lower values suggest concentrating defect typical of AIN
    - Urine dipstick protein: AIN typically shows minimal proteinuria (1+ or lower)
    - Local AIN prevalence: Institution-specific prevalence among kidney biopsies
    
    Clinical Applications:
    - Risk stratification for patients being considered for kidney biopsy
    - Guidance for empirical AIN-specific therapy decisions
    - Resource optimization for kidney biopsy utilization
    - Supporting clinical decision-making in ambiguous AKI presentations
    - High NPV (>90%) makes it excellent for ruling out AIN
    
    Risk Categories and Management:
    - Low Risk (<20%): AIN unlikely, focus on alternative AKI causes
    - Intermediate Risk (20-50%): Clinical correlation needed, consider additional testing
    - High Risk (≥50%): Strong consideration for immediate AIN-specific therapy
    
    Important Clinical Considerations:
    - Should only be used for patients in whom kidney biopsy is being considered
    - Developed in hospitalized patients with acute kidney injury
    - Does not replace clinical judgment but provides objective probability assessment
    - Early AIN recognition and treatment can prevent permanent kidney damage
    - Misdiagnosis may lead to inappropriate medication withdrawal or steroid therapy
    
    Limitations:
    - Validated primarily in academic medical centers
    - May not apply to all patient populations or clinical settings
    - Kidney biopsy remains the gold standard for definitive AIN diagnosis
    - Should be interpreted within the complete clinical context
    
    References:
    1. Moledina DG, Luciano RL, Kukova L, et al. Kidney biopsy-related complications 
       in hospitalized patients with acute kidney disease. Clin J Am Soc Nephrol. 2018;13(11):1633-1640.
    2. Moledina DG, Wilson FP, Kukova L, et al. Prevalence and outcomes of kidney biopsy 
       in hospitalized patients with acute kidney injury. J Am Soc Nephrol. 2017;28(4):1342-1349.
    3. Perazella MA, Moledina DG. Drug-induced acute interstitial nephritis. 
       Clin J Am Soc Nephrol. 2017;12(12):2046-2049.
    
    Args:
        request: Clinical and laboratory parameters including creatinine, BUN, urine specific 
                gravity, urine protein, and local AIN prevalence needed for probability calculation
        
    Returns:
        AinRiskCalculatorResponse: AIN probability with risk stratification and clinical 
                                  interpretation for management guidance
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("ain_risk_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating AIN Risk probability",
                    "details": {"parameters": parameters}
                }
            )
        
        return AinRiskCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for AIN Risk Calculator",
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