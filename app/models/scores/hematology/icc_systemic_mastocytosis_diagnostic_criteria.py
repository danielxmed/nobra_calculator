"""
International Consensus Classification (ICC) Diagnostic Criteria for Systemic Mastocytosis Models

Request and response models for ICC systemic mastocytosis diagnostic criteria calculation.

References (Vancouver style):
1. Leguit RJ, van der Linden MP, Jansen JH, Hebeda KM, Lam KH, Leenders WP, et al. The international 
   consensus classification of mastocytosis and related entities. Virchows Arch. 2023 Jan;482(1):99-112. 
   doi: 10.1007/s00428-022-03454-6.
2. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
   Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
   clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
3. Valent P, Akin C, Bonadonna P, Hartmann K, Alvarez-Twose I, Brockow K, et al. Updated Diagnostic 
   Criteria and Classification of Mast Cell Disorders: A Consensus Proposal. HemaSphere. 2021 Oct 29;5(11):e646. 
   doi: 10.1097/HS9.0000000000000646.

The International Consensus Classification (ICC) Diagnostic Criteria for Systemic Mastocytosis 
provide a systematic framework for diagnosing mast cell disorders based on morphological, 
immunophenotypic, and molecular criteria. Published in 2022, the ICC criteria refine the WHO 
classification system with enhanced diagnostic specificity. The diagnosis requires either the 
major criterion (multifocal dense mast cell infiltrates ≥15 cells in aggregates) OR at least 
3 minor criteria (atypical morphology, aberrant markers, KIT mutation, elevated tryptase). 
This classification system facilitates accurate diagnosis, appropriate staging, and treatment 
planning for patients with suspected systemic mastocytosis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IccSystemicMastocytosisDiagnosticCriteriaRequest(BaseModel):
    """
    Request model for ICC Diagnostic Criteria for Systemic Mastocytosis
    
    The ICC criteria use a systematic approach with one major and four minor criteria:
    
    Major Criterion:
    - Multifocal dense infiltrates of tryptase- and/or CD117-positive mast cells (≥15 mast cells 
      in aggregates) detected in sections of bone marrow and/or other extracutaneous organ(s)
    
    Minor Criteria:
    1. In bone marrow/extracutaneous organs, >25% of mast cells are spindle-shaped or have 
       atypical immature morphology
    2. Mast cells express additional markers CD25, CD2, or CD30 (in addition to standard markers)
    3. KIT D816V mutation or other activating KIT mutation detected in bone marrow, peripheral 
       blood, or other extracutaneous organs
    4. Elevated serum tryptase level persistently >20 ng/mL (not applicable in SM-AMN)
    
    Diagnostic Algorithm:
    - Systemic Mastocytosis diagnosed if: Major Criterion present OR ≥3 Minor Criteria present
    
    References (Vancouver style):
    1. Leguit RJ, van der Linden MP, Jansen JH, Hebeda KM, Lam KH, Leenders WP, et al. The international 
    consensus classification of mastocytosis and related entities. Virchows Arch. 2023 Jan;482(1):99-112. 
    doi: 10.1007/s00428-022-03454-6.
    2. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
    Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
    clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
    3. Valent P, Akin C, Bonadonna P, Hartmann K, Alvarez-Twose I, Brockow K, et al. Updated Diagnostic 
    Criteria and Classification of Mast Cell Disorders: A Consensus Proposal. HemaSphere. 2021 Oct 29;5(11):e646. 
    doi: 10.1097/HS9.0000000000000646.
    """
    
    multifocal_mast_cell_infiltrates: Literal["present", "absent"] = Field(
        ...,
        description="Multifocal dense infiltrates of tryptase- and/or CD117-positive mast cells (≥15 mast cells in aggregates) detected in sections of bone marrow and/or other extracutaneous organ(s) - MAJOR CRITERION. Requires adequate bone marrow biopsy specimen with immunohistochemical staining",
        example="present"
    )
    
    atypical_mast_cell_morphology: Literal["yes", "no"] = Field(
        ...,
        description="In bone marrow/extracutaneous organs, >25% of mast cells are spindle-shaped or have atypical immature morphology - MINOR CRITERION 1. Atypical features include elongated shape, hypogranular cytoplasm, and immature nuclear features",
        example="yes"
    )
    
    aberrant_mast_cell_markers: Literal["yes", "no"] = Field(
        ...,
        description="Mast cells express additional markers CD25, CD2, or CD30 in addition to standard mast cell markers (tryptase, CD117) - MINOR CRITERION 2. Assessed by flow cytometry or immunohistochemistry on bone marrow or tissue specimens",
        example="yes"
    )
    
    kit_mutation_detected: Literal["yes", "no"] = Field(
        ...,
        description="KIT D816V mutation or other activating KIT mutation detected in bone marrow, peripheral blood, or other extracutaneous organs - MINOR CRITERION 3. High-sensitivity PCR recommended with variant allele frequency (VAF) ≥1%",
        example="yes"
    )
    
    elevated_serum_tryptase: Literal["yes", "no"] = Field(
        ...,
        description="Elevated serum tryptase level persistently >20 ng/mL - MINOR CRITERION 4. Not applicable in SM with associated myeloid neoplasm (SM-AMN). Baseline tryptase should be measured when not acutely symptomatic",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "multifocal_mast_cell_infiltrates": "present",
                "atypical_mast_cell_morphology": "yes",
                "aberrant_mast_cell_markers": "yes",
                "kit_mutation_detected": "yes",
                "elevated_serum_tryptase": "no"
            }
        }


class IccSystemicMastocytosisDiagnosticCriteriaResponse(BaseModel):
    """
    Response model for ICC Diagnostic Criteria for Systemic Mastocytosis
    
    The diagnostic outcome is determined by the presence of the major criterion 
    OR at least 3 minor criteria:
    
    Diagnostic Categories:
    - Systemic Mastocytosis Diagnosed: ICC criteria met (major criterion OR ≥3 minor criteria)
    - Systemic Mastocytosis Not Diagnosed: ICC criteria not met
    
    Clinical Implications:
    - Diagnosed: Requires subtype classification and staging evaluation
    - Not Diagnosed: Consider alternative diagnoses and additional testing
    
    Systemic Mastocytosis Subtypes (require additional evaluation):
    - Indolent SM (ISM): Most common, good prognosis
    - Smoldering SM (SSM): Intermediate features
    - Aggressive SM (ASM): Organ dysfunction
    - Mast Cell Leukemia (MCL): Rare, poor prognosis
    - SM with Associated Myeloid Neoplasm (SM-AMN): Concurrent myeloid disorder
    
    Reference: Leguit RJ, et al. Virchows Arch. 2023;482(1):99-112.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on ICC criteria evaluation (Systemic Mastocytosis Diagnosed or Systemic Mastocytosis Not Diagnosed)",
        example="Systemic Mastocytosis Diagnosed"
    )
    
    unit: None = Field(
        None,
        description="No unit applicable for diagnostic result"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with diagnostic implications and management recommendations based on ICC criteria evaluation",
        example="Diagnosis of systemic mastocytosis established according to ICC criteria. Requires comprehensive staging evaluation including bone marrow biopsy, imaging studies, and laboratory assessment. Consider subtype classification (ISM, SSM, ASM, MCL, SM-AMN) based on additional clinical and laboratory findings. Evaluate for organ dysfunction and associated symptoms including mediator-related symptoms, organomegaly, cytopenias, and osteoporosis. Discuss treatment options including symptom management with antihistamines and mast cell stabilizers, cytoreductive therapy, or targeted therapies (KIT inhibitors) based on subtype and severity."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (Systemic Mastocytosis Diagnosed or Systemic Mastocytosis Not Diagnosed)",
        example="Systemic Mastocytosis Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category",
        example="ICC Criteria Met"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Systemic Mastocytosis Diagnosed",
                "unit": None,
                "interpretation": "Diagnosis of systemic mastocytosis established according to ICC criteria. Requires comprehensive staging evaluation including bone marrow biopsy, imaging studies, and laboratory assessment. Consider subtype classification (ISM, SSM, ASM, MCL, SM-AMN) based on additional clinical and laboratory findings. Evaluate for organ dysfunction and associated symptoms including mediator-related symptoms, organomegaly, cytopenias, and osteoporosis. Discuss treatment options including symptom management with antihistamines and mast cell stabilizers, cytoreductive therapy, or targeted therapies (KIT inhibitors) based on subtype and severity.",
                "stage": "Systemic Mastocytosis Diagnosed",
                "stage_description": "ICC Criteria Met"
            }
        }