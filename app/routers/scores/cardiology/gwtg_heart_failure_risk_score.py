"""
GWTG-Heart Failure Risk Score Router

Endpoint for calculating GWTG-Heart Failure Risk Score.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.gwtg_heart_failure_risk_score import (
    GwtgHeartFailureRiskScoreRequest,
    GwtgHeartFailureRiskScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gwtg_heart_failure_risk_score",
    response_model=GwtgHeartFailureRiskScoreResponse,
    summary="Calculate GWTG-Heart Failure Risk Score",
    description="Predicts all-cause in-hospital mortality in admitted patients with heart failure using validated AHA Get With The Guidelines data",
    response_description="The calculated gwtg heart failure risk score with interpretation",
    operation_id="calculate_gwtg_heart_failure_risk_score"
)
async def calculate_gwtg_heart_failure_risk_score(request: GwtgHeartFailureRiskScoreRequest):
    """
    Calculates GWTG-Heart Failure Risk Score
    
    The GWTG-Heart Failure Risk Score is a validated tool that predicts all-cause 
    in-hospital mortality in admitted patients with heart failure. This calculator was 
    developed using the American Heart Association Get With The Guidelines-Heart Failure 
    (GWTG-HF) program data from 39,783 patients from 198 hospitals and demonstrates 
    good discriminative ability with a C-index of 0.75.
    
    **Clinical Background**:
    Heart failure is a leading cause of hospitalization and mortality in adults, with 
    in-hospital mortality rates averaging 2.86% across diverse patient populations. 
    Accurate risk prediction enables clinicians to identify high-risk patients who may 
    benefit from intensive monitoring, advanced therapies, and appropriate resource 
    allocation while facilitating informed discussions with patients and families about 
    prognosis and care goals.
    
    **Development and Validation**:
    The GWTG-HF risk score was derived and validated using data from patients admitted 
    between January 1, 2005, and June 26, 2007, with the cohort divided into derivation 
    (70%, n=27,850) and validation (30%, n=11,933) samples. The model demonstrated 
    consistent performance across both datasets and showed good discrimination with 
    predicted mortality varying more than 24-fold across score deciles (range, 0.4% to 9.7%).
    
    **Seven Key Risk Factors**:
    
    **1. Age** (Continuous Variable):
    - Each year above 65 contributes incrementally to the risk score
    - Advanced age reflects reduced physiologic reserve and increased comorbidities
    - Associated with accumulated cardiovascular damage and reduced adaptive capacity
    
    **2. Systolic Blood Pressure**:
    - Lower values indicate hemodynamic compromise and increased mortality risk
    - Values below 140 mmHg contribute to higher risk scores
    - Reflects acute hemodynamic status and cardiac contractile function
    
    **3. Blood Urea Nitrogen (BUN)**:
    - Elevated values indicate renal dysfunction and cardiorenal syndrome
    - Values above 20 mg/dL increase risk score proportionally
    - BUN elevation often indicates more severe disease with worse prognosis
    
    **4. Heart Rate**:
    - Elevated rates may indicate compensatory tachycardia or hemodynamic instability
    - Values above 70 bpm contribute to higher risk scores
    - Reflects autonomic nervous system activation and cardiovascular stress response
    
    **5. Serum Sodium**:
    - Lower values indicate neurohormonal activation and volume overload
    - Hyponatremia below 140 mEq/L increases mortality risk significantly
    - Strongly associated with increased mortality and longer hospital stays
    
    **6. Chronic Obstructive Pulmonary Disease (COPD)**:
    - **Present** (+2 points): Documented history of COPD
    - **Absent** (0 points): No history of COPD
    - COPD complicates heart failure management and increases respiratory complications
    
    **7. Race** (Black vs. Non-Black):
    - **Black Race** (+1 point): Protective factor in this scoring system
    - **Non-Black Race** (+4 points): Higher risk category
    - Reflects population-based differences in heart failure outcomes
    
    **Risk Calculation**:
    The score ranges from 0-100 points, calculated by summing contributions from all 
    seven variables. The final score corresponds to specific mortality risk categories.
    
    **Clinical Risk Categories and Management**:
    
    **Very Low Risk (Score 0-33, <1% Mortality)**:
    - Standard heart failure care protocols and monitoring
    - Evidence-based heart failure medications, standard fluid management
    - Routine follow-up within 7-14 days, standard patient education
    
    **Low Risk (Score 34-50, 1-5% Mortality)**:
    - Standard care with optimization of heart failure therapy
    - Maximize guideline-directed medical therapy, optimize volume status
    - Enhanced patient education, follow-up within 1-2 weeks
    
    **Moderate Risk (Score 51-57, 5-15% Mortality)**:
    - Enhanced monitoring and aggressive heart failure management
    - Optimize diuretics, vasodilators, and neurohormonal blockade
    - Consider cardiology consultation, close outpatient follow-up within 3-7 days
    
    **High Risk (Score 58-70, 15-30% Mortality)**:
    - Intensive monitoring and consideration of advanced therapies
    - Evaluate for advanced heart failure interventions, inotropic support
    - Cardiology consultation, initiate palliative care discussions
    
    **Very High Risk (Score >70, >30% Mortality)**:
    - Intensive care management with advanced therapies
    - ICU-level monitoring, mechanical circulatory support evaluation
    - Advanced heart failure specialist, comprehensive end-of-life care planning
    
    **Clinical Applications**:
    
    **Risk Stratification**:
    - Systematic identification of high-risk patients requiring intensive management
    - Resource allocation decisions for monitoring intensity and specialized care
    - Prognostic information for clinical decision-making and care planning
    - Quality improvement initiatives and outcome prediction
    
    **Patient and Family Communication**:
    - Evidence-based prognostic information for informed consent discussions
    - Risk-benefit analysis for advanced therapies and interventions
    - Care goal discussions and advance directive planning
    - Realistic expectation setting for hospitalization outcomes
    
    **Quality Improvement**:
    - Benchmarking institutional heart failure mortality rates
    - Identification of patient populations for targeted interventions
    - Resource planning and cost-effectiveness analysis
    - Clinical pathway development and standardization
    
    **Advantages of Validated Risk Assessment**:
    - Superior predictive performance (C-index 0.75) compared to clinical judgment alone
    - Objective, standardized risk assessment reducing inter-provider variability
    - Evidence-based tool developed from large, multicenter prospective database
    - Enables targeted resource allocation and intervention strategies
    - Facilitates informed consent discussions with specific risk percentages
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data
    - Should complement comprehensive clinical assessment and professional judgment
    - Score is applicable to both preserved and reduced ejection fraction heart failure
    - Individual patient factors may modify risk beyond model predictions
    - Consider social determinants of health and individual patient preferences
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations**:
    - Does not include echocardiographic parameters or detailed hemodynamic data
    - May not fully capture complexity of certain patient populations or comorbidities
    - Race-based adjustment requires careful interpretation in clinical context
    - Should be used as part of comprehensive heart failure assessment
    - Developed primarily in hospitalized patients, may have limitations in other settings
    
    **Research and Validation**:
    The GWTG-Heart Failure Risk Score has been extensively validated across diverse 
    clinical settings including cardiac intensive care units, general cardiology populations, 
    and various procedural contexts. It represents a significant advance in evidence-based 
    heart failure risk assessment and has been incorporated into major clinical guidelines 
    and quality improvement initiatives.
    
    This calculator enables clinicians to provide evidence-based prognostic information, 
    make informed decisions about care intensity, and facilitate appropriate discussions 
    with patients and families about goals of care and treatment options.
    
    Args:
        request: GWTG-Heart Failure Risk Score parameters including age, systolic BP, 
                BUN, heart rate, sodium, COPD history, and race
        
    Returns:
        GwtgHeartFailureRiskScoreResponse: Mortality risk percentage with comprehensive 
                                         clinical recommendations and management strategies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gwtg_heart_failure_risk_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating GWTG-Heart Failure Risk Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return GwtgHeartFailureRiskScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for GWTG-Heart Failure Risk Score Calculator",
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