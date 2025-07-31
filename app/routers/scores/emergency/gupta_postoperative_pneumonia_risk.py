"""
Gupta Postoperative Pneumonia Risk Router

Endpoint for calculating Gupta Postoperative Pneumonia Risk.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.emergency.gupta_postoperative_pneumonia_risk import (
    GuptaPostoperativePneumoniaRiskRequest,
    GuptaPostoperativePneumoniaRiskResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/gupta_postoperative_pneumonia_risk",
    response_model=GuptaPostoperativePneumoniaRiskResponse,
    summary="Calculate Gupta Postoperative Pneumonia Risk Calculator",
    description="Predicts risk of pneumonia after surgery using validated preoperative risk factors from ACS NSQIP data",
    response_description="The calculated gupta postoperative pneumonia risk with interpretation",
    operation_id="calculate_gupta_postoperative_pneumonia_risk"
)
async def calculate_gupta_postoperative_pneumonia_risk(request: GuptaPostoperativePneumoniaRiskRequest):
    """
    Calculates Gupta Postoperative Pneumonia Risk
    
    The Gupta Postoperative Pneumonia Risk calculator is a validated tool that predicts 
    the probability of pneumonia within 30 days after surgery. This calculator was 
    developed using the American College of Surgeons' National Surgical Quality 
    Improvement Program (ACS NSQIP) multicenter, prospective data set from 2007-2008 
    and demonstrates excellent predictive performance with a C-statistic of 0.860.
    
    **Clinical Background**:
    Postoperative pneumonia is a serious complication that occurs in approximately 1.8% 
    of surgical patients and is associated with significantly higher 30-day mortality 
    (17.0% vs 1.5% in patients without pneumonia). Accurate risk prediction enables 
    clinicians to implement targeted prevention strategies, optimize perioperative care, 
    and improve patient outcomes through evidence-based interventions.
    
    **Development and Validation**:
    The calculator was developed using 211,410 patients from the 2007 ACS NSQIP database 
    as the training set and validated on 257,385 patients from the 2008 database. Seven 
    preoperative predictors were identified through multivariate logistic regression 
    analysis, creating a highly accurate prediction model that significantly outperforms 
    clinical judgment alone for pneumonia risk assessment.
    
    **Seven Key Risk Factors**:
    
    **1. Age** (Continuous Variable):
    - Each year of age contributes 0.0144 points to the risk score
    - Advanced age is associated with decreased immune function, reduced respiratory 
      muscle strength, and impaired cough reflex
    - Risk increases continuously with age due to physiological changes and comorbidity accumulation
    
    **2. Chronic Obstructive Pulmonary Disease (COPD)**:
    - **No COPD** (-0.4553 points): Protective factor reflecting normal lung function
    - **COPD Present** (0.0 points): Reference category indicating compromised respiratory function
    - COPD patients have impaired secretion clearance, increased bacterial colonization, 
      and reduced respiratory reserve
    
    **3. Functional Status** (Activities of Daily Living):
    - **Independent** (0.0 points): Can perform all ADLs without assistance
    - **Partially Dependent** (0.7653 points): Requires assistance with some ADLs
    - **Totally Dependent** (0.9400 points): Requires assistance with all ADLs
    - Reflects overall health, mobility, and ability to perform pulmonary hygiene measures
    
    **4. ASA Physical Status Classification**:
    - **ASA I** (-3.0225 points): Normal healthy patient without systemic disease
    - **ASA II** (-1.6057 points): Patient with mild systemic disease
    - **ASA III** (-0.4915 points): Patient with severe systemic disease limiting activity
    - **ASA IV** (0.0123 points): Patient with severe life-threatening systemic disease
    - **ASA V** (0.0 points): Moribund patient not expected to survive without operation
    
    **5. Preoperative Sepsis Status**:
    - **None** (-0.7641 points): No signs of systemic inflammatory response or infection
    - **SIRS** (0.0 points): Systemic Inflammatory Response Syndrome (reference category)  
    - **Sepsis** (-0.0842 points): SIRS with documented or suspected infection
    - **Septic Shock** (0.1048 points): Sepsis with hypotension despite adequate fluid resuscitation
    
    **6. Smoking Within Last Year**:
    - **No Smoking** (-0.4306 points): Protective factor reflecting better respiratory health
    - **Current Smoking** (0.0 points): Reference category indicating compromised respiratory function
    - Smoking impairs ciliary function, increases secretions, and compromises immune function
    
    **7. Type of Surgical Procedure** (Procedure-Specific Risk):
    Surgical procedures are categorized by inherent pneumonia risk based on anatomical 
    location, duration, invasiveness, and impact on respiratory function:
    - **Highest Risk**: Aortic (0.7178), Brain (0.6405), Cardiac (0.4492) surgery
    - **High Risk**: Thoracic non-cardiac (0.2806), Neck (0.1633), Peripheral vascular (0.1382)
    - **Moderate Risk**: Foregut/hepatobiliary (0.1239) to Orthopedic non-spine (0.0189)
    - **Low Risk**: Renal (-0.0234) to Obstetric/gynecologic (-0.1789)
    - **Lowest Risk**: Skin (-0.3254) to Breast (-2.3318) surgery
    
    **Risk Calculation**:
    The calculator uses logistic regression: **Risk (%) = e^x / (1 + e^x) × 100**
    Where: **x = -2.8977 + (age × 0.0144) + COPD + functional_status + ASA + sepsis + smoking + procedure**
    
    **Clinical Risk Categories and Management**:
    
    **Very Low Risk (0.0-1.0%)**:
    - Standard perioperative care and monitoring protocols
    - Routine pulmonary hygiene measures and early mobilization
    - Standard nursing assessments and discharge criteria
    
    **Low Risk (1.0-3.0%)**:
    - Standard care with enhanced pulmonary awareness
    - Incentive spirometry, deep breathing exercises, early ambulation
    - Patient education about importance of pulmonary hygiene measures
    
    **Moderate Risk (3.0-6.0%)**:
    - Enhanced pulmonary care and closer respiratory monitoring
    - Chest physiotherapy, aggressive incentive spirometry protocols
    - Consider respiratory therapy consultation for specialized interventions
    - Optimize pain control to facilitate effective coughing and mobility
    
    **High Risk (6.0-15.0%)**:
    - Aggressive pneumonia prevention strategies and intensive monitoring
    - Consider preoperative pulmonary rehabilitation and smoking cessation programs
    - Intensive chest physiotherapy and specialized respiratory therapy protocols
    - Enhanced respiratory monitoring with pulmonology consultation consideration
    
    **Very High Risk (>15.0%)**:
    - Comprehensive pulmonary optimization and intensive monitoring
    - Consider postponing elective surgery for preoperative pulmonary optimization
    - ICU-level respiratory monitoring with intensive pulmonary care protocols
    - Multidisciplinary team approach including pulmonology and respiratory therapy
    
    **Clinical Applications**:
    
    **Preoperative Assessment**:
    - Risk stratification for surgical planning and resource allocation
    - Patient and family counseling with specific pneumonia risk percentages
    - Decision-making for preoperative pulmonary optimization strategies
    - Determination of appropriate level of postoperative monitoring and care
    
    **Perioperative Management**:
    - Selection of targeted pneumonia prevention interventions based on risk level
    - Respiratory therapy consultation decisions and specialized protocol implementation
    - Pulmonology consultation decisions for high-risk patients requiring expert management
    - Postoperative care planning and surveillance strategies for early complication detection
    
    **Quality Improvement**:
    - Benchmarking institutional pneumonia rates and prevention program effectiveness
    - Identification of high-risk patient populations for targeted interventions
    - Resource planning and cost-effectiveness analysis of prevention strategies
    - Clinical pathway development and standardization of evidence-based care protocols
    
    **Prevention Strategies by Risk Level**:
    - **All Patients**: Early mobilization, adequate pain control, smoking cessation counseling
    - **Moderate Risk**: Incentive spirometry protocols, chest physiotherapy, respiratory therapy consultation
    - **High Risk**: Preoperative pulmonary rehabilitation, intensive postoperative monitoring
    - **Very High Risk**: Comprehensive optimization, consider surgery delay for elective procedures
    
    **Advantages Over Clinical Judgment Alone**:
    - Superior predictive performance (C-statistic 0.860) compared to clinical assessment
    - Objective, standardized risk assessment reducing inter-provider variability
    - Evidence-based tool developed from large, multicenter prospective database
    - Enables targeted resource allocation and intervention strategies
    - Facilitates informed consent discussions with specific risk percentages
    
    **Important Clinical Considerations**:
    - Calculator provides probability estimates based on validated population data
    - Should complement comprehensive clinical assessment and professional judgment
    - Individual patient factors may modify risk beyond model predictions
    - Urgent/emergent surgery may require risk acceptance despite high predicted risk
    - Regular reassessment may be needed for changing clinical conditions
    
    **Limitations**:
    - Does not include all potential pneumonia risk factors or specific comorbidities
    - May not fully capture complexity of certain patient populations or specialized procedures
    - Developed primarily in general surgical populations with potential limitations in specialty surgery
    - Should be used as part of comprehensive perioperative assessment, not as sole decision-making tool
    
    **Research and Validation**:
    The Gupta Postoperative Pneumonia Risk calculator has been extensively validated 
    and is widely adopted in clinical practice. It is incorporated into major clinical 
    guidelines and quality improvement initiatives, representing a significant advance 
    in evidence-based perioperative medicine that enhances patient care and clinical decision-making.
    
    Args:
        request: Gupta Postoperative Pneumonia Risk parameters including age, COPD status, 
                functional status, ASA class, sepsis status, smoking history, and procedure type
        
    Returns:
        GuptaPostoperativePneumoniaRiskResponse: Pneumonia risk percentage with comprehensive 
                                                clinical recommendations and management strategies
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("gupta_postoperative_pneumonia_risk", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating Gupta Postoperative Pneumonia Risk",
                    "details": {"parameters": parameters}
                }
            )
        
        return GuptaPostoperativePneumoniaRiskResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for Gupta Postoperative Pneumonia Risk Calculator",
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