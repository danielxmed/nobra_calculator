"""
Emergency Heart Failure Mortality Risk Grade (EHMRG) Router

Endpoint for calculating EHMRG score for 7-day mortality risk prediction in emergency department patients with acute heart failure.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.emergency_heart_failure_mortality_risk_grade_ehmrg import (
    EmergencyHeartFailureMortalityRiskGradeEhmrgRequest,
    EmergencyHeartFailureMortalityRiskGradeEhmrgResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/emergency_heart_failure_mortality_risk_grade_ehmrg",
    response_model=EmergencyHeartFailureMortalityRiskGradeEhmrgResponse,
    summary="Calculate Emergency Heart Failure Mortality Risk Grade",
    description="Estimates 7-day mortality risk in emergency department patients with acute heart failure using clinical variables routinely collected on arrival.",
    response_description="The calculated emergency heart failure mortality risk grade ehmrg with interpretation",
    operation_id="calculate_emergency_heart_failure_mortality_risk_grade_ehmrg"
)
async def calculate_emergency_heart_failure_mortality_risk_grade_ehmrg(request: EmergencyHeartFailureMortalityRiskGradeEhmrgRequest):
    """
    Calculates Emergency Heart Failure Mortality Risk Grade (EHMRG)
    
    The Emergency Heart Failure Mortality Risk Grade (EHMRG) is a validated clinical 
    decision tool that estimates 7-day mortality risk in emergency department patients 
    presenting with acute heart failure. This evidence-based risk stratification tool 
    uses ten clinical variables routinely collected on arrival to provide personalized 
    risk assessment and guide clinical decision-making.
    
    Historical Development and Validation:
    
    Derivation and Internal Validation:
    The EHMRG was originally derived and internally validated using data from a large 
    cohort of emergency department patients with acute heart failure. The development 
    process involved comprehensive analysis of clinical variables available at the 
    time of ED presentation to identify independent predictors of short-term mortality.
    
    The scoring algorithm was developed using multivariable logistic regression, with 
    coefficients transformed into integer points for clinical ease of use. The model 
    underwent rigorous internal validation with bootstrap resampling techniques to 
    assess discrimination and calibration performance.
    
    External Validation Studies:
    Multiple external validation studies have confirmed the EHMRG's performance across 
    diverse healthcare systems and populations:
    
    - Canadian validation cohorts demonstrated consistent discrimination with C-statistics 
      typically exceeding 0.70 for 7-day mortality prediction
    - Spanish cohort validation confirmed applicability across different healthcare 
      systems and populations
    - International studies have validated the tool's performance in various clinical 
      settings and demographics
    
    Clinical Variables and Scoring Logic:
    
    The EHMRG incorporates ten clinical variables with specific scoring weights:
    
    Demographic and Presentation Factors:
    - Age: Continuous variable with linear relationship (2 points per year)
    - EMS Transport: Binary variable reflecting presentation acuity (60 points if yes)
    
    Vital Signs with Physiologic Boundaries:
    - Systolic Blood Pressure: Inverse relationship capped at 160 mmHg (protective factor)
    - Heart Rate: Constrained to 80-120 bpm range reflecting optimal therapeutic range
    - Oxygen Saturation: Inverse relationship capped at 92% (protective factor with multiplier)
    
    Laboratory Markers:
    - Creatinine: Continuous variable reflecting renal function (20-point multiplier)
    - Potassium: Categorical scoring reflecting electrolyte disturbances
    - Troponin: Binary variable indicating myocardial injury (60 points if elevated)
    
    Clinical Comorbidities:
    - Active Cancer: Binary variable reflecting overall prognosis (45 points if present)
    - Metolazone Use: Binary variable indicating advanced heart failure (60 points if used)
    
    Mathematical Formula Implementation:
    
    Score = (2 × age) + (60 if EMS transport) + (-1 × min(SBP, 160)) + 
            (1 × max(80, min(HR, 120))) + (-2 × min(O2sat, 92)) + 
            (20 × creatinine) + potassium_points + (60 if troponin elevated) + 
            (45 if active cancer) + (60 if metolazone use) + 12
    
    Where potassium_points = 5 if K≤3.9, 0 if K 4.0-4.5, 30 if K≥4.6
    
    Risk Stratification and Clinical Interpretation:
    
    The EHMRG classifies patients into six risk groups with specific 7-day mortality rates:
    
    Very Low Risk Groups (Groups 1-2):
    - Score ≤-15.9: Mortality rates 0.3-0.5%
    - Clinical approach: Consider accelerated discharge pathways
    - Management focus: Standard heart failure care with outpatient follow-up
    - Monitoring: Routine clinical assessment sufficient
    
    Intermediate Risk (Group 3):
    - Score -15.8 to 17.9: Mortality rate 0.7%
    - Clinical approach: Standard inpatient management with careful monitoring
    - Management focus: Optimization of heart failure therapy
    - Monitoring: Regular clinical assessment with appropriate follow-up
    
    High Risk Groups (Groups 4-5):
    - Score 18.0-89.3: Mortality rates 2.1-3.3%
    - Clinical approach: Intensive monitoring and aggressive management
    - Management focus: Advanced heart failure interventions
    - Monitoring: Close inpatient observation, cardiology consultation
    
    Highest Risk (Group 5b):
    - Score ≥89.4: Mortality rate 8.0%
    - Clinical approach: Immediate intensive care
    - Management focus: Advanced mechanical support consideration
    - Monitoring: ICU-level care, urgent specialist consultation
    
    Clinical Decision Support Applications:
    
    Disposition Planning:
    - Low-risk patients: Facilitate early discharge with appropriate follow-up
    - High-risk patients: Guide admission decisions and level of care
    - Risk-stratified pathway development for emergency departments
    
    Resource Allocation:
    - Identify patients requiring intensive monitoring resources
    - Guide cardiology consultation decisions
    - Inform family discussions about prognosis and care goals
    
    Quality of Care:
    - Standardize risk assessment across providers
    - Supplement clinical judgment with objective risk quantification
    - Improve communication between healthcare teams
    
    Performance Characteristics and Validation Results:
    
    Discrimination Performance:
    - C-statistic typically 0.70-0.75 for 7-day mortality prediction
    - Superior performance compared to clinical judgment alone
    - Consistent performance across diverse populations and healthcare systems
    
    Calibration Assessment:
    - Good agreement between predicted and observed mortality rates
    - Reliable performance across all risk categories
    - Stable performance in external validation cohorts
    
    Clinical Impact Studies:
    - Physicians tend to overestimate risk in low-risk patients
    - Physicians tend to underestimate risk in high-risk patients
    - EHMRG provides more accurate risk stratification than clinical assessment alone
    
    Implementation Considerations:
    
    Practical Applications:
    - Electronic calculation recommended to minimize computational errors
    - Integration with electronic health records for seamless clinical workflow
    - Staff training on interpretation and clinical application
    
    Quality Assurance:
    - Regular validation of input data accuracy
    - Monitoring of clinical outcomes to ensure continued performance
    - Periodic review of risk thresholds and management protocols
    
    Limitations and Considerations:
    
    Population Applicability:
    - Derived and validated in emergency department populations
    - May not apply to non-acute heart failure presentations
    - Consider local population characteristics and healthcare system factors
    
    Clinical Judgment Integration:
    - Tool should supplement, not replace, clinical assessment
    - Consider individual patient factors not captured in the score
    - Account for social and functional factors in disposition decisions
    
    Temporal Considerations:
    - Designed for 7-day mortality prediction
    - Extended models available for 30-day prediction
    - Regular reassessment may be needed for changing clinical status
    
    Future Directions and Research:
    
    Model Enhancement:
    - Investigation of additional predictive variables
    - Machine learning approaches for improved discrimination
    - Integration with novel biomarkers and advanced diagnostics
    
    Implementation Science:
    - Studies on optimal clinical workflow integration
    - Assessment of clinical impact on patient outcomes
    - Cost-effectiveness analyses of risk-stratified care pathways
    
    Population-Specific Validation:
    - Validation in specialized populations (elderly, pediatric, specific comorbidities)
    - Assessment in different healthcare delivery models
    - Adaptation for resource-limited settings
    
    The EHMRG represents a significant advancement in emergency heart failure care, 
    providing evidence-based risk stratification that enhances clinical decision-making, 
    optimizes resource utilization, and improves patient outcomes through personalized 
    risk assessment and management approaches.
    
    Args:
        request: EHMRG calculation parameters including demographics, vital signs, laboratory values, and clinical factors
        
    Returns:
        EmergencyHeartFailureMortalityRiskGradeEhmrgResponse: EHMRG score with risk stratification and clinical management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("emergency_heart_failure_mortality_risk_grade_ehmrg", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Emergency Heart Failure Mortality Risk Grade",
                    "details": {"parameters": parameters}
                }
            )
        
        return EmergencyHeartFailureMortalityRiskGradeEhmrgResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for EHMRG calculation",
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
                "message": "Internal error in EHMRG calculation",
                "details": {"error": str(e)}
            }
        )