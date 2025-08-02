"""
YEARS Algorithm for Pulmonary Embolism (PE) Models

Request and response models for YEARS Algorithm calculation for PE diagnosis.

References (Vancouver style):
1. van der Hulle T, Cheung WY, Kooij S, et al. Simplified diagnostic management of suspected 
   pulmonary embolism (the YEARS study): a prospective, multicentre, cohort study. 
   Lancet. 2017;390(10091):289-297. doi: 10.1016/S0140-6736(17)30885-1
2. van der Pol LM, Tromeur C, Bistervels IM, et al. Pregnancy-Adapted YEARS Algorithm for 
   Diagnosis of Suspected Pulmonary Embolism. N Engl J Med. 2019;380(12):1139-1149. 
   doi: 10.1056/NEJMoa1813865
3. Freund Y, Drogrey M, Miró Ò, et al. Association between pulmonary embolism response 
   team activation and clinical outcomes. Am J Respir Crit Care Med. 2019;200(9):1167-1175.

The YEARS Algorithm is a simplified diagnostic tool that uses variable D-dimer thresholds 
based on three clinical criteria to rule out pulmonary embolism in hemodynamically stable 
patients ≥18 years old. It reduces unnecessary CT pulmonary angiography by 14% compared to 
standard algorithms while maintaining safety with a 3-month VTE incidence of 0.43% for 
patients not undergoing CTPA.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class YearsAlgorithmPeRequest(BaseModel):
    """
    Request model for YEARS Algorithm for Pulmonary Embolism (PE)
    
    The YEARS Algorithm assesses three clinical criteria to determine appropriate 
    D-dimer thresholds for ruling out pulmonary embolism:
    
    **THE THREE YEARS CRITERIA:**
    
    1. **Clinical Signs of Deep Vein Thrombosis (DVT):**
       - Unilateral leg swelling
       - Palpable deep venous thrombosis
       - Clinical signs suggestive of DVT
    
    2. **Hemoptysis:**
       - Coughing up blood
       - Frank hemoptysis or blood-streaked sputum
    
    3. **PE is the Most Likely Diagnosis:**
       - Clinical judgment that alternative diagnoses are less likely than PE
       - PE is considered the primary differential diagnosis
       - Based on overall clinical assessment
    
    **VARIABLE D-DIMER THRESHOLDS:**
    
    The algorithm uses different D-dimer cutoff values based on the number of YEARS criteria:
    
    **0 YEARS Items Present:**
    - D-dimer threshold: 1000 ng/mL FEU
    - If D-dimer <1000 ng/mL → PE excluded
    - Higher threshold allows more patients to avoid imaging
    
    **≥1 YEARS Items Present:**
    - D-dimer threshold: 500 ng/mL FEU  
    - If D-dimer <500 ng/mL → PE excluded
    - Lower threshold reflects higher pre-test probability
    
    **D-dimer Above Threshold:**
    - CTPA (CT pulmonary angiography) required
    - Proceed with imaging to exclude PE
    
    **CLINICAL VALIDATION:**
    
    Performance Characteristics:
    - Reduces CTPA by 14% compared to standard algorithms
    - 3-month VTE incidence: 0.43% for patients not undergoing CTPA
    - Sensitivity: 90%, Specificity: 65%
    - Miss rate: 0.5% (95% CI 0.2 to 1.1%)
    
    Safety Profile:
    - Extensively validated in prospective multicenter studies
    - Safe for ruling out PE in appropriate patient populations
    - Not associated with increased missed clinically significant PEs
    
    **PATIENT SELECTION CRITERIA:**
    
    Appropriate for:
    - Hemodynamically stable patients ≥18 years old
    - Suspected pulmonary embolism
    - Patients able to undergo CTPA if indicated
    
    Exclusions:
    - Patients on therapeutic anticoagulation
    - Life expectancy <3 months
    - Geographic follow-up limitations
    - Contrast agent allergies or contraindications to CTPA
    - Pregnancy (requires Pregnancy-Adapted YEARS Algorithm)
    
    **CLINICAL IMPLEMENTATION:**
    
    Algorithm Steps:
    1. Assess three YEARS criteria (DVT signs, hemoptysis, PE most likely)
    2. Count positive criteria (0, 1, 2, or 3)
    3. Apply appropriate D-dimer threshold
    4. Make diagnostic recommendation based on D-dimer result
    
    Decision Making:
    - D-dimer below threshold → PE excluded, no imaging
    - D-dimer above threshold → CTPA indicated
    - Clinical judgment remains important for implementation
    
    **SPECIAL CONSIDERATIONS:**
    
    Pregnancy:
    - Standard YEARS not validated in pregnancy
    - Use Pregnancy-Adapted YEARS Algorithm
    - Includes compression ultrasonography for DVT signs
    
    Age Considerations:
    - Caution with age-adjusted D-dimer interpretations
    - Among patients with no YEARS criteria and D-dimer <1000 ng/mL 
      but above age-adjusted cutoff, PE diagnosed in 6.3%
    
    **ADVANTAGES OVER OTHER ALGORITHMS:**
    
    Simplicity:
    - Only three clinical criteria to assess
    - Less complex than Wells score or Geneva score
    - Easier implementation in busy emergency departments
    
    Efficiency:
    - Reduces unnecessary imaging by 14%
    - Decreases false positives and radiation exposure
    - Cost-effective diagnostic approach
    
    Safety:
    - Maintained safety compared to standard algorithms
    - Low miss rate for clinically significant PE
    - Appropriate negative predictive value
    
    References (Vancouver style):
    1. van der Hulle T, Cheung WY, Kooij S, et al. Simplified diagnostic management of suspected 
    pulmonary embolism (the YEARS study): a prospective, multicentre, cohort study. 
    Lancet. 2017;390(10091):289-297. doi: 10.1016/S0140-6736(17)30885-1
    2. van der Pol LM, Tromeur C, Bistervels IM, et al. Pregnancy-Adapted YEARS Algorithm for 
    Diagnosis of Suspected Pulmonary Embolism. N Engl J Med. 2019;380(12):1139-1149.
    """
    
    clinical_signs_dvt: Literal["yes", "no"] = Field(
        ...,
        description="Clinical signs of deep vein thrombosis (unilateral leg swelling, palpable deep venous thrombosis)",
        example="no"
    )
    
    hemoptysis: Literal["yes", "no"] = Field(
        ...,
        description="Hemoptysis (coughing up blood)",
        example="no"
    )
    
    pe_most_likely: Literal["yes", "no"] = Field(
        ...,
        description="PE is the most likely diagnosis (clinical judgment that alternative diagnoses are less likely than PE)",
        example="yes"
    )
    
    d_dimer: float = Field(
        ...,
        description="D-dimer level in ng/mL FEU (fibrinogen equivalent units)",
        ge=0,
        le=50000,
        example=750.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_signs_dvt": "no",
                "hemoptysis": "no", 
                "pe_most_likely": "yes",
                "d_dimer": 750.0
            }
        }


class YearsAlgorithmPeResponse(BaseModel):
    """
    Response model for YEARS Algorithm for Pulmonary Embolism (PE)
    
    The YEARS Algorithm provides a diagnostic recommendation based on the number of 
    clinical criteria present and the D-dimer level relative to variable thresholds.
    
    **INTERPRETATION CATEGORIES:**
    
    **PE Excluded:**
    - D-dimer below the appropriate threshold
    - No further imaging required for PE workup
    - 3-month VTE incidence of 0.43% for these patients
    - Consider alternative diagnoses for patient symptoms
    
    **CTPA Required:**
    - D-dimer above the appropriate threshold
    - CT pulmonary angiography indicated to exclude PE
    - Proceed with imaging based on clinical urgency
    - Consider interim anticoagulation if high suspicion
    
    **CLINICAL DECISION SUPPORT:**
    
    Next Steps for PE Excluded:
    - No further diagnostic testing for PE required
    - Consider alternative diagnoses (pneumonia, pleuritis, etc.)
    - Follow up based on alternative differential diagnosis
    - Patient education about symptoms warranting re-evaluation
    
    Next Steps for CTPA Required:
    - Proceed with CT pulmonary angiography
    - Consider ventilation-perfusion scan if CTPA contraindicated
    - Evaluate need for interim anticoagulation
    - Assess hemodynamic stability and clinical urgency
    
    **SAFETY CONSIDERATIONS:**
    
    Algorithm Limitations:
    - Not validated in patients on therapeutic anticoagulation
    - Not appropriate for hemodynamically unstable patients
    - Pregnancy requires modified algorithm
    - Clinical judgment remains essential
    
    Performance Metrics:
    - 14% reduction in CTPA compared to standard algorithms
    - 0.5% miss rate (95% CI 0.2 to 1.1%)
    - 0.43% 3-month VTE incidence for patients not undergoing CTPA
    - Sensitivity 90%, Specificity 65%
    
    Reference: van der Hulle T, et al. Lancet. 2017;390(10091):289-297.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic recommendation based on YEARS criteria and D-dimer threshold",
        example="CTPA Required"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="categorical"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and diagnostic recommendation based on YEARS Algorithm",
        example="Based on YEARS Algorithm: 1 YEARS items present, D-dimer 750.0 ng/mL exceeds threshold of 500 ng/mL. CT pulmonary angiography (CTPA) is required to exclude pulmonary embolism."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (PE Excluded or CTPA Required)",
        example="CTPA Required"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic recommendation",
        example="CT pulmonary angiography indicated"
    )
    
    years_count: int = Field(
        ...,
        description="Number of positive YEARS criteria (0-3)",
        ge=0,
        le=3,
        example=1
    )
    
    d_dimer_threshold: float = Field(
        ...,
        description="D-dimer threshold used based on YEARS count (500 ng/mL for ≥1 items, 1000 ng/mL for 0 items)",
        example=500.0
    )
    
    d_dimer_value: float = Field(
        ...,
        description="Patient's D-dimer level in ng/mL FEU",
        example=750.0
    )
    
    years_items: Dict[str, bool] = Field(
        ...,
        description="Individual YEARS criteria assessment",
        example={
            "clinical_signs_dvt": False,
            "hemoptysis": False,
            "pe_most_likely": True
        }
    )
    
    clinical_decision: Dict[str, Any] = Field(
        ...,
        description="Clinical decision support and next steps based on the algorithm result",
        example={
            "next_steps": "Proceed with CT pulmonary angiography (CTPA)",
            "urgency": "Based on clinical assessment and hemodynamic stability",
            "alternative": "Consider ventilation-perfusion scan if CTPA contraindicated",
            "anticoagulation": "Consider interim anticoagulation pending imaging if high clinical suspicion"
        }
    )
    
    safety_information: Dict[str, Any] = Field(
        ...,
        description="Important safety information and algorithm limitations",
        example={
            "validated_population": "Hemodynamically stable patients ≥18 years old with suspected PE",
            "exclusions": [
                "Patients on therapeutic anticoagulation",
                "Life expectancy <3 months",
                "Geographic follow-up limitations",
                "Contrast agent allergies"
            ],
            "pregnancy": "Requires modified Pregnancy-Adapted YEARS Algorithm",
            "performance": "Reduces CTPA by 14% compared to standard algorithms with maintained safety"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "CTPA Required",
                "unit": "categorical",
                "interpretation": "Based on YEARS Algorithm: 1 YEARS items present, D-dimer 750.0 ng/mL exceeds threshold of 500 ng/mL. CT pulmonary angiography (CTPA) is required to exclude pulmonary embolism.",
                "stage": "CTPA Required",
                "stage_description": "CT pulmonary angiography indicated",
                "years_count": 1,
                "d_dimer_threshold": 500.0,
                "d_dimer_value": 750.0,
                "years_items": {
                    "clinical_signs_dvt": False,
                    "hemoptysis": False,
                    "pe_most_likely": True
                },
                "clinical_decision": {
                    "next_steps": "Proceed with CT pulmonary angiography (CTPA)",
                    "urgency": "Based on clinical assessment and hemodynamic stability",
                    "alternative": "Consider ventilation-perfusion scan if CTPA contraindicated",
                    "anticoagulation": "Consider interim anticoagulation pending imaging if high clinical suspicion"
                },
                "safety_information": {
                    "validated_population": "Hemodynamically stable patients ≥18 years old with suspected PE",
                    "exclusions": [
                        "Patients on therapeutic anticoagulation",
                        "Life expectancy <3 months",
                        "Geographic follow-up limitations",
                        "Contrast agent allergies"
                    ],
                    "pregnancy": "Requires modified Pregnancy-Adapted YEARS Algorithm",
                    "performance": "Reduces CTPA by 14% compared to standard algorithms with maintained safety"
                }
            }
        }