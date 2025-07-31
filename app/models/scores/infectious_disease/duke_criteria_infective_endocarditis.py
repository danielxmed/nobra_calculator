"""
Duke Criteria for Infective Endocarditis Models

Request and response models for Duke Criteria for Infective Endocarditis calculation.

References (Vancouver style):
1. Durack DT, Lukes AS, Bright DK. New criteria for diagnosis of infective endocarditis: 
   utilization of specific echocardiographic findings. Duke Endocarditis Service. Am J Med. 
   1994;96(3):200-9. doi: 10.1016/0002-9343(94)90143-0.
2. Li JS, Sexton DJ, Mick N, Nettles R, Fowler VG Jr, Ryan T, et al. Proposed modifications 
   to the Duke criteria for the diagnosis of infective endocarditis. Clin Infect Dis. 
   2000;30(4):633-8. doi: 10.1086/313753.
3. Habib G, Lancellotti P, Antunes MJ, Bongiorni MG, Casalta JP, Del Zotti F, et al. 2015 ESC 
   Guidelines for the management of infective endocarditis: The Task Force for the Management 
   of Infective Endocarditis of the European Society of Cardiology (ESC). Eur Heart J. 
   2015;36(44):3075-3128. doi: 10.1093/eurheartj/ehv319.

The Duke Criteria for Infective Endocarditis provides standardized diagnostic criteria 
for infective endocarditis based on clinical, microbiological, and echocardiographic 
findings. It classifies patients into three categories: definite, possible, or rejected 
endocarditis based on major and minor criteria. This system has been the gold standard 
for IE diagnosis since 1994 and was modified in 2000 to improve diagnostic accuracy.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DukeCriteriaInfectiveEndocarditisRequest(BaseModel):
    """
    Request model for Duke Criteria for Infective Endocarditis
    
    The Duke Criteria uses major and minor criteria to diagnose infective endocarditis:
    
    Major Criteria (2 criteria):
    1. Blood Culture Positive for IE:
       - Typical microorganisms from 2 separate blood cultures (Viridans streptococci, 
         S. bovis, HACEK group, S. aureus, community-acquired enterococci)
       - Persistently positive cultures (≥2 cultures >12h apart, or 3/4 separate cultures)
       - Single positive culture for Coxiella burnetii or phase I IgG >1:800
    
    2. Evidence of Endocardial Involvement:
       - Positive echocardiogram: vegetation, abscess, new prosthetic valve dehiscence
       - New valvular regurgitation (worsening or changing of pre-existing murmur not sufficient)
    
    Minor Criteria (5 criteria):
    1. Predisposition: predisposing heart condition or injection drug use
    2. Fever: temperature >38°C (100.4°F)
    3. Vascular phenomena: major arterial emboli, septic pulmonary infarcts, mycotic aneurysm, 
       intracranial hemorrhage, conjunctival hemorrhages, Janeway lesions
    4. Immunologic phenomena: glomerulonephritis, Osler nodes, Roth spots, rheumatoid factor
    5. Microbiological evidence: positive blood culture not meeting major criterion or 
       serological evidence of active infection
    
    Diagnostic Categories:
    - Definite IE: 2 major OR 1 major + 3 minor OR 5 minor criteria
    - Possible IE: 1 major + 1 minor OR 3 minor criteria
    - Rejected: Does not meet possible criteria OR firm alternate diagnosis OR 
      resolution with ≤4 days antibiotics
    
    Clinical Applications:
    - Gold standard for IE diagnosis in clinical practice and research
    - Guides antibiotic therapy decisions and need for surgical consultation
    - Used in clinical trials and epidemiological studies
    - Essential for distinguishing IE from other cardiac and systemic conditions
    
    References (Vancouver style):
    1. Durack DT, Lukes AS, Bright DK. New criteria for diagnosis of infective endocarditis: 
       utilization of specific echocardiographic findings. Duke Endocarditis Service. Am J Med. 
       1994;96(3):200-9.
    2. Li JS, Sexton DJ, Mick N, Nettles R, Fowler VG Jr, Ryan T, et al. Proposed modifications 
       to the Duke criteria for the diagnosis of infective endocarditis. Clin Infect Dis. 
       2000;30(4):633-8.
    3. Habib G, Lancellotti P, Antunes MJ, Bongiorni MG, Casalta JP, Del Zotti F, et al. 2015 ESC 
       Guidelines for the management of infective endocarditis. Eur Heart J. 2015;36(44):3075-3128.
    """
    
    blood_culture_major: Literal["yes", "no"] = Field(
        ...,
        description="MAJOR CRITERION: Blood culture positive for IE - typical microorganisms from 2 separate cultures (Viridans strep, S. bovis, HACEK, S. aureus, enterococci) OR persistently positive cultures OR single positive for Coxiella burnetii",
        example="no"
    )
    
    endocardial_involvement: Literal["yes", "no"] = Field(
        ...,
        description="MAJOR CRITERION: Evidence of endocardial involvement - positive echocardiogram showing vegetation, abscess, or new prosthetic valve dehiscence OR new valvular regurgitation",
        example="yes"
    )
    
    predisposition: Literal["yes", "no"] = Field(
        ...,
        description="MINOR CRITERION: Predisposing heart condition (valve disease, congenital heart disease, prosthetic valve) or injection drug use",
        example="yes"
    )
    
    fever: Literal["yes", "no"] = Field(
        ...,
        description="MINOR CRITERION: Fever greater than 38°C (100.4°F)",
        example="yes"
    )
    
    vascular_phenomena: Literal["yes", "no"] = Field(
        ...,
        description="MINOR CRITERION: Vascular phenomena - major arterial emboli, septic pulmonary infarcts, mycotic aneurysm, intracranial hemorrhage, conjunctival hemorrhages, Janeway lesions",
        example="no"
    )
    
    immunologic_phenomena: Literal["yes", "no"] = Field(
        ...,
        description="MINOR CRITERION: Immunologic phenomena - glomerulonephritis, Osler nodes, Roth spots, positive rheumatoid factor",
        example="no"
    )
    
    microbiological_evidence: Literal["yes", "no"] = Field(
        ...,
        description="MINOR CRITERION: Microbiological evidence - positive blood culture that does not meet major criterion OR serological evidence of active infection with organism consistent with IE",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "blood_culture_major": "no",
                "endocardial_involvement": "yes",
                "predisposition": "yes",
                "fever": "yes",
                "vascular_phenomena": "no",
                "immunologic_phenomena": "no",
                "microbiological_evidence": "yes"
            }
        }


class DukeCriteriaInfectiveEndocarditisResponse(BaseModel):
    """
    Response model for Duke Criteria for Infective Endocarditis
    
    The Duke Criteria classifies patients into three diagnostic categories:
    
    Definite Infective Endocarditis:
    - Requires 2 major criteria OR 1 major + 3 minor criteria OR 5 minor criteria
    - Immediate antimicrobial therapy indicated
    - Cardiology and infectious disease consultation recommended
    - Consider surgical evaluation for complicated IE
    - Mortality risk varies based on organism, complications, and patient factors
    
    Possible Infective Endocarditis:
    - Requires 1 major + 1 minor criterion OR 3 minor criteria
    - Findings consistent with IE but do not meet definite criteria
    - Consider further diagnostic workup including:
      * Repeat echocardiography (especially TEE if TTE negative)
      * Additional blood cultures before antibiotics
      * Advanced imaging (CT, MRI, PET-CT in selected cases)
      * Specialist consultation for management guidance
    
    Rejected (IE Unlikely):
    - Does not meet criteria for possible or definite IE
    - Firm alternate diagnosis established
    - Resolution of syndrome with ≤4 days of antibiotic therapy
    - Consider alternative diagnoses:
      * Non-infectious valve disease (degenerative, rheumatic)
      * Systemic infections without endocardial involvement
      * Autoimmune conditions (lupus, antiphospholipid syndrome)
      * Other cardiac conditions (myxoma, papillary fibroelastoma)
    
    Clinical Significance:
    - The Duke Criteria has sensitivity of 76% and high specificity for IE diagnosis
    - TEE (transesophageal echocardiography) is more sensitive than TTE for vegetations
    - Blood cultures should be obtained before antibiotic therapy when possible
    - Culture-negative endocarditis may require molecular diagnostic methods
    - Early diagnosis and treatment are crucial for preventing complications
    
    Important Considerations:
    - Prosthetic valve endocarditis may have modified presentations
    - Healthcare-associated IE is increasingly common
    - HACEK organisms and fastidious bacteria may require extended culture periods
    - Consider 2023 Duke-ISCVID criteria for updated diagnostic approaches
    
    Reference: Durack DT, et al. Am J Med. 1994;96(3):200-9.
    """
    
    result: str = Field(
        ...,
        description="Duke Criteria diagnostic classification (Definite, Possible, or Rejected)",
        example="Possible"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the result",
        example="category"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on diagnostic classification",
        example="Possible infective endocarditis based on 1 major and 3 minor criteria. Findings are consistent with IE but do not meet criteria for definite IE. Consider further diagnostic workup including repeat echocardiography, additional blood cultures, and specialist consultation."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic classification category (Definite, Possible, Rejected)",
        example="Possible"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the diagnostic category",
        example="Possible infective endocarditis"
    )
    
    major_criteria_count: int = Field(
        ...,
        description="Number of positive major criteria (0-2)",
        example=1
    )
    
    minor_criteria_count: int = Field(
        ...,
        description="Number of positive minor criteria (0-5)",
        example=3
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "Possible",
                "unit": "category",
                "interpretation": "Possible infective endocarditis based on 1 major and 3 minor criteria. Findings are consistent with IE but do not meet criteria for definite IE. Consider further diagnostic workup including repeat echocardiography, additional blood cultures, and specialist consultation.",
                "stage": "Possible",
                "stage_description": "Possible infective endocarditis",
                "major_criteria_count": 1,
                "minor_criteria_count": 3
            }
        }