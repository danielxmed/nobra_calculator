"""
Multiple Myeloma Diagnostic Criteria (IMWG) Models

Request and response models for Multiple Myeloma Diagnostic Criteria calculation.

References (Vancouver style):
1. Rajkumar SV, Dimopoulos MA, Palumbo A, Blade J, Merlini G, Mateos MV, et al. 
   International Myeloma Working Group updated criteria for the diagnosis of multiple 
   myeloma. Lancet Oncol. 2014;15(12):e538-48. doi: 10.1016/S1470-2045(14)70442-5.
2. Kumar S, Paiva B, Anderson KC, Durie B, Landgren O, Moreau P, et al. International 
   Myeloma Working Group consensus criteria for response and minimal residual disease 
   assessment in multiple myeloma. Lancet Oncol. 2016;17(8):e328-e346. 
   doi: 10.1016/S1470-2045(16)30206-6.
3. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. 
   Revised International Staging System for Multiple Myeloma: A Report From International 
   Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-9. doi: 10.1200/JCO.2015.61.2267.

The International Myeloma Working Group (IMWG) diagnostic criteria for multiple myeloma 
require both clonal plasma cell evidence AND myeloma defining events. The 2014 update 
introduced SLiM biomarkers (60% plasma cells, Light chain ratio ≥100, MRI >1 focal lesion) 
alongside traditional CRAB criteria (Calcium, Renal, Anemia, Bone) to allow earlier 
diagnosis before end-organ damage occurs.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MultipleMyelomaDiagnosticCriteriaRequest(BaseModel):
    """
    Request model for Multiple Myeloma Diagnostic Criteria (IMWG)
    
    The IMWG criteria require BOTH:
    A) Clonal Plasma Cell Evidence (≥1 required):
       - Clonal bone marrow plasma cells ≥10%, OR  
       - Biopsy-proven bony or extramedullary plasmacytoma
    
    B) Myeloma Defining Events (≥1 required):
       - CRAB Criteria (traditional end-organ damage):
         * Hypercalcemia: Serum calcium >1 mg/dL above normal or >11 mg/dL
         * Renal insufficiency: Creatinine clearance <40 mL/min or serum creatinine >2 mg/dL  
         * Anemia: Hemoglobin >2 g/dL below normal or <10 g/dL
         * Bone lesions: ≥1 osteolytic lesion on imaging
       - SLiM Biomarkers (2014 update - biomarkers of malignancy):
         * 60% or more clonal bone marrow plasma cells
         * Involved:uninvolved serum free light chain ratio ≥100
         * >1 focal lesion on MRI studies
    
    Clinical Applications:
    - Distinguishes multiple myeloma from MGUS and smoldering myeloma
    - Allows earlier treatment before end-organ damage (SLiM criteria)
    - Guides appropriate staging and treatment planning
    - Helps identify patients who would benefit from immediate therapy
    
    Key Updates (2014 IMWG Revision):
    - Added SLiM biomarkers to allow diagnosis without end-organ damage
    - Maintained traditional CRAB criteria for established disease
    - Emphasized need for clonal plasma cell confirmation
    - Clarified imaging requirements for bone disease assessment
    
    References (Vancouver style):
    1. Rajkumar SV, Dimopoulos MA, Palumbo A, Blade J, Merlini G, Mateos MV, et al. 
    International Myeloma Working Group updated criteria for the diagnosis of multiple 
    myeloma. Lancet Oncol. 2014;15(12):e538-48. doi: 10.1016/S1470-2045(14)70442-5.
    2. Kumar S, Paiva B, Anderson KC, Durie B, Landgren O, Moreau P, et al. International 
    Myeloma Working Group consensus criteria for response and minimal residual disease 
    assessment in multiple myeloma. Lancet Oncol. 2016;17(8):e328-e346. 
    doi: 10.1016/S1470-2045(16)30206-6.
    3. Palumbo A, Avet-Loiseau H, Oliva S, Lokhorst HM, Goldschmidt H, Rosinol L, et al. 
    Revised International Staging System for Multiple Myeloma: A Report From International 
    Myeloma Working Group. J Clin Oncol. 2015;33(26):2863-9. doi: 10.1200/JCO.2015.61.2267.
    """
    
    clonal_plasma_cells_bone_marrow: Literal["yes", "no"] = Field(
        ...,
        description="Clonal bone marrow plasma cells ≥10%. Confirmed by flow cytometry, immunohistochemistry, or immunofluorescence. Part of required clonal plasma cell evidence",
        example="yes"
    )
    
    biopsy_proven_plasmacytoma: Literal["yes", "no"] = Field(
        ...,
        description="Biopsy-proven bony or extramedullary plasmacytoma. Tissue diagnosis required. Alternative to bone marrow plasma cells for clonal evidence",
        example="no"
    )
    
    hypercalcemia: Literal["yes", "no"] = Field(
        ...,
        description="Hypercalcemia: Serum calcium >1 mg/dL above upper limit of normal or >11 mg/dL. Part of CRAB criteria for end-organ damage",
        example="no"
    )
    
    renal_insufficiency: Literal["yes", "no"] = Field(
        ...,
        description="Renal insufficiency: Creatinine clearance <40 mL/min or serum creatinine >2 mg/dL. Part of CRAB criteria for kidney damage",
        example="yes"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Anemia: Hemoglobin >2 g/dL below lower limit of normal or <10 g/dL. Part of CRAB criteria for hematologic impact",
        example="yes"
    )
    
    bone_lesions: Literal["yes", "no"] = Field(
        ...,
        description="Bone lesions: ≥1 osteolytic lesion on skeletal radiography, CT, or PET-CT. Part of CRAB criteria for bone disease",
        example="no"
    )
    
    plasma_cells_60_percent: Literal["yes", "no"] = Field(
        ...,
        description="Clonal bone marrow plasma cells ≥60%. Part of SLiM biomarkers (2014 update) allowing diagnosis without end-organ damage",
        example="no"
    )
    
    light_chain_ratio: Literal["yes", "no"] = Field(
        ...,
        description="Involved:uninvolved serum free light chain ratio ≥100. Part of SLiM biomarkers indicating high malignant potential",
        example="no"
    )
    
    focal_mri_lesions: Literal["yes", "no"] = Field(
        ...,
        description=">1 focal lesion on MRI studies. Part of SLiM biomarkers for detecting early bone involvement before osteolytic changes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clonal_plasma_cells_bone_marrow": "yes",
                "biopsy_proven_plasmacytoma": "no", 
                "hypercalcemia": "no",
                "renal_insufficiency": "yes",
                "anemia": "yes",
                "bone_lesions": "no",
                "plasma_cells_60_percent": "no",
                "light_chain_ratio": "no",
                "focal_mri_lesions": "no"
            }
        }


class MultipleMyelomaDiagnosticCriteriaResponse(BaseModel):
    """
    Response model for Multiple Myeloma Diagnostic Criteria (IMWG)
    
    The IMWG diagnostic criteria provide a binary diagnostic decision (Multiple Myeloma 
    vs Not Diagnostic) based on the presence of both clonal plasma cell evidence AND 
    myeloma defining events.
    
    Diagnostic Categories:
    
    Multiple Myeloma:
    - Meets IMWG criteria requiring both clonal evidence AND myeloma defining events
    - Requires immediate staging (ISS/R-ISS), cytogenetic analysis, and treatment planning
    - May present with traditional CRAB criteria (end-organ damage) or SLiM biomarkers
    - Indicates need for hematologic oncology consultation and treatment initiation
    
    Not Diagnostic:
    - Does not meet full IMWG criteria for multiple myeloma diagnosis
    - May suggest MGUS (monoclonal gammopathy of undetermined significance)
    - Could indicate smoldering multiple myeloma requiring monitoring
    - Needs continued surveillance and repeat evaluation as clinically indicated
    
    Clinical Management by Diagnostic Result:
    
    Multiple Myeloma Diagnosis:
    - Immediate hematologic oncology consultation
    - Complete staging workup including ISS/R-ISS staging system
    - Cytogenetic analysis and FISH studies for risk stratification
    - Bone marrow biopsy with flow cytometry if not already performed
    - Complete metabolic panel, LDH, beta-2 microglobulin, albumin
    - Serum protein electrophoresis (SPEP) and immunofixation
    - Serum and urine free light chain assays
    - Imaging studies (whole-body MRI or PET-CT preferred)
    - Assessment of performance status and comorbidities
    - Treatment planning based on eligibility for autologous stem cell transplant
    - Consider clinical trial enrollment if appropriate
    
    Not Diagnostic Result:
    - Serial monitoring with SPEP, immunofixation, and serum free light chains
    - Annual follow-up or sooner if clinical symptoms develop
    - Patient education regarding plasma cell disorders and warning signs
    - Consider repeat bone marrow biopsy if clinical suspicion remains high
    - Monitor for progression to symptomatic multiple myeloma
    - Baseline imaging studies for future comparison
    - Regular assessment of kidney function, calcium, and complete blood count
    
    Important Considerations:
    - The criteria distinguish symptomatic multiple myeloma requiring treatment
    - SLiM biomarkers allow earlier diagnosis before end-organ damage
    - Concurrent medical conditions may complicate interpretation
    - Multidisciplinary evaluation is essential for optimal management
    - Regular monitoring is critical regardless of initial diagnostic outcome
    
    Reference: Rajkumar SV, et al. Lancet Oncol. 2014;15(12):e538-48.
    """
    
    result: str = Field(
        ...,
        description="Diagnostic assessment result (Multiple Myeloma or Not Diagnostic)",
        example="Multiple Myeloma"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for diagnostic criteria)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed diagnostic interpretation with clinical recommendations and next steps",
        example="DIAGNOSIS: Multiple myeloma according to IMWG criteria. CLONAL EVIDENCE: clonal bone marrow plasma cells ≥10%. CRAB CRITERIA: renal insufficiency, anemia. NEXT STEPS: Proceed with staging (ISS/R-ISS), cytogenetic analysis, and treatment planning. Consider bone marrow biopsy if not already performed, serum protein electrophoresis, immunofixation, serum free light chains, LDH, beta-2 microglobulin, and albumin. Imaging studies including whole-body MRI or PET-CT may be indicated. Multidisciplinary hematologic consultation is recommended for treatment planning. The patient requires immediate oncologic evaluation and staging workup."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (Multiple Myeloma or Not Diagnostic)",
        example="Multiple Myeloma"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic result",
        example="Criteria met for multiple myeloma"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Multiple Myeloma",
                "unit": "",
                "interpretation": "DIAGNOSIS: Multiple myeloma according to IMWG criteria. CLONAL EVIDENCE: clonal bone marrow plasma cells ≥10%. CRAB CRITERIA: renal insufficiency, anemia. NEXT STEPS: Proceed with staging (ISS/R-ISS), cytogenetic analysis, and treatment planning. Consider bone marrow biopsy if not already performed, serum protein electrophoresis, immunofixation, serum free light chains, LDH, beta-2 microglobulin, and albumin. Imaging studies including whole-body MRI or PET-CT may be indicated. Multidisciplinary hematologic consultation is recommended for treatment planning. The patient requires immediate oncologic evaluation and staging workup.",
                "stage": "Multiple Myeloma",
                "stage_description": "Criteria met for multiple myeloma"
            }
        }