"""
Gupta Postoperative Respiratory Failure Risk Router

Endpoint for calculating Gupta Postoperative Respiratory Failure Risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.gupta_postoperative_respiratory_failure_risk import (
    GuptaPostoperativeRespiratoryFailureRiskRequest,
    GuptaPostoperativeRespiratoryFailureRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gupta_postoperative_respiratory_failure_risk",
    response_model=GuptaPostoperativeRespiratoryFailureRiskResponse,
    summary="Calculate Gupta Postoperative Respiratory Failure Risk Ca...",
    description="Predicts risk of mechanical ventilation for >48 hours post-op or reintubation within 30 days using validated preoperative risk factors from ACS NSQIP data",
    response_description="The calculated gupta postoperative respiratory failure risk with interpretation",
    operation_id="calculate_gupta_postoperative_respiratory_failure_risk"
)
async def calculate_gupta_postoperative_respiratory_failure_risk(request: GuptaPostoperativeRespiratoryFailureRiskRequest):
    """
    Calculates Gupta Postoperative Respiratory Failure Risk
    
    The Gupta Postoperative Respiratory Failure Risk calculator is a validated tool that 
    predicts the probability of respiratory failure requiring mechanical ventilation for 
    >48 hours after surgery or unplanned intubation within 30 days of surgery. This 
    calculator was developed using the American College of Surgeons' National Surgical 
    Quality Improvement Program (ACS NSQIP) multicenter, prospective data set from 
    2007-2008 and demonstrates excellent predictive performance with a C-statistic of 0.894-0.897.
    
    **Clinical Background**:
    Postoperative respiratory failure is a serious complication that occurs in approximately 
    3.1% of surgical patients and is associated with significantly higher 30-day mortality 
    (25.62% vs 0.98% in patients without respiratory failure). This dramatic difference in 
    mortality rates underscores the critical importance of accurate preoperative risk 
    prediction to enable targeted prevention strategies and appropriate care planning.
    
    **Development and Validation**:
    The calculator was developed using 211,410 patients from the 2007 ACS NSQIP database 
    as the training set and validated on 257,385 patients from the 2008 database. Five 
    preoperative predictors were identified through multivariate logistic regression 
    analysis, creating a highly accurate prediction model that significantly outperforms 
    clinical judgment alone for respiratory failure risk assessment.
    
    **Five Key Risk Factors**:
    
    **1. Functional Status** (Activities of Daily Living):
    - **Independent** (0.0 points): Can perform all ADLs without assistance
    - **Partially Dependent** (0.7678 points): Requires assistance with some ADLs  
    - **Totally Dependent** (1.4046 points): Requires assistance with all ADLs
    - Reflects overall health, respiratory muscle strength, and ability to perform 
      respiratory hygiene measures such as deep breathing and effective coughing
    
    **2. ASA Physical Status Classification**:
    - **ASA I** (-3.5265 points): Normal healthy patient without systemic disease
    - **ASA II** (-2.0008 points): Patient with mild systemic disease
    - **ASA III** (-0.6201 points): Patient with severe systemic disease limiting activity
    - **ASA IV** (0.2441 points): Patient with severe life-threatening systemic disease
    - **ASA V** (0.0 points): Moribund patient not expected to survive without operation
    - Higher ASA classes indicate greater systemic illness and reduced physiologic reserve
    
    **3. Preoperative Sepsis Status**:
    - **None** (-0.7840 points): No signs of systemic inflammatory response (protective)
    - **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)
    - **Sepsis** (0.2752 points): SIRS with documented or suspected infection
    - **Septic Shock** (0.9035 points): Sepsis with hypotension despite adequate fluid resuscitation
    - Preoperative infection and inflammation significantly increase respiratory complication risk
    
    **4. Emergency Case Status**:
    - **Elective Surgery** (-0.5739 points): Planned, scheduled procedure (protective factor)
    - **Emergency Surgery** (0.0 points): Urgent or emergent procedure (reference category)
    - Emergency surgery is associated with higher complication rates due to lack of 
      preoperative optimization time and acute illness severity
    
    **5. Type of Surgical Procedure** (Procedure-Specific Risk):
    Surgical procedures are categorized by inherent respiratory failure risk based on 
    anatomical location, duration, invasiveness, and impact on respiratory mechanics:
    - **Highest Risk**: Aortic (1.0781), Brain (0.8086), Thoracic non-cardiac (0.7737), Cardiac (0.6959)
    - **High Risk**: Foregut/hepatobiliary (0.4949) to Gallbladder/appendix/adrenals/spleen (0.2135)
    - **Moderate Risk**: Intestinal (0.1964) to Orthopedic non-spine (0.0654)
    - **Low Risk**: Other abdomen (0.0481) to Obstetric/gynecologic (-0.1456)
    - **Lowest Risk**: Other hematologic (-0.2341) to Breast (-2.6462) surgery
    
    **Risk Calculation**:
    The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
    Where: **x = -1.7397 + functional_status + ASA_class + sepsis + emergency + procedure**
    
    **Clinical Risk Categories and Management**:
    
    **Very Low Risk (0.0-1.0%)**:
    - Standard perioperative care and monitoring protocols
    - Routine respiratory care, early mobilization, standard pain management
    - Standard nursing assessments and discharge criteria
    
    **Low Risk (1.0-3.0%)**:
    - Standard care with enhanced respiratory awareness
    - Ensure adequate pain control to facilitate deep breathing and coughing
    - Monitor for signs of respiratory complications, implement pulmonary hygiene
    - Patient education about respiratory exercises and early mobilization
    
    **Moderate Risk (3.0-8.0%)**:
    - Enhanced respiratory monitoring and pulmonary care protocols
    - Aggressive pulmonary hygiene, incentive spirometry, respiratory therapy consultation
    - Closer respiratory assessment, oxygen saturation monitoring
    - Optimize pain control to facilitate effective coughing and deep breathing
    
    **High Risk (8.0-20.0%)**:
    - Intensive respiratory monitoring and consider ICU-level care
    - Strong consideration for pulmonology consultation and preoperative optimization
    - Intensive respiratory therapy, mechanical ventilation readiness protocols
    - Enhanced postoperative surveillance, continuous respiratory monitoring
    - Multidisciplinary involvement including pulmonology and critical care
    
    **Very High Risk (>20.0%)**:
    - Comprehensive respiratory optimization and intensive monitoring
    - Consider postponing elective surgery for respiratory optimization
    - ICU-level monitoring with mechanical ventilation readily available
    - Multidisciplinary team including pulmonology, anesthesia, and critical care
    - Extended hospitalization with intensive outpatient respiratory follow-up
    
    **Clinical Applications**:
    
    **Preoperative Assessment**:
    - Risk stratification for surgical planning and resource allocation
    - Patient and family counseling with specific respiratory failure risk percentages
    - Decision-making for preoperative respiratory optimization strategies
    - Determination of appropriate level of postoperative monitoring and care intensity
    
    **Perioperative Management**:
    - Selection of targeted respiratory failure prevention interventions based on risk level
    - ICU admission decisions and mechanical ventilation readiness protocols
    - Pulmonology consultation decisions for high-risk patients requiring specialized management
    - Postoperative care planning and surveillance strategies for early complication detection
    
    **Quality Improvement**:
    - Benchmarking institutional respiratory failure rates and prevention program effectiveness
    - Identification of high-risk patient populations for targeted interventions and protocols
    - Resource planning and cost-effectiveness analysis of prevention strategies and ICU utilization
    - Clinical pathway development and standardization of evidence-based respiratory care protocols
    
    **Prevention Strategies by Risk Level**:
    - **All Patients**: Early mobilization protocols, adequate pain control, standard respiratory care
    - **Moderate Risk**: Intensive pulmonary hygiene, respiratory therapy consultation, enhanced monitoring
    - **High Risk**: Preoperative optimization, ICU-level care consideration, pulmonology involvement
    - **Very High Risk**: Comprehensive optimization, surgery delay consideration for elective procedures
    
    **Advantages Over Clinical Judgment Alone**:
    - Superior predictive performance (C-statistic 0.894-0.897) compared to clinical assessment
    - Objective, standardized risk assessment reducing inter-provider variability
    - Evidence-based tool developed from large, multicenter prospective database
    - Enables targeted resource allocation and intervention strategies
    - Facilitates informed consent discussions with specific risk percentages
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data from large cohorts
    - Should complement comprehensive clinical assessment and professional judgment
    - Individual patient factors may modify risk beyond model predictions (pulmonary function tests)
    - Urgent/emergent surgery may require risk acceptance despite high predicted risk scores
    - Regular reassessment may be needed for changing clinical conditions during hospitalization
    
    **Limitations**:
    - Does not include specific pulmonary function test results or detailed respiratory history
    - May not fully capture complexity of certain patient populations or highly specialized procedures
    - Developed primarily in general surgical populations with potential limitations in specialty surgery
    - Should be used as part of comprehensive perioperative assessment, not as sole decision-making tool
    
    **Research and Validation**:
    The Gupta Postoperative Respiratory Failure Risk calculator has been extensively 
    validated and is widely adopted in clinical practice. It is incorporated into major 
    clinical guidelines and quality improvement initiatives, representing a significant 
    advance in evidence-based perioperative medicine that enhances patient care and 
    clinical decision-making.
    
    This calculator enables clinicians to identify patients at highest risk for respiratory 
    failure, implement targeted prevention strategies, and allocate appropriate resources 
    to improve patient outcomes and reduce the significant mortality associated with 
    postoperative respiratory complications.
    
    Args:
        request: Gupta Postoperative Respiratory Failure Risk parameters including functional 
                status, ASA class, sepsis status, emergency case status, and procedure type
        
    Returns:
        GuptaPostoperativeRespiratoryFailureRiskResponse: Respiratory failure risk percentage 
                                                        with comprehensive clinical recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gupta_postoperative_respiratory_failure_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gupta Postoperative Respiratory Failure Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return GuptaPostoperativeRespiratoryFailureRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gupta Postoperative Respiratory Failure Risk Calculator",
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