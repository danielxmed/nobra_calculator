"""
MAGGIC Risk Calculator Router

Endpoint for calculating MAGGIC Risk Score for Heart Failure mortality prediction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.maggic_risk_calculator import (
    MaggicRiskCalculatorRequest,
    MaggicRiskCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/maggic_risk_calculator",
    response_model=MaggicRiskCalculatorResponse,
    summary="Calculate MAGGIC Risk Score for Heart Failure",
    description="Calculates the MAGGIC (Meta-Analysis Global Group In Chronic Heart Failure) risk score "
                "for predicting 1- and 3-year mortality in heart failure patients. This validated prognostic "
                "tool was developed from a meta-analysis of 39,372 patients from 30 studies and uses 13 clinical "
                "variables including demographics, cardiac function, laboratory values, comorbidities, and "
                "medications. The score ranges from 0-50+ points and provides accurate risk stratification "
                "applicable to both HFrEF and HFpEF patients. It helps guide clinical decision-making including "
                "prognosis discussions, therapy intensity, specialist referrals, device therapy consideration, "
                "and advanced therapy evaluation. The calculator has been extensively validated with C-indices "
                "of 0.70-0.75 for mortality prediction across diverse international populations.",
    response_description="The calculated MAGGIC risk score with mortality estimates and comprehensive management recommendations",
    operation_id="maggic_risk_calculator"
)
async def calculate_maggic_risk_calculator(request: MaggicRiskCalculatorRequest):
    """
    Calculates MAGGIC Risk Score for Heart Failure mortality prediction and management guidance
    
    The MAGGIC risk calculator is a validated prognostic tool that provides accurate mortality
    estimates and helps guide clinical decision-making in heart failure patients.
    
    Key Features:
    - Estimates 1-year and 3-year mortality risk
    - Applicable to both HFrEF (EF ≤40%) and HFpEF (EF >40%) patients
    - Uses 13 readily available clinical variables
    - Extensively validated across diverse populations
    - C-index of 0.70-0.75 for mortality prediction
    
    Clinical Applications:
    - Prognosis discussions with patients and families
    - Risk stratification for clinical decision-making
    - Intensity of medical therapy and monitoring
    - Referral timing to advanced heart failure specialists
    - Device therapy evaluation (ICD/CRT) consideration
    - Advanced therapy assessment (transplant, mechanical support)
    - End-of-life care planning when appropriate
    - Clinical trial enrollment and research applications
    
    Risk Categories:
    - Low Risk (0-15 points): 1-year <5%, 3-year <15% mortality
      Standard heart failure management with evidence-based therapy
    - Intermediate Risk (16-25 points): 1-year 5-15%, 3-year 15-40% mortality
      Optimized medical therapy and closer monitoring recommended
    - High Risk (26-35 points): 1-year 15-40%, 3-year 40-70% mortality
      Advanced therapies and specialist referral may be indicated
    - Very High Risk (>35 points): 1-year >40%, 3-year >70% mortality
      Urgent advanced heart failure evaluation recommended
    
    Scoring Components:
    1. Age (varies by EF category): Higher age increases risk, especially in HFpEF
    2. Male gender: +1 point additional risk
    3. Ejection fraction: Lower EF associated with higher mortality
    4. NYHA class: Worse functional capacity increases risk significantly
    5. Creatinine: Kidney dysfunction strongly predicts mortality
    6. Systolic BP: Lower BP associated with worse prognosis
    7. BMI: Obesity paradox - higher BMI is protective in heart failure
    8. Diabetes: +3 points - significant mortality predictor
    9. COPD: +2 points - comorbidity burden
    10. Current smoking: +1 point - ongoing cardiovascular risk
    11. HF duration >18 months: +2 points - established disease
    12. No beta-blocker: +3 points - lack of evidence-based therapy
    13. No ACE-I/ARB: +1 point - suboptimal medical therapy
    
    Validation and Performance:
    - Developed from 39,372 patients from 30 international studies
    - Validated in Swedish Heart Failure Registry (51,043 patients)
    - Used in major clinical trials (PARADIGM-HF, EMPHASIS-HF)
    - Available online calculator at www.heartfailurerisk.org
    - Mortality estimates: 1-year ranges from 1.5% (score 0) to 84.2% (score 50+)
    - 3-year mortality: ranges from 3.9% (score 0) to 98.5% (score 50+)
    
    Limitations:
    - Does not include biomarkers (BNP/NT-proBNP)
    - Developed before newer therapies (SGLT2 inhibitors, ENTRESTO)
    - May underestimate risk in some contemporary populations
    - Should be used in conjunction with clinical judgment
    
    Args:
        request: MAGGIC calculation parameters including all 13 clinical variables
        
    Returns:
        MaggicRiskCalculatorResponse: Score with risk category and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("maggic_risk_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating MAGGIC Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return MaggicRiskCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for MAGGIC Risk Calculator",
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
                "message": "Internal error in MAGGIC Risk Calculator",
                "details": {"error": str(e)}
            }
        )