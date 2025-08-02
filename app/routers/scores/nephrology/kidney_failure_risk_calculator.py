"""
Kidney Failure Risk Calculator (4-Variable) Router

Endpoint for calculating Kidney Failure Risk using the 4-variable KFRE.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.nephrology.kidney_failure_risk_calculator import (
    KidneyFailureRiskCalculatorRequest,
    KidneyFailureRiskCalculatorResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/kidney_failure_risk_calculator",
    response_model=KidneyFailureRiskCalculatorResponse,
    summary="Calculate Kidney Failure Risk (4-Variable KFRE)",
    description="Calculates the risk of kidney failure requiring dialysis or transplantation at 2 and 5 years "
                "for patients with CKD stages 3-5 using the 4-variable Kidney Failure Risk Equation (KFRE). "
                "This validated tool uses age, sex, eGFR, and urine albumin-to-creatinine ratio to predict "
                "progression to end-stage renal disease. The KFRE has been validated in over 700,000 patients "
                "across 30+ countries and is the most accurate tool for kidney failure prediction. Results help "
                "guide nephrology referral timing (often triggered by 2-year risk >5% or 5-year risk >15%), "
                "dialysis access planning, transplant evaluation, and patient counseling. Different calibration "
                "factors are applied for North American vs. non-North American populations.",
    response_description="2-year and 5-year kidney failure risk with clinical interpretation and management recommendations",
    operation_id="kidney_failure_risk_calculator"
)
async def calculate_kidney_failure_risk_calculator(request: KidneyFailureRiskCalculatorRequest):
    """
    Calculates Kidney Failure Risk using 4-Variable KFRE
    
    The Kidney Failure Risk Equation is the gold standard for predicting 
    progression to kidney failure in CKD patients. It outperforms clinical 
    judgment and other risk equations.
    
    Input Parameters:
    - Age: 18-110 years
    - Sex: Male/female (males have slightly higher risk)
    - eGFR: 1-60 mL/min/1.73 m² (CKD stages 3-5)
    - Urine ACR: 0.1-25,000 mg/g (higher = worse prognosis)
    - Region: For appropriate calibration
    
    Risk Categories and Clinical Actions:
    - Low (<5% at 5 years): Primary care management often appropriate
    - Intermediate (5-15%): Consider nephrology referral
    - High (15-30%): Nephrology referral recommended, begin RRT planning
    - Very High (>30%): Urgent referral, immediate RRT preparation
    
    Clinical Applications:
    - Nephrology referral triage
    - Dialysis access timing (typically when 2-year risk >20%)
    - Transplant evaluation planning
    - Patient education and counseling
    - Resource allocation
    
    Validation:
    - C-statistic: 0.83-0.92 for 2-year prediction
    - Validated in >700,000 patients globally
    - Superior to eGFR alone or clinical judgment
    
    Args:
        request: Kidney Failure Risk Calculator parameters
        
    Returns:
        KidneyFailureRiskCalculatorResponse: Risk assessment with recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("kidney_failure_risk_calculator", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Kidney Failure Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return KidneyFailureRiskCalculatorResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Kidney Failure Risk Calculator",
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