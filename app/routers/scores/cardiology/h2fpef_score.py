"""
H2FPEF Score Router

Endpoint for calculating H2FPEF Score for Heart Failure with Preserved Ejection Fraction.
"""

from fastapi import APIRouter, HTTPException
from app.models.scores.cardiology.h2fpef_score import (
    H2fpefScoreRequest,
    H2fpefScoreResponse
)
from app.services.calculator_service import calculator_service

router = APIRouter()


@router.post(
    "/h2fpef_score",
    response_model=H2fpefScoreResponse,
    summary="Calculate H2FPEF Score for Heart Failure with P...",
    description="Estimates probability of heart failure with preserved ejection fraction (HFpEF) in euvolemic patients with unexplained exertional dyspnea who have had an echocardiogram. Uses clinical characteristics and echocardiographic parameters to distinguish HFpEF from noncardiac causes of dyspnea.",
    response_description="The calculated h2fpef score with interpretation",
    operation_id="calculate_h2fpef_score"
)
async def calculate_h2fpef_score(request: H2fpefScoreRequest):
    """
    Calculates H2FPEF Score for Heart Failure with Preserved Ejection Fraction
    
    The H2FPEF Score estimates the probability of heart failure with preserved ejection 
    fraction (HFpEF) in euvolemic patients with unexplained exertional dyspnea who have 
    had an echocardiogram. This evidence-based diagnostic tool addresses the historical 
    difficulty in diagnosing HFpEF using consensus-based criteria.
    
    **Clinical Background**:
    Heart failure with preserved ejection fraction (HFpEF) accounts for approximately 
    50% of all heart failure cases and represents a significant clinical challenge due 
    to diagnostic uncertainty. Unlike heart failure with reduced ejection fraction 
    (HFrEF), HFpEF diagnosis has historically relied on subjective consensus-based 
    criteria, leading to inconsistency in clinical practice and potential delays in 
    appropriate treatment.
    
    **Development and Validation**:
    The H2FPEF score was derived from 414 consecutive patients with unexplained dyspnea 
    referred for invasive hemodynamic exercise testing, including 267 HFpEF cases and 
    147 controls (HFpEF prevalence 64%). The model was validated in a separate cohort 
    of 100 consecutive patients with 61 HFpEF cases (prevalence 61%). The score 
    demonstrated superior performance to existing consensus-based algorithms with an 
    area under the curve of 0.841, representing a significant improvement in diagnostic 
    accuracy.
    
    **Five Key Diagnostic Parameters**:
    
    **1. Age** (Continuous Variable):
    - **Clinical Significance**: Advanced age is strongly associated with HFpEF through 
      age-related cardiovascular changes including myocardial fibrosis, arterial 
      stiffening, and impaired ventricular relaxation
    - **Mechanism**: Each additional year increases HFpEF probability through accumulated 
      cardiovascular damage and reduced adaptive capacity
    - **Assessment**: Patient's current age in years
    
    **2. Body Mass Index (BMI)**:
    - **Clinical Significance**: Obesity is a major risk factor for HFpEF through multiple 
      pathophysiologic mechanisms including increased blood volume, enhanced sympathetic 
      activity, myocardial metabolic changes, and increased cardiac workload
    - **Calculation**: Weight (kg) divided by height (m) squared
    - **Impact**: Higher BMI values significantly increase HFpEF diagnostic probability
    
    **3. E/e' Ratio** (Echocardiographic Parameter):
    - **Technical Definition**: Ratio of early mitral inflow velocity (E) to early 
      diastolic mitral annular velocity (e') measured by echocardiography
    - **Clinical Significance**: Reflects left ventricular filling pressures and diastolic 
      dysfunction, with higher ratios indicating elevated left atrial pressure
    - **Interpretation**: Normal <8, intermediate 8-15, elevated >15
    - **Mechanism**: Elevated E/e' indicates impaired ventricular relaxation and increased 
      filling pressures characteristic of HFpEF
    
    **4. Pulmonary Artery Systolic Pressure (PASP)**:
    - **Measurement**: Estimated by echocardiography using tricuspid regurgitation velocity
    - **Formula**: PASP = 4 × (TR velocity)² + right atrial pressure estimate
    - **Clinical Significance**: Elevated PASP reflects increased left-sided filling 
      pressures transmitted backward through the pulmonary circulation
    - **Normal Range**: Typically <35 mmHg at rest
    - **Pathophysiology**: Results from elevated left ventricular end-diastolic pressure 
      causing secondary pulmonary hypertension
    
    **5. Atrial Fibrillation**:
    - **Definition**: Includes paroxysmal, persistent, or permanent atrial fibrillation
    - **Clinical Significance**: AF and HFpEF have a complex bidirectional relationship 
      where each condition promotes and worsens the other
    - **Mechanisms**: 
      - HFpEF → AF: Elevated left atrial pressure and atrial remodeling promote AF
      - AF → HFpEF: Loss of atrial kick and irregular heart rate worsen diastolic filling
    - **Impact**: Presence of AF significantly increases HFpEF diagnostic probability
    
    **Probability Calculation and Formula**:
    The H2FPEF score uses logistic regression to calculate HFpEF probability:
    - **Probability** = (Z / (1 + Z)) × 100
    - **Where**: Z = e^y
    - **Linear predictor**: y = -9.1917 + (0.0451 × age) + (0.1307 × BMI) + 
      (0.0859 × E/e' ratio) + (0.0520 × PASP) + (1.6997 × atrial fibrillation)
    
    **Clinical Risk Categories and Management**:
    
    **Low Probability (<25%)**:
    - **Clinical Interpretation**: HFpEF unlikely, consider alternate causes of dyspnea
    - **Differential Diagnosis**: 
      - **Pulmonary**: Asthma, COPD, interstitial lung disease, pulmonary embolism
      - **Metabolic**: Anemia, thyroid disorders, deconditioning, obesity
      - **Other Cardiac**: Coronary artery disease, valvular disease, pericardial disease
    - **Management Approach**: Focus on identified alternative diagnoses
    - **Follow-up**: Reassess if symptoms persist after treating alternative causes
    - **Testing**: Additional cardiac workup may not be indicated unless other features suggest cardiac etiology
    
    **Intermediate Probability (25-75%)**:
    - **Clinical Interpretation**: Uncertain diagnosis, additional testing recommended
    - **Diagnostic Testing Options**:
      - **Gold Standard**: Invasive hemodynamic exercise testing
      - **Biomarkers**: BNP or NT-proBNP levels (consider age and kidney function)
      - **Advanced Imaging**: Stress echocardiography, cardiac MRI with late gadolinium enhancement
      - **Functional Assessment**: Cardiopulmonary exercise testing, 6-minute walk test
      - **Other**: Diastolic stress testing, cardiac catheterization if clinically indicated
    - **Management**: Symptomatic treatment while pursuing definitive diagnosis
    - **Monitoring**: Close clinical follow-up pending additional test results
    - **Clinical Correlation**: Consider symptoms, functional capacity, and response to diuretics
    
    **High Probability (>75%)**:
    - **Clinical Interpretation**: HFpEF highly likely, consider empiric treatment
    - **Guideline-Directed Medical Therapy**:
      - **Renin-Angiotensin System**: ACE inhibitors, ARBs, or ARNIs for blood pressure control
      - **Aldosterone Antagonists**: Spironolactone or eplerenone (monitor potassium and kidney function)
      - **SGLT2 Inhibitors**: Emerging evidence for HFpEF benefit (empagliflozin, dapagliflozin)
      - **Beta-blockers**: If concurrent coronary artery disease or hypertension
    - **Comorbidity Management**:
      - **Hypertension**: Aggressive blood pressure control (<130/80 mmHg)
      - **Diabetes**: Optimal glycemic control, preferentially use SGLT2 inhibitors
      - **Obesity**: Weight reduction through structured diet and exercise programs
      - **Sleep Apnea**: Screening and treatment with CPAP therapy if indicated
      - **Coronary Disease**: Appropriate revascularization and secondary prevention
    - **Lifestyle Modifications**:
      - **Dietary**: Sodium restriction (<2-3g daily), fluid management if volume overloaded
      - **Exercise**: Structured exercise training programs as tolerated and appropriate
      - **Monitoring**: Daily weight monitoring, symptom tracking, medication adherence
    - **Specialist Care**: Regular cardiology follow-up, consider advanced heart failure consultation
    
    **Clinical Applications and Decision-Making**:
    
    **Diagnostic Utility**:
    - **Pre-test Probability**: Establishes HFpEF likelihood before additional testing
    - **Test Selection**: Guides appropriate selection and sequencing of confirmatory tests
    - **Resource Optimization**: Optimizes use of expensive or invasive diagnostic procedures
    - **Clinical Efficiency**: Reduces diagnostic uncertainty and time to appropriate treatment
    - **Standardization**: Promotes consistent diagnostic approach across providers and institutions
    
    **Patient Communication and Shared Decision-Making**:
    - **Prognostic Information**: Provides evidence-based probability estimates for patient discussions
    - **Risk-Benefit Analysis**: Supports informed consent discussions about diagnostic testing
    - **Treatment Planning**: Facilitates decisions about empiric therapy versus additional testing
    - **Expectation Management**: Sets realistic expectations for diagnostic process and outcomes
    - **Care Planning**: Enables appropriate intensity of monitoring and follow-up
    
    **Quality Improvement Applications**:
    - **Clinical Pathways**: Supports development of standardized HFpEF diagnostic pathways
    - **Outcome Measurement**: Enables tracking of diagnostic accuracy and clinical efficiency
    - **Provider Education**: Provides framework for teaching evidence-based HFpEF diagnosis
    - **Research**: Supports clinical research through standardized patient stratification
    - **Guidelines**: Informs clinical practice guidelines and consensus statements
    
    **Advantages of the H2FPEF Score**:
    - **Evidence-Based**: Derived from rigorous clinical validation with invasive hemodynamics
    - **Objective**: Uses quantifiable clinical and echocardiographic parameters
    - **Practical**: Simple calculation using readily available clinical data
    - **Superior Performance**: Significantly outperforms subjective consensus-based algorithms
    - **Validated**: Demonstrated accuracy in independent patient cohorts
    - **Clinically Relevant**: Provides actionable probability ranges for clinical decision-making
    
    **Important Clinical Considerations and Limitations**:
    - **Patient Selection**: Use specifically in euvolemic patients with unexplained exertional dyspnea
    - **Echocardiographic Quality**: Requires adequate technical assessment of diastolic function parameters
    - **Clinical Context**: Should complement rather than replace comprehensive clinical evaluation
    - **Exclusions**: Not validated in patients with reduced ejection fraction or significant valvular disease
    - **Timing**: Should be used when patients are clinically stable and euvolemic
    - **Interpretation**: Clinical judgment remains essential for individual patient management decisions
    - **Follow-up**: May require reassessment if clinical status changes significantly
    
    **Research Foundation and Future Directions**:
    The H2FPEF score represents a paradigm shift from subjective consensus-based criteria 
    to objective, evidence-based HFpEF diagnosis. This tool has been validated across 
    multiple clinical settings and continues to inform ongoing research into HFpEF 
    pathophysiology, diagnosis, and treatment. Future developments may include integration 
    with additional biomarkers, imaging parameters, or functional assessments to further 
    refine diagnostic accuracy.
    
    **Educational Value**:
    The H2FPEF score provides an excellent educational framework for understanding the 
    key pathophysiologic features of HFpEF, including the relationships between age, 
    obesity, diastolic dysfunction, pulmonary pressures, and atrial arrhythmias. This 
    tool helps clinicians develop a systematic approach to HFpEF diagnosis while 
    reinforcing the importance of evidence-based medicine in cardiovascular care.
    
    This calculator enables clinicians to make more informed, evidence-based decisions 
    about HFpEF diagnosis, optimize healthcare resource utilization, and provide patients 
    with objective prognostic information while guiding appropriate therapeutic 
    interventions and monitoring strategies.
    
    Args:
        request: H2FPEF Score parameters including age, BMI, E/e' ratio, PASP, and 
                atrial fibrillation history
        
    Returns:
        H2fpefScoreResponse: HFpEF probability percentage with comprehensive clinical 
                           interpretation and management recommendations
    """
    try:
        # Convert request to dictionary for calculator service
        parameters = request.dict()
        
        # Execute calculation
        result = calculator_service.calculate_score("h2fpef_score", parameters)
        
        if result is None:
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "CalculationError",
                    "message": "Error calculating H2FPEF Score",
                    "details": {"parameters": parameters}
                }
            )
        
        return H2fpefScoreResponse(**result)
        
    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail={
                "error": "ValidationError",
                "message": "Invalid parameters for H2FPEF Score Calculator",
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