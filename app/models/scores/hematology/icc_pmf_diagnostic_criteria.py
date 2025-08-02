"""
International Consensus Classification (ICC) Diagnostic Criteria for Primary Myelofibrosis (PMF) Models

Request and response models for ICC PMF diagnostic criteria calculation.

References (Vancouver style):
1. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
   Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
   clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
2. Tefferi A, Guglielmelli P, Larson DR, Finke C, Wassie EA, Pieri L, et al. Long-term survival 
   and blast transformation in molecularly annotated essential thrombocythemia, polycythemia vera, 
   and myelofibrosis. Blood. 2014 Oct 16;124(16):2507-13. doi: 10.1182/blood-2014-05-579136.
3. Barbui T, Thiele J, Gisslinger H, Kvasnicka HM, Vannucchi AM, Guglielmelli P, et al. The 2016 
   WHO classification and diagnostic criteria for myeloproliferative neoplasms: document summary 
   and in-depth discussion. Blood Cancer J. 2018 Feb 15;8(2):15. doi: 10.1038/s41408-018-0054-y.

The International Consensus Classification (ICC) Diagnostic Criteria for Primary Myelofibrosis 
provide a systematic framework for diagnosing PMF based on morphological, genetic, and clinical 
criteria. Published in 2022, the ICC criteria distinguish between prefibrotic (early) and overt 
(fibrotic) stages of PMF. The diagnosis requires all three major criteria plus at least one minor 
criterion, confirmed in two consecutive determinations. This classification system enhances 
diagnostic accuracy and facilitates appropriate staging and treatment planning.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IccPmfDiagnosticCriteriaRequest(BaseModel):
    """
    Request model for ICC Diagnostic Criteria for Primary Myelofibrosis
    
    The ICC criteria use a systematic approach with major and minor criteria:
    
    Major Criteria (ALL must be present):
    1. Bone marrow morphology: Megakaryocytic proliferation and atypia
    2. Genetic clonality: JAK2, CALR, or MPL mutation, or other clonal marker
    3. Exclusion criteria: Reactive fibrosis and other myeloproliferative neoplasms excluded
    
    Minor Criteria (≥1 must be present):
    - Anemia not attributable to comorbid conditions
    - Leukocytosis ≥11 × 10^9/L
    - Palpable splenomegaly
    - Lactate dehydrogenase above reference range
    
    Staging Based on Fibrosis Grade:
    - Prefibrotic PMF: Bone marrow fibrosis grade 0-1
    - Overt PMF: Bone marrow fibrosis grade 2-3
    
    References (Vancouver style):
    1. Arber DA, Orazi A, Hasserjian RP, Borowitz MJ, Calvo KR, Kvasnicka HM, et al. International 
    Consensus Classification of Myeloid Neoplasms and Acute Leukemias: integrating morphologic, 
    clinical, and genomic data. Blood. 2022 Sep 15;140(11):1200-1228. doi: 10.1182/blood.2022015850.
    2. Tefferi A, Guglielmelli P, Larson DR, Finke C, Wassie EA, Pieri L, et al. Long-term survival 
    and blast transformation in molecularly annotated essential thrombocythemia, polycythemia vera, 
    and myelofibrosis. Blood. 2014 Oct 16;124(16):2507-13. doi: 10.1182/blood-2014-05-579136.
    3. Barbui T, Thiele J, Gisslinger H, Kvasnicka HM, Vannucchi AM, Guglielmelli P, et al. The 2016 
    WHO classification and diagnostic criteria for myeloproliferative neoplasms: document summary 
    and in-depth discussion. Blood Cancer J. 2018 Feb 15;8(2):15. doi: 10.1038/s41408-018-0054-y.
    """
    
    bone_marrow_megakaryocytic_proliferation: Literal["present", "absent"] = Field(
        ...,
        description="Presence of megakaryocytic proliferation and atypia on bone marrow biopsy (Major Criterion 1). This includes increased megakaryocyte density with atypical morphology and clustering",
        example="present"
    )
    
    bone_marrow_fibrosis_grade: Literal["grade_0_1", "grade_2_3"] = Field(
        ...,
        description="Bone marrow reticulin and/or collagen fibrosis grade using WHO grading scale. Grade 0-1 indicates prefibrotic stage, Grade 2-3 indicates overt fibrotic stage. Assessment requires adequate bone marrow biopsy specimen",
        example="grade_0_1"
    )
    
    genetic_mutation_present: Literal["yes", "no"] = Field(
        ...,
        description="Presence of JAK2 V617F, CALR exon 9, MPL exon 10 mutation, or another clonal genetic marker (Major Criterion 2). High-sensitivity assays with VAF ≥1% recommended for detection",
        example="yes"
    )
    
    reactive_fibrosis_excluded: Literal["yes", "no"] = Field(
        ...,
        description="Reactive bone marrow fibrosis due to infection, autoimmune disorder, hairy cell leukemia, metastatic malignancy, or drug-induced causes excluded (Part of Major Criterion 3)",
        example="yes"
    )
    
    other_mpn_excluded: Literal["yes", "no"] = Field(
        ...,
        description="Essential thrombocythemia, polycythemia vera, BCR::ABL1-positive chronic myeloid leukemia, myelodysplastic syndromes, and other myeloid neoplasms excluded (Part of Major Criterion 3)",
        example="yes"
    )
    
    anemia_present: Literal["yes", "no"] = Field(
        ...,
        description="Anemia not attributable to comorbid conditions such as iron deficiency, chronic kidney disease, chronic inflammation, or hemolysis (Minor Criterion). Use age and sex-adjusted reference ranges",
        example="no"
    )
    
    leukocytosis_present: Literal["yes", "no"] = Field(
        ...,
        description="White blood cell count ≥11 × 10^9/L (Minor Criterion). Should not be attributable to infection, inflammation, or other secondary causes",
        example="yes"
    )
    
    splenomegaly_present: Literal["yes", "no"] = Field(
        ...,
        description="Palpable splenomegaly on physical examination (Minor Criterion). Imaging studies may supplement clinical assessment but palpable splenomegaly is the primary criterion",
        example="yes"
    )
    
    elevated_ldh: Literal["yes", "no"] = Field(
        ...,
        description="Lactate dehydrogenase level above institutional upper limit of normal reference range (Minor Criterion). Should not be attributable to hemolysis, tissue necrosis, or other secondary causes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bone_marrow_megakaryocytic_proliferation": "present",
                "bone_marrow_fibrosis_grade": "grade_0_1",
                "genetic_mutation_present": "yes",
                "reactive_fibrosis_excluded": "yes",
                "other_mpn_excluded": "yes",
                "anemia_present": "no",
                "leukocytosis_present": "yes",
                "splenomegaly_present": "yes",
                "elevated_ldh": "no"
            }
        }


class IccPmfDiagnosticCriteriaResponse(BaseModel):
    """
    Response model for ICC Diagnostic Criteria for Primary Myelofibrosis
    
    The diagnostic outcome is determined by the presence of all major criteria 
    plus at least one minor criterion:
    
    Diagnostic Categories:
    - Pre-PMF Diagnosed: Prefibrotic primary myelofibrosis (fibrosis grade 0-1)
    - Overt PMF Diagnosed: Overt fibrotic primary myelofibrosis (fibrosis grade 2-3)
    - PMF Not Diagnosed: Diagnostic criteria not met
    
    Clinical Implications:
    - Pre-PMF: Early stage requiring monitoring and risk stratification
    - Overt PMF: Advanced stage requiring comprehensive evaluation and treatment planning
    - Not Diagnosed: Consider alternative diagnoses and additional testing
    
    Reference: Arber DA, et al. Blood. 2022;140(11):1200-1228.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic result based on ICC criteria evaluation (Pre-PMF Diagnosed, Overt PMF Diagnosed, or PMF Not Diagnosed)",
        example="Pre-PMF Diagnosed"
    )
    
    unit: None = Field(
        None,
        description="No unit applicable for diagnostic result"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with diagnostic implications and management recommendations based on ICC criteria evaluation",
        example="Diagnosis of prefibrotic (early) primary myelofibrosis established. Early stage with megakaryocytic proliferation but minimal fibrosis (grade 0-1). Requires close hematologic monitoring and staging workup. Consider risk stratification with prognostic scoring systems (IPSS-R, GIPSS). Regular surveillance for disease progression to overt fibrotic stage. Discuss treatment options including observation, symptom management, or therapeutic intervention based on risk profile and symptoms."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage or category (Pre-PMF Diagnosed, Overt PMF Diagnosed, PMF Not Diagnosed)",
        example="Pre-PMF Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category",
        example="Prefibrotic Primary Myelofibrosis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Pre-PMF Diagnosed",
                "unit": None,
                "interpretation": "Diagnosis of prefibrotic (early) primary myelofibrosis established. Early stage with megakaryocytic proliferation but minimal fibrosis (grade 0-1). Requires close hematologic monitoring and staging workup. Consider risk stratification with prognostic scoring systems (IPSS-R, GIPSS). Regular surveillance for disease progression to overt fibrotic stage. Discuss treatment options including observation, symptom management, or therapeutic intervention based on risk profile and symptoms.",
                "stage": "Pre-PMF Diagnosed",
                "stage_description": "Prefibrotic Primary Myelofibrosis"
            }
        }