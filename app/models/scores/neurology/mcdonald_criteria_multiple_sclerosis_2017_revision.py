"""
McDonald Criteria for Multiple Sclerosis (2017 Revision) Models

Request and response models for McDonald Criteria MS diagnosis.

References (Vancouver style):
1. Thompson AJ, Banwell BL, Barkhof F, Carroll WM, Coetzee T, Comi G, et al. Diagnosis of 
   multiple sclerosis: 2017 revisions of the McDonald criteria. Lancet Neurol. 2018 Feb;17(2):162-173. 
   doi: 10.1016/S1474-4422(17)30470-2.
2. Polman CH, Reingold SC, Banwell B, Clanet M, Cohen JA, Filippi M, et al. Diagnostic criteria 
   for multiple sclerosis: 2010 revisions to the McDonald criteria. Ann Neurol. 2011 Feb;69(2):292-302. 
   doi: 10.1002/ana.22366.
3. McNicholas N, McGuigan C, Kehoe L, Gallagher L, Teeling M, Hamid SH, et al. Clinical Application 
   of 2017 McDonald Diagnostic Criteria for Multiple Sclerosis. J Clin Neurol. 2018 Jul;14(3):387-398. 
   doi: 10.3988/jcn.2018.14.3.387.
4. Arrambide G, Tintore M, Espejo C, Auger C, Castillo M, Rio J, et al. The value of oligoclonal 
   bands in the multiple sclerosis diagnostic criteria. Brain. 2018 Apr 1;141(4):1075-1084. 
   doi: 10.1093/brain/awy006.

The McDonald Criteria for Multiple Sclerosis (2017 Revision) represent the gold standard 
for MS diagnosis, incorporating clinical attacks, MRI findings, and CSF analysis. The 2017 
revision introduced key changes including the use of CSF oligoclonal bands to substitute 
for dissemination in time and acceptance of cortical lesions for dissemination in space. 
This diagnostic framework aims to facilitate earlier diagnosis while preserving specificity 
and reducing misdiagnosis rates.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class McdonaldCriteriaMultipleSclerosis2017RevisionRequest(BaseModel):
    """
    Request model for McDonald Criteria for Multiple Sclerosis (2017 Revision)
    
    The McDonald Criteria evaluate multiple sclerosis diagnosis using six key parameters:
    
    **1. Clinical Attacks (Episodes of neurological dysfunction):**
    - 0: No clinical attacks documented
    - 1: Single clinical attack (monophasic episode ≥24 hours)  
    - 2_or_more: Multiple clinical attacks (≥2 separate episodes)
    
    **Clinical Attack Definition:**
    - Inflammatory demyelinating CNS event lasting ≥24 hours
    - Objective neurological dysfunction
    - May be current symptoms or historical account
    - Must represent acute or subacute onset
    
    **2. Objective Clinical Evidence (Lesions with clinical correlation):**
    - 0: No lesions with objective clinical evidence
    - 1: Single lesion with objective clinical evidence
    - 2_or_more: Multiple lesions with objective clinical evidence (≥2)
    
    **Objective Clinical Evidence Definition:**
    - Abnormality on neurological examination
    - Abnormality on visual evoked potentials (for optic nerve)
    - MRI findings consistent with clinical symptoms
    
    **3. Dissemination in Space (DIS) - Multiple CNS locations affected:**
    - not_demonstrated: DIS criteria not met
    - demonstrated: DIS criteria fulfilled
    
    **DIS Requirements (≥1 T2-hyperintense lesions in ≥2 of 4 locations):**
    - Periventricular (≥1 lesion, unless patient >50 years - seek higher number)
    - Cortical or juxtacortical (cortical lesions new in 2017 revision)
    - Infratentorial (brainstem, cerebellum)
    - Spinal cord
    
    **4. Dissemination in Time (DIT) - Disease progression over time:**
    - not_demonstrated: DIT criteria not met  
    - demonstrated: DIT criteria fulfilled
    
    **DIT Requirements (any of the following):**
    - Additional clinical attack at different time
    - New T2-hyperintense lesion on follow-up MRI compared to baseline
    - Gadolinium-enhancing lesion on follow-up MRI (if not baseline)
    - Simultaneous gadolinium-enhancing and non-enhancing T2 lesions on single MRI
    
    **5. CSF Oligoclonal Bands (2017 revision key change):**
    - absent: No CSF-specific oligoclonal bands detected
    - present: CSF-specific oligoclonal bands present (≥2 bands in CSF not in serum)
    - not_tested: CSF analysis not performed
    
    **2017 Revision Innovation:**
    - CSF oligoclonal bands can substitute for DIT when DIS is demonstrated
    - Provides earlier diagnosis opportunity
    - Maintains diagnostic specificity
    
    **6. Alternative Diagnosis Exclusion:**
    - excluded: No better explanation for clinical presentation
    - possible: Alternative diagnosis could explain findings
    
    **Alternative Diagnoses to Consider:**
    - Neuromyelitis optica spectrum disorders (NMOSD)
    - Acute disseminated encephalomyelitis (ADEM)
    - CNS vasculitis, infections, neoplasms
    - Genetic or metabolic conditions
    - Psychiatric disorders mimicking neurological symptoms
    
    **Diagnostic Algorithm Summary:**
    
    **Path 1: ≥2 attacks + ≥2 objective lesions** → MS diagnosed (no additional tests needed)
    
    **Path 2: ≥2 attacks + 1 objective lesion** → Need DIS demonstration
    
    **Path 3: 1 attack + ≥2 objective lesions** → Need DIT demonstration (or CSF-OCB if DIS present)
    
    **Path 4: 1 attack + 1 objective lesion** → Need both DIS and DIT (CSF-OCB can substitute for DIT)
    
    **Clinical Notes:**
    - Primary progressive MS has separate diagnostic criteria not covered here
    - Criteria apply primarily to relapsing-remitting presentations
    - Regular clinical and MRI monitoring recommended for incomplete criteria
    - Multidisciplinary care essential for optimal MS management
    - Early treatment initiation improves long-term outcomes
    
    References (Vancouver style):
    1. Thompson AJ, Banwell BL, Barkhof F, Carroll WM, Coetzee T, Comi G, et al. Diagnosis of 
    multiple sclerosis: 2017 revisions of the McDonald criteria. Lancet Neurol. 2018 Feb;17(2):162-173. 
    doi: 10.1016/S1474-4422(17)30470-2.
    2. Polman CH, Reingold SC, Banwell B, Clanet M, Cohen JA, Filippi M, et al. Diagnostic criteria 
    for multiple sclerosis: 2010 revisions to the McDonald criteria. Ann Neurol. 2011 Feb;69(2):292-302. 
    doi: 10.1002/ana.22366.
    3. McNicholas N, McGuigan C, Kehoe L, Gallagher L, Teeling M, Hamid SH, et al. Clinical Application 
    of 2017 McDonald Diagnostic Criteria for Multiple Sclerosis. J Clin Neurol. 2018 Jul;14(3):387-398. 
    doi: 10.3988/jcn.2018.14.3.387.
    4. Arrambide G, Tintore M, Espejo C, Auger C, Castillo M, Rio J, et al. The value of oligoclonal 
    bands in the multiple sclerosis diagnostic criteria. Brain. 2018 Apr 1;141(4):1075-1084. 
    doi: 10.1093/brain/awy006.
    """
    
    clinical_attacks: Literal["0", "1", "2_or_more"] = Field(
        ...,
        description="Number of clinical attacks. Clinical attack defined as inflammatory demyelinating CNS event lasting ≥24 hours with objective neurological dysfunction",
        example="1"
    )
    
    objective_clinical_evidence: Literal["0", "1", "2_or_more"] = Field(
        ...,
        description="Number of lesions with objective clinical evidence. Evidence includes abnormality on neurologic exam, imaging, or visual evoked potentials",
        example="2_or_more"
    )
    
    dissemination_in_space: Literal["not_demonstrated", "demonstrated"] = Field(
        ...,
        description="Dissemination in Space (DIS) - Evidence of lesions in multiple CNS locations. Requires ≥1 T2-hyperintense lesions in ≥2 of 4 locations: periventricular, cortical/juxtacortical, infratentorial, spinal cord",
        example="demonstrated"
    )
    
    dissemination_in_time: Literal["not_demonstrated", "demonstrated"] = Field(
        ...,
        description="Dissemination in Time (DIT) - Additional clinical attack, new T2/gadolinium-enhancing lesion on follow-up MRI, or simultaneous gadolinium-enhancing and non-enhancing lesions on single MRI",
        example="not_demonstrated"
    )
    
    csf_oligoclonal_bands: Literal["absent", "present", "not_tested"] = Field(
        ...,
        description="CSF-specific oligoclonal bands present. In 2017 revision, can substitute for dissemination in time when dissemination in space is demonstrated",
        example="present"
    )
    
    alternative_diagnosis: Literal["excluded", "possible"] = Field(
        ...,
        description="Alternative diagnosis that better explains the clinical presentation and findings",
        example="excluded"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_attacks": "1",
                "objective_clinical_evidence": "2_or_more",
                "dissemination_in_space": "demonstrated",
                "dissemination_in_time": "not_demonstrated",
                "csf_oligoclonal_bands": "present",
                "alternative_diagnosis": "excluded"
            }
        }


class McdonaldCriteriaMultipleSclerosis2017RevisionResponse(BaseModel):
    """
    Response model for McDonald Criteria for Multiple Sclerosis (2017 Revision)
    
    The McDonald Criteria provide three possible diagnostic outcomes:
    - **MS Diagnosed**: Criteria fulfilled, definitive MS diagnosis
    - **Possible MS**: Suggestive findings but incomplete criteria (CIS/early disease)
    - **MS Not Diagnosed**: Criteria not met, alternative diagnosis likely
    
    Reference: Thompson AJ, et al. Lancet Neurol. 2018;17(2):162-173.
    """
    
    result: str = Field(
        ...,
        description="Multiple sclerosis diagnosis based on 2017 McDonald Criteria",
        example="MS Diagnosed"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnosis",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the diagnosis",
        example="The 2017 McDonald Criteria for multiple sclerosis are fulfilled. The patient meets the diagnostic requirements for MS with evidence of dissemination in space and time, appropriate clinical presentation, and exclusion of alternative diagnoses. Initiate appropriate disease-modifying therapy, provide patient education, and establish multidisciplinary care."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category (MS Diagnosed, Possible MS, MS Not Diagnosed)",
        example="MS Diagnosed"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic outcome",
        example="Criteria fulfilled"
    )
    
    criteria_details: Dict[str, Any] = Field(
        ...,
        description="Detailed breakdown of criteria evaluation and rationale",
        example={
            "clinical_attacks": "1 attack present",
            "objective_evidence": "≥2 lesions with objective evidence",
            "dissemination_in_space": "Demonstrated",
            "dissemination_in_time": "Substituted by CSF oligoclonal bands"
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "MS Diagnosed",
                "unit": "diagnosis",
                "interpretation": "The 2017 McDonald Criteria for multiple sclerosis are fulfilled. The patient meets the diagnostic requirements for MS with evidence of dissemination in space and time, appropriate clinical presentation, and exclusion of alternative diagnoses. Initiate appropriate disease-modifying therapy, provide patient education, and establish multidisciplinary care.",
                "stage": "MS Diagnosed",
                "stage_description": "Criteria fulfilled",
                "criteria_details": {
                    "clinical_attacks": "1 attack present",
                    "objective_evidence": "≥2 lesions with objective evidence",
                    "dissemination_in_space": "Demonstrated",
                    "dissemination_in_time": "Substituted by CSF oligoclonal bands"
                }
            }
        }