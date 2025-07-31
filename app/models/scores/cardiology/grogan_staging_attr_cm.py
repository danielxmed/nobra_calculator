"""
Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM) Models

Request and response models for Grogan Staging calculation.

References (Vancouver style):
1. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin 
   cardiac amyloidosis and risk stratification using a novel staging system. J Am 
   Coll Cardiol. 2016;68(10):1014-1020. doi: 10.1016/j.jacc.2016.06.033
2. Cappelli F, Baldasseroni S, Bergesio F, et al. Biomarker-based staging system 
   for cardiac transthyretin-related amyloidosis. Eur J Heart Fail. 2020;22(11):2187-2196. 
   doi: 10.1002/ejhf.1898
3. Maurer MS, Hanna M, Grogan M, et al. Genotype and phenotype of transthyretin 
   cardiac amyloidosis: THAOS (Transthyretin Amyloid Outcome Survey). J Am Coll 
   Cardiol. 2016;68(2):161-172. doi: 10.1016/j.jacc.2016.03.596

The Grogan Staging System is a validated prognostic tool for patients with wild-type 
transthyretin amyloid cardiomyopathy (ATTRwt-CM), developed at Mayo Clinic. This biomarker-based 
staging system uses two key cardiac biomarkers to classify patients into three prognostic 
categories, helping clinicians make informed decisions about treatment planning and prognosis.

**Clinical Background**:
Transthyretin amyloid cardiomyopathy (ATTR-CM) is an underdiagnosed and potentially fatal 
disease of the heart muscle caused by deposition of misfolded transthyretin protein. 
Wild-type ATTR-CM typically affects elderly men and has a median survival from diagnosis 
of approximately 3.5-4 years in untreated patients, but prognosis varies significantly 
based on disease stage at presentation.

**Biomarker-Based Staging System**:
The Grogan system uses two well-established cardiac biomarkers that reflect different 
aspects of cardiac involvement:

**NT-proBNP (N-terminal pro-B-type natriuretic peptide)**:
- Normal: ≤3000 pg/mL (better prognosis)
- Elevated: >3000 pg/mL (worse prognosis)
- Reflects hemodynamic stress and volume overload
- Produced by ventricular cardiomyocytes in response to wall tension

**Troponin T (cardiac troponin T)**:
- Normal: ≤0.05 ng/mL (better prognosis)
- Elevated: >0.05 ng/mL (worse prognosis)
- Reflects ongoing myocardial injury and necrosis
- Highly specific marker of cardiac muscle damage

**Three-Stage Classification System**:

**Stage I (Best Prognosis)**:
- Criteria: Both biomarkers below thresholds (NT-proBNP ≤3000 AND Troponin T ≤0.05)
- 4-year survival: 57%
- Median survival: 66 months
- Clinical approach: Early disease-modifying therapy, aggressive interventions, clinical trials

**Stage II (Intermediate Prognosis)**:
- Criteria: One biomarker above threshold
- 4-year survival: 42%
- Median survival: 42 months
- Clinical approach: Disease-modifying therapy indicated, multidisciplinary care

**Stage III (Poor Prognosis)**:
- Criteria: Both biomarkers above thresholds (NT-proBNP >3000 AND Troponin T >0.05)
- 4-year survival: 18%
- Median survival: 20 months
- Clinical approach: Urgent therapy consideration, advanced heart failure management

**Clinical Applications**:
1. **Prognosis Assessment**: Provides evidence-based survival estimates for patient counseling
2. **Treatment Planning**: Guides decisions about disease-modifying therapies (tafamidis, diflunisal)
3. **Clinical Trial Stratification**: Enables risk-stratified enrollment in research studies
4. **Goals of Care**: Facilitates discussions about treatment intensity and end-of-life planning
5. **Monitoring**: Serial biomarker assessment can track disease progression and treatment response

**Treatment Implications by Stage**:
- **Stage I**: Consider early intervention with disease-modifying therapy, appropriate for 
  aggressive treatments and clinical trial participation
- **Stage II**: Disease-modifying therapy strongly indicated, initiate heart failure 
  medications as needed
- **Stage III**: Urgent consideration of all available therapies, evaluate for advanced 
  heart failure treatments including transplantation

**Important Clinical Considerations**:
- Specifically validated for wild-type ATTR-CM (not hereditary forms)
- Should complement, not replace, comprehensive clinical assessment
- Biomarker levels may be affected by renal function, age, and comorbidities
- Regular reassessment recommended as biomarkers change with disease progression
- Multidisciplinary team approach essential for optimal management
- Early diagnosis and treatment initiation associated with better outcomes

**Validation and Evidence**:
The original Mayo Clinic study analyzed 244 patients with wild-type ATTR-CM, demonstrating 
clear prognostic discrimination between stages. Subsequent validation studies have confirmed 
the utility of this staging system across different populations and healthcare systems.

This staging system represents a significant advance in ATTR-CM management, providing 
clinicians with an objective, evidence-based tool for risk stratification and treatment 
planning in this complex disease.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class GroganStagingAttrCmRequest(BaseModel):
    """
    Request model for Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    The Grogan Staging System uses two cardiac biomarkers to classify prognosis in patients 
    with wild-type transthyretin amyloid cardiomyopathy. Both biomarkers should be obtained 
    from the same clinical assessment period for accurate staging.
    
    **NT-proBNP (N-terminal pro-B-type natriuretic peptide)**:
    - **Range**: 0-50,000 pg/mL (typical clinical range)
    - **Threshold**: 3000 pg/mL (values >3000 indicate worse prognosis)
    - **Clinical significance**: Reflects hemodynamic stress, volume overload, and ventricular 
      wall tension. Elevated levels indicate more advanced heart failure and worse prognosis.
    - **Considerations**: May be affected by age, renal function, atrial fibrillation, and 
      other cardiac conditions. Should be interpreted in clinical context.
    
    **Troponin T (cardiac troponin T)**:
    - **Range**: 0.000-5.000 ng/mL (typical clinical range)
    - **Threshold**: 0.05 ng/mL (values >0.05 indicate worse prognosis)
    - **Clinical significance**: Reflects ongoing myocardial injury and cardiomyocyte death. 
      Elevated levels indicate active cardiac damage and worse prognosis.
    - **Considerations**: Highly specific for cardiac muscle injury. May be elevated in 
      other cardiac conditions, renal disease, or acute medical illnesses.
    
    **Staging Logic**:
    - **Stage I**: Both biomarkers below thresholds (best prognosis)
    - **Stage II**: One biomarker above threshold (intermediate prognosis)
    - **Stage III**: Both biomarkers above thresholds (poor prognosis)
    
    **Sample Collection Considerations**:
    - Both biomarkers should be drawn during stable clinical conditions when possible
    - Avoid sampling during acute decompensation or intercurrent illness
    - Results should be interpreted in conjunction with clinical presentation
    - Serial measurements can help track disease progression and treatment response
    
    References (Vancouver style):
    1. Grogan M, Scott CG, Kyle RA, et al. Natural history of wild-type transthyretin 
    cardiac amyloidosis and risk stratification using a novel staging system. J Am 
    Coll Cardiol. 2016;68(10):1014-1020. doi: 10.1016/j.jacc.2016.06.033
    2. Cappelli F, Baldasseroni S, Bergesio F, et al. Biomarker-based staging system 
    for cardiac transthyretin-related amyloidosis. Eur J Heart Fail. 2020;22(11):2187-2196. 
    doi: 10.1002/ejhf.1898
    """
    
    nt_probnp: float = Field(
        ...,
        description="N-terminal pro-B-type natriuretic peptide level in pg/mL. Reflects hemodynamic stress and volume overload. Threshold: 3000 pg/mL (values >3000 pg/mL indicate worse prognosis)",
        ge=0.0,
        le=50000.0,
        example=2500.0
    )
    
    troponin_t: float = Field(
        ...,
        description="Cardiac troponin T level in ng/mL. Reflects ongoing myocardial injury and cardiomyocyte death. Threshold: 0.05 ng/mL (values >0.05 ng/mL indicate worse prognosis)",
        ge=0.000,
        le=5.000,
        example=0.035
    )
    
    @validator('nt_probnp')
    def validate_nt_probnp(cls, v):
        if v < 0:
            raise ValueError('NT-proBNP cannot be negative')
        if v > 50000:
            raise ValueError('NT-proBNP value seems unusually high (>50,000 pg/mL), please verify')
        return v
    
    @validator('troponin_t')
    def validate_troponin_t(cls, v):
        if v < 0:
            raise ValueError('Troponin T cannot be negative')
        if v > 5.0:
            raise ValueError('Troponin T value seems unusually high (>5.0 ng/mL), please verify')
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "nt_probnp": 2500.0,
                "troponin_t": 0.035
            }
        }


class GroganStagingAttrCmResponse(BaseModel):
    """
    Response model for Grogan Staging System for Transthyretin Amyloid Cardiomyopathy (ATTR-CM)
    
    Provides the calculated Grogan stage with comprehensive prognostic information and clinical 
    recommendations based on validated survival outcomes from the original Mayo Clinic study 
    and subsequent validation studies.
    
    **Stage Classifications and Clinical Implications**:
    
    **Stage I (Best Prognosis)**:
    - Criteria: NT-proBNP ≤3000 pg/mL AND Troponin T ≤0.05 ng/mL
    - 4-year survival: 57%
    - Median survival: 66 months
    - Clinical approach: Excellent prognosis with lowest cardiac biomarker burden. Consider early 
      disease-modifying therapy initiation. Patients are appropriate candidates for aggressive 
      interventions and clinical trial enrollment. Regular monitoring recommended to detect 
      disease progression before symptoms worsen.
    
    **Stage II (Intermediate Prognosis)**:
    - Criteria: One biomarker above threshold (mixed elevation pattern)
    - 4-year survival: 42%
    - Median survival: 42 months
    - Clinical approach: Intermediate prognosis with moderate cardiac biomarker elevation. 
      Disease-modifying therapy strongly indicated to slow progression. Multidisciplinary team 
      approach recommended. Consider initiation of heart failure therapies and close monitoring 
      for symptom progression.
    
    **Stage III (Poor Prognosis)**:
    - Criteria: NT-proBNP >3000 pg/mL AND Troponin T >0.05 ng/mL
    - 4-year survival: 18%
    - Median survival: 20 months
    - Clinical approach: Poor prognosis with both biomarkers elevated, indicating advanced 
      cardiac involvement. Urgent consideration of disease-modifying therapy. Aggressive heart 
      failure management required. Consider evaluation for advanced therapies including heart 
      transplantation in appropriate candidates. Focus on symptom management and quality of life.
    
    **Treatment Decision Framework**:
    - **Disease-Modifying Therapy**: Tafamidis (FDA-approved), diflunisal (off-label)
    - **Heart Failure Management**: ACE inhibitors, diuretics, rate control for atrial fibrillation
    - **Advanced Therapies**: Heart transplantation, mechanical circulatory support (selected cases)
    - **Supportive Care**: Symptom management, quality of life optimization, palliative care consultation
    
    **Monitoring and Follow-up Recommendations**:
    - **Stage I**: Every 6 months clinical assessment, annual biomarker reassessment
    - **Stage II**: Every 3-6 months clinical assessment, every 6 months biomarker reassessment
    - **Stage III**: Monthly to quarterly clinical assessment, every 3-6 months biomarker reassessment
    
    **Important Clinical Considerations**:
    - Staging should complement comprehensive clinical assessment including symptoms, imaging, and functional status
    - Biomarker levels may be affected by renal function, age, atrial fibrillation, and other comorbidities
    - Serial biomarker monitoring can track disease progression and treatment response
    - Consider multidisciplinary team involvement including cardiology, hematology, and heart failure specialists
    - Patient and family education about prognosis should be individualized and sensitive to values and preferences
    
    **Research and Clinical Trial Considerations**:
    - Staging system widely used for clinical trial stratification
    - Patients in all stages may be candidates for clinical trials of novel therapies
    - Consider enrollment in ATTR-CM registries for long-term outcome tracking
    
    Reference: Grogan M, et al. J Am Coll Cardiol. 2016;68(10):1014-1020.
    """
    
    result: str = Field(
        ...,
        description="Grogan stage classification (Stage I, Stage II, or Stage III)",
        pattern="^Stage (I|II|III)$",
        example="Stage I"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the staging result",
        example="stage"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including biomarker levels, threshold comparisons, stage classification, survival estimates, and specific clinical recommendations with important considerations for ATTR-CM management",
        example="Biomarker levels: NT-proBNP 2,500 pg/mL, Troponin T 0.035 ng/mL. NT-proBNP is normal (threshold: 3,000 pg/mL), Troponin T is normal (threshold: 0.050 ng/mL). Grogan Classification: Stage I (Best prognosis). Four-year survival: 57%. Median survival: 66 months. Clinical implications: Excellent prognosis with lowest cardiac biomarker burden. Consider early disease-modifying therapy. Appropriate for aggressive interventions and clinical trial enrollment. Regular monitoring recommended to detect disease progression. Important considerations: This staging system is specifically validated for wild-type transthyretin amyloid cardiomyopathy (ATTRwt-CM). Should be used in conjunction with clinical assessment, imaging findings, and tissue diagnosis. Regular reassessment recommended as biomarkers may change with disease progression or treatment response. Consider multidisciplinary team approach for optimal management."
    )
    
    stage: str = Field(
        ...,
        description="Stage classification (Stage I, Stage II, Stage III)",
        example="Stage I"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the prognostic category",
        example="Best prognosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Stage I",
                "unit": "stage",
                "interpretation": "Biomarker levels: NT-proBNP 2,500 pg/mL, Troponin T 0.035 ng/mL. NT-proBNP is normal (threshold: 3,000 pg/mL), Troponin T is normal (threshold: 0.050 ng/mL). Grogan Classification: Stage I (Best prognosis). Four-year survival: 57%. Median survival: 66 months. Clinical implications: Excellent prognosis with lowest cardiac biomarker burden. Consider early disease-modifying therapy. Appropriate for aggressive interventions and clinical trial enrollment. Regular monitoring recommended to detect disease progression. Important considerations: This staging system is specifically validated for wild-type transthyretin amyloid cardiomyopathy (ATTRwt-CM). Should be used in conjunction with clinical assessment, imaging findings, and tissue diagnosis. Regular reassessment recommended as biomarkers may change with disease progression or treatment response. Consider multidisciplinary team approach for optimal management.",
                "stage": "Stage I",
                "stage_description": "Best prognosis"
            }
        }