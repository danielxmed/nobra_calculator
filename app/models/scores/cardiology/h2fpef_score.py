"""
H2FPEF Score Models

Request and response models for H2FPEF Score calculation.

References (Vancouver style):
1. Reddy YNV, Carter RE, Obokata M, Redfield MM, Borlaug BA. A Simple, Evidence-Based 
   Approach to Help Guide Diagnosis of Heart Failure With Preserved Ejection Fraction. 
   Circulation. 2018;138(9):861-870. doi: 10.1161/CIRCULATIONAHA.118.034646
2. Borlaug BA, Reddy YNV. The Role of the Pulmonary Circulation in Heart Failure With 
   Preserved Ejection Fraction. JACC Heart Fail. 2019;7(5):393-403. 
   doi: 10.1016/j.jchf.2019.02.011
3. Pieske B, Tschöpe C, de Boer RA, et al. How to diagnose heart failure with preserved 
   ejection fraction: the HFA-PEFF diagnostic algorithm: a consensus recommendation from 
   the Heart Failure Association (HFA) of the European Society of Cardiology (ESC). 
   Eur Heart J. 2019;40(40):3297-3317. doi: 10.1093/eurheartj/ehz641

The H2FPEF Score estimates the probability of heart failure with preserved ejection 
fraction (HFpEF) in euvolemic patients with unexplained exertional dyspnea who have 
had an echocardiogram. This evidence-based diagnostic tool was developed to address 
the historical difficulty in diagnosing HFpEF using consensus-based criteria.

**Clinical Background**:
Heart failure with preserved ejection fraction (HFpEF) accounts for approximately 
50% of all heart failure cases and is associated with significant morbidity and 
mortality. Unlike heart failure with reduced ejection fraction (HFrEF), HFpEF 
diagnosis has historically relied on subjective consensus-based criteria, leading 
to diagnostic uncertainty and inconsistency in clinical practice.

**Development and Validation**:
The H2FPEF score was derived from 414 consecutive patients with unexplained dyspnea 
referred for invasive hemodynamic exercise testing (267 HFpEF cases, 147 controls; 
HFpEF prevalence 64%). The model was validated in a separate cohort of 100 consecutive 
patients (61 with HFpEF; prevalence 61%). The score demonstrated superior performance 
to existing consensus-based algorithms with an area under the curve of 0.841.

**Five Key Parameters**:

**1. Age** (Continuous Variable):
- **Clinical Significance**: Advanced age is associated with increased cardiovascular 
  stiffness, diastolic dysfunction, and higher likelihood of HFpEF
- **Mechanism**: Age-related changes include myocardial fibrosis, arterial stiffening, 
  and impaired ventricular relaxation
- **Coefficient**: 0.0451 (each additional year increases probability)

**2. Body Mass Index (BMI)**:
- **Clinical Significance**: Obesity is strongly associated with HFpEF through multiple 
  mechanisms including increased blood volume, enhanced sympathetic activity, and 
  myocardial metabolic changes
- **Pathophysiology**: Obesity leads to increased preload, afterload, and myocardial 
  oxygen demand, contributing to diastolic dysfunction
- **Coefficient**: 0.1307 (higher BMI increases HFpEF probability)
- **Assessment**: Calculated as weight (kg) / height (m)²

**3. E/e' Ratio** (Echocardiographic Parameter):
- **Clinical Significance**: The E/e' ratio is a key indicator of left ventricular 
  filling pressures and diastolic dysfunction
- **Technical Details**: 
  - **E velocity**: Early mitral inflow velocity (transmitral Doppler)
  - **e' velocity**: Early diastolic mitral annular velocity (tissue Doppler)
  - **Normal values**: Generally <8 (normal), 8-15 (intermediate), >15 (elevated)
- **Coefficient**: 0.0859 (higher E/e' increases HFpEF probability)
- **Clinical Interpretation**: Elevated E/e' indicates increased left atrial pressure 
  and impaired ventricular relaxation

**4. Pulmonary Artery Systolic Pressure (PASP)**:
- **Clinical Significance**: Elevated PASP reflects increased left-sided filling 
  pressures and is a consequence of diastolic dysfunction in HFpEF
- **Measurement**: Estimated by echocardiography using tricuspid regurgitation velocity
- **Formula**: PASP = 4 × (TR velocity)² + right atrial pressure estimate
- **Normal Range**: Typically <35 mmHg at rest
- **Coefficient**: 0.0520 (higher PASP increases HFpEF probability)
- **Pathophysiology**: Elevated PASP results from backward transmission of elevated 
  left ventricular end-diastolic pressure

**5. Atrial Fibrillation**:
- **Clinical Significance**: Atrial fibrillation is both a cause and consequence of 
  HFpEF, creating a complex pathophysiologic relationship
- **Types**: Includes paroxysmal, persistent, and permanent atrial fibrillation
- **Mechanisms**: 
  - **HFpEF → AF**: Elevated left atrial pressure and atrial remodeling promote AF
  - **AF → HFpEF**: Loss of atrial kick and irregular heart rate worsen diastolic filling
- **Coefficient**: 1.6997 (presence of AF significantly increases HFpEF probability)
- **Assessment**: Based on documented history, ECG findings, or rhythm monitoring

**Probability Calculation**:
The H2FPEF score uses logistic regression to calculate HFpEF probability:
- **Formula**: Probability = (Z / (1 + Z)) × 100
- **Where**: Z = e^y
- **Linear predictor**: y = -9.1917 + (0.0451 × age) + (0.1307 × BMI) + 
  (0.0859 × E/e' ratio) + (0.0520 × PASP) + (1.6997 × atrial fibrillation)

**Clinical Risk Categories and Management**:

**Low Probability (<25%)**:
- **Clinical Approach**: Consider alternate causes of dyspnea
- **Differential Diagnosis**: 
  - **Pulmonary**: Asthma, COPD, interstitial lung disease, pulmonary embolism
  - **Metabolic**: Anemia, thyroid disorders, deconditioning
  - **Cardiac**: Coronary artery disease, valvular disease, pericardial disease
- **Management**: Focus on alternative diagnoses, HFpEF workup may not be indicated
- **Follow-up**: Address identified alternative causes, reassess if symptoms persist

**Intermediate Probability (25-75%)**:
- **Clinical Approach**: Additional testing recommended
- **Diagnostic Options**:
  - **Gold Standard**: Invasive hemodynamic exercise testing
  - **Biomarkers**: BNP or NT-proBNP levels
  - **Advanced Imaging**: Stress echocardiography, cardiac MRI
  - **Functional Assessment**: 6-minute walk test, cardiopulmonary exercise testing
- **Management**: Symptomatic treatment while pursuing definitive diagnosis
- **Monitoring**: Close follow-up pending additional test results

**High Probability (>75%)**:
- **Clinical Approach**: HFpEF likely, consider empiric treatment
- **Guideline-Directed Medical Therapy**:
  - **ACE inhibitors/ARBs or ARNIs**: For blood pressure control and cardiac remodeling
  - **Aldosterone receptor antagonists**: Spironolactone or eplerenone
  - **SGLT2 inhibitors**: Emerging evidence for HFpEF benefit
  - **Beta-blockers**: If concurrent coronary disease or hypertension
- **Comorbidity Management**:
  - **Hypertension**: Aggressive blood pressure control (<130/80 mmHg)
  - **Diabetes**: Optimal glycemic control, prefer SGLT2 inhibitors
  - **Obesity**: Weight reduction through diet and exercise
  - **Sleep apnea**: Screening and treatment with CPAP if indicated
- **Lifestyle Modifications**:
  - **Dietary**: Sodium restriction (<2-3g daily), fluid management if indicated
  - **Exercise**: Structured exercise training programs as tolerated
  - **Monitoring**: Daily weights, symptom tracking

**Clinical Applications**:

**Diagnostic Decision-Making**:
- **Pre-test Probability**: Establishes HFpEF likelihood before additional testing
- **Test Selection**: Guides appropriate selection of confirmatory tests
- **Resource Allocation**: Optimizes use of expensive or invasive diagnostic procedures
- **Clinical Efficiency**: Reduces diagnostic uncertainty and time to diagnosis

**Patient Communication**:
- **Prognostic Information**: Provides evidence-based probability estimates
- **Shared Decision-Making**: Facilitates discussions about diagnostic testing
- **Treatment Planning**: Supports decisions about empiric therapy vs. further testing
- **Expectation Management**: Sets realistic expectations for diagnostic process

**Quality Improvement**:
- **Standardization**: Promotes consistent diagnostic approach across providers
- **Guideline Implementation**: Supports evidence-based HFpEF diagnosis
- **Outcome Measurement**: Enables tracking of diagnostic accuracy and efficiency
- **Education**: Provides framework for teaching HFpEF diagnostic principles

**Advantages of the H2FPEF Score**:
- **Evidence-Based**: Derived from rigorous clinical validation studies
- **Objective**: Uses quantifiable clinical and echocardiographic parameters
- **Practical**: Simple calculation using readily available clinical data
- **Superior Performance**: Outperforms subjective consensus-based algorithms
- **Validated**: Demonstrated accuracy in independent patient cohorts

**Important Clinical Considerations**:
- **Patient Selection**: Use in euvolemic patients with unexplained exertional dyspnea
- **Echocardiographic Quality**: Requires adequate assessment of diastolic function
- **Clinical Context**: Should complement comprehensive clinical evaluation
- **Exclusions**: Not validated in patients with reduced ejection fraction or 
  significant valvular disease
- **Limitations**: Does not replace clinical judgment or definitive testing when indicated

**Research and Future Directions**:
The H2FPEF score represents a significant advance in HFpEF diagnostic methodology, 
providing clinicians with an objective, evidence-based tool for diagnostic 
decision-making. Ongoing research continues to refine HFpEF diagnosis and treatment, 
with the H2FPEF score serving as a foundation for future diagnostic algorithms and 
clinical decision support systems.

This calculator enables clinicians to make more informed decisions about HFpEF 
diagnosis, optimize resource utilization, and provide patients with evidence-based 
prognostic information while guiding appropriate therapeutic interventions.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class H2fpefScoreRequest(BaseModel):
    """
    Request model for H2FPEF Score Calculator
    
    The H2FPEF Score estimates the probability of heart failure with preserved ejection 
    fraction (HFpEF) using five clinical and echocardiographic parameters. This tool 
    should be used in euvolemic patients with unexplained exertional dyspnea who have 
    undergone echocardiographic assessment.
    
    **Age**: Advanced age increases HFpEF probability due to age-related cardiovascular 
    changes including myocardial fibrosis, arterial stiffening, and impaired ventricular 
    relaxation. Each additional year contributes to increased diagnostic probability.
    
    **Body Mass Index (BMI)**: Obesity is strongly associated with HFpEF through multiple 
    mechanisms including increased blood volume, enhanced sympathetic activity, and 
    myocardial metabolic changes. Higher BMI values increase HFpEF probability.
    
    **E/e' Ratio**: This echocardiographic parameter reflects left ventricular filling 
    pressures and diastolic dysfunction. The ratio combines early mitral inflow velocity 
    (E) with early diastolic mitral annular velocity (e'). Higher ratios indicate elevated 
    left atrial pressure and impaired ventricular relaxation.
    
    **Pulmonary Artery Systolic Pressure (PASP)**: Elevated PASP reflects increased 
    left-sided filling pressures as a consequence of diastolic dysfunction. Measured by 
    echocardiography using tricuspid regurgitation velocity, with normal values typically 
    <35 mmHg at rest.
    
    **Atrial Fibrillation**: The presence of atrial fibrillation (paroxysmal, persistent, 
    or permanent) significantly increases HFpEF probability. AF and HFpEF have a complex 
    bidirectional relationship where each condition promotes the other.
    
    **Clinical Application**:
    - Use in euvolemic patients with unexplained exertional dyspnea
    - Requires adequate echocardiographic assessment of diastolic function
    - Provides objective, evidence-based diagnostic probability
    - Superior to consensus-based diagnostic algorithms (AUC 0.841)
    
    References (Vancouver style):
    1. Reddy YNV, Carter RE, Obokata M, Redfield MM, Borlaug BA. A Simple, Evidence-Based 
    Approach to Help Guide Diagnosis of Heart Failure With Preserved Ejection Fraction. 
    Circulation. 2018;138(9):861-870. doi: 10.1161/CIRCULATIONAHA.118.034646
    2. Borlaug BA, Reddy YNV. The Role of the Pulmonary Circulation in Heart Failure With 
    Preserved Ejection Fraction. JACC Heart Fail. 2019;7(5):393-403. 
    doi: 10.1016/j.jchf.2019.02.011
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Advanced age increases HFpEF probability due to age-related cardiovascular changes including myocardial fibrosis and arterial stiffening",
        ge=18,
        le=120,
        example=68
    )
    
    bmi: float = Field(
        ...,
        description="Body mass index in kg/m². Obesity is strongly associated with HFpEF through increased blood volume, sympathetic activity, and myocardial metabolic changes",
        ge=10.0,
        le=80.0,
        example=32.5
    )
    
    e_e_prime_ratio: float = Field(
        ...,
        description="Echocardiographic E/e' ratio (early mitral inflow velocity to early diastolic mitral annular velocity). Reflects left ventricular filling pressures and diastolic dysfunction. Normal <8, intermediate 8-15, elevated >15",
        ge=1.0,
        le=50.0,
        example=12.5
    )
    
    pasp: int = Field(
        ...,
        description="Pulmonary artery systolic pressure by echocardiography in mmHg. Estimated using tricuspid regurgitation velocity. Normal <35 mmHg. Elevated PASP reflects increased left-sided filling pressures",
        ge=15,
        le=120,
        example=42
    )
    
    atrial_fibrillation: Literal["no", "yes"] = Field(
        ...,
        description="History of atrial fibrillation (paroxysmal, persistent, or permanent). AF and HFpEF have a bidirectional relationship where each condition promotes the other",
        example="yes"
    )
    
    @validator('age')
    def validate_age(cls, v):
        if v < 18 or v > 120:
            raise ValueError('Age must be between 18 and 120 years')
        return v
    
    @validator('bmi')
    def validate_bmi(cls, v):
        if v < 10.0 or v > 80.0:
            raise ValueError('BMI must be between 10.0 and 80.0 kg/m²')
        return v
    
    @validator('e_e_prime_ratio')
    def validate_e_e_prime_ratio(cls, v):
        if v < 1.0 or v > 50.0:
            raise ValueError('E/e\' ratio must be between 1.0 and 50.0')
        return v
    
    @validator('pasp')
    def validate_pasp(cls, v):
        if v < 15 or v > 120:
            raise ValueError('PASP must be between 15 and 120 mmHg')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "age": 68,
                "bmi": 32.5,
                "e_e_prime_ratio": 12.5,
                "pasp": 42,
                "atrial_fibrillation": "yes"
            }
        }


class H2fpefScoreResponse(BaseModel):
    """
    Response model for H2FPEF Score Calculator
    
    Provides the calculated probability of heart failure with preserved ejection fraction 
    (HFpEF) with comprehensive clinical interpretation and management recommendations 
    based on validated diagnostic criteria.
    
    **Probability Interpretation and Clinical Management**:
    
    **Low Probability (<25%)**:
    - **Clinical Approach**: HFpEF unlikely, consider alternate causes of dyspnea
    - **Differential Diagnosis**: Pulmonary (asthma, COPD, ILD, PE), metabolic (anemia, 
      thyroid), or other cardiac causes (CAD, valvular disease)
    - **Management**: Focus on identified alternative diagnoses
    - **Follow-up**: Reassess if symptoms persist after treating alternative causes
    
    **Intermediate Probability (25-75%)**:
    - **Clinical Approach**: Additional testing recommended for definitive diagnosis
    - **Diagnostic Testing Options**:
      - Invasive hemodynamic exercise testing (gold standard)
      - Natriuretic peptides (BNP/NT-proBNP)
      - Stress echocardiography or cardiac MRI
      - Cardiopulmonary exercise testing
    - **Management**: Symptomatic treatment while pursuing confirmatory testing
    - **Monitoring**: Close clinical follow-up pending additional test results
    
    **High Probability (>75%)**:
    - **Clinical Approach**: HFpEF likely, consider empiric guideline-directed therapy
    - **Pharmacological Management**:
      - ACE inhibitors/ARBs or ARNIs for blood pressure control
      - Aldosterone receptor antagonists (spironolactone, eplerenone)
      - SGLT2 inhibitors (emerging evidence for HFpEF benefit)
      - Beta-blockers if concurrent CAD or hypertension
    - **Comorbidity Management**:
      - Aggressive hypertension control (<130/80 mmHg)
      - Optimal diabetes management (prefer SGLT2 inhibitors)
      - Weight reduction for obesity
      - Sleep apnea screening and treatment
    - **Lifestyle Modifications**:
      - Sodium restriction (<2-3g daily)
      - Structured exercise training programs
      - Daily weight monitoring and symptom tracking
    
    **Clinical Applications**:
    - **Diagnostic Decision-Making**: Establishes pre-test probability for additional testing
    - **Resource Optimization**: Guides appropriate use of invasive or expensive diagnostics
    - **Patient Communication**: Provides evidence-based probability for shared decision-making
    - **Quality Improvement**: Enables standardized, objective HFpEF diagnostic approach
    
    **Important Clinical Considerations**:
    - **Patient Selection**: Use in euvolemic patients with unexplained exertional dyspnea
    - **Echocardiographic Quality**: Requires adequate diastolic function assessment
    - **Clinical Context**: Should complement comprehensive clinical evaluation
    - **Validation**: Derived from 414 patients with area under the curve of 0.841
    - **Limitations**: Not validated in reduced EF or significant valvular disease
    
    **Research Foundation**:
    The H2FPEF score was developed to address historical limitations of subjective, 
    consensus-based HFpEF diagnostic criteria. It provides clinicians with an objective, 
    evidence-based tool that outperforms traditional diagnostic approaches and enables 
    more informed clinical decision-making.
    
    Reference: Reddy YNV, et al. Circulation. 2018;138(9):861-870.
    """
    
    result: float = Field(
        ...,
        description="Probability of heart failure with preserved ejection fraction as a percentage",
        ge=0.0,
        le=100.0,
        example=78.3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the HFpEF probability calculation",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including patient characteristics, probability percentage, risk category, and specific clinical recommendations for HFpEF diagnosis and management",
        example="Patient characteristics: 68 years old, BMI 32.5 kg/m², E/e' ratio 12.5, PASP 42 mmHg, atrial fibrillation present. H2FPEF probability: 78.3%. Risk Category: High Probability (High probability of HFpEF). Clinical recommendations: High probability of heart failure with preserved ejection fraction (78.3%). HFpEF is likely and empiric treatment should be considered. Initiate guideline-directed medical therapy including: (1) ACE inhibitors/ARBs or ARNIs, (2) Aldosterone receptor antagonists, (3) SGLT2 inhibitors, (4) Beta-blockers if indicated. Address comorbidities: hypertension control, diabetes management, obesity reduction, sleep apnea treatment. Lifestyle modifications: sodium restriction, fluid management, exercise training as tolerated. Regular cardiology follow-up and monitoring for progression or decompensation. Important considerations: The H2FPEF score was derived and validated in patients with unexplained exertional dyspnea and provides probability estimates for HFpEF diagnosis. This score should be used in euvolemic patients who have undergone echocardiographic assessment. Clinical judgment remains essential, and individual patient factors may modify the diagnostic probability. The score demonstrates superior performance compared to consensus-based algorithms with an area under the curve of 0.841 in validation studies."
    )
    
    stage: str = Field(
        ...,
        description="Probability category classification (Low Probability, Intermediate Probability, High Probability)",
        example="High Probability"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the HFpEF probability category",
        example="High probability of HFpEF"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 78.3,
                "unit": "percentage",
                "interpretation": "Patient characteristics: 68 years old, BMI 32.5 kg/m², E/e' ratio 12.5, PASP 42 mmHg, atrial fibrillation present. H2FPEF probability: 78.3%. Risk Category: High Probability (High probability of HFpEF). Clinical recommendations: High probability of heart failure with preserved ejection fraction (78.3%). HFpEF is likely and empiric treatment should be considered. Initiate guideline-directed medical therapy including: (1) ACE inhibitors/ARBs or ARNIs, (2) Aldosterone receptor antagonists, (3) SGLT2 inhibitors, (4) Beta-blockers if indicated. Address comorbidities: hypertension control, diabetes management, obesity reduction, sleep apnea treatment. Lifestyle modifications: sodium restriction, fluid management, exercise training as tolerated. Regular cardiology follow-up and monitoring for progression or decompensation. Important considerations: The H2FPEF score was derived and validated in patients with unexplained exertional dyspnea and provides probability estimates for HFpEF diagnosis. This score should be used in euvolemic patients who have undergone echocardiographic assessment. Clinical judgment remains essential, and individual patient factors may modify the diagnostic probability. The score demonstrates superior performance compared to consensus-based algorithms with an area under the curve of 0.841 in validation studies.",
                "stage": "High Probability",
                "stage_description": "High probability of HFpEF"
            }
        }