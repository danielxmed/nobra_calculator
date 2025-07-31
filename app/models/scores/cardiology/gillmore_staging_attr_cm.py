"""
Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Models

Request and response models for Gillmore staging calculation.

References (Vancouver style):
1. Gillmore JD, Damy T, Fontana M, et al. A new staging system for cardiac transthyretin 
   amyloidosis. Eur Heart J. 2018;39(30):2799-2806. doi: 10.1093/eurheartj/ehx589.
2. Fontana M, Corovic A, Scully P, Moon JC. Myocardial amyloidosis: the exemplar 
   interstitial disease. JACC Cardiovasc Imaging. 2019;12(11 Pt 2):2345-2356. 
   doi: 10.1016/j.jcmg.2019.06.023.
3. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin cardiac 
   amyloidosis and risk stratification using a novel staging system. J Am Coll Cardiol. 
   2016;68(10):1014-1020. doi: 10.1016/j.jacc.2016.06.033.

The Gillmore staging system is a prognostic classification system for patients with 
transthyretin amyloid cardiomyopathy (ATTR-CM) developed by the UK National Amyloidosis 
Centre. This system uses two readily available biomarkers to stratify patients into 
three distinct prognostic categories, applicable to both wild-type (ATTRwt) and variant 
(ATTRv) forms of cardiac amyloidosis.

Key Clinical Applications:
- Prognostic stratification for newly diagnosed ATTR-CM patients
- Treatment planning and intensity decisions for disease-specific therapies
- Clinical trial eligibility assessment and stratification
- Monitoring disease progression through serial biomarker assessment
- Multidisciplinary care coordination and resource allocation planning

The staging system demonstrates excellent prognostic discrimination with significant 
survival differences between stages. It was developed from a cohort of 869 patients 
(553 wild-type, 316 variant) and validated in an independent cohort of 318 patients, 
showing consistent prognostic performance across different ATTR-CM populations and 
healthcare systems.

Clinical validation studies have consistently demonstrated that this simple staging 
system effectively stratifies patients into clinically meaningful prognostic categories: 
Stage I patients have median survival of 69.2 months with the best prognosis, Stage II 
patients have intermediate survival of 46.7 months, and Stage III patients have the 
poorest prognosis with median survival of 24.1 months. The system uses universally 
available biomarkers making it practical for widespread clinical implementation.
"""

from pydantic import BaseModel, Field
from typing import Literal


class GillmoreStagingAttrCmRequest(BaseModel):
    """
    Request model for Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    The Gillmore staging system provides prognostic stratification for patients with 
    transthyretin amyloid cardiomyopathy using two readily available biomarkers that 
    reflect both cardiac dysfunction and renal involvement in this systemic disease.
    
    **CLINICAL CONTEXT AND INDICATIONS**:
    
    **Primary Clinical Application**:
    - **Target Population**: Patients with confirmed transthyretin amyloid cardiomyopathy (both ATTRwt and ATTRv)
    - **Clinical Settings**: Cardiology clinics, amyloid centers, heart failure programs, tertiary care centers
    - **Assessment Timing**: At diagnosis, during treatment planning, and for serial monitoring
    - **Diagnostic Prerequisite**: Confirmed ATTR-CM diagnosis through appropriate imaging and/or biopsy
    
    **Key Advantages for ATTR-CM Management**:
    - **Universal Applicability**: Effective for both wild-type and variant forms of ATTR-CM
    - **Readily Available Biomarkers**: Uses standard laboratory tests available in most healthcare settings
    - **Validated Performance**: Extensively validated in large cohorts with consistent prognostic accuracy
    - **Clinical Decision Support**: Guides treatment intensity, monitoring frequency, and care coordination
    - **Trial Eligibility**: Useful for clinical trial stratification and enrollment decisions
    
    **BIOMARKER INTERPRETATION FRAMEWORK**:
    
    **NT-proBNP (N-terminal pro-B-type Natriuretic Peptide)**:
    
    **Clinical Significance**: Primary biomarker of cardiac dysfunction and heart failure severity
    - **Physiological Role**: Released by ventricular myocytes in response to wall stress and volume overload
    - **ATTR-CM Context**: Elevated due to amyloid infiltration causing diastolic dysfunction and heart failure
    - **Prognostic Value**: Higher levels associated with advanced cardiac involvement and worse outcomes
    - **Threshold Rationale**: 3000 ng/L cutoff derived from optimal prognostic discrimination in ATTR-CM cohorts
    
    **Laboratory Considerations**:
    - **Units**: Expressed in ng/L (nanograms per liter) or pg/mL (picograms per milliliter, 1 ng/L = 1 pg/mL)
    - **Normal Range**: Typically <125 pg/mL in healthy adults, varies by age and clinical laboratory
    - **ATTR-CM Range**: Often markedly elevated (hundreds to thousands ng/L) reflecting cardiac dysfunction
    - **Assay Variability**: Results may vary between different laboratory platforms and methodologies
    
    **Clinical Interpretation Guidelines**:
    - **≤3000 ng/L**: Indicates relatively preserved cardiac function with better prognosis
    - **>3000 ng/L**: Suggests significant cardiac dysfunction with increased mortality risk
    - **Serial Monitoring**: Changes over time reflect disease progression or treatment response
    - **Confounding Factors**: May be elevated due to other causes of heart failure, renal dysfunction, or age
    
    **eGFR (Estimated Glomerular Filtration Rate)**:
    
    **Clinical Significance**: Biomarker of renal function and systemic disease involvement
    - **Physiological Role**: Measure of kidney's filtering capacity, indicating overall renal health
    - **ATTR-CM Context**: Renal involvement common in systemic amyloidosis, affects prognosis significantly
    - **Prognostic Value**: Lower eGFR associated with multiorgan involvement and worse survival
    - **Threshold Rationale**: 45 ml/min cutoff reflects moderate renal impairment with prognostic significance
    
    **Calculation Methods**:
    - **CKD-EPI Formula**: Preferred method incorporating age, sex, race, and serum creatinine
    - **MDRD Formula**: Alternative calculation method, less accurate at higher GFR levels
    - **Units**: Expressed as ml/min/1.73m² (milliliters per minute per 1.73 square meters body surface area)
    - **Standardization**: Adjusted for standard body surface area for population comparisons
    
    **Clinical Interpretation Guidelines**:
    - **≥45 ml/min**: Normal to mildly impaired renal function with better prognosis
    - **<45 ml/min**: Moderate to severe renal impairment indicating systemic disease involvement
    - **CKD Staging**: Corresponds to CKD Stage 3b or worse (moderate to severe reduction)
    - **Progressive Decline**: Serial measurements help assess disease progression and treatment response
    
    **STAGING SYSTEM FRAMEWORK**:
    
    **Stage I Criteria (Best Prognosis)**:
    - **Biomarker Profile**: NT-proBNP ≤3000 ng/L AND eGFR ≥45 ml/min
    - **Clinical Significance**: Both cardiac and renal biomarkers in favorable ranges
    - **Patient Characteristics**: Earlier disease stage with preserved organ function
    - **Median Survival**: 69.2 months (approximately 5.8 years)
    - **Management Approach**: Standard ATTR-CM care with regular monitoring and optimization
    
    **Stage II Criteria (Intermediate Prognosis)**:
    - **Biomarker Profile**: Mixed pattern not meeting Stage I or III criteria
    - **Clinical Significance**: One biomarker elevated while the other remains favorable
    - **Patient Characteristics**: Intermediate disease severity with selective organ involvement
    - **Median Survival**: 46.7 months (approximately 3.9 years)
    - **Management Approach**: Enhanced monitoring with consideration for disease-specific therapies
    
    **Stage III Criteria (Worst Prognosis)**:
    - **Biomarker Profile**: NT-proBNP >3000 ng/L AND eGFR <45 ml/min
    - **Clinical Significance**: Both cardiac and renal biomarkers indicating advanced disease
    - **Patient Characteristics**: Advanced multiorgan involvement with significant dysfunction
    - **Median Survival**: 24.1 months (approximately 2 years)
    - **Management Approach**: Urgent consideration for intensive therapies and multidisciplinary care
    
    **CLINICAL VALIDATION AND PERFORMANCE**:
    
    **Development Cohort**:
    - **Population**: 869 patients with cardiac ATTR amyloidosis (553 wild-type, 316 variant)
    - **Setting**: UK National Amyloidosis Centre, tertiary referral center
    - **Follow-up**: Comprehensive survival data with median follow-up period
    - **Outcome**: All-cause mortality as primary endpoint
    
    **Validation Cohort**:
    - **Population**: Independent cohort of 318 patients for external validation
    - **Consistency**: Confirmed prognostic performance across different patient populations
    - **Generalizability**: Demonstrated applicability in diverse clinical settings
    - **Reproducibility**: Consistent results across different healthcare systems
    
    **Statistical Performance**:
    - **Discrimination**: Excellent separation between survival curves (p < 0.0001)
    - **Hazard Ratios**: Stage II HR 2.05 (95% CI 1.54-2.72), Stage III HR 3.80 (95% CI 2.73-5.28)
    - **Prognostic Accuracy**: Strong predictive value for mortality risk stratification
    - **Clinical Utility**: Meaningful survival differences supporting clinical decision-making
    
    **CLINICAL IMPLEMENTATION GUIDELINES**:
    
    **Assessment Timing**:
    - **Initial Evaluation**: Obtain staging at time of ATTR-CM diagnosis
    - **Treatment Planning**: Use staging to guide therapeutic intensity and monitoring frequency
    - **Serial Assessment**: Repeat staging periodically to monitor disease progression
    - **Clinical Trials**: Incorporate staging for patient stratification and eligibility assessment
    
    **Laboratory Requirements**:
    - **NT-proBNP**: Fasting not required, avoid hemolysis, results available same day
    - **Creatinine**: For eGFR calculation, fasting preferred but not essential
    - **Timing**: Obtain during stable clinical condition, avoid during acute illness
    - **Quality Assurance**: Ensure laboratory accreditation and appropriate reference ranges
    
    **Clinical Interpretation**:
    - **Multifactorial Assessment**: Consider staging within overall clinical context
    - **Comorbidity Assessment**: Account for other conditions affecting biomarkers
    - **Treatment Response**: Monitor changes in staging with disease-specific therapies
    - **Prognosis Communication**: Use staging data to inform patients and families about expected outcomes
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Confounding Factors**:
    - **Heart Failure**: Other causes may elevate NT-proBNP independent of amyloid burden
    - **Renal Disease**: Primary kidney disease may affect eGFR independently of amyloidosis
    - **Age**: Both biomarkers may be elevated in elderly patients without amyloidosis
    - **Medications**: Certain drugs may affect biomarker levels (diuretics, ACE inhibitors, etc.)
    
    **Treatment Implications**:
    - **Disease-Specific Therapy**: Higher stages may benefit more from early aggressive treatment
    - **Monitoring Intensity**: Advanced stages require more frequent clinical and laboratory assessment
    - **Multidisciplinary Care**: Stage III patients may need cardiology, nephrology, and palliative care
    - **Clinical Trials**: Staging helps determine appropriate trial eligibility and stratification
    
    **Prognostic Counseling**:
    - **Survival Estimates**: Provide median survival data while emphasizing individual variation
    - **Treatment Impact**: Explain how disease-specific therapies may modify natural history
    - **Quality of Life**: Discuss functional outcomes and symptom management strategies
    - **Care Planning**: Use staging data to guide advanced directive discussions and care goals
    
    References (Vancouver style):
    1. Gillmore JD, Damy T, Fontana M, et al. A new staging system for cardiac transthyretin 
       amyloidosis. Eur Heart J. 2018;39(30):2799-2806. doi: 10.1093/eurheartj/ehx589.
    2. Fontana M, Corovic A, Scully P, Moon JC. Myocardial amyloidosis: the exemplar 
       interstitial disease. JACC Cardiovasc Imaging. 2019;12(11 Pt 2):2345-2356.
    3. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin cardiac 
       amyloidosis and risk stratification using a novel staging system. J Am Coll Cardiol. 
       2016;68(10):1014-1020.
    """
    
    nt_probnp: float = Field(
        ...,
        description="N-terminal pro-B-type natriuretic peptide (NT-proBNP) level in ng/L. Biomarker of cardiac dysfunction and heart failure severity. Threshold of 3000 ng/L used for prognostic stratification",
        ge=0,
        le=50000,
        example=2500.0
    )
    
    egfr: float = Field(
        ..., 
        description="Estimated glomerular filtration rate (eGFR) in ml/min. Biomarker of renal function calculated using serum creatinine. Threshold of 45 ml/min represents moderate renal impairment",
        ge=5,
        le=150,
        example=55.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "nt_probnp": 2500.0,
                "egfr": 55.0
            }
        }


class GillmoreStagingAttrCmResponse(BaseModel):
    """
    Response model for Gillmore Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    The response provides the calculated Gillmore stage with comprehensive clinical interpretation 
    and evidence-based management recommendations based on validated prognostic categories 
    from extensive clinical validation studies.
    
    **CLINICAL INTERPRETATION FRAMEWORK**:
    
    **Gillmore Staging Components and Validation**:
    - **Biomarker Integration**: Combines NT-proBNP (cardiac dysfunction) and eGFR (renal function)
    - **Prognostic Accuracy**: Validated in 869 patients with external validation in 318 patients
    - **Population Applicability**: Effective for both wild-type (ATTRwt) and variant (ATTRv) ATTR-CM
    - **Statistical Significance**: Strong prognostic discrimination (p < 0.0001) with clear survival differences
    
    **Stage Definitions and Clinical Implications**:
    
    **Stage I (Best Prognosis)**:
    - **Biomarker Criteria**: NT-proBNP ≤3000 ng/L AND eGFR ≥45 ml/min
    - **Population Prevalence**: 393 patients (45% of original cohort)
    - **Median Survival**: 69.2 months (approximately 5.8 years)
    - **Clinical Significance**: Both cardiac and renal biomarkers in favorable ranges
    - **Management Approach**: Standard ATTR-CM care with regular monitoring and optimization
    
    **Stage II (Intermediate Prognosis)**:
    - **Biomarker Criteria**: Mixed pattern not meeting Stage I or III criteria
    - **Population Prevalence**: 334 patients (38% of original cohort) 
    - **Median Survival**: 46.7 months (approximately 3.9 years)
    - **Hazard Ratio**: 2.05 (95% CI 1.54-2.72) compared to Stage I
    - **Clinical Significance**: One biomarker elevated while the other remains in favorable range
    - **Management Approach**: Enhanced monitoring with consideration for disease-specific therapies
    
    **Stage III (Worst Prognosis)**:
    - **Biomarker Criteria**: NT-proBNP >3000 ng/L AND eGFR <45 ml/min
    - **Population Prevalence**: 142 patients (16% of original cohort)
    - **Median Survival**: 24.1 months (approximately 2 years)
    - **Hazard Ratio**: 3.80 (95% CI 2.73-5.28) compared to Stage I
    - **Clinical Significance**: Both cardiac and renal biomarkers indicating advanced multiorgan disease
    - **Management Approach**: Urgent consideration for intensive therapies and multidisciplinary care
    
    **CLINICAL MANAGEMENT BY STAGE**:
    
    **Stage I Management (Best Prognosis)**:
    
    **Treatment Approach**:
    - **Standard Care**: Implement guideline-directed heart failure therapy
    - **Disease-Specific Therapy**: Consider tafamidis or other ATTR-specific treatments
    - **Monitoring Strategy**: Regular clinical assessment every 3-6 months
    - **Biomarker Surveillance**: Serial NT-proBNP and eGFR monitoring to detect progression
    
    **Clinical Optimization**:
    - **Heart Failure Management**: ACE inhibitors/ARBs, beta-blockers as tolerated
    - **Symptom Control**: Diuretics for volume management, rate control for arrhythmias
    - **Lifestyle Counseling**: Dietary sodium restriction, fluid management, exercise as appropriate
    - **Comorbidity Management**: Optimize diabetes, hypertension, and other cardiovascular risk factors
    
    **Stage II Management (Intermediate Prognosis)**:
    
    **Enhanced Monitoring**:
    - **Increased Frequency**: Clinical assessments every 2-3 months
    - **Biomarker Tracking**: More frequent NT-proBNP and renal function monitoring
    - **Functional Assessment**: Regular evaluation of exercise capacity and quality of life
    - **Imaging Surveillance**: Consider periodic echocardiography or cardiac MRI
    
    **Treatment Intensification**:
    - **Disease-Specific Therapy**: Strong consideration for tafamidis or investigational agents
    - **Heart Failure Optimization**: Maximize guideline-directed medical therapy
    - **Specialist Referral**: Ensure cardiology and possibly nephrology involvement
    - **Clinical Trial Consideration**: Evaluate eligibility for appropriate research studies
    
    **Stage III Management (Worst Prognosis)**:
    
    **Urgent Intervention**:
    - **Immediate Assessment**: Comprehensive evaluation within 1-2 weeks of staging
    - **Disease-Specific Therapy**: Urgent consideration for all available ATTR-specific treatments
    - **Multidisciplinary Care**: Coordinate cardiology, nephrology, and palliative care consultation
    - **Advanced Therapies**: Evaluate for heart transplantation or mechanical circulatory support if appropriate
    
    **Intensive Monitoring**:
    - **Frequent Visits**: Clinical assessments every 4-6 weeks or as clinically indicated
    - **Close Surveillance**: Weekly to biweekly laboratory monitoring during treatment initiation
    - **Symptom Management**: Aggressive optimization of heart failure therapy and symptom control
    - **Quality of Life**: Focus on maintaining functional capacity and patient comfort
    
    **Palliative Care Integration**:
    - **Early Consultation**: Involve palliative care specialists for symptom management and care planning
    - **Goals of Care**: Discuss treatment goals, advance directives, and care preferences
    - **Family Support**: Provide education and support resources for patients and caregivers
    - **Hospice Referral**: Consider hospice care when appropriate based on prognosis and patient preferences
    
    **SPECIAL CLINICAL CONSIDERATIONS**:
    
    **Treatment Response Monitoring**:
    - **Biomarker Changes**: Monitor for improvements in NT-proBNP with effective therapy
    - **Functional Outcomes**: Assess changes in exercise tolerance, quality of life measures
    - **Imaging Response**: Serial cardiac imaging to evaluate treatment effects
    - **Stage Migration**: Potential for patients to move between stages with effective treatment
    
    **Clinical Trial Implications**:
    - **Stratification**: Use staging for patient stratification in clinical trials
    - **Eligibility**: Different stages may have different eligibility criteria for experimental therapies
    - **Endpoint Assessment**: Staging useful for subgroup analyses and treatment effect assessment
    - **Recruitment**: Balanced enrollment across stages to ensure representative study populations
    
    **Prognostic Counseling Guidelines**:
    - **Median Survival**: Provide survival estimates while emphasizing individual variation
    - **Treatment Impact**: Discuss how disease-specific therapies may improve outcomes
    - **Trajectory**: Explain expected disease course and potential complications
    - **Hope and Realism**: Balance realistic prognostic information with hope for treatment advances
    
    **Quality Improvement Applications**:
    - **Population Health**: Track staging distribution in ATTR-CM patient populations
    - **Care Quality Metrics**: Monitor time to staging, treatment initiation rates by stage
    - **Resource Allocation**: Guide allocation of specialist care and advanced therapies
    - **Outcome Assessment**: Use staging for quality improvement initiatives and research
    
    Reference: Gillmore JD, et al. Eur Heart J. 2018;39(30):2799-2806.
    """
    
    result: str = Field(
        ...,
        description="Gillmore staging result for ATTR-CM prognosis (Stage I, Stage II, or Stage III)",
        example="Stage I"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for staging result",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with prognostic assessment and evidence-based management recommendations",
        example="Gillmore Staging: Stage I (NT-proBNP: 2500 ng/L, eGFR: 55.0 ml/min). Best prognostic category with median survival of 69.2 months. Both biomarkers within favorable ranges (NT-proBNP ≤3000 ng/L and eGFR ≥45 ml/min). Continue standard ATTR-CM management with regular monitoring. Consider for clinical trials. Optimize heart failure therapy and manage comorbidities. Monitor for disease progression with serial biomarker assessment and imaging."
    )
    
    stage: str = Field(
        ...,
        description="Gillmore stage classification (Stage I, Stage II, Stage III)",
        example="Stage I"
    )
    
    stage_description: str = Field(
        ..., 
        description="Brief description of prognostic category",
        example="Best prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Stage I",
                "unit": "stage", 
                "interpretation": "Gillmore Staging: Stage I (NT-proBNP: 2500 ng/L, eGFR: 55.0 ml/min). Best prognostic category with median survival of 69.2 months. Both biomarkers within favorable ranges (NT-proBNP ≤3000 ng/L and eGFR ≥45 ml/min). Continue standard ATTR-CM management with regular monitoring. Consider for clinical trials. Optimize heart failure therapy and manage comorbidities. Monitor for disease progression with serial biomarker assessment and imaging.",
                "stage": "Stage I", 
                "stage_description": "Best prognosis"
            }
        }