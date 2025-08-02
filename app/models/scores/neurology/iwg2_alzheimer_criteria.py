"""
International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis Models

Request and response models for IWG-2 AD diagnosis.

References (Vancouver style):
1. Dubois B, Feldman HH, Jacova C, Hampel H, Molinuevo JL, Blennow K, et al. Advancing 
   research diagnostic criteria for Alzheimer's disease: the IWG-2 criteria. Lancet Neurol. 
   2014 Jun;13(6):614-29. doi: 10.1016/S1474-4422(14)70090-0.
2. Jack CR Jr, Bennett DA, Blennow K, Carrillo MC, Dunn B, Haeberlein SB, et al. NIA-AA 
   Research Framework: Toward a biological definition of Alzheimer's disease. Alzheimers 
   Dement. 2018 Apr;14(4):535-562. doi: 10.1016/j.jalz.2018.02.018.
3. Dubois B, Hampel H, Feldman HH, Scheltens P, Aisen P, Andrieu S, et al. Preclinical 
   Alzheimer's disease: Definition, natural history, and diagnostic criteria. Alzheimers 
   Dement. 2016 Mar;12(3):292-323. doi: 10.1016/j.jalz.2016.02.002.

The International Working Group (IWG-2) criteria represent a major advancement in AD diagnosis 
by integrating clinical phenotypes with pathophysiological biomarkers. The core requirement 
is an appropriate clinical AD phenotype (typical, atypical, mixed, or asymptomatic) combined 
with pathophysiological biomarker evidence of Alzheimer pathology. This framework enables 
diagnosis across the full disease spectrum and facilitates earlier intervention and research 
enrollment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class Iwg2AlzheimerCriteriaRequest(BaseModel):
    """
    Request model for International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis
    
    The IWG-2 criteria integrate clinical phenotypes with pathophysiological biomarkers:
    
    Clinical Phenotypes:
    - typical_ad: Most common presentation with episodic memory impairment
    - atypical_ad: Non-amnestic presentations (e.g., posterior cortical atrophy, logopenic aphasia)
    - mixed_ad: AD pathology coexisting with other neurodegenerative processes
    - asymptomatic: Cognitively normal individuals
    
    Pathophysiological Biomarkers (required for diagnosis):
    - CSF Aβ1-42: Inversely reflects brain amyloid burden (decreased = pathological)
    - CSF T-tau: Directly reflects neuronal degeneration (elevated = pathological)
    - CSF P-tau: Direct marker of tau pathology (elevated = pathological)
    - Amyloid PET: In vivo assessment of brain amyloid plaques (positive = pathological)
    
    Clinical Features:
    - Memory impairment: Characteristic of typical AD
    - Cognitive domains: Single vs. multiple domain involvement
    - Functional decline: Progressive decline in activities of daily living
    
    Core Diagnostic Algorithm:
    Clinical AD phenotype + Pathophysiological biomarker evidence = AD diagnosis

    References (Vancouver style):
    1. Dubois B, Feldman HH, Jacova C, Hampel H, Molinuevo JL, Blennow K, et al. Advancing 
    research diagnostic criteria for Alzheimer's disease: the IWG-2 criteria. Lancet Neurol. 
    2014 Jun;13(6):614-29. doi: 10.1016/S1474-4422(14)70090-0.
    2. Jack CR Jr, Bennett DA, Blennow K, Carrillo MC, Dunn B, Haeberlein SB, et al. NIA-AA 
    Research Framework: Toward a biological definition of Alzheimer's disease. Alzheimers 
    Dement. 2018 Apr;14(4):535-562. doi: 10.1016/j.jalz.2018.02.018.
    3. Dubois B, Hampel H, Feldman HH, Scheltens P, Aisen P, Andrieu S, et al. Preclinical 
    Alzheimer's disease: Definition, natural history, and diagnostic criteria. Alzheimers 
    Dement. 2016 Mar;12(3):292-323. doi: 10.1016/j.jalz.2016.02.002.
    """
    
    clinical_phenotype: Literal["typical_ad", "atypical_ad", "mixed_ad", "asymptomatic"] = Field(
        ...,
        description="Clinical presentation pattern of cognitive impairment. Typical AD shows episodic memory impairment, atypical AD has non-amnestic presentations, mixed AD combines AD with other pathologies, asymptomatic refers to cognitively normal individuals",
        example="typical_ad"
    )
    
    memory_impairment: Literal["present", "absent"] = Field(
        ...,
        description="Presence of episodic memory impairment characteristic of typical AD. Required for typical AD diagnosis but may be absent in atypical presentations",
        example="present"
    )
    
    cognitive_domains_affected: Literal["single_domain", "multiple_domains"] = Field(
        ...,
        description="Number of cognitive domains significantly impaired. Multiple domain involvement suggests more advanced disease or atypical presentations",
        example="multiple_domains"
    )
    
    csf_amyloid_beta: Literal["normal", "decreased", "not_available"] = Field(
        ...,
        description="CSF Aβ1-42 levels (pathophysiological biomarker). Decreased levels (<530 pg/mL typical cutoff) indicate brain amyloid accumulation. Core diagnostic biomarker for AD pathology",
        example="decreased"
    )
    
    csf_tau: Literal["normal", "elevated", "not_available"] = Field(
        ...,
        description="CSF total tau (T-tau) levels (pathophysiological biomarker). Elevated levels (>350 pg/mL typical cutoff) reflect neuronal degeneration intensity. Supports AD diagnosis when elevated",
        example="elevated"
    )
    
    csf_ptau: Literal["normal", "elevated", "not_available"] = Field(
        ...,
        description="CSF phosphorylated tau (P-tau) levels (pathophysiological biomarker). Elevated levels (>60 pg/mL typical cutoff) indicate tau pathology specific to AD. Highly specific for AD diagnosis",
        example="elevated"
    )
    
    amyloid_pet: Literal["negative", "positive", "not_available"] = Field(
        ...,
        description="Amyloid PET imaging results (pathophysiological biomarker). Positive scan indicates significant brain amyloid plaque burden. Alternative to CSF Aβ1-42 for detecting amyloid pathology",
        example="positive"
    )
    
    functional_decline: Literal["present", "absent", "mild"] = Field(
        ...,
        description="Progressive functional decline in activities of daily living. Present or mild decline supports clinical significance of cognitive symptoms. Required for symptomatic AD diagnosis",
        example="mild"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "clinical_phenotype": "typical_ad",
                "memory_impairment": "present",
                "cognitive_domains_affected": "multiple_domains",
                "csf_amyloid_beta": "decreased",
                "csf_tau": "elevated",
                "csf_ptau": "elevated",
                "amyloid_pet": "not_available",
                "functional_decline": "mild"
            }
        }


class Iwg2AlzheimerCriteriaResponse(BaseModel):
    """
    Response model for International Working Group (IWG) 2 Criteria for Alzheimer's Disease Diagnosis
    
    The IWG-2 criteria provide diagnostic classifications:
    
    Diagnostic Outcomes:
    - Typical AD: Characteristic memory impairment with biomarker evidence
    - Atypical AD: Non-amnestic presentation with biomarker evidence
    - Mixed AD: AD pathology with other neurodegenerative processes
    - Asymptomatic at Risk: Positive biomarkers in cognitively normal individuals
    - Insufficient Criteria: Does not meet diagnostic requirements
    
    The IWG-2 framework enables earlier diagnosis and appropriate treatment planning
    across the full Alzheimer's disease spectrum.
    
    Reference: Dubois B, et al. Lancet Neurol. 2014;13(6):614-29.
    """
    
    result: str = Field(
        ...,
        description="IWG-2 diagnostic classification (typical_ad, atypical_ad, mixed_ad, asymptomatic_at_risk, insufficient_criteria)",
        example="typical_ad"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the diagnostic result",
        example="diagnosis"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with diagnostic conclusions and management recommendations",
        example="Diagnosis of typical Alzheimer's disease confirmed. Clinical phenotype shows characteristic episodic memory impairment with pathophysiological biomarker evidence. Recommend standard AD treatment protocols, monitoring for disease progression, and consideration for appropriate clinical trials. Discuss prognosis and long-term care planning with patient and family."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category classification",
        example="Typical AD"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic classification",
        example="Meets criteria for typical Alzheimer's disease"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "typical_ad",
                "unit": "diagnosis",
                "interpretation": "Diagnosis of typical Alzheimer's disease confirmed. Clinical phenotype shows characteristic episodic memory impairment with pathophysiological biomarker evidence. Recommend standard AD treatment protocols, monitoring for disease progression, and consideration for appropriate clinical trials. Discuss prognosis and long-term care planning with patient and family.",
                "stage": "Typical AD",
                "stage_description": "Meets criteria for typical Alzheimer's disease"
            }
        }