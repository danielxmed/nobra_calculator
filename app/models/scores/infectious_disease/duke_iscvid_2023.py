"""
2023 Duke-ISCVID Criteria Models

Request and response models for 2023 Duke-ISCVID Criteria calculation.
"""

from pydantic import BaseModel, Field
from typing import Optional, Literal


class DukeIscvid2023Request(BaseModel):
    """Request model for 2023 Duke-ISCVID Criteria"""
    
    # Major Microbiologic Criteria
    microbiologic_major_typical: Literal["none", "present"] = Field(
        "none", 
        description="Microorganisms that commonly cause IE isolated from 2+ separate blood culture sets"
    )
    microbiologic_major_nontypical: Literal["none", "present"] = Field(
        "none", 
        description="Microorganisms that occasionally/rarely cause IE isolated from 3+ separate blood culture sets"
    )
    pcr_positive_coxiella_bartonella_tropheryma: Literal["none", "present"] = Field(
        "none", 
        description="Positive PCR/nucleic acid for Coxiella burnetii, Bartonella spp, or Tropheryma whipplei from blood"
    )
    coxiella_antibody_titer: Literal["none", "present"] = Field(
        "none", 
        description="Coxiella burnetii antiphase I IgG titer >1:800 or isolated from single blood culture"
    )
    bartonella_antibody_titer: Literal["none", "present"] = Field(
        "none", 
        description="Indirect IFA for Bartonella henselae/quintana with IgG titer ≥1:800"
    )
    
    # Major Imaging Criteria
    imaging_major_echo_ct: Literal["none", "present"] = Field(
        "none", 
        description="Echo/cardiac CT showing vegetation, perforation, aneurysm, abscess, pseudoaneurysm, fistula"
    )
    new_valvular_regurgitation: Literal["none", "present"] = Field(
        "none", 
        description="Significant new valvular regurgitation on echo vs previous imaging"
    )
    prosthetic_valve_dehiscence: Literal["none", "present"] = Field(
        "none", 
        description="New partial dehiscence of prosthetic valve vs previous imaging"
    )
    pet_ct_abnormal_activity: Literal["none", "present"] = Field(
        "none", 
        description="[18F]FDG PET/CT abnormal activity involving valve/graft/device/prosthetic material"
    )
    
    # Major Surgical Criteria
    surgical_evidence: Literal["none", "present"] = Field(
        "none", 
        description="Evidence of IE by direct inspection during heart surgery"
    )
    
    # Minor Criteria - Predisposing Conditions
    previous_ie: Literal["none", "present"] = Field(
        "none", 
        description="Previous history of infective endocarditis"
    )
    prosthetic_valve: Literal["none", "present"] = Field(
        "none", 
        description="Prosthetic valve present"
    )
    previous_valve_repair: Literal["none", "present"] = Field(
        "none", 
        description="Previous valve repair"
    )
    congenital_heart_disease: Literal["none", "present"] = Field(
        "none", 
        description="Congenital heart disease"
    )
    significant_regurgitation_stenosis: Literal["none", "present"] = Field(
        "none", 
        description="More than mild regurgitation or stenosis of any etiology"
    )
    endovascular_cied: Literal["none", "present"] = Field(
        "none", 
        description="Endovascular cardiac implantable electronic device (CIED)"
    )
    hypertrophic_cardiomyopathy: Literal["none", "present"] = Field(
        "none", 
        description="Hypertrophic obstructive cardiomyopathy"
    )
    injection_drug_use: Literal["none", "present"] = Field(
        "none", 
        description="Injection drug use"
    )
    
    # Minor Criteria - Clinical Manifestations
    fever: Literal["none", "present"] = Field(
        "none", 
        description="Fever with documented temperature >38.0°C (100.4°F)"
    )
    vascular_phenomena: Literal["none", "present"] = Field(
        "none", 
        description="Vascular phenomena (emboli, septic infarcts, mycotic aneurysm, hemorrhage, Janeway lesions)"
    )
    immunologic_phenomena: Literal["none", "present"] = Field(
        "none", 
        description="Immunologic phenomena (RF+, Osler nodes, Roth spots, glomerulonephritis)"
    )
    positive_blood_cultures_minor: Literal["none", "present"] = Field(
        "none", 
        description="Positive blood cultures for organism consistent with IE but not meeting major criterion"
    )
    positive_sterile_site_culture: Literal["none", "present"] = Field(
        "none", 
        description="Positive culture/PCR from sterile body site other than cardiac tissue/arterial embolus"
    )
    pet_ct_within_3_months: Literal["none", "present"] = Field(
        "none", 
        description="Abnormal [18F]FDG PET/CT activity within 3 months of prosthetic material implantation"
    )
    new_regurgitation_auscultation: Literal["none", "present"] = Field(
        "none", 
        description="New valvular regurgitation on auscultation (if echo not available)"
    )
    
    # Pathologic Criteria
    pathologic_microorganisms: Literal["none", "present"] = Field(
        "none", 
        description="Microorganisms identified in vegetation with clinical signs of active endocarditis"
    )
    pathologic_active_endocarditis: Literal["none", "present"] = Field(
        "none", 
        description="Active endocarditis identified in or on vegetation histologically"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "microbiologic_major_typical": "present",
                "imaging_major_echo_ct": "present", 
                "fever": "present",
                "injection_drug_use": "present",
                "vascular_phenomena": "none",
                "prosthetic_valve": "none",
                "pathologic_microorganisms": "none"
            }
        }


class DukeIscvid2023Response(BaseModel):
    """Response model for 2023 Duke-ISCVID Criteria"""
    result: str = Field(
        ..., 
        description="Duke-ISCVID diagnosis result",
        example="Definite IE"
    )
    pathologic_criteria_count: int = Field(
        ..., 
        description="Number of positive pathologic criteria",
        example=0
    )
    major_criteria_count: int = Field(
        ..., 
        description="Number of positive major criteria", 
        example=2
    )
    minor_criteria_count: int = Field(
        ..., 
        description="Number of positive minor criteria",
        example=2
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation and recommendations",
        example="Patient meets Duke-ISCVID criteria for definite infective endocarditis. Appropriate antimicrobial therapy and cardiology/infectious disease consultation recommended."
    )
    stage: str = Field(
        ...,
        description="Diagnostic classification",
        example="Definite IE"
    )
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic stage", 
        example="Meets criteria for definite infective endocarditis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Definite IE",
                "pathologic_criteria_count": 0,
                "major_criteria_count": 2,
                "minor_criteria_count": 2,
                "interpretation": "Patient meets Duke-ISCVID criteria for definite infective endocarditis. Appropriate antimicrobial therapy and cardiology/infectious disease consultation recommended.",
                "stage": "Definite IE",
                "stage_description": "Meets criteria for definite infective endocarditis"
            }
        }