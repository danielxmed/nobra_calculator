"""
GRACE ACS Risk and Mortality Calculator Router

Endpoint for calculating GRACE ACS Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.grace_acs_risk import (
    GraceAcsRiskRequest,
    GraceAcsRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/grace_acs_risk",
    response_model=GraceAcsRiskResponse,
    summary="Calculate GRACE ACS Risk and Mortality Calculator",
    description="Estimates admission to 6-month mortality risk for patients with acute coronary syndrome. Uses 8 clinical variables to provide risk stratification and guide treatment decisions in both ST-elevation and non-ST-elevation ACS.",
    response_description="The calculated grace acs risk with interpretation",
    operation_id="grace_acs_risk"
)
async def calculate_grace_acs_risk(request: GraceAcsRiskRequest):
    """
    Calculates GRACE ACS Risk and Mortality Score
    
    The GRACE (Global Registry of Acute Coronary Events) ACS Risk Score is a validated 
    tool for estimating admission to 6-month mortality risk in patients with acute coronary 
    syndrome. It is one of the most widely used and well-validated risk stratification 
    tools in cardiovascular medicine, recommended by NICE guidelines for ACS management.
    
    **Clinical Applications**:
    - Risk stratification for ACS patients to identify high-risk individuals
    - Guide decisions about invasive vs. conservative treatment strategies
    - Determine appropriate level of care and monitoring intensity
    - Provide evidence-based prognostic information to patients and families
    - Support quality improvement initiatives in ACS care protocols
    
    **Scoring System (8 Variables)**:
    The GRACE score uses 8 clinical variables measured at hospital admission:
    
    **Continuous Variables** (with algorithmic point calculations):
    - Age: Higher age increases risk (~2.5 points per year over 40)
    - Heart Rate: Tachycardia increases risk (0-46 points based on ranges)
    - Systolic Blood Pressure: Hypotension increases risk (0-58 points, inverse relationship)
    - Serum Creatinine: Renal dysfunction increases risk (1-28 points based on ranges)
    
    **Categorical/Binary Variables**:
    - Killip Class: Heart failure signs (0-59 points based on severity)
    - Cardiac Arrest at Admission: 39 points if present
    - ST Segment Deviation on ECG: 28 points if present
    - Elevated Cardiac Biomarkers: 14 points if present
    
    **Risk Categories and Mortality Estimates**:
    - Very Low Risk (0-87 points): 0-2% mortality - suitable for early discharge
    - Low Risk (88-128 points): 3-10% mortality - standard care
    - Intermediate Risk (129-149 points): 10-20% mortality - careful monitoring
    - High Risk (150-173 points): 20-30% mortality - intensive monitoring/interventions
    - Very High Risk (174-284 points): 40-90% mortality - aggressive interventions
    - Extremely High Risk (≥285 points): ≥99% mortality - maximum intensive care
    
    **Clinical Decision Framework**:
    - Lower risk patients: Conservative management, early discharge consideration
    - Intermediate risk patients: Selective invasive strategy, careful monitoring
    - Higher risk patients: Intensive monitoring, aggressive interventions, early invasive strategy
    
    **Important Clinical Considerations**:
    - Validated in over 43,000 patients from 94 hospitals worldwide
    - Applicable to both STEMI and NSTEMI patients
    - Should be used in conjunction with clinical judgment and patient preferences
    - Provides both in-hospital and 6-month mortality predictions
    - Higher scores indicate increased need for intensive care and invasive interventions
    
    Args:
        request: GRACE score parameters including age, vital signs, lab values, and clinical findings
        
    Returns:
        GraceAcsRiskResponse: GRACE score with mortality risk category and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("grace_acs_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GRACE ACS Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GraceAcsRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GRACE ACS Risk Score",
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