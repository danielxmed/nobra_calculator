"""
MASCC Risk Index for Febrile Neutropenia Models

Request and response models for MASCC Risk Index calculation.

References (Vancouver style):
1. Klastersky J, Paesmans M, Rubenstein EB, Boyer M, Elting L, Feld R, et al. 
   The Multinational Association for Supportive Care in Cancer risk index: 
   A multinational scoring system for identifying low-risk febrile neutropenic 
   cancer patients. J Clin Oncol. 2000 Aug;18(16):3038-51. doi: 10.1200/JCO.2000.18.16.3038.
2. Freifeld AG, Bow EJ, Sepkowitz KA, Boeckh MJ, Ito JI, Mullen CA, et al. 
   Clinical practice guideline for the use of antimicrobial agents in neutropenic 
   patients with cancer: 2010 update by the infectious diseases society of america. 
   Clin Infect Dis. 2011 Feb 15;52(4):e56-93. doi: 10.1093/cid/cir073.
3. Uys A, Rapoport BL, Anderson R. Febrile neutropenia: a prospective study to 
   validate the Multinational Association of Supportive Care of Cancer (MASCC) 
   risk-index score. Support Care Cancer. 2004 Aug;12(8):555-60. doi: 10.1007/s00520-004-0614-5.

The MASCC Risk Index is a validated clinical prediction tool developed by the 
Multinational Association for Supportive Care in Cancer to identify cancer patients 
with febrile neutropenia who are at low risk for serious complications. The index 
uses seven clinical variables to generate a score ranging from 0-26 points, with 
a cut-off of ≥21 points indicating low risk for complications including death, 
ICU admission, confusion, cardiac complications, respiratory failure, renal failure, 
hypotension, bleeding, and other serious medical complications. This stratification 
helps guide treatment decisions regarding outpatient vs. inpatient management and 
oral vs. intravenous antibiotic therapy.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class MasccRiskIndexFebrileNeutropeniaRequest(BaseModel):
    """
    Request model for MASCC Risk Index for Febrile Neutropenia
    
    The MASCC Risk Index evaluates seven clinical variables to assess complication 
    risk in cancer patients with febrile neutropenia:
    
    **Seven Clinical Variables:**
    
    1. **Burden of Illness (Symptom Severity)**:
       - None/Mild: 5 points - Minimal symptoms, well-appearing
       - Moderate: 3 points - Moderate symptoms affecting function
       - Severe: 0 points - Severe symptoms, significant distress
    
    2. **Hypotension**: Systolic blood pressure <90 mmHg
       - No: 5 points - Hemodynamically stable
       - Yes: 0 points - Hypotensive, hemodynamic compromise
    
    3. **Active COPD**: Chronic obstructive pulmonary disease
       - No: 4 points - No active respiratory comorbidity
       - Yes: 0 points - Active COPD increases respiratory risk
    
    4. **Cancer Type and Fungal History**:
       - Solid tumor OR hematologic without prior fungal: 4 points
       - Hematologic malignancy WITH prior fungal infection: 0 points
    
    5. **Dehydration Requiring IV Fluids**:
       - No: 3 points - Adequate hydration status
       - Yes: 0 points - Volume depleted, hemodynamic risk
    
    6. **Status at Fever Onset**:
       - Outpatient: 3 points - Community-acquired episode
       - Inpatient: 0 points - Nosocomial episode, higher risk
    
    7. **Age**: Chronological age in years
       - <60 years: 2 points - Lower age-related risk
       - ≥60 years: 0 points - Higher age-related complication risk
    
    **Risk Stratification:**
    - **Low Risk (≥21 points)**: 91% PPV for uncomplicated course
    - **High Risk (<21 points)**: Increased complication risk, requires inpatient care
    
    **Clinical Applications:**
    - Treatment setting decision (outpatient vs. inpatient)
    - Antibiotic route selection (oral vs. intravenous)
    - Resource allocation and care planning
    - Patient counseling and shared decision-making
    - Quality improvement and standardization of care
    
    **Validation Performance:**
    - Original validation: PPV 91%, Sensitivity 71%, Specificity 68%
    - External validation studies: PPV 83-98%, Sensitivity 59-95%
    - Endorsed by Infectious Diseases Society of America (IDSA)
    
    **Important Limitations:**
    - Adult patients only (≥18 years)
    - Not recommended for acute leukemia or stem cell transplant patients
    - Does not incorporate neutrophil count or expected duration
    - Clinical judgment should override score when indicated
    - Requires reliable access to medical care for outpatient management
    
    References (Vancouver style):
    1. Klastersky J, Paesmans M, Rubenstein EB, Boyer M, Elting L, Feld R, et al. 
       The Multinational Association for Supportive Care in Cancer risk index: 
       A multinational scoring system for identifying low-risk febrile neutropenic 
       cancer patients. J Clin Oncol. 2000 Aug;18(16):3038-51. doi: 10.1200/JCO.2000.18.16.3038.
    2. Freifeld AG, Bow EJ, Sepkowitz KA, Boeckh MJ, Ito JI, Mullen CA, et al. 
       Clinical practice guideline for the use of antimicrobial agents in neutropenic 
       patients with cancer: 2010 update by the infectious diseases society of america. 
       Clin Infect Dis. 2011 Feb 15;52(4):e56-93. doi: 10.1093/cid/cir073.
    """
    
    burden_of_illness: Literal["none_mild", "moderate", "severe"] = Field(
        ...,
        description="Burden of illness based on symptom severity assessment. None/mild (5 pts): minimal symptoms, well-appearing. Moderate (3 pts): moderate symptoms affecting function. Severe (0 pts): severe symptoms with significant distress",
        example="none_mild"
    )
    
    hypotension: Literal["yes", "no"] = Field(
        ...,
        description="Presence of hypotension defined as systolic blood pressure <90 mmHg. Hypotension indicates hemodynamic instability and significantly increases complication risk",
        example="no"
    )
    
    active_copd: Literal["yes", "no"] = Field(
        ...,
        description="Active chronic obstructive pulmonary disease. COPD increases risk of respiratory complications during febrile neutropenia episodes",
        example="no"
    )
    
    cancer_type: Literal["solid_tumor_or_hematologic_no_prior_fungal", "hematologic_with_prior_fungal"] = Field(
        ...,
        description="Type of underlying cancer and history of fungal infection. Solid tumor or hematologic malignancy without prior fungal infection (4 pts). Hematologic malignancy with prior fungal infection (0 pts) carries significantly higher risk",
        example="solid_tumor_or_hematologic_no_prior_fungal"
    )
    
    dehydration_requiring_iv: Literal["yes", "no"] = Field(
        ...,
        description="Dehydration requiring intravenous fluid therapy. Volume depletion indicates potential for hemodynamic compromise and increased complication risk",
        example="no"
    )
    
    fever_onset_status: Literal["outpatient", "inpatient"] = Field(
        ...,
        description="Patient status at fever onset. Outpatient onset (3 pts) typically associated with lower complication risk. Inpatient onset (0 pts) suggests nosocomial infection with higher risk",
        example="outpatient"
    )
    
    patient_age: int = Field(
        ...,
        ge=18,
        le=100,
        description="Patient age in years. Age <60 years (2 pts) associated with lower complication risk. Age ≥60 years (0 pts) associated with increased complication risk in febrile neutropenia",
        example=45
    )
    
    class Config:
        schema_extra = {
            "example": {
                "burden_of_illness": "none_mild",
                "hypotension": "no",
                "active_copd": "no",
                "cancer_type": "solid_tumor_or_hematologic_no_prior_fungal",
                "dehydration_requiring_iv": "no",
                "fever_onset_status": "outpatient",
                "patient_age": 45
            }
        }


class MasccRiskIndexFebrileNeutropeniaResponse(BaseModel):
    """
    Response model for MASCC Risk Index for Febrile Neutropenia
    
    The MASCC Risk Index provides evidence-based risk stratification for cancer 
    patients with febrile neutropenia:
    
    **Low Risk (≥21 points):**
    - Positive predictive value: 91% for uncomplicated course
    - Management: Consider oral antibiotic therapy and/or outpatient management
    - Monitoring: Close follow-up with reliable access to medical care
    - Benefits: Reduced hospitalization, improved quality of life, cost savings
    - Requirements: Patient education, social support, ability to return if worsening
    
    **High Risk (<21 points):**
    - Complication likelihood: Increased risk for serious complications
    - Management: Inpatient admission for empiric intravenous antibiotics
    - Monitoring: Intensive monitoring for early recognition of complications
    - Complications: Death, ICU admission, organ failure, bleeding, sepsis
    - Care level: May require ICU-level monitoring and aggressive supportive care
    
    **Clinical Decision Support:**
    - Evidence-based guidance for treatment setting selection
    - Standardization of febrile neutropenia management protocols
    - Resource allocation optimization in oncology care
    - Patient safety through appropriate risk stratification
    - Support for shared decision-making with patients and families
    
    **Quality Assurance:**
    - Validated across multiple cancer populations and healthcare settings
    - Endorsed by major infectious disease and oncology societies
    - Regular outcome monitoring for quality improvement
    - Integration with institutional clinical pathways
    
    **Implementation Considerations:**
    - Clinical judgment should always supplement score-based decisions
    - Consider patient preferences, values, and social circumstances
    - Account for institutional resources and expertise
    - Maintain awareness of score limitations and exclusions
    - Regular reassessment as clinical condition evolves
    
    Reference: Klastersky J, et al. J Clin Oncol. 2000;18(16):3038-51.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Comprehensive MASCC Risk Index assessment including component scores, risk stratification, and detailed clinical management guidance",
        example={
            "total_score": 22,
            "component_scores": {
                "burden_of_illness": 5,
                "hypotension": 5,
                "active_copd": 4,
                "cancer_type": 4,
                "dehydration": 3,
                "fever_onset": 3,
                "age": 2
            },
            "component_breakdown": {
                "burden_of_illness": "Burden of illness (none mild): 5 points",
                "hypotension": "Hypotension: 5 points",
                "active_copd": "Active COPD: 4 points",
                "cancer_type": "Cancer type: 4 points",
                "dehydration": "Dehydration requiring IV: 3 points",
                "fever_onset": "Fever onset status (outpatient): 3 points",
                "age": "Age (45 years): 2 points"
            },
            "assessment_data": {
                "risk_level": "Low Risk",
                "positive_predictive_value": "91%",
                "recommendation": "Consider oral antibiotic therapy and/or outpatient management",
                "management_approach": "Outpatient management with close follow-up may be appropriate",
                "monitoring_requirements": "Reliable access to medical care and ability to return if worsening",
                "score_threshold": "Cut-off ≥21 points for low risk",
                "original_validation": "PPV 91%, Sensitivity 71%, Specificity 68%",
                "external_validation": "PPV range 83-98%, Sensitivity range 59-95%",
                "clinical_judgment": "Clinical assessment should always override score when indicated"
            }
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Comprehensive clinical interpretation with risk assessment, positive predictive value, management recommendations, and monitoring requirements",
        example="MASCC Risk Index score of 22 indicates low risk for serious complications of febrile neutropenia with 91% positive predictive value for uncomplicated course. These patients may be considered for oral antibiotic therapy and/or outpatient management with close follow-up."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category and clinical implications",
        example="Low risk for complications"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "total_score": 22,
                    "component_scores": {
                        "burden_of_illness": 5,
                        "hypotension": 5,
                        "active_copd": 4,
                        "cancer_type": 4,
                        "dehydration": 3,
                        "fever_onset": 3,
                        "age": 2
                    },
                    "component_breakdown": {
                        "burden_of_illness": "Burden of illness (none mild): 5 points",
                        "hypotension": "Hypotension: 5 points",
                        "active_copd": "Active COPD: 4 points",
                        "cancer_type": "Cancer type: 4 points",
                        "dehydration": "Dehydration requiring IV: 3 points",
                        "fever_onset": "Fever onset status (outpatient): 3 points",
                        "age": "Age (45 years): 2 points"
                    },
                    "assessment_data": {
                        "risk_level": "Low Risk",
                        "positive_predictive_value": "91%",
                        "recommendation": "Consider oral antibiotic therapy and/or outpatient management",
                        "management_approach": "Outpatient management with close follow-up may be appropriate",
                        "monitoring_requirements": "Reliable access to medical care and ability to return if worsening",
                        "score_threshold": "Cut-off ≥21 points for low risk",
                        "original_validation": "PPV 91%, Sensitivity 71%, Specificity 68%",
                        "external_validation": "PPV range 83-98%, Sensitivity range 59-95%",
                        "clinical_judgment": "Clinical assessment should always override score when indicated"
                    }
                },
                "unit": "points",
                "interpretation": "MASCC Risk Index score of 22 indicates low risk for serious complications of febrile neutropenia with 91% positive predictive value for uncomplicated course. These patients may be considered for oral antibiotic therapy and/or outpatient management with close follow-up. However, clinical judgment should always override the score, and patients must have reliable access to medical care with ability to return immediately if symptoms worsen.",
                "stage": "Low Risk",
                "stage_description": "Low risk for complications"
            }
        }