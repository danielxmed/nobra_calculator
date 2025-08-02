"""
Multiple Myeloma Response Criteria (IMWG) Models

Request and response models for Multiple Myeloma Response Criteria calculation.

References (Vancouver style):
1. Kumar S, Paiva B, Anderson KC, Durie B, Landgren O, Moreau P, et al. International 
   Myeloma Working Group consensus criteria for response and minimal residual disease 
   assessment in multiple myeloma. Lancet Oncol. 2016;17(8):e328-e346. 
   doi: 10.1016/S1470-2045(16)30206-6.
2. Durie BG, Harousseau JL, Miguel JS, Bladé J, Barlogie B, Anderson K, et al. 
   International uniform response criteria for multiple myeloma. Leukemia. 2006;20(9):1467-73. 
   doi: 10.1038/sj.leu.2404284.
3. Rajkumar SV, Harousseau JL, Durie B, Anderson KC, Dimopoulos M, Kyle R, et al. 
   Consensus guidelines for the uniform reporting of clinical trials: report of the 
   International Myeloma Workshop Consensus Panel 1. Blood. 2011;117(18):4691-5. 
   doi: 10.1182/blood-2010-10-299487.

The International Myeloma Working Group (IMWG) response criteria provide standardized 
assessment of treatment response in multiple myeloma. These criteria define six response 
categories from Stringent Complete Response (best) to Progressive Disease (worst), enabling 
uniform evaluation across clinical trials and treatment settings.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class MultipleMyelomaResponseCriteriaRequest(BaseModel):
    """
    Request model for Multiple Myeloma Response Criteria (IMWG)
    
    The IMWG response criteria evaluate treatment response using multiple parameters:
    
    Core Required Parameters:
    - Serum immunofixation: More sensitive than electrophoresis for detecting M protein
    - Urine immunofixation: Detects urinary light chain excretion
    - Bone marrow plasma cells: Percentage of clonal plasma cells in bone marrow
    - Soft tissue plasmacytomas: Presence of extramedullary disease masses
    
    Additional Parameters for Complete Assessment:
    - Free light chain ratio: Serum kappa/lambda or lambda/kappa ratio (normal 0.26-1.65)
    - Clonal cells in bone marrow: Detected by immunohistochemistry/immunofluorescence
    - M protein reduction: Percentage decrease from baseline levels
    - Urine M protein: 24-hour urinary protein excretion
    - Electrophoresis detectability: Whether M component visible on protein electrophoresis
    - Plasmacytoma size reduction: Percentage decrease in soft tissue masses
    
    Response Categories:
    
    Stringent Complete Response (sCR):
    - All CR criteria PLUS normal free light chain ratio AND absence of clonal cells
    - Best possible response with undetectable disease by all methods
    - Associated with longest progression-free and overall survival
    
    Complete Response (CR):
    - Negative serum and urine immunofixation
    - <5% plasma cells in bone marrow
    - Disappearance of soft tissue plasmacytomas
    - Excellent prognosis with extended remission duration
    
    Very Good Partial Response (VGPR):
    - M component detectable by immunofixation but not electrophoresis, OR
    - ≥90% reduction in serum M component plus urine M protein <100 mg/24h
    - Represents minimal residual disease with good outcomes
    
    Partial Response (PR):
    - ≥50% reduction in serum M protein
    - ≥90% reduction in urine M protein (or <200 mg/24h)
    - ≥50% reduction in plasmacytoma size if present
    - Meaningful clinical benefit requiring continued therapy
    
    Stable Disease (SD):
    - Does not meet criteria for other response categories
    - May represent disease control or insufficient response
    
    Progressive Disease (PD):
    - 25% increase from lowest achieved response
    - New bone lesions or hypercalcemia
    - Requires immediate treatment modification
    
    Clinical Applications:
    - Treatment response monitoring in clinical trials
    - Standardized assessment across institutions
    - Treatment decision-making and modification
    - Prognostic stratification and patient counseling
    - Regulatory approval of new therapies
    
    Validation and Implementation:
    - Used in major clinical trials worldwide
    - Endorsed by regulatory agencies (FDA, EMA)
    - Integrated into treatment guidelines (NCCN, ESMO)
    - Requires confirmation on two consecutive assessments
    - May be combined with minimal residual disease (MRD) testing
    
    References (Vancouver style):
    1. Kumar S, Paiva B, Anderson KC, Durie B, Landgren O, Moreau P, et al. International 
    Myeloma Working Group consensus criteria for response and minimal residual disease 
    assessment in multiple myeloma. Lancet Oncol. 2016;17(8):e328-e346. 
    doi: 10.1016/S1470-2045(16)30206-6.
    2. Durie BG, Harousseau JL, Miguel JS, Bladé J, Barlogie B, Anderson K, et al. 
    International uniform response criteria for multiple myeloma. Leukemia. 2006;20(9):1467-73. 
    doi: 10.1038/sj.leu.2404284.
    3. Rajkumar SV, Harousseau JL, Durie B, Anderson KC, Dimopoulos M, Kyle R, et al. 
    Consensus guidelines for the uniform reporting of clinical trials: report of the 
    International Myeloma Workshop Consensus Panel 1. Blood. 2011;117(18):4691-5. 
    doi: 10.1182/blood-2010-10-299487.
    """
    
    serum_immunofixation: Literal["negative", "positive"] = Field(
        ...,
        description="Serum immunofixation result. More sensitive than electrophoresis for detecting monoclonal proteins. Negative result required for Complete Response",
        example="negative"
    )
    
    urine_immunofixation: Literal["negative", "positive"] = Field(
        ...,
        description="Urine immunofixation result. Detects urinary light chain excretion. Negative result required for Complete Response",
        example="negative"
    )
    
    bone_marrow_plasma_cells: float = Field(
        ...,
        ge=0,
        le=100,
        description="Percentage of plasma cells in bone marrow biopsy. Must be <5% for Complete Response. Normal is typically <5%",
        example=3.2
    )
    
    soft_tissue_plasmacytomas: Literal["absent", "present"] = Field(
        ...,
        description="Presence of soft tissue plasmacytomas (extramedullary disease masses). Must be absent for Complete Response",
        example="absent"
    )
    
    free_light_chain_ratio: Optional[float] = Field(
        None,
        gt=0,
        le=1000,
        description="Serum free light chain ratio (involved/uninvolved or kappa/lambda). Normal range 0.26-1.65. Required for Stringent Complete Response assessment",
        example=0.8
    )
    
    clonal_cells_bone_marrow: Optional[Literal["absent", "present"]] = Field(
        None,
        description="Clonal cells in bone marrow detected by immunohistochemistry or immunofluorescence. Must be absent for Stringent Complete Response",
        example="absent"
    )
    
    serum_m_protein_reduction: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage reduction in serum M protein from baseline. ≥90% for VGPR, ≥50% for Partial Response",
        example=95.0
    )
    
    urine_m_protein_24h: Optional[float] = Field(
        None,
        ge=0,
        le=10000,
        description="24-hour urine M protein level in mg. <100 mg for VGPR, <200 mg for Partial Response",
        example=50.0
    )
    
    serum_electrophoresis_detectable: Optional[Literal["yes", "no"]] = Field(
        None,
        description="M component detectable by serum protein electrophoresis. Should be 'no' for VGPR if immunofixation positive",
        example="no"
    )
    
    plasmacytoma_reduction: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Percentage reduction in soft tissue plasmacytoma size from baseline. ≥50% required for Partial Response",
        example=75.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "serum_immunofixation": "negative",
                "urine_immunofixation": "negative",
                "bone_marrow_plasma_cells": 3.2,
                "soft_tissue_plasmacytomas": "absent",
                "free_light_chain_ratio": 0.8,
                "clonal_cells_bone_marrow": "absent",
                "serum_m_protein_reduction": 95.0,
                "urine_m_protein_24h": 50.0,
                "serum_electrophoresis_detectable": "no",
                "plasmacytoma_reduction": 75.0
            }
        }


class MultipleMyelomaResponseCriteriaResponse(BaseModel):
    """
    Response model for Multiple Myeloma Response Criteria (IMWG)
    
    The IMWG response assessment provides standardized evaluation of treatment response 
    with six distinct categories, each with specific clinical implications:
    
    Stringent Complete Response (sCR) - Best Possible Response:
    - All Complete Response criteria plus normal free light chain ratio and absence of clonal cells
    - Represents deepest remission with undetectable disease by all available methods
    - Associated with longest progression-free survival and overall survival
    - May be considered for treatment discontinuation in select cases
    - Monitoring every 3-6 months with comprehensive laboratory assessment
    
    Complete Response (CR) - Excellent Response:
    - Negative serum and urine immunofixation, <5% bone marrow plasma cells, no plasmacytomas
    - Excellent prognosis with extended remission duration
    - Consider evaluation for stringent CR if additional testing available
    - Continue maintenance therapy as appropriate
    - Regular monitoring every 3-6 months for sustained remission
    
    Very Good Partial Response (VGPR) - Near-Complete Response:
    - M component detectable only by immunofixation or ≥90% M protein reduction
    - Minimal residual disease with good long-term outcomes
    - May progress to complete response with continued therapy
    - Continue current treatment with goal of deeper response
    - Monitor every 2-3 months for response improvement
    
    Partial Response (PR) - Significant Response:
    - ≥50% reduction in serum M protein with additional criteria met
    - Meaningful clinical benefit requiring continued therapy
    - May achieve deeper responses with treatment continuation
    - Consider treatment intensification if response plateaus
    - Regular assessment every 2-3 months during active treatment
    
    Stable Disease (SD) - Disease Control:
    - Does not meet criteria for other response categories
    - May represent disease control or insufficient response
    - Evaluate need for treatment modification if lack of initial response
    - May be acceptable if on maintenance therapy
    - Close monitoring every 1-2 months with potential treatment changes
    
    Progressive Disease (PD) - Treatment Failure:
    - 25% increase from lowest response value or new disease manifestations
    - Requires immediate treatment modification and salvage therapy
    - Consider clinical trial enrollment and novel therapeutic approaches
    - Immediate oncologic consultation and treatment planning required
    - Frequent monitoring during treatment transition period
    
    Clinical Decision Making:
    
    Response Confirmation:
    - All responses should be confirmed on two consecutive assessments
    - Timing of assessments depends on treatment phase and response category
    - Consider minimal residual disease (MRD) testing when available
    
    Treatment Modifications:
    - Continue therapy for improving responses (PR to VGPR to CR)
    - Consider intensification for stable partial responses
    - Modify treatment immediately for progressive disease
    - Discuss maintenance therapy for patients achieving CR/sCR
    
    Prognostic Implications:
    - Depth of response correlates with progression-free and overall survival
    - Earlier achievement of response associated with better outcomes
    - Stringent CR and CR predict longest disease-free intervals
    - Progressive disease requires immediate intervention
    
    Reference: Kumar S, et al. Lancet Oncol. 2016;17(8):e328-e346.
    """
    
    result: str = Field(
        ...,
        description="IMWG response category classification",
        example="Stringent Complete Response (sCR)"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for response criteria)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation with management recommendations and prognostic information",
        example="STRINGENT COMPLETE RESPONSE (sCR): The patient has achieved the highest level of response to multiple myeloma treatment. CRITERIA MET: Negative serum and urine immunofixation, <5% bone marrow plasma cells, absence of soft tissue plasmacytomas, normal free light chain ratio (0.26-1.65), and absence of clonal cells in bone marrow by immunohistochemistry/immunofluorescence. CLINICAL SIGNIFICANCE: This represents the deepest possible remission with undetectable disease by all available methods. Patients achieving sCR typically have the best long-term outcomes and lowest risk of relapse. MANAGEMENT: Continue current treatment regimen if on maintenance therapy. Monitor with regular laboratory assessments every 3-6 months. Consider minimal residual disease (MRD) testing if available. Discuss long-term prognosis and surveillance plan. FOLLOW-UP: Regular monitoring with serum protein electrophoresis, immunofixation, free light chains, and complete blood count. Imaging as clinically indicated."
    )
    
    stage: str = Field(
        ...,
        description="Response category designation",
        example="Stringent Complete Response (sCR)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the response level",
        example="Best possible response"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Stringent Complete Response (sCR)",
                "unit": "",
                "interpretation": "STRINGENT COMPLETE RESPONSE (sCR): The patient has achieved the highest level of response to multiple myeloma treatment. CRITERIA MET: Negative serum and urine immunofixation, <5% bone marrow plasma cells, absence of soft tissue plasmacytomas, normal free light chain ratio (0.26-1.65), and absence of clonal cells in bone marrow by immunohistochemistry/immunofluorescence. CLINICAL SIGNIFICANCE: This represents the deepest possible remission with undetectable disease by all available methods. Patients achieving sCR typically have the best long-term outcomes and lowest risk of relapse. MANAGEMENT: Continue current treatment regimen if on maintenance therapy. Monitor with regular laboratory assessments every 3-6 months. Consider minimal residual disease (MRD) testing if available. Discuss long-term prognosis and surveillance plan. FOLLOW-UP: Regular monitoring with serum protein electrophoresis, immunofixation, free light chains, and complete blood count. Imaging as clinically indicated.",
                "stage": "Stringent Complete Response (sCR)",
                "stage_description": "Best possible response"
            }
        }