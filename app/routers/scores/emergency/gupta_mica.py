"""
Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA) Router

Endpoint for calculating Gupta MICA perioperative cardiac risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.gupta_mica import (
    GuptaMicaRequest,
    GuptaMicaResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gupta_mica",
    response_model=GuptaMicaResponse,
    summary="Calculate Gupta Perioperative Risk for Myocardial Infarct...",
    description="Predicts risk of myocardial infarction or cardiac arrest within 30 days after surgery using five validated perioperative risk factors",
    response_description="The calculated gupta mica with interpretation",
    operation_id="calculate_gupta_mica"
)
async def calculate_gupta_mica(request: GuptaMicaRequest):
    """
    Calculates Gupta Perioperative Risk for Myocardial Infarction or Cardiac Arrest (MICA)
    
    The Gupta MICA risk calculator is a validated tool that predicts the probability of 
    myocardial infarction or cardiac arrest within 30 days after surgery. This calculator 
    represents a significant advancement in perioperative cardiac risk assessment, offering 
    superior predictive ability compared to previous tools such as the Revised Cardiac Risk Index.
    
    **Clinical Background**:
    Perioperative cardiac events are major causes of morbidity and mortality in surgical 
    patients, occurring in approximately 1-5% of procedures depending on patient and surgical 
    factors. Accurate risk prediction is essential for optimal perioperative management, 
    including decisions about monitoring intensity, preoperative optimization, and postoperative 
    care planning.
    
    **Development and Validation**:
    The Gupta MICA calculator was developed using data from more than 400,000 patients in 
    the American College of Surgeons National Surgical Quality Improvement Program (ACS-NSQIP) 
    database. The model demonstrated superior discriminative ability with a C-statistic of 0.88, 
    significantly outperforming existing risk assessment tools including the Revised Cardiac 
    Risk Index (C-statistic 0.75).
    
    **Five Key Risk Factors**:
    
    **1. Age** (Continuous Variable):
    - Each year of age contributes 0.02 points to the risk score
    - Advanced age reflects reduced physiologic reserve and increased cardiovascular comorbidities
    - Risk increases continuously and gradually with each year of life
    
    **2. Functional Status** (Activities of Daily Living):
    - **Independent** (0.0 points): Can perform all ADLs without assistance
    - **Partially Dependent** (0.65 points): Requires assistance with some ADLs
    - **Totally Dependent** (1.03 points): Requires assistance with all ADLs
    - Reflects overall health status, cardiovascular fitness, and stress tolerance
    
    **3. ASA Physical Status Classification**:
    - **ASA I** (-5.17 points): Normal healthy patient without systemic disease
    - **ASA II** (-3.29 points): Patient with mild systemic disease
    - **ASA III** (-1.92 points): Patient with severe systemic disease limiting activity
    - **ASA IV** (-0.95 points): Patient with severe life-threatening systemic disease
    - **ASA V** (0.0 points): Moribund patient not expected to survive without operation
    
    **4. Creatinine Status** (Kidney Function):
    - **Normal** (0.0 points): Serum creatinine ≤1.5 mg/dL
    - **Elevated** (0.61 points): Serum creatinine >1.5 mg/dL
    - **Unknown** (-0.10 points): Creatinine level not available
    - Elevated creatinine indicates reduced kidney function and associated cardiovascular risk
    
    **5. Surgery Type** (Procedure-Specific Risk):
    Surgical procedures are categorized by inherent cardiac risk based on physiologic stress, 
    duration, blood loss potential, and hemodynamic changes:
    - **Highest Risk**: Aortic surgery (1.60), Brain surgery (1.40), Cardiac surgery (1.01)
    - **High Risk**: Foregut/hepatobiliary (0.82), Gallbladder/appendix/adrenals/spleen (0.67)
    - **Moderate Risk**: Intestinal (0.58), Neck (0.40), OB/GYN (0.28), Orthopedic (0.20)
    - **Low Risk**: Skin (0.12), Spine (0.10), Thoracic non-cardiac (0.06), Hernia (0.0)
    - **Lowest Risk**: Thyroid/parathyroid (-0.32), Eye (-1.05), Vein (-1.09), Breast (-1.61)
    
    **Risk Calculation**:
    The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
    Where: **x = -5.25 + (age × 0.02) + functional_status + ASA_class + creatinine + surgery_type**
    
    **Clinical Risk Categories and Management**:
    
    **Very Low Risk (0.0-0.5%)**:
    - Standard perioperative monitoring and routine postoperative care
    - Continue home medications as appropriate
    - No additional cardiac interventions typically required
    
    **Low Risk (0.5-1.0%)**:
    - Standard monitoring with attention to cardiac symptoms
    - Continue cardiac medications, monitor for ischemic symptoms
    - Basic cardiac precautions and patient education
    
    **Moderate Risk (1.0-2.0%)**:
    - Enhanced monitoring with cardiac telemetry consideration
    - Serial troponin measurements and cardiology consultation for high-risk procedures
    - Optimize medical management of cardiovascular risk factors
    
    **High Risk (2.0-5.0%)**:
    - Intensive monitoring and preoperative cardiology evaluation
    - Continuous cardiac monitoring, postoperative ICU consideration
    - Optimize beta-blockers, statins, and cardioprotective medications
    
    **Very High Risk (>5.0%)**:
    - Comprehensive cardiac evaluation and multidisciplinary approach
    - Consider surgery delay for cardiac optimization
    - Preoperative stress testing and advanced cardiac assessment
    - ICU-level monitoring and specialized care planning
    
    **Clinical Applications**:
    
    **Preoperative Assessment**:
    - Risk stratification for surgical planning and resource allocation
    - Patient and family counseling with specific risk percentages
    - Decision-making for preoperative cardiac testing and optimization
    - Determination of appropriate monitoring intensity
    
    **Perioperative Management**:
    - Selection of monitoring level (standard, telemetry, ICU)
    - Postoperative surveillance strategies and biomarker monitoring
    - Cardiology consultation decisions and timing
    - Discharge planning and follow-up care coordination
    
    **Quality Improvement**:
    - Benchmarking institutional cardiac complication rates
    - Identification of high-risk populations for targeted interventions
    - Resource planning and cost-effectiveness analysis
    - Clinical pathway development and outcome tracking
    
    **Advantages Over Previous Tools**:
    - Superior predictive performance (C-statistic 0.88 vs. 0.75 for RCRI)
    - Includes procedure-specific risk assessment
    - Provides continuous risk estimates rather than categorical classifications
    - Developed and validated in large, contemporary surgical populations
    - Applicable to both cardiac and non-cardiac surgical procedures
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on population data
    - Should complement comprehensive clinical assessment and judgment
    - Individual patient factors may modify risk beyond model predictions
    - Does not include stress test results, echocardiography, or coronary anatomy
    - Urgent/emergent surgery may require risk acceptance despite high scores
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations**:
    - Does not include coronary artery disease history (except prior procedures)
    - Beta-blocker therapy status and other cardiac medications not incorporated
    - May not fully capture complexity of certain patient populations
    - Developed primarily in non-cardiac surgery populations
    - Should be used as part of comprehensive perioperative assessment
    
    Args:
        request: Gupta MICA parameters including age, functional status, ASA class, creatinine status, and surgery type
        
    Returns:
        GuptaMicaResponse: Cardiac risk percentage with comprehensive clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gupta_mica", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gupta MICA Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return GuptaMicaResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gupta MICA Calculator",
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