"""
FeverPAIN Score for Strep Pharyngitis Models

Request and response models for FeverPAIN Score calculation.

References (Vancouver style):
1. Little P, Hobbs FD, Moore M, Mant D, Williamson I, McNulty C, et al. Incidence 
   and clinical variables associated with streptococcal throat infections: a 
   prospective diagnostic cohort study. Br J Gen Pract. 2012 Nov;62(604):e787-94. 
   doi: 10.3399/bjgp12X658322. PMID: 23211259.
2. Little P, Moore M, Hobbs FD, Mant D, McNulty C, Williamson I, et al. Clinical 
   score and rapid antigen detection test to guide antibiotic use for sore throats: 
   randomised controlled trial of PRISM (primary care streptococcal management). 
   BMJ. 2013 Oct 10;347:f5806. doi: 10.1136/bmj.f5806. PMID: 24114306.

The FeverPAIN score is a clinical prediction rule for streptococcal pharyngitis 
that helps identify patients who are more likely to have Group A Streptococcus 
(GAS) infection and may benefit from antibiotic treatment. The score was validated 
in a large UK primary care cohort and has been shown to reduce antibiotic 
prescribing by 30% while maintaining clinical outcomes.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FeverpainScoreRequest(BaseModel):
    """
    Request model for FeverPAIN Score for Strep Pharyngitis calculation
    
    The FeverPAIN score uses 5 clinical criteria to predict the likelihood of 
    streptococcal pharyngitis:
    
    F - Fever in past 24 hours: History of fever (≥38°C/100.4°F) reported by 
        patient or documented
    
    P - Purulence: Visible pus on the tonsils on examination
    
    A - Attend rapidly: Patient presented within 3 days of symptom onset
        (indicates acute presentation)
    
    I - Inflamed tonsils: Severe tonsil inflammation visible on examination
    
    N - No cough or coryza: Absence of typical viral upper respiratory symptoms
        (cough or nasal congestion/rhinorrhea)
    
    Each positive criterion scores 1 point. Higher scores indicate higher 
    likelihood of streptococcal infection.
    
    Note: For use in patients aged 3 years and older presenting with sore throat.
    
    References (Vancouver style):
    1. Little P, Hobbs FD, Moore M, Mant D, Williamson I, McNulty C, et al. 
       Br J Gen Pract. 2012 Nov;62(604):e787-94.
    """
    
    fever_24h: Literal["yes", "no"] = Field(
        ...,
        description="Fever in past 24 hours. History of fever (≥38°C/100.4°F) reported by patient or documented in last 24 hours",
        example="yes"
    )
    
    absence_cough_coryza: Literal["yes", "no"] = Field(
        ...,
        description="Absence of cough or coryza. No cough or nasal congestion/rhinorrhea (typical viral symptoms)",
        example="yes"
    )
    
    symptom_onset_3days: Literal["yes", "no"] = Field(
        ...,
        description="Symptom onset ≤3 days (attend rapidly). Patient presented within 3 days of symptom onset",
        example="yes"
    )
    
    purulent_tonsils: Literal["yes", "no"] = Field(
        ...,
        description="Purulent tonsils. Visible pus on the tonsils on examination",
        example="no"
    )
    
    severe_tonsil_inflammation: Literal["yes", "no"] = Field(
        ...,
        description="Severe tonsil inflammation. Marked erythema and swelling of tonsils on examination",
        example="yes"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "fever_24h": "yes",
                "absence_cough_coryza": "yes",
                "symptom_onset_3days": "yes",
                "purulent_tonsils": "no",
                "severe_tonsil_inflammation": "yes"
            }
        }


class FeverpainScoreResponse(BaseModel):
    """
    Response model for FeverPAIN Score for Strep Pharyngitis calculation
    
    The FeverPAIN score ranges from 0 to 5 and correlates with the likelihood 
    of streptococcal infection:
    
    - Score 0-1: 13-18% likelihood of streptococcus isolation
      → No antibiotics recommended
    
    - Score 2: 30-35% likelihood of streptococcus isolation
      → Delayed antibiotic prescription may be appropriate
    
    - Score 3: 39-48% likelihood of streptococcus isolation
      → Delayed antibiotic prescription may be appropriate
    
    - Score 4-5: 62-65% likelihood of streptococcus isolation
      → Consider antibiotics if symptoms severe; short delay may be appropriate
    
    Implementation of the FeverPAIN score has been shown to reduce antibiotic 
    prescribing by 30% while maintaining good clinical outcomes and patient 
    satisfaction.
    
    Reference: Little P, et al. BMJ. 2013;347:f5806.
    """
    
    result: int = Field(
        ...,
        description="FeverPAIN score (0-5 points)",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with antibiotic prescribing guidance",
        example="39-48% likelihood of streptococcus isolation. Delayed antibiotic prescription may be appropriate. Consider 3-day delayed prescribing strategy."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on score",
        example="Moderate-High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of streptococcus isolation likelihood",
        example="39-48% strep isolation"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "39-48% likelihood of streptococcus isolation. Delayed antibiotic prescription may be appropriate. Consider 3-day delayed prescribing strategy.",
                "stage": "Moderate-High Risk",
                "stage_description": "39-48% strep isolation"
            }
        }