"""
Common Terminology Criteria for Adverse Events (CTCAE) v5.0 Models

Request and response models for CTCAE hematologic adverse event grading calculation.

References (Vancouver style):
1. National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0. 
   Published: November 27, 2017. U.S. Department of Health and Human Services, National Institutes 
   of Health, National Cancer Institute.
2. Freites-Martinez A, Santana N, Arias-Santiago S, Viera A. Using the Common Terminology Criteria 
   for Adverse Events (CTCAE - Version 5.0) to Evaluate the Severity of Adverse Events of Anticancer 
   Therapies. Actas Dermosifiliogr (Engl Ed). 2021 Feb;112(2):90-92. doi: 10.1016/j.ad.2019.05.009.
3. Basch E, Reeve BB, Mitchell SA, et al. Development of the National Cancer Institute's patient-reported 
   outcomes version of the common terminology criteria for adverse events (PRO-CTCAE). J Natl Cancer Inst. 
   2014;106(9):dju244. doi: 10.1093/jnci/dju244.

The CTCAE v5.0 is the standard terminology used by the oncology community to report 
adverse events in a clear, precise, and reproducible manner. It provides standardized 
grading criteria for adverse events from cancer treatment, facilitating consistent 
reporting across clinical trials and enabling meaningful comparisons between studies.

Clinical Background:

Development and Purpose:
The CTCAE was developed by the National Cancer Institute (NCI) to provide a comprehensive, 
standardized system for adverse event reporting in cancer clinical trials. The system 
enables consistent grading of adverse events across different institutions, studies, 
and treatment modalities, supporting evidence-based medicine and regulatory decision-making.

Grading Philosophy:
The CTCAE uses a 5-point scale (Grades 1-5) that reflects the severity of adverse events:
- Grade 1: Mild; asymptomatic or mild symptoms; clinical or diagnostic observations only
- Grade 2: Moderate; minimal, local, or noninvasive intervention indicated
- Grade 3: Severe; medically significant but not immediately life-threatening
- Grade 4: Life-threatening consequences; urgent intervention indicated  
- Grade 5: Death related to adverse event

Hematologic Adverse Events Focus:
This implementation focuses on common hematologic and lymphatic system disorders that 
are frequently encountered in cancer treatment, including:

Anemia:
- Most common hematologic toxicity in cancer patients
- Graded based on hemoglobin levels with sex-specific normal ranges
- Grade 3 may indicate need for transfusion support
- Can significantly impact quality of life and treatment tolerance

Neutropenia:
- Critical toxicity affecting infection risk
- Graded based on absolute neutrophil count (ANC)
- Grade 3-4 neutropenia requires intensive monitoring and prophylaxis
- Major dose-limiting toxicity for many chemotherapy regimens

Thrombocytopenia:
- Important bleeding risk factor in cancer patients
- Graded based on platelet count levels
- Grade 3-4 may require platelet transfusion and bleeding precautions
- Can limit ability to continue treatment or perform procedures

Febrile Neutropenia:
- Medical emergency requiring immediate intervention
- Defined by combination of neutropenia (ANC <1000) and fever (>38.3°C)
- Always graded as Grade 3 regardless of other factors
- Associated with significant morbidity and mortality risk

Leukocytosis:
- Elevated white blood cell count
- May indicate infection, inflammation, or hematologic malignancy
- Graded based on total WBC count elevation above normal
- Can affect treatment decisions and require further evaluation

Lymphopenia:
- Decreased lymphocyte count affecting immune function
- Common with certain chemotherapy regimens and radiation
- Graded based on absolute lymphocyte count
- May increase infection risk and affect vaccine responses

Clinical Implementation Considerations:

Laboratory Considerations:
- Reference ranges may vary between laboratories
- Consider institutional normal values when available
- Account for patient's baseline values and comorbidities
- Timing of laboratory assessment relative to treatment is important

Clinical Context:
- CTCAE grades should be interpreted within clinical context
- Patient symptoms and functional status inform management decisions
- Causality assessment may influence treatment modifications
- Baseline medical conditions can affect grade interpretation

Treatment Implications:
- Grade 1-2: Generally manageable with supportive care
- Grade 3: Often requires treatment delays or dose modifications
- Grade 4: May necessitate treatment discontinuation
- Consistent grading supports evidence-based treatment algorithms

Quality Assurance:
- Training on CTCAE criteria improves inter-rater reliability
- Regular calibration exercises maintain grading consistency
- Documentation should include relevant clinical details
- Version control is important as CTCAE criteria evolve

Research Applications:
- Standardized reporting enables meta-analyses and systematic reviews
- Facilitates comparison between different treatment regimens
- Supports regulatory submissions and drug approvals
- Enables development of predictive models for toxicity risk

Patient Safety:
- Systematic adverse event monitoring improves patient outcomes
- Early recognition of severe toxicities prevents complications
- Standardized grading supports clinical decision-making
- Facilitates communication between healthcare providers

This calculator provides automated CTCAE v5.0 grading for common hematologic adverse 
events, supporting clinical decision-making, research, and quality improvement initiatives 
in oncology care.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List, Union
from enum import Enum


class AdverseEventType(str, Enum):
    """Enumeration of supported hematologic adverse event types"""
    ANEMIA = "anemia"
    NEUTROPENIA = "neutropenia"
    THROMBOCYTOPENIA = "thrombocytopenia"
    FEBRILE_NEUTROPENIA = "febrile_neutropenia"
    LEUKOCYTOSIS = "leukocytosis"
    LYMPHOPENIA = "lymphopenia"


class PatientSex(str, Enum):
    """Enumeration of patient biological sex options"""
    MALE = "male"
    FEMALE = "female"


class TransfusionIndication(str, Enum):
    """Enumeration of transfusion indication options"""
    YES = "yes"
    NO = "no"


class CtcaeRequest(BaseModel):
    """
    Request model for Common Terminology Criteria for Adverse Events (CTCAE) v5.0
    
    The CTCAE v5.0 provides standardized terminology and grading criteria for adverse 
    events in cancer clinical trials and clinical practice. This calculator focuses 
    on hematologic and lymphatic adverse events commonly encountered in cancer treatment.
    
    Supported Adverse Event Types:
    
    Anemia:
    - Definition: Decreased red blood cell count or hemoglobin level
    - Parameter Required: hemoglobin (g/dL)
    - Normal Ranges: Male 14.0-18.0 g/dL, Female 12.0-16.0 g/dL
    - Grading Criteria:
      * Grade 1: Hemoglobin <LLN-10.0 g/dL (Male <13.9, Female <11.9 g/dL)
      * Grade 2: Hemoglobin <10.0-8.0 g/dL
      * Grade 3: Hemoglobin <8.0 g/dL; transfusion indicated
      * Grade 4: Life-threatening consequences; urgent intervention indicated
    - Clinical Significance: Most common cancer treatment toxicity; affects quality of life
    
    Neutropenia:
    - Definition: Decreased neutrophil count increasing infection risk
    - Parameter Required: neutrophil_count (cells/mm³ or x10⁹/L)
    - Normal Range: 1,500-8,000 cells/mm³
    - Grading Criteria:
      * Grade 1: ANC <LLN-1,500 cells/mm³ (<1.5 x10⁹/L)
      * Grade 2: ANC <1,500-1,000 cells/mm³ (<1.5-1.0 x10⁹/L)
      * Grade 3: ANC <1,000-500 cells/mm³ (<1.0-0.5 x10⁹/L)
      * Grade 4: ANC <500 cells/mm³ (<0.5 x10⁹/L)
    - Clinical Significance: Major dose-limiting toxicity; requires infection precautions
    
    Thrombocytopenia:
    - Definition: Decreased platelet count increasing bleeding risk
    - Parameter Required: platelet_count (cells/mm³ or x10⁹/L)
    - Normal Range: 150,000-450,000 cells/mm³
    - Grading Criteria:
      * Grade 1: Platelets <LLN-75,000 cells/mm³ (<LLN-75 x10⁹/L)
      * Grade 2: Platelets <75,000-50,000 cells/mm³ (<75-50 x10⁹/L)
      * Grade 3: Platelets <50,000-25,000 cells/mm³ (<50-25 x10⁹/L)
      * Grade 4: Platelets <25,000 cells/mm³ (<25 x10⁹/L)
    - Clinical Significance: Bleeding risk; may require transfusion and procedure delays
    
    Febrile Neutropenia:
    - Definition: Combination of neutropenia and fever indicating possible infection
    - Parameters Required: neutrophil_count (cells/mm³) and temperature (°C)
    - Diagnostic Criteria: ANC <1,000 cells/mm³ AND temperature >38.3°C (or ≥38°C sustained >1 hour)
    - Grading: Always Grade 3 when criteria are met
    - Clinical Significance: Medical emergency requiring immediate broad-spectrum antibiotics
    
    Leukocytosis:
    - Definition: Elevated white blood cell count
    - Parameter Required: wbc_count (cells/mm³)
    - Normal Range: 4,000-11,000 cells/mm³
    - Grading Criteria:
      * Grade 1: WBC >ULN-20,000 cells/mm³
      * Grade 2: WBC >20,000-50,000 cells/mm³
      * Grade 3: WBC >50,000-100,000 cells/mm³
      * Grade 4: WBC >100,000 cells/mm³
    - Clinical Significance: May indicate infection, inflammation, or hematologic disorders
    
    Lymphopenia:
    - Definition: Decreased lymphocyte count affecting immune function
    - Parameter Required: lymphocyte_count (cells/mm³)
    - Normal Range: 1,000-4,000 cells/mm³
    - Grading Criteria:
      * Grade 1: Lymphocytes <LLN-800 cells/mm³
      * Grade 2: Lymphocytes <800-500 cells/mm³
      * Grade 3: Lymphocytes <500-200 cells/mm³
      * Grade 4: Lymphocytes <200 cells/mm³
    - Clinical Significance: Increased infection risk; may affect vaccine responses
    
    Laboratory Considerations:
    
    Units and Conversions:
    - Cell counts can be entered in cells/mm³ or x10⁹/L (equivalent values)
    - Hemoglobin should be entered in g/dL
    - Temperature should be entered in Celsius
    - Consider laboratory-specific reference ranges when available
    
    Timing and Context:
    - Laboratory values should reflect nadir (lowest) counts when applicable
    - Consider baseline values and patient comorbidities
    - Account for hydration status and other confounding factors
    - Document timing relative to treatment administration
    
    Clinical Implementation:
    
    Assessment Requirements:
    - Complete blood count with differential for most evaluations
    - Vital signs including temperature for febrile neutropenia assessment
    - Clinical evaluation for symptoms and functional impact
    - Review of concurrent medications and comorbidities
    
    Quality Assurance:
    - Use standardized laboratory reference ranges
    - Document assessment timing and clinical context
    - Consider inter-laboratory variability for critical values
    - Ensure staff training on CTCAE criteria and grading principles
    
    Treatment Integration:
    - CTCAE grades inform dose modification algorithms
    - Grade 3-4 toxicities often require treatment delays or reductions
    - Standardized grading supports clinical trial eligibility and safety monitoring
    - Facilitates communication between healthcare providers and across institutions
    
    References (Vancouver style):
    1. National Cancer Institute. Common Terminology Criteria for Adverse Events (CTCAE) Version 5.0. 
    Published: November 27, 2017. U.S. Department of Health and Human Services, National Institutes 
    of Health, National Cancer Institute.
    2. Freites-Martinez A, Santana N, Arias-Santiago S, Viera A. Using the Common Terminology Criteria 
    for Adverse Events (CTCAE - Version 5.0) to Evaluate the Severity of Adverse Events of Anticancer 
    Therapies. Actas Dermosifiliogr (Engl Ed). 2021 Feb;112(2):90-92.
    """
    
    adverse_event_type: AdverseEventType = Field(
        ...,
        description="Type of hematologic adverse event to grade according to CTCAE v5.0 criteria",
        example="anemia"
    )
    
    patient_sex: PatientSex = Field(
        ...,
        description="Patient biological sex for determining appropriate normal reference ranges. Required for anemia grading due to sex-specific hemoglobin normal values",
        example="female"
    )
    
    hemoglobin: Optional[float] = Field(
        None,
        ge=0.0,
        le=25.0,
        description="Hemoglobin level in g/dL. Required for anemia grading. Normal ranges: Male 14.0-18.0 g/dL, Female 12.0-16.0 g/dL",
        example=9.5
    )
    
    neutrophil_count: Optional[float] = Field(
        None,
        ge=0.0,
        le=50000.0,
        description="Absolute neutrophil count (ANC) in cells/mm³. Required for neutropenia and febrile neutropenia grading. Normal range: 1,500-8,000 cells/mm³",
        example=800
    )
    
    platelet_count: Optional[float] = Field(
        None,
        ge=0.0,
        le=2000000.0,
        description="Platelet count in cells/mm³. Required for thrombocytopenia grading. Normal range: 150,000-450,000 cells/mm³",
        example=45000
    )
    
    wbc_count: Optional[float] = Field(
        None,
        ge=0.0,
        le=500000.0,
        description="White blood cell (WBC) count in cells/mm³. Required for leukocytosis grading. Normal range: 4,000-11,000 cells/mm³",
        example=25000
    )
    
    lymphocyte_count: Optional[float] = Field(
        None,
        ge=0.0,
        le=50000.0,
        description="Absolute lymphocyte count in cells/mm³. Required for lymphopenia grading. Normal range: 1,000-4,000 cells/mm³",
        example=450
    )
    
    temperature: Optional[float] = Field(
        None,
        ge=30.0,
        le=45.0,
        description="Body temperature in Celsius. Required for febrile neutropenia grading. Fever criteria: >38.3°C or sustained ≥38.0°C for >1 hour",
        example=38.8
    )
    
    transfusion_indicated: Optional[TransfusionIndication] = Field(
        None,
        description="Clinical indication for transfusion. Helps determine anemia Grade 3 when hemoglobin is in borderline range and clinical judgment supports transfusion need",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "adverse_event_type": "anemia",
                "patient_sex": "female",
                "hemoglobin": 9.5,
                "neutrophil_count": None,
                "platelet_count": None,
                "wbc_count": None,
                "lymphocyte_count": None,
                "temperature": None,
                "transfusion_indicated": "no"
            }
        }


class ClinicalDetails(BaseModel):
    """Clinical details and recommendations for CTCAE assessment"""
    
    adverse_event_type: str = Field(
        ...,
        description="Type of adverse event assessed",
        example="Anemia"
    )
    
    primary_value: Optional[Any] = Field(
        None,
        description="Primary laboratory value used for grading (may be single value or composite for complex assessments)",
        example=9.5
    )
    
    value_unit: str = Field(
        ...,
        description="Unit of measurement for the primary value",
        example="g/dL"
    )
    
    grade_description: str = Field(
        ...,
        description="Description of the CTCAE grade level",
        example="Moderate adverse event"
    )
    
    clinical_significance: str = Field(
        ...,
        description="Clinical significance and intervention requirements for this grade",
        example="Minimal intervention indicated; may limit age-appropriate activities of daily living"
    )
    
    monitoring_requirements: List[str] = Field(
        ...,
        description="Recommended monitoring strategies for this grade level",
        example=["More frequent laboratory monitoring recommended", "Clinical assessment for symptoms and functional impact"]
    )
    
    intervention_considerations: List[str] = Field(
        ...,
        description="Recommended interventions for this grade level",
        example=["Supportive care measures as appropriate", "Consider prophylactic interventions if indicated"]
    )
    
    dose_modification_guidance: List[str] = Field(
        ...,
        description="Guidance for treatment dose modifications based on this grade",
        example=["Consider dose delay until improvement to Grade 1 or baseline", "May require dose reduction per protocol guidelines"]
    )


class CtcaeResponse(BaseModel):
    """
    Response model for Common Terminology Criteria for Adverse Events (CTCAE) v5.0
    
    Provides comprehensive CTCAE grading results with clinical interpretation, evidence-based 
    recommendations, and detailed guidance for clinical decision-making in oncology care.
    
    CTCAE v5.0 Grading Framework:
    
    Grade Definitions and Clinical Implications:
    
    Grade 0 (Within Normal Limits):
    - No adverse event detected
    - Laboratory values within normal reference ranges
    - No intervention required; continue routine monitoring
    - Baseline status for comparison with future assessments
    
    Grade 1 (Mild Adverse Event):
    - Asymptomatic or mild symptoms
    - Clinical or diagnostic observations only
    - Intervention not indicated
    - Patient education and monitoring recommended
    - Generally no dose modifications required
    
    Grade 2 (Moderate Adverse Event):
    - Minimal, local, or noninvasive intervention indicated
    - May limit age-appropriate instrumental activities of daily living
    - Supportive care measures appropriate
    - Consider dose delays or modifications per protocol
    - Increased monitoring frequency recommended
    
    Grade 3 (Severe Adverse Event):
    - Severe or medically significant but not immediately life-threatening
    - Hospitalization or prolongation of hospitalization may be indicated
    - Disabling; limiting self-care activities of daily living
    - Active medical management required
    - Treatment delays and dose reductions typically necessary
    
    Grade 4 (Life-Threatening Adverse Event):
    - Life-threatening consequences
    - Urgent intervention indicated
    - Intensive monitoring and supportive care required
    - Treatment discontinuation often necessary
    - Risk-benefit assessment for future therapy
    
    Grade 5 (Death):
    - Death related to adverse event
    - Requires comprehensive investigation and reporting
    - Informs future treatment protocols and safety measures
    
    Hematologic-Specific Interpretations:
    
    Anemia Management Considerations:
    - Grade 1-2: Iron supplementation, nutritional support, monitoring
    - Grade 3: Transfusion consideration, erythropoiesis-stimulating agents
    - Grade 4: Urgent transfusion, comprehensive hematologic evaluation
    - Consider underlying causes: bleeding, hemolysis, bone marrow suppression
    
    Neutropenia Management Protocol:
    - Grade 1-2: Monitor for infection signs, patient education
    - Grade 3: Infection precautions, consider growth factor support
    - Grade 4: Strict isolation, prophylactic antibiotics, G-CSF support
    - All grades: Avoid live vaccines, crowd exposure, invasive procedures
    
    Thrombocytopenia Management Strategy:
    - Grade 1-2: Bleeding precautions, avoid anticoagulants
    - Grade 3: Platelet transfusion consideration, procedure restrictions
    - Grade 4: Active bleeding management, urgent transfusion
    - Monitor for spontaneous bleeding, CNS symptoms
    
    Febrile Neutropenia Emergency Protocol:
    - Always Grade 3: Medical emergency requiring immediate intervention
    - Broad-spectrum antibiotics within 1 hour of recognition
    - Blood cultures before antibiotic administration
    - Daily reassessment and culture monitoring
    - G-CSF support consideration per institutional guidelines
    
    Clinical Decision Support:
    
    Treatment Modification Guidelines:
    - Grade 0-1: Continue treatment as planned with routine monitoring
    - Grade 2: Consider dose delays; monitor closely for progression
    - Grade 3: Hold treatment until improvement; dose reduction upon resumption
    - Grade 4: Discontinue treatment; consider alternative regimens
    
    Monitoring Recommendations:
    - Grade 0-1: Standard protocol monitoring intervals
    - Grade 2: Increase monitoring frequency (typically weekly)
    - Grade 3-4: Daily to twice-weekly monitoring until improvement
    - Document trends and response to interventions
    
    Patient Safety Considerations:
    - Educate patients on signs and symptoms to report immediately
    - Provide 24-hour contact information for urgent concerns
    - Coordinate care with primary oncology team and supportive services
    - Document all interventions and patient responses
    
    Quality Assurance Framework:
    
    Documentation Standards:
    - Record exact laboratory values and reference ranges used
    - Document clinical context and contributing factors
    - Note timing relative to treatment administration
    - Include relevant patient symptoms and functional status
    
    Inter-professional Communication:
    - Use standardized CTCAE terminology in all communications
    - Provide grade rationale when borderline or complex cases
    - Coordinate with pharmacy for dose modification implementation
    - Inform all team members of significant grade changes
    
    Research and Regulatory Considerations:
    
    Clinical Trial Integration:
    - CTCAE grades inform protocol-specified dose modifications
    - Standardized reporting enables cross-study comparisons
    - Facilitates regulatory review and drug approval processes
    - Supports development of predictive toxicity models
    
    Quality Improvement Applications:
    - Monitor institutional toxicity rates by treatment and grade
    - Identify opportunities for supportive care interventions
    - Track time to toxicity recognition and intervention
    - Benchmark against published standards and peer institutions
    
    Reference: National Cancer Institute. CTCAE v5.0. Published November 27, 2017.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=5,
        description="CTCAE severity grade (0-5) for the specified hematologic adverse event",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CTCAE assessment",
        example="grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the CTCAE grade with specific laboratory values and evidence-based recommendations",
        example="Grade 2 Anemia detected with 9.5 g/dL. Minimal intervention indicated; may limit age-appropriate activities of daily living."
    )
    
    stage: str = Field(
        ...,
        description="CTCAE grade classification (Grade 0-5)",
        example="Grade 2"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the CTCAE grade severity level",
        example="Moderate adverse event"
    )
    
    clinical_details: ClinicalDetails = Field(
        ...,
        description="Comprehensive clinical details including monitoring requirements, intervention considerations, and dose modification guidance"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "grade",
                "interpretation": "Grade 2 Anemia detected with 9.5 g/dL. Minimal intervention indicated; may limit age-appropriate activities of daily living.",
                "stage": "Grade 2",
                "stage_description": "Moderate adverse event",
                "clinical_details": {
                    "adverse_event_type": "Anemia",
                    "primary_value": 9.5,
                    "value_unit": "g/dL",
                    "grade_description": "Moderate adverse event",
                    "clinical_significance": "Minimal intervention indicated; may limit age-appropriate activities of daily living",
                    "monitoring_requirements": [
                        "More frequent laboratory monitoring recommended",
                        "Clinical assessment for symptoms and functional impact"
                    ],
                    "intervention_considerations": [
                        "Supportive care measures as appropriate",
                        "Consider prophylactic interventions if indicated"
                    ],
                    "dose_modification_guidance": [
                        "Consider dose delay until improvement to Grade 1 or baseline",
                        "May require dose reduction per protocol guidelines"
                    ]
                }
            }
        }