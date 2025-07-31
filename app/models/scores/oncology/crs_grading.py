"""
Cytokine Release Syndrome (CRS) Grading Models

Request and response models for CRS grading calculation.

References (Vancouver style):
1. Lee DW, Santomasso BD, Locke FL, et al. ASTCT Consensus Grading for Cytokine Release 
   Syndrome and Neurologic Toxicity Associated with Immune Effector Cells. Biol Blood 
   Marrow Transplant. 2019;25(4):625-638. doi: 10.1016/j.bbmt.2018.12.758.
2. Porter D, Frey N, Wood PA, Weng Y, Grupp SA. Grading of cytokine release syndrome 
   associated with the CAR T cell therapy tisagenlecleucel. J Hematol Oncol. 2018;11(1):35. 
   doi: 10.1186/s13045-018-0571-y.
3. Neelapu SS, Tummala S, Kebriaei P, et al. Chimeric antigen receptor T-cell therapy - 
   assessment and management of toxicities. Nat Rev Clin Oncol. 2018;15(1):47-62. 
   doi: 10.1038/nrclinonc.2017.148.
4. Maude SL, Barrett D, Teachey DT, Grupp SA. Managing cytokine release syndrome 
   associated with novel T cell-engaging therapies. Cancer J. 2014;20(2):119-122. 
   doi: 10.1097/PPO.0000000000000035.

Cytokine Release Syndrome (CRS) is an acute inflammatory process characterized by 
systemic inflammation and a spectrum of clinical symptoms ranging from mild constitutional 
symptoms to life-threatening organ dysfunction. CRS is most commonly associated with 
immune effector cell therapies, particularly CAR-T cell therapy, but can also occur 
with other immunotherapies such as TCR-T cells, bispecific antibodies, and checkpoint 
inhibitors.

The ASTCT consensus grading system provides standardized criteria for CRS assessment 
across institutions and clinical trials, enabling consistent patient management and 
research comparisons. This grading system is essential for guiding treatment decisions, 
determining appropriate care settings, and monitoring therapeutic interventions.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional, List, Dict


class CrsGradingRequest(BaseModel):
    """
    Request model for Cytokine Release Syndrome (CRS) Grading
    
    The ASTCT consensus grading system for CRS uses clinical parameters to assign 
    severity grades from 1-5, guiding treatment decisions and care setting determination.
    
    Clinical Parameters Assessment:
    
    **Fever Assessment:**
    - fever_present: Presence of fever ≥38°C (100.4°F) or fever suppressed by 
      anti-pyretic or anti-cytokine therapy. Fever is required for Grade 1 CRS 
      but not required for Grades 2-4 if actively suppressed by treatment.
    
    **Hypotension Categories:**
    - none: No hypotension, normal blood pressure for patient
    - responsive_to_fluids: Hypotension that responds to IV fluid resuscitation
    - low_dose_single_pressor: Requires low-dose single vasopressor support
    - high_dose_multiple_pressors: Requires high-dose or multiple vasopressor support
    
    **Oxygen Requirements:**
    - none: No supplemental oxygen required, normal oxygen saturation
    - low_flow_oxygen: Low-flow nasal cannula oxygen (<40% FiO2 or <6L/min)
    - high_flow_oxygen_40_plus: High-flow oxygen ≥40% FiO2 or high-flow nasal cannula
    - ventilator_required: Requires positive pressure ventilation (invasive or non-invasive)
    
    **Organ Toxicity Grading:**
    Uses Common Terminology Criteria for Adverse Events (CTCAE) v5.0 grading:
    - 0: No organ toxicity or dysfunction
    - 1: Mild organ toxicity, minimal intervention required
    - 2: Moderate organ toxicity, medical intervention indicated
    - 3: Severe organ toxicity, hospitalization indicated
    - 4: Life-threatening organ toxicity, urgent intervention required
    
    Note: Grade 4 transaminitis (liver toxicity) is considered Grade 3 CRS per ASTCT criteria
    
    **Risk Factors:**
    - patient_age: Age influences CRS severity and management approach
    - comorbidities_present: Significant comorbidities affect treatment tolerance and monitoring needs
    
    **Grading Algorithm:**
    CRS grade is determined by the highest severity parameter among hypotension, 
    oxygen requirements, and organ toxicity. Grade 1 requires fever (unless suppressed) 
    with minimal other symptoms. Grades 2-4 are determined by severity of organ support 
    needs and systemic manifestations.
    
    References (Vancouver style):
    1. Lee DW, Santomasso BD, Locke FL, et al. ASTCT Consensus Grading for Cytokine Release 
    Syndrome and Neurologic Toxicity Associated with Immune Effector Cells. Biol Blood 
    Marrow Transplant. 2019;25(4):625-638. doi: 10.1016/j.bbmt.2018.12.758.
    2. Porter D, Frey N, Wood PA, Weng Y, Grupp SA. Grading of cytokine release syndrome 
    associated with the CAR T cell therapy tisagenlecleucel. J Hematol Oncol. 2018;11(1):35. 
    doi: 10.1186/s13045-018-0571-y.
    """
    
    fever_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of fever ≥38°C (100.4°F) or fever suppressed by anti-pyretic/anti-cytokine therapy. Required for Grade 1, not required for Grades 2-4 if actively suppressed",
        example="yes"
    )
    
    hypotension_status: Literal["none", "responsive_to_fluids", "low_dose_single_pressor", "high_dose_multiple_pressors"] = Field(
        ...,
        description="Hypotension severity and intervention requirements. Ranges from no hypotension to requiring high-dose/multiple vasopressor support",
        example="none"
    )
    
    oxygen_requirement: Literal["none", "low_flow_oxygen", "high_flow_oxygen_40_plus", "ventilator_required"] = Field(
        ...,
        description="Oxygen support requirements. Ranges from room air to mechanical ventilation. High-flow oxygen is ≥40% FiO2 or high-flow nasal cannula",
        example="none"
    )
    
    organ_toxicity_grade: int = Field(
        ...,
        ge=0,
        le=4,
        description="Highest grade of organ toxicity using CTCAE criteria (0-4), excluding fever and hypotension. Grade 4 transaminitis counts as Grade 3 CRS",
        example=0
    )
    
    patient_age: Optional[int] = Field(
        None,
        ge=0,
        le=120,
        description="Patient age in years for risk stratification and management considerations. Pediatric and elderly patients may require modified monitoring approaches",
        example=45
    )
    
    comorbidities_present: Optional[Literal["yes", "no", "unknown"]] = Field(
        None,
        description="Presence of significant comorbidities that may affect CRS management, treatment tolerance, or monitoring requirements",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "fever_present": "yes",
                "hypotension_status": "none",
                "oxygen_requirement": "none",
                "organ_toxicity_grade": 0,
                "patient_age": 45,
                "comorbidities_present": "no"
            }
        }


class CrsGradingResponse(BaseModel):
    """
    Response model for Cytokine Release Syndrome (CRS) Grading
    
    Provides comprehensive CRS assessment with ASTCT consensus grading, severity 
    classification, clinical interpretation, and evidence-based management recommendations.
    
    **CRS Grading Scale (ASTCT 2019):**
    
    **Grade 1 - Mild:**
    - Symptoms not life-threatening
    - Only symptomatic treatment required
    - Examples: fever, nausea, fatigue, headache, myalgias, malaise
    - Care setting: Inpatient ward with oncology monitoring
    
    **Grade 2 - Moderate:**
    - Moderate intervention required
    - Oxygen requirement <40%, hypotension responsive to fluids, or Grade 2 organ toxicity
    - Care setting: Inpatient ward with enhanced monitoring or step-down unit
    
    **Grade 3 - Severe:**
    - Aggressive intervention required
    - Oxygen requirement ≥40%, high-dose/multiple pressors, or Grade 3 organ toxicity
    - Care setting: Intensive care unit (ICU)
    
    **Grade 4 - Life-threatening:**
    - Life-threatening symptoms requiring immediate intervention
    - Ventilator requirement or Grade 4 organ toxicity (excluding transaminitis)
    - Care setting: ICU with advanced life support
    
    **Grade 5 - Death:**
    - Death directly attributable to CRS
    - Care setting: Comfort care
    
    **Management Principles:**
    - Early recognition and prompt intervention are critical
    - Treatment should be individualized based on patient factors
    - Monitor for infection risk with immunosuppressive treatments
    - Multidisciplinary approach recommended for severe cases
    
    Reference: Lee DW, et al. Biol Blood Marrow Transplant. 2019;25(4):625-638.
    """
    
    result: int = Field(
        ...,
        ge=1,
        le=5,
        description="CRS grade according to ASTCT consensus criteria (1-5)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CRS grade",
        example="CRS grade"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation of CRS grade with management guidance and prognosis",
        example="CRS Grade 1 (Grade 1 - Mild) indicates mild symptoms. Patient has mild constitutional symptoms requiring only symptomatic treatment. Prognosis is excellent with supportive care."
    )
    
    stage: str = Field(
        ...,
        description="CRS severity classification (Grade 1-5 with descriptive label)",
        example="Grade 1 - Mild"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the CRS grade characteristics",
        example="Mild symptoms"
    )
    
    crs_grade: int = Field(
        ...,
        description="Numeric CRS grade (1-5) for clinical documentation",
        example=1
    )
    
    severity_level: str = Field(
        ...,
        description="Severity classification (mild, moderate, severe, life_threatening, fatal)",
        example="mild"
    )
    
    intervention_type: str = Field(
        ...,
        description="Type of intervention required (symptomatic, supportive, aggressive, intensive, none)",
        example="symptomatic"
    )
    
    clinical_assessment: Dict = Field(
        ...,
        description="Detailed clinical assessment including severity indicators, risk factors, and clinical features",
        example={
            "crs_grade": 1,
            "severity_indicators": [],
            "risk_factors": [],
            "clinical_features": ["Fever", "Constitutional symptoms", "Mild discomfort"]
        }
    )
    
    management_recommendations: Dict = Field(
        ...,
        description="Comprehensive management recommendations including primary interventions, medications, and monitoring",
        example={
            "primary_interventions": [
                "Supportive care with symptomatic treatment",
                "Monitor vital signs and symptoms closely",
                "Adequate hydration and fever management",
                "No specific anti-cytokine therapy required"
            ],
            "additional_considerations": [],
            "medication_options": ["Acetaminophen/paracetamol for fever", "Adequate hydration", "Symptomatic care"],
            "monitoring_frequency": "Every 4-8 hours"
        }
    )
    
    monitoring_requirements: Dict = Field(
        ...,
        description="Specific monitoring parameters, frequency, and laboratory studies required",
        example={
            "parameters": ["Vital signs", "Temperature", "Oxygen saturation", "Mental status"],
            "frequency": "Every 4-8 hours",
            "laboratory_studies": ["Basic metabolic panel", "Complete blood count"]
        }
    )
    
    treatment_urgency: str = Field(
        ...,
        description="Treatment urgency level based on CRS grade",
        example="Routine - symptomatic care"
    )
    
    prognosis: Dict = Field(
        ...,
        description="Prognosis assessment with outlook and description",
        example={
            "outlook": "Excellent",
            "description": "Expected full recovery with supportive care"
        }
    )
    
    care_setting: str = Field(
        ...,
        description="Recommended care setting based on CRS grade and clinical needs",
        example="Inpatient ward with oncology monitoring"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "CRS grade",
                "interpretation": "CRS Grade 1 (Grade 1 - Mild) indicates mild symptoms. Patient has mild constitutional symptoms requiring only symptomatic treatment. Prognosis is excellent with supportive care.",
                "stage": "Grade 1 - Mild",
                "stage_description": "Mild symptoms",
                "crs_grade": 1,
                "severity_level": "mild",
                "intervention_type": "symptomatic",
                "clinical_assessment": {
                    "crs_grade": 1,
                    "severity_indicators": [],
                    "risk_factors": [],
                    "clinical_features": ["Fever", "Constitutional symptoms", "Mild discomfort"]
                },
                "management_recommendations": {
                    "primary_interventions": [
                        "Supportive care with symptomatic treatment",
                        "Monitor vital signs and symptoms closely",
                        "Adequate hydration and fever management",
                        "No specific anti-cytokine therapy required"
                    ],
                    "additional_considerations": [],
                    "medication_options": ["Acetaminophen/paracetamol for fever", "Adequate hydration", "Symptomatic care"],
                    "monitoring_frequency": "Every 4-8 hours"
                },
                "monitoring_requirements": {
                    "parameters": ["Vital signs", "Temperature", "Oxygen saturation", "Mental status"],
                    "frequency": "Every 4-8 hours",
                    "laboratory_studies": ["Basic metabolic panel", "Complete blood count"]
                },
                "treatment_urgency": "Routine - symptomatic care",
                "prognosis": {
                    "outlook": "Excellent",
                    "description": "Expected full recovery with supportive care"
                },
                "care_setting": "Inpatient ward with oncology monitoring"
            }
        }