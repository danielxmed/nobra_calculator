"""
PSI/PORT Score: Pneumonia Severity Index for CAP Models

Request and response models for PSI/PORT Score calculation.

References (Vancouver style):
1. Fine MJ, Auble TE, Yealy DM, Hanusa BH, Weissfeld LA, Singer DE, et al. 
   A prediction rule to identify low-risk patients with community-acquired 
   pneumonia. N Engl J Med. 1997;336(4):243-50. doi: 10.1056/NEJM199701233360402.
2. Fine MJ, Hanusa BH, Lave JR, Singer DE, Stone RA, Weissfeld LA, et al. 
   Comparison of a disease-specific and a generic severity of illness measure 
   for patients with community-acquired pneumonia. J Gen Intern Med. 
   1995;10(7):359-68. doi: 10.1007/BF02599829.
3. Metlay JP, Waterer GW, Long AC, Anzueto A, Brozek J, Crothers K, et al. 
   Diagnosis and Treatment of Adults with Community-acquired Pneumonia. 
   An Official Clinical Practice Guideline of the American Thoracic Society 
   and Infectious Diseases Society of America. Am J Respir Crit Care Med. 
   2019;200(7):e45-e67. doi: 10.1164/rccm.201908-1581ST.
4. Aujesky D, Auble TE, Yealy DM, Stone RA, Obrosky DS, Meehan TP, et al. 
   Prospective comparison of three validated prediction rules for prognosis 
   in community-acquired pneumonia. Am J Med. 2005;118(4):384-92. 
   doi: 10.1016/j.amjmed.2005.01.006.

The PSI/PORT Score (Pneumonia Severity Index/Patient Outcomes Research Team) is the most 
extensively validated clinical prediction rule for community-acquired pneumonia (CAP) 
mortality risk assessment. Developed from a cohort of over 14,000 patients and validated 
on more than 50,000 patients, this tool guides critical decisions about hospitalization 
and care intensity for adults with CAP.

Clinical Applications:
- Risk stratification for 30-day mortality in CAP patients
- Hospitalization decision support and resource allocation
- Quality improvement initiatives and standardized care protocols
- Cost-effective triage to appropriate care settings
- Benchmark for pneumonia severity assessment in research

The PSI uses 20 clinical variables including demographics, comorbidities, physical 
examination findings, and laboratory results to calculate a point score. Patients are 
classified into five risk classes (I-V) with corresponding mortality rates and treatment 
recommendations:

Risk Classes and 30-Day Mortality:
- Class I: Young patients (<50) with no comorbidities or high-risk findings (<1% mortality)
- Class II: Score ≤70 points (<3% mortality)
- Class III: Score 71-90 points (<3% mortality)  
- Class IV: Score 91-130 points (8-9% mortality)
- Class V: Score >130 points (27-31% mortality)

Treatment Recommendations:
- Classes I-II: Outpatient treatment with oral antibiotics
- Class III: Outpatient vs. brief observation admission
- Class IV: Inpatient admission with standard monitoring
- Class V: Inpatient admission with ICU consideration

Clinical Advantages:
- Preferred over CURB-65 in 2019 ATS/IDSA guidelines
- Incorporates comprehensive clinical assessment
- Excellent discrimination for mortality prediction
- Validated across diverse patient populations
- Reduces unnecessary hospitalizations safely
- Improves quality and consistency of care decisions

The PSI has demonstrated superior performance compared to other severity scores in 
multiple validation studies and is recommended as the primary tool for CAP risk 
assessment in emergency department and outpatient settings.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class PsiPortScoreRequest(BaseModel):
    """
    Request model for PSI/PORT Score: Pneumonia Severity Index for CAP
    
    This comprehensive clinical prediction rule estimates 30-day mortality risk 
    in adults with community-acquired pneumonia using 20 clinical variables. 
    The model incorporates patient demographics, comorbidities, physical examination 
    findings, and laboratory results to guide hospitalization decisions and 
    treatment intensity.
    
    Demographics and Comorbidities:
    - Age contributes its absolute value as points (e.g., 65 years = 65 points)
    - Female sex provides protective effect (-10 points)
    - Nursing home residence indicates frailty and infection risk (+10 points)
    - Comorbidities reflect reduced physiologic reserve and immune function
    
    Physical Examination Findings:
    - Altered mental status indicates severe illness (+20 points)
    - Vital sign abnormalities reflect physiologic decompensation
    - Temperature extremes indicate severe inflammatory response
    
    Laboratory Findings:
    - Metabolic derangements indicate organ dysfunction
    - Hematologic abnormalities reflect disease severity
    - Arterial blood gas values (pH, PaO2) are optional but improve accuracy
    - Imaging findings (pleural effusion) indicate complicated pneumonia
    
    Scoring Algorithm:
    Class I: Age <50 with no comorbidities or high-risk findings (0 points)
    Classes II-V: Calculated point total determines risk stratification
    
    Clinical Usage:
    - Emergency department triage and disposition planning
    - Primary care assessment of pneumonia severity
    - Hospital admission criteria standardization
    - Quality improvement and resource utilization monitoring
    - Research stratification and outcome prediction
    
    Important Considerations:
    - Applies only to community-acquired pneumonia in adults ≥18 years
    - Not validated for hospital-acquired, healthcare-associated, or aspiration pneumonia
    - Does not apply to immunocompromised patients or those with HIV
    - May underestimate severity in young patients with severe disease
    - Should be used in conjunction with clinical judgment
    
    References: See module docstring for complete citation list.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Age contributes its absolute value as points to the total score (e.g., a 65-year-old patient receives 65 points for age alone).",
        example=65
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Female sex provides a protective effect with -10 point adjustment due to lower mortality risk in women with pneumonia.",
        example="female"
    )
    
    nursing_home_resident: Literal["yes", "no"] = Field(
        ...,
        description="Current nursing home residence status. Nursing home residents have increased mortality risk due to frailty, functional dependence, and exposure to resistant organisms (+10 points if yes).",
        example="no"
    )
    
    neoplastic_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of neoplastic disease including any active or treated cancer within the past year (excluding non-melanoma skin cancer). Indicates immunocompromised state and reduced physiologic reserve (+30 points if yes).",
        example="no"
    )
    
    liver_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of liver disease including cirrhosis, chronic hepatitis, or other chronic liver conditions. Indicates altered immune function and increased infection susceptibility (+20 points if yes).",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="History of congestive heart failure with reduced ejection fraction or clinical heart failure symptoms. Indicates reduced cardiopulmonary reserve and poor pneumonia tolerance (+10 points if yes).",
        example="no"
    )
    
    cerebrovascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of cerebrovascular disease including stroke, transient ischemic attack (TIA), or other cerebrovascular events. Associated with aspiration risk and functional impairment (+10 points if yes).",
        example="no"
    )
    
    renal_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of renal disease including chronic kidney disease, end-stage renal disease, or dialysis dependence. Indicates reduced immune function and medication clearance issues (+10 points if yes).",
        example="no"
    )
    
    altered_mental_status: Literal["yes", "no"] = Field(
        ...,
        description="Presence of altered mental status including confusion, disorientation, decreased consciousness, or change from baseline cognitive function. Indicates severe illness and poor prognosis (+20 points if yes).",
        example="no"
    )
    
    respiratory_rate: int = Field(
        ...,
        ge=5,
        le=60,
        description="Respiratory rate in breaths per minute. Tachypnea (≥30 breaths/min) indicates respiratory distress and disease severity (+20 points if ≥30).",
        example=22
    )
    
    systolic_blood_pressure: int = Field(
        ...,
        ge=50,
        le=250,
        description="Systolic blood pressure in mmHg. Hypotension (<90 mmHg) indicates hemodynamic instability and severe illness (+20 points if <90).",
        example=120
    )
    
    temperature: float = Field(
        ...,
        ge=30.0,
        le=45.0,
        description="Body temperature in degrees Celsius. Temperature extremes (<35°C or ≥40°C) indicate severe inflammatory response or hypothermic shock (+15 points for extremes).",
        example=38.5
    )
    
    pulse: int = Field(
        ...,
        ge=30,
        le=200,
        description="Heart rate in beats per minute. Tachycardia (≥125 bpm) indicates physiologic stress and compensatory response to illness (+10 points if ≥125).",
        example=88
    )
    
    ph: Optional[float] = Field(
        None,
        ge=6.5,
        le=8.0,
        description="Arterial blood gas pH (optional). Acidemia (pH <7.35) indicates severe illness with metabolic decompensation or respiratory failure (+30 points if <7.35). Improves risk stratification when available.",
        example=7.42
    )
    
    bun: float = Field(
        ...,
        ge=1.0,
        le=200.0,
        description="Blood urea nitrogen (BUN) in mg/dL. Elevated BUN (≥30 mg/dL) indicates renal dysfunction, dehydration, or hypercatabolic state (+20 points if ≥30).",
        example=15.0
    )
    
    sodium: float = Field(
        ...,
        ge=100.0,
        le=170.0,
        description="Serum sodium in mmol/L (mEq/L). Hyponatremia (<130 mmol/L) indicates SIADH, volume depletion, or severe illness (+20 points if <130).",
        example=140.0
    )
    
    glucose: float = Field(
        ...,
        ge=30.0,
        le=800.0,
        description="Serum glucose in mg/dL. Hyperglycemia (≥250 mg/dL) indicates stress response, diabetes decompensation, or steroid effects (+10 points if ≥250).",
        example=95.0
    )
    
    hematocrit: float = Field(
        ...,
        ge=10.0,
        le=70.0,
        description="Hematocrit percentage. Anemia (hematocrit <30%) indicates chronic disease, blood loss, or bone marrow suppression (+10 points if <30%).",
        example=42.0
    )
    
    pao2: Optional[float] = Field(
        None,
        ge=20.0,
        le=200.0,
        description="Partial pressure of oxygen in arterial blood (PaO2) in mmHg (optional). Hypoxemia (PaO2 <60 mmHg) indicates respiratory failure and poor gas exchange (+10 points if <60). Improves accuracy when available.",
        example=85.0
    )
    
    pleural_effusion: Literal["yes", "no"] = Field(
        ...,
        description="Presence of pleural effusion on chest X-ray or CT scan. Indicates complicated pneumonia with increased mortality risk (+10 points if yes).",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 65,
                "sex": "female",
                "nursing_home_resident": "no",
                "neoplastic_disease": "no",
                "liver_disease": "no",
                "congestive_heart_failure": "no",
                "cerebrovascular_disease": "no",
                "renal_disease": "no",
                "altered_mental_status": "no",
                "respiratory_rate": 22,
                "systolic_blood_pressure": 120,
                "temperature": 38.5,
                "pulse": 88,
                "ph": 7.42,
                "bun": 15.0,
                "sodium": 140.0,
                "glucose": 95.0,
                "hematocrit": 42.0,
                "pao2": 85.0,
                "pleural_effusion": "no"
            }
        }


class PsiPortScoreResponse(BaseModel):
    """
    Response model for PSI/PORT Score: Pneumonia Severity Index for CAP
    
    The PSI/PORT Score provides comprehensive risk stratification for adults with 
    community-acquired pneumonia, guiding critical decisions about hospitalization, 
    care intensity, and resource allocation. The scoring system has been extensively 
    validated and is recommended in major clinical guidelines.
    
    Risk Classes and Clinical Interpretation:
    
    Class I (0 points - Special Category):
    - Young patients (<50 years) with no comorbidities or high-risk findings
    - 30-day mortality: <1%
    - Recommendation: Outpatient treatment with oral antibiotics
    - Follow-up: Within 24-48 hours for clinical reassessment
    
    Class II (≤70 points):
    - Low risk for mortality and complications
    - 30-day mortality: <3%
    - Recommendation: Outpatient treatment with oral antibiotics
    - Monitoring: Close outpatient follow-up within 24-72 hours
    
    Class III (71-90 points):
    - Low risk but may benefit from brief observation
    - 30-day mortality: <3%
    - Recommendation: Outpatient vs. brief observation admission (8-24 hours)
    - Consideration: Social factors, comorbidity management, adherence concerns
    
    Class IV (91-130 points):
    - Moderate risk requiring hospitalization
    - 30-day mortality: 8-9%
    - Recommendation: Inpatient admission with standard monitoring
    - Care level: Medical ward with routine pneumonia protocols
    
    Class V (>130 points):
    - High risk requiring intensive management
    - 30-day mortality: 27-31%
    - Recommendation: Inpatient admission with ICU consideration
    - Care level: Close monitoring, aggressive treatment, early specialist consultation
    
    Clinical Implementation:
    - Use in conjunction with clinical judgment and patient preferences
    - Consider social factors, functional status, and support systems
    - Reassess risk class if clinical condition changes
    - Document rationale for decisions that deviate from score recommendations
    
    Quality Improvement Applications:
    - Benchmark for appropriate admission rates and care intensity
    - Risk adjustment for pneumonia outcome comparisons
    - Tool for reducing unnecessary hospitalizations and healthcare costs
    - Standardization of pneumonia care protocols across providers
    
    Limitations:
    - May underestimate severity in young immunocompromised patients
    - Not validated for healthcare-associated or hospital-acquired pneumonia
    - Does not capture social determinants or functional status
    - Requires clinical correlation for optimal decision-making
    
    The PSI/PORT Score represents the gold standard for pneumonia severity assessment 
    and should be used systematically in emergency departments and primary care 
    settings to optimize patient outcomes and healthcare resource utilization.
    
    Reference: See module docstring for complete citation list.
    """
    
    result: int = Field(
        ...,
        description="PSI/PORT score calculated from clinical variables. Range varies from 0 (Class I) to potentially >200 points for highest risk patients. Score determines risk class and treatment recommendations.",
        example=55
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the PSI/PORT score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation including mortality risk, disposition recommendations, care level guidance, and monitoring requirements based on the calculated PSI/PORT score and risk class.",
        example="Low risk for mortality. Outpatient treatment recommended. 30-day mortality rate <3%. Consider outpatient oral antibiotics and close follow-up."
    )
    
    stage: str = Field(
        ...,
        description="PSI/PORT risk class (Class I, Class II, Class III, Class IV, or Class V) with risk level designation (Low Risk, Moderate Risk, High Risk)",
        example="Class II (Low Risk)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the mortality risk level associated with the calculated PSI/PORT score",
        example="Low mortality risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 55,
                "unit": "points",
                "interpretation": "Low risk for mortality. Outpatient treatment recommended. 30-day mortality rate <3%. Consider outpatient oral antibiotics and close follow-up.",
                "stage": "Class II (Low Risk)",
                "stage_description": "Low mortality risk"
            }
        }