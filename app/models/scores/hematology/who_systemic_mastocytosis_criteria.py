"""
WHO Diagnostic Criteria for Systemic Mastocytosis (2016) Models

Request and response models for WHO 2016 systemic mastocytosis diagnostic criteria.

References (Vancouver style):
1. Valent P, Akin C, Hartmann K, et al. Updated diagnostic criteria and classification 
   of mast cell disorders: a consensus proposal. HemaSphere. 2021;5(11):e646. 
   doi: 10.1097/HS9.0000000000000646
2. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
   Organization classification of myeloid neoplasms and acute leukemia. Blood. 
   2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
3. Valent P, Alin C, Metcalfe DD. Mastocytosis: 2016 updated WHO classification 
   and novel emerging treatment concepts. Blood. 2017;129(11):1420-1427. 
   doi: 10.1182/blood-2016-09-731893
4. Pardanani A. Systemic mastocytosis in adults: 2023 update on diagnosis, risk 
   stratification and management. Am J Hematol. 2023;98(8):1306-1325. 
   doi: 10.1002/ajh.26962

The WHO 2016 criteria for systemic mastocytosis require either:
- 1 major criterion + 1 minor criterion, OR
- 3 minor criteria

This diagnostic framework distinguishes systemic mastocytosis from cutaneous 
mastocytosis and other mast cell disorders. The criteria emphasize tissue 
infiltration patterns, molecular markers, and serum biomarkers.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class WhoSystemicMastocytosisCriteriaRequest(BaseModel):
    """
    Request model for WHO 2016 Diagnostic Criteria for Systemic Mastocytosis
    
    The WHO 2016 criteria evaluate systemic mastocytosis diagnosis using 1 major 
    criterion and 4 minor criteria. Diagnosis requires either:
    - 1 major criterion + 1 minor criterion, OR
    - 3 minor criteria
    
    **MAJOR CRITERION:**
    
    1. **Multifocal Mast Cell Infiltrates:**
       - Dense infiltrates of mast cells (≥15 mast cells in aggregates)
       - Found in bone marrow biopsies and/or other extracutaneous organ sections
       - Evaluated by histopathology with immunohistochemistry
    
    **MINOR CRITERIA:**
    
    1. **Atypical Mast Cell Morphology:**
       - ≥25% of mast cells are atypical (type I or II) on bone marrow smears
       - OR spindle-shaped mast cells in tissue infiltrates
       - Assessed by morphological evaluation of bone marrow/tissue specimens
    
    2. **KIT Mutations:**
       - KIT-activating point mutations at codon 816 (most commonly D816V)
       - OR other critical KIT regions with transformative behavior
       - Detected by molecular genetic testing (PCR, sequencing)
    
    3. **Aberrant CD Expression:**
       - Mast cells express CD2 and/or CD25 and/or CD30
       - In addition to normal mast cell markers (CD117, tryptase)
       - Detected by flow cytometry or immunohistochemistry
    
    4. **Elevated Serum Tryptase:**
       - Baseline serum tryptase concentration >20 ng/mL
       - Only valid in absence of associated myeloid neoplasm
       - Normal range: <11.4 ng/mL
    
    **Clinical Significance:**
    Systemic mastocytosis is a clonal mast cell disorder characterized by 
    abnormal accumulation and activation of mast cells in various organs. 
    Early diagnosis enables appropriate management of symptoms, monitoring 
    for disease progression, and prevention of severe systemic reactions.
    
    **Laboratory Parameters:**
    
    Multifocal Mast Cell Infiltrates: Histopathological finding
    - yes: Dense aggregates ≥15 mast cells identified in bone marrow/organs
    - no: Insufficient aggregates or <15 cells per aggregate
    - not_assessed: Tissue evaluation not performed
    
    Atypical Mast Cell Morphology: Morphological assessment
    - yes: ≥25% atypical forms (spindle-shaped, type I/II morphology)
    - no: Normal mast cell morphology, <25% atypical
    - not_assessed: Morphological evaluation not performed
    
    KIT Mutation: Molecular genetic testing
    - d816v_positive: KIT D816V mutation detected (~95% of cases)
    - other_kit_positive: Other activating KIT mutations at critical regions
    - negative: No KIT mutations detected
    - not_tested: Molecular testing not performed
    
    Aberrant CD Expression: Immunophenotyping
    - yes: CD2/CD25/CD30 expression detected (aberrant phenotype)
    - no: Normal mast cell immunophenotype only
    - not_assessed: Flow cytometry/immunohistochemistry not performed
    
    Serum Tryptase: Biomarker level in ng/mL
    - Normal: <11.4 ng/mL
    - Criterion threshold: >20 ng/mL
    - Range: 0-200 ng/mL
    
    Associated Myeloid Neoplasm: Comorbid hematologic condition
    - yes: Concurrent myeloid malignancy (invalidates tryptase criterion)
    - no: No associated myeloid neoplasm
    - unknown: Status uncertain or not evaluated
    
    References (Vancouver style):
    1. Valent P, Akin C, Hartmann K, et al. Updated diagnostic criteria and classification 
    of mast cell disorders: a consensus proposal. HemaSphere. 2021;5(11):e646. 
    doi: 10.1097/HS9.0000000000000646
    2. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
    Organization classification of myeloid neoplasms and acute leukemia. Blood. 
    2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
    3. Valent P, Alin C, Metcalfe DD. Mastocytosis: 2016 updated WHO classification 
    and novel emerging treatment concepts. Blood. 2017;129(11):1420-1427. 
    doi: 10.1182/blood-2016-09-731893
    """
    
    multifocal_mast_cell_infiltrates: Literal["yes", "no", "not_assessed"] = Field(
        ...,
        description="Multifocal dense infiltrates of mast cells (≥15 mast cells in aggregates) in bone marrow biopsies and/or other extracutaneous organ sections (MAJOR CRITERION)",
        example="yes"
    )
    
    atypical_mast_cell_morphology: Literal["yes", "no", "not_assessed"] = Field(
        ...,
        description="≥25% of mast cells are atypical (type I or II) on bone marrow smears or spindle-shaped in mast cell infiltrates (MINOR CRITERION 1)",
        example="yes"
    )
    
    kit_mutation: Literal["d816v_positive", "other_kit_positive", "negative", "not_tested"] = Field(
        ...,
        description="KIT-activating point mutations at codon 816 (usually D816V) or other critical KIT regions (MINOR CRITERION 2)",
        example="d816v_positive"
    )
    
    aberrant_cd_expression: Literal["yes", "no", "not_assessed"] = Field(
        ...,
        description="Mast cells express CD2 and/or CD25 and/or CD30 (aberrant phenotype) in addition to normal mast cell markers (MINOR CRITERION 3)",
        example="yes"
    )
    
    serum_tryptase: float = Field(
        ...,
        description="Baseline serum tryptase concentration in ng/mL. Normal <11.4 ng/mL, criterion met if >20 ng/mL in absence of associated myeloid neoplasm (MINOR CRITERION 4)",
        ge=0.0,
        le=200.0,
        example=45.2
    )
    
    associated_myeloid_neoplasm: Literal["yes", "no", "unknown"] = Field(
        ...,
        description="Presence of associated myeloid neoplasm (affects interpretation of serum tryptase criterion - criterion invalid if myeloid neoplasm present)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "multifocal_mast_cell_infiltrates": "yes",
                "atypical_mast_cell_morphology": "yes",
                "kit_mutation": "d816v_positive",
                "aberrant_cd_expression": "yes",
                "serum_tryptase": 45.2,
                "associated_myeloid_neoplasm": "no"
            }
        }


class WhoSystemicMastocytosisCriteriaResponse(BaseModel):
    """
    Response model for WHO 2016 Diagnostic Criteria for Systemic Mastocytosis
    
    The WHO 2016 criteria provide systematic evaluation for systemic mastocytosis diagnosis.
    Results are categorized as:
    
    **DIAGNOSIS CATEGORIES:**
    
    1. **diagnosis_met**: WHO criteria satisfied
       - 1 major criterion + 1 minor criterion, OR
       - 3 minor criteria met
       - Systemic mastocytosis diagnosis confirmed
    
    2. **probable_sm**: Partial criteria met
       - Some criteria fulfilled but diagnosis incomplete
       - Additional testing needed to confirm/exclude systemic mastocytosis
    
    3. **criteria_not_met**: Insufficient criteria
       - Current findings do not support systemic mastocytosis diagnosis
       - Consider cutaneous mastocytosis, MCAS, or other conditions
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    Diagnosis Met:
    - Refer to hematology-oncology for specialized management
    - Perform disease subtype classification and staging
    - Assess for organ involvement and functional impairment
    - Consider allergy/immunology consultation for symptom management
    - Monitor for disease progression and complications
    
    Probable Systemic Mastocytosis:
    - Complete comprehensive diagnostic workup
    - Hematology consultation for expert evaluation
    - Monitor symptoms and clinical progression
    - Consider interim symptom management
    
    Criteria Not Met:
    - Consider cutaneous mastocytosis if skin involvement
    - Evaluate for mast cell activation syndrome
    - Test for hereditary alpha-tryptasemia
    - Specialist referral if clinical suspicion persists
    
    **PROGNOSTIC CONSIDERATIONS:**
    
    Systemic mastocytosis patients may have:
    - Variable clinical course depending on subtype
    - Indolent forms with near-normal life expectancy
    - Aggressive forms requiring intensive treatment
    - Risk of anaphylaxis and mediator release symptoms
    - Potential for associated hematologic malignancies
    
    Reference: Valent P, et al. HemaSphere. 2021;5(11):e646.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic assessment result based on WHO 2016 criteria evaluation (diagnosis_met, probable_sm, criteria_not_met)",
        example="diagnosis_met"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="categorical"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with management recommendations based on criteria fulfillment and diagnostic certainty",
        example="WHO 2016 diagnostic criteria for systemic mastocytosis are MET. Patient fulfills 1 major criterion and 4 minor criteria. Diagnosis of systemic mastocytosis is confirmed. Proceed with staging, risk stratification, and appropriate management. Consider referral to hematology-oncology for specialized care and evaluation of disease subtype and prognosis."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage or category based on criteria assessment",
        example="Systemic Mastocytosis Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="WHO 2016 criteria met - diagnosis confirmed"
    )
    
    major_criteria_met: int = Field(
        ...,
        description="Number of major criteria fulfilled (0-1). Major criterion: Multifocal mast cell infiltrates ≥15 cells",
        ge=0,
        le=1,
        example=1
    )
    
    minor_criteria_met: int = Field(
        ...,
        description="Number of minor criteria fulfilled (0-4). Minor criteria: (1) Atypical morphology, (2) KIT mutations, (3) Aberrant CD expression, (4) Elevated tryptase",
        ge=0,
        le=4,
        example=4
    )
    
    total_major_criteria: int = Field(
        ...,
        description="Total number of major criteria evaluated (always 1 for WHO 2016 criteria)",
        example=1
    )
    
    total_minor_criteria: int = Field(
        ...,
        description="Total number of minor criteria evaluated (always 4 for WHO 2016 criteria)",
        example=4
    )
    
    criteria_details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of each criterion assessment including descriptions, fulfillment status, and clinical details",
        example={
            "major_criterion": {
                "description": "Multifocal dense infiltrates of mast cells (≥15 mast cells in aggregates) in bone marrow biopsies and/or other extracutaneous organ sections",
                "met": True,
                "details": "Multifocal dense infiltrates of mast cells (≥15 cells in aggregates) present in bone marrow and/or extracutaneous organs"
            },
            "minor_criterion_1": {
                "description": "≥25% of mast cells are atypical (type I or II) on bone marrow smears or spindle-shaped in mast cell infiltrates",
                "met": True,
                "details": "≥25% of mast cells show atypical morphology (type I/II) or spindle-shaped appearance"
            }
        }
    )
    
    detailed_analysis: Dict[str, Any] = Field(
        ...,
        description="Comprehensive analysis including criteria summary, clinical recommendations, laboratory interpretation, differential diagnosis, and follow-up plans",
        example={
            "criteria_summary": {
                "major_criteria": "1/1 met",
                "minor_criteria": "4/4 met",
                "diagnosis_requirement": "1 major criterion + 1 minor criterion OR 3 minor criteria"
            },
            "clinical_recommendations": [
                "Refer to hematology-oncology for specialized management and staging",
                "Perform disease subtype classification",
                "Assess for organ involvement and functional impairment"
            ],
            "laboratory_interpretation": {
                "tryptase_analysis": {"value": "45.2 ng/mL", "elevated": True, "meets_criterion": True}
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "diagnosis_met",
                "unit": "categorical",
                "interpretation": "WHO 2016 diagnostic criteria for systemic mastocytosis are MET. Patient fulfills 1 major criterion and 4 minor criteria. Diagnosis of systemic mastocytosis is confirmed. Proceed with staging, risk stratification, and appropriate management. Consider referral to hematology-oncology for specialized care and evaluation of disease subtype and prognosis.",
                "stage": "Systemic Mastocytosis Diagnosed",
                "stage_description": "WHO 2016 criteria met - diagnosis confirmed",
                "major_criteria_met": 1,
                "minor_criteria_met": 4,
                "total_major_criteria": 1,
                "total_minor_criteria": 4,
                "criteria_details": {
                    "major_criterion": {
                        "description": "Multifocal dense infiltrates of mast cells (≥15 mast cells in aggregates) in bone marrow biopsies and/or other extracutaneous organ sections",
                        "met": True,
                        "details": "Multifocal dense infiltrates of mast cells (≥15 cells in aggregates) present in bone marrow and/or extracutaneous organs"
                    },
                    "minor_criterion_1": {
                        "description": "≥25% of mast cells are atypical (type I or II) on bone marrow smears or spindle-shaped in mast cell infiltrates",
                        "met": True,
                        "details": "≥25% of mast cells show atypical morphology (type I/II) or spindle-shaped appearance"
                    },
                    "minor_criterion_2": {
                        "description": "KIT-activating point mutations at codon 816 (usually D816V) or other critical KIT regions",
                        "met": True,
                        "details": "KIT D816V mutation detected (most common activating mutation in systemic mastocytosis)"
                    },
                    "minor_criterion_3": {
                        "description": "Mast cells express CD2 and/or CD25 and/or CD30 (aberrant phenotype) in addition to normal mast cell markers",
                        "met": True,
                        "details": "Mast cells express aberrant markers (CD2/CD25/CD30) by flow cytometry or immunohistochemistry"
                    },
                    "minor_criterion_4": {
                        "description": "Baseline serum tryptase concentration >20 ng/mL (in absence of associated myeloid neoplasm)",
                        "met": True,
                        "details": "Serum tryptase 45.2 ng/mL > 20.0 ng/mL threshold, no associated myeloid neoplasm"
                    }
                },
                "detailed_analysis": {
                    "criteria_summary": {
                        "major_criteria": "1/1 met",
                        "minor_criteria": "4/4 met",
                        "diagnosis_requirement": "1 major criterion + 1 minor criterion OR 3 minor criteria"
                    },
                    "clinical_recommendations": [
                        "Refer to hematology-oncology for specialized management and staging",
                        "Perform disease subtype classification (indolent, smoldering, aggressive, etc.)",
                        "Assess for organ involvement and functional impairment",
                        "Consider bone marrow cytogenetics to evaluate for associated hematologic neoplasm",
                        "Screen for mediator release symptoms and treat accordingly"
                    ],
                    "laboratory_interpretation": {
                        "tryptase_analysis": {
                            "value": "45.2 ng/mL",
                            "normal_range": "<11.4 ng/mL",
                            "threshold": ">20.0 ng/mL",
                            "elevated": True,
                            "meets_criterion": True,
                            "degree_elevation": "moderate"
                        },
                        "molecular_testing": {
                            "kit_mutation": "d816v_positive",
                            "significance": "KIT D816V most common in systemic mastocytosis"
                        }
                    }
                }
            }
        }