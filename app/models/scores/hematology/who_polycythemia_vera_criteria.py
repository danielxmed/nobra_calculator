"""
WHO Diagnostic Criteria for Polycythemia Vera (2016) Models

Request and response models for WHO 2016 polycythemia vera diagnostic criteria.

References (Vancouver style):
1. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
   Organization classification of myeloid neoplasms and acute leukemia. Blood. 
   2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
2. Barbui T, Thiele J, Gisslinger H, et al. The 2016 WHO classification and diagnostic 
   criteria for myeloproliferative neoplasms: document summary and in-depth discussion. 
   Blood Cancer J. 2018;8(2):15. doi: 10.1038/s41408-018-0054-y
3. Tefferi A, Barbui T. Polycythemia vera and essential thrombocythemia: 2021 update 
   on diagnosis, risk-stratification and management. Am J Hematol. 2020;95(12):1599-1613. 
   doi: 10.1002/ajh.26008
4. Alvarez-Larrán A, Kerguelen A, Hernández-Boluda JC, et al. Frequency and prognostic 
   value of resistance/intolerance to hydroxycarbamide in 890 patients with polycythaemia 
   vera. Br J Haematol. 2016;172(5):786-793. doi: 10.1111/bjh.13884

The WHO 2016 criteria for polycythemia vera require either 3 major criteria OR 
2 major criteria + 1 minor criterion for diagnosis. These revised criteria were 
designed to detect "masked polycythemia vera" cases that were missed by the 2008 
criteria, which had higher hemoglobin thresholds and resulted in significant 
false negatives. The 2016 criteria lowered hemoglobin thresholds and introduced 
hematocrit cutoffs as alternative diagnostic parameters.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any, List


class WhoPolycythemiaVeraCriteriaRequest(BaseModel):
    """
    Request model for WHO 2016 Diagnostic Criteria for Polycythemia Vera
    
    The WHO 2016 criteria evaluate polycythemia vera diagnosis using 3 major criteria 
    and 1 minor criterion. Diagnosis requires either:
    - All 3 major criteria, OR
    - 2 major criteria + 1 minor criterion
    
    **MAJOR CRITERIA:**
    
    1. **Hemoglobin/Hematocrit/Red Cell Mass Criterion:**
       - Hemoglobin >16.5 g/dL (men) or >16.0 g/dL (women), OR
       - Hematocrit >49% (men) or >48% (women), OR  
       - Red cell mass >25% above mean normal predicted value
    
    2. **Bone Marrow Hypercellularity:**
       - Bone marrow biopsy showing hypercellularity for age with trilineage growth
       - Prominent erythroid, granulocytic, and megakaryocytic proliferation
       - Pleomorphic, mature megakaryocytes (distinct from ET and PMF)
    
    3. **JAK2 Mutation:**
       - Presence of JAK2V617F mutation (~95% of PV patients), OR
       - JAK2 exon 12 mutation (~3% of PV patients)
    
    **MINOR CRITERION:**
    
    1. **Subnormal Serum Erythropoietin (EPO) Level:**
       - Helps distinguish primary from secondary polycythemia
       - EPO typically suppressed in PV due to autonomous red cell production
    
    **Key Changes from WHO 2008 Criteria:**
    - Lower hemoglobin thresholds (2008: >18.5 g/dL men, >16.5 g/dL women)
    - Introduction of hematocrit thresholds as alternative to hemoglobin
    - Bone marrow morphology elevated from minor to major criterion
    - EPO level changed from major to minor criterion
    
    **Clinical Significance:**
    The 2016 criteria detect ~46% more cases than 2008 criteria, particularly 
    identifying "masked PV" patients who would have been classified as 
    myeloproliferative neoplasm-unclassifiable (MPN-U) under previous criteria.
    
    **Laboratory Parameters:**
    
    Gender: Required for appropriate hemoglobin/hematocrit thresholds
    - male: Hemoglobin >16.5 g/dL, Hematocrit >49%
    - female: Hemoglobin >16.0 g/dL, Hematocrit >48%
    
    Hemoglobin: Blood hemoglobin concentration in g/dL
    - Normal ranges: Men 13.8-17.2 g/dL, Women 12.1-15.1 g/dL
    - PV threshold: Men >16.5 g/dL, Women >16.0 g/dL
    
    Hematocrit: Percentage of blood volume occupied by red blood cells
    - Normal ranges: Men 40.7-50.3%, Women 36.1-44.3%
    - PV threshold: Men >49%, Women >48%
    
    Red Cell Mass: Alternative measurement to Hgb/Hct
    - yes: >25% above mean normal predicted value
    - no: Within normal range or <25% elevation
    - not_measured: Test not performed
    
    Bone Marrow Biopsy: Essential for PV diagnosis
    - yes: Shows characteristic hypercellularity with trilineage growth
    - no: Normal or non-characteristic findings
    - not_performed: Biopsy not done (criterion cannot be met)
    
    JAK2 Mutation Testing: Critical molecular marker
    - jak2v617f_positive: JAK2V617F mutation detected (~95% of PV)
    - jak2_exon12_positive: JAK2 exon 12 mutation detected (~3% of PV)
    - negative: No JAK2 mutations found
    - not_tested: Molecular testing not performed
    
    Erythropoietin Level: Distinguishes primary from secondary polycythemia
    - subnormal: Below normal range (supports PV diagnosis)
    - normal: Within normal range
    - elevated: Above normal (suggests secondary polycythemia)
    - not_measured: EPO not tested
    
    References (Vancouver style):
    1. Arber DA, Orazi A, Hasserjian R, et al. The 2016 revision to the World Health 
    Organization classification of myeloid neoplasms and acute leukemia. Blood. 
    2016;127(20):2391-2405. doi: 10.1182/blood-2016-03-643544
    2. Barbui T, Thiele J, Gisslinger H, et al. The 2016 WHO classification and diagnostic 
    criteria for myeloproliferative neoplasms: document summary and in-depth discussion. 
    Blood Cancer J. 2018;8(2):15. doi: 10.1038/s41408-018-0054-y
    3. Tefferi A, Barbui T. Polycythemia vera and essential thrombocythemia: 2021 update 
    on diagnosis, risk-stratification and management. Am J Hematol. 2020;95(12):1599-1613. 
    doi: 10.1002/ajh.26008
    """
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender (affects hemoglobin and hematocrit diagnostic thresholds). Males: Hgb >16.5 g/dL, Hct >49%. Females: Hgb >16.0 g/dL, Hct >48%",
        example="male"
    )
    
    hemoglobin: float = Field(
        ...,
        description="Blood hemoglobin concentration in g/dL. WHO 2016 thresholds: >16.5 g/dL (men) or >16.0 g/dL (women) for polycythemia vera diagnosis",
        ge=5.0,
        le=25.0,
        example=17.2
    )
    
    hematocrit: float = Field(
        ...,
        description="Hematocrit percentage (red blood cell volume percentage). WHO 2016 thresholds: >49% (men) or >48% (women) for polycythemia vera diagnosis",
        ge=10.0,
        le=80.0,
        example=52.5
    )
    
    red_cell_mass_elevated: Literal["yes", "no", "not_measured"] = Field(
        ...,
        description="Red cell mass >25% above mean normal predicted value (alternative to hemoglobin/hematocrit criteria). 'yes' = elevated >25%, 'no' = normal/mildly elevated, 'not_measured' = test not performed",
        example="not_measured"
    )
    
    bone_marrow_hypercellular: Literal["yes", "no", "not_performed"] = Field(
        ...,
        description="Bone marrow biopsy showing hypercellularity for age with trilineage growth (erythroid, granulocytic, megakaryocytic proliferation). Required major criterion for PV diagnosis",
        example="yes"
    )
    
    jak2_mutation: Literal["jak2v617f_positive", "jak2_exon12_positive", "negative", "not_tested"] = Field(
        ...,
        description="JAK2 mutation status. JAK2V617F found in ~95% of PV patients, JAK2 exon 12 in ~3%. Either mutation satisfies major criterion 3",
        example="jak2v617f_positive"
    )
    
    erythropoietin_level: Literal["subnormal", "normal", "elevated", "not_measured"] = Field(
        ...,
        description="Serum erythropoietin (EPO) level status. Subnormal EPO supports PV diagnosis (minor criterion). Elevated EPO suggests secondary polycythemia",
        example="subnormal"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "gender": "male",
                "hemoglobin": 17.2,
                "hematocrit": 52.5,
                "red_cell_mass_elevated": "not_measured",
                "bone_marrow_hypercellular": "yes",
                "jak2_mutation": "jak2v617f_positive",
                "erythropoietin_level": "subnormal"
            }
        }


class WhoPolycythemiaVeraCriteriaResponse(BaseModel):
    """
    Response model for WHO 2016 Diagnostic Criteria for Polycythemia Vera
    
    The WHO 2016 criteria provide systematic evaluation for polycythemia vera diagnosis.
    Results are categorized as:
    
    **DIAGNOSIS CATEGORIES:**
    
    1. **diagnosis_met**: WHO criteria satisfied
       - 3 major criteria met, OR
       - 2 major criteria + 1 minor criterion met
       - Polycythemia vera diagnosis confirmed
    
    2. **probable_pv**: Partial criteria met
       - Some major criteria fulfilled but diagnosis incomplete
       - Additional testing needed to confirm/exclude PV
    
    3. **criteria_not_met**: Insufficient criteria
       - Current findings do not support PV diagnosis
       - Consider secondary causes or alternative conditions
    
    **CLINICAL MANAGEMENT IMPLICATIONS:**
    
    Diagnosis Met:
    - Initiate therapeutic phlebotomy (target hematocrit <45%)
    - Consider low-dose aspirin for thrombosis prevention
    - Evaluate for cytoreductive therapy in high-risk patients
    - Regular hematology-oncology follow-up
    - Monitor for disease progression/transformation
    
    Probable PV:
    - Complete missing diagnostic workup
    - Hematology consultation for expert evaluation
    - Consider therapeutic phlebotomy if symptomatic
    - Close monitoring of blood parameters
    
    Criteria Not Met:
    - Investigate secondary causes of erythrocytosis
    - Consider alternative myeloproliferative neoplasms
    - Evaluate for relative polycythemia
    - Specialist referral if erythrocytosis persists
    
    **PROGNOSTIC CONSIDERATIONS:**
    
    Polycythemia vera patients have:
    - Increased thrombotic risk (especially if untreated)
    - Risk of transformation to myelofibrosis (~15% at 15 years)
    - Small risk of acute leukemia transformation (~2-5% at 20 years)
    - Good overall prognosis with appropriate management
    - Near-normal life expectancy with modern treatment
    
    Reference: Arber DA, et al. Blood. 2016;127(20):2391-2405.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic assessment result based on WHO 2016 criteria evaluation (diagnosis_met, probable_pv, criteria_not_met)",
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
        example="WHO 2016 diagnostic criteria for polycythemia vera are MET. Patient fulfills 3 of 3 major criteria. Diagnosis of polycythemia vera is confirmed. Initiate appropriate management including phlebotomy, cytoreductive therapy as indicated, and monitoring for thrombotic complications. Consider referral to hematology-oncology for specialized care and risk stratification."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic stage or category based on criteria assessment",
        example="Polycythemia Vera Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage",
        example="WHO 2016 criteria met - diagnosis confirmed"
    )
    
    major_criteria_met: int = Field(
        ...,
        description="Number of major criteria fulfilled (0-3). Major criteria: (1) Hgb/Hct/RCM thresholds, (2) Bone marrow hypercellularity, (3) JAK2 mutation",
        ge=0,
        le=3,
        example=3
    )
    
    minor_criteria_met: int = Field(
        ...,
        description="Number of minor criteria fulfilled (0-1). Minor criterion: Subnormal serum erythropoietin level",
        ge=0,
        le=1,
        example=1
    )
    
    total_major_criteria: int = Field(
        ...,
        description="Total number of major criteria evaluated (always 3 for WHO 2016 criteria)",
        example=3
    )
    
    total_minor_criteria: int = Field(
        ...,
        description="Total number of minor criteria evaluated (always 1 for WHO 2016 criteria)",
        example=1
    )
    
    criteria_details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of each criterion assessment including descriptions, fulfillment status, and clinical details",
        example={
            "major_criterion_1": {
                "description": "Hemoglobin >16.5 g/dL (men) or >16.0 g/dL (women) OR Hematocrit >49% (men) or >48% (women) OR elevated red cell mass >25% above normal",
                "met": True,
                "details": "Hemoglobin criteria met: 17.2 > 16.5 g/dL; Hematocrit criteria met: 52.5 > 49%",
                "components": {
                    "hemoglobin": {"value": 17.2, "threshold": ">16.5 g/dL", "met": True},
                    "hematocrit": {"value": 52.5, "threshold": ">49%", "met": True}
                }
            }
        }
    )
    
    detailed_analysis: Dict[str, Any] = Field(
        ...,
        description="Comprehensive analysis including criteria summary, clinical recommendations, laboratory interpretation, differential diagnosis, and follow-up plans",
        example={
            "criteria_summary": {
                "major_criteria": "3/3 met",
                "minor_criteria": "1/1 met",
                "diagnosis_requirement": "3 major criteria OR 2 major + 1 minor criterion"
            },
            "clinical_recommendations": [
                "Initiate therapeutic phlebotomy to maintain hematocrit <45%",
                "Consider low-dose aspirin (81-100 mg daily) unless contraindicated",
                "Refer to hematology-oncology for specialized management"
            ],
            "laboratory_interpretation": {
                "hemoglobin_analysis": {"value": "17.2 g/dL", "elevated": True},
                "hematocrit_analysis": {"value": "52.5%", "elevated": True}
            }
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "diagnosis_met",
                "unit": "categorical",
                "interpretation": "WHO 2016 diagnostic criteria for polycythemia vera are MET. Patient fulfills 3 of 3 major criteria. Diagnosis of polycythemia vera is confirmed. Initiate appropriate management including phlebotomy, cytoreductive therapy as indicated, and monitoring for thrombotic complications. Consider referral to hematology-oncology for specialized care and risk stratification.",
                "stage": "Polycythemia Vera Diagnosed",
                "stage_description": "WHO 2016 criteria met - diagnosis confirmed",
                "major_criteria_met": 3,
                "minor_criteria_met": 1,
                "total_major_criteria": 3,
                "total_minor_criteria": 1,
                "criteria_details": {
                    "major_criterion_1": {
                        "description": "Hemoglobin >16.5 g/dL (men) or >16.0 g/dL (women) OR Hematocrit >49% (men) or >48% (women) OR elevated red cell mass >25% above normal",
                        "met": True,
                        "details": "Hemoglobin criteria met: 17.2 > 16.5 g/dL; Hematocrit criteria met: 52.5 > 49%"
                    },
                    "major_criterion_2": {
                        "description": "Bone marrow hypercellularity for age with trilineage growth including prominent erythroid, granulocytic, and megakaryocytic proliferation",
                        "met": True,
                        "details": "Bone marrow biopsy shows hypercellularity with trilineage growth"
                    },
                    "major_criterion_3": {
                        "description": "Presence of JAK2V617F or JAK2 exon 12 mutation",
                        "met": True,
                        "details": "JAK2V617F mutation detected"
                    },
                    "minor_criterion_1": {
                        "description": "Subnormal serum erythropoietin level",
                        "met": True,
                        "details": "Serum erythropoietin level is subnormal"
                    }
                },
                "detailed_analysis": {
                    "criteria_summary": {
                        "major_criteria": "3/3 met",
                        "minor_criteria": "1/1 met",
                        "diagnosis_requirement": "3 major criteria OR 2 major + 1 minor criterion"
                    },
                    "clinical_recommendations": [
                        "Initiate therapeutic phlebotomy to maintain hematocrit <45%",
                        "Consider low-dose aspirin (81-100 mg daily) unless contraindicated",
                        "Evaluate thrombotic risk factors and cardiovascular comorbidities",
                        "Refer to hematology-oncology for specialized management"
                    ],
                    "laboratory_interpretation": {
                        "hemoglobin_analysis": {
                            "value": "17.2 g/dL",
                            "threshold": ">16.5 g/dL (male)",
                            "elevated": True,
                            "degree_elevation": "mild"
                        },
                        "hematocrit_analysis": {
                            "value": "52.5%",
                            "threshold": ">49% (male)",
                            "elevated": True,
                            "degree_elevation": "mild"
                        }
                    }
                }
            }
        }