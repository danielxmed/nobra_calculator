"""
Appendicitis Inflammatory Response (AIR) Score Models

Request and response models for AIR Score calculation.

References (Vancouver style):
1. Andersson M, Andersson RE. The appendicitis inflammatory response score: 
   a tool for the diagnosis of acute appendicitis that outperforms the Alvarado score. 
   World J Surg. 2008;32(8):1843-9.
2. Sammalkorpi HE, Mentula P, Leppäniemi A. A new adult appendicitis score improves 
   diagnostic accuracy of acute appendicitis—a prospective study. BMC Gastroenterol. 
   2014;14:114.
3. Scott AJ, Mason SE, Arunakirinathan M, et al. Risk stratification by the 
   Appendicitis Inflammatory Response score to guide decision-making in patients 
   with suspected appendicitis. Br J Surg. 2015;102(5):563-72.

The AIR Score diagnoses appendicitis based on clinical and laboratory findings using 
seven variables: vomiting, right iliac fossa pain, rebound tenderness, fever, 
polymorphonuclear leukocyte percentage, white blood cell count, and C-reactive protein level.

The score is designed with high sensitivity for advanced appendicitis, which is most 
clinically important to identify. It performs well across age groups from 2-96 years 
and is particularly effective in children and women, though may be less specific 
in elderly patients.

Key clinical insights:
- The proportion of neutrophils is particularly important as advanced appendicitis 
  often causes lymphopenia
- Rebound tenderness (percussion tenderness) reflects peritoneal irritation
- Patients with short symptom duration may have low scores as the immune system 
  hasn't fully reacted yet
- Consider rescoring after 4-8 hours in patients with indeterminate scores
"""

from pydantic import BaseModel, Field
from typing import Literal


class AirScoreRequest(BaseModel):
    """
    Request model for Appendicitis Inflammatory Response (AIR) Score
    
    The AIR Score uses seven clinical and laboratory variables to assess appendicitis probability:
    
    Clinical Variables:
    - Vomiting: Present or absent (0-1 point)
    - Right iliac fossa (RIF) pain: Present or absent (0-1 point)
    - Rebound tenderness: Graded intensity reflecting peritoneal irritation (0-3 points)
    - Fever: Temperature ≥38.5°C/101.3°F (0-1 point)
    
    Laboratory Variables:
    - Polymorphonuclear leukocytes: Neutrophil percentage (0-2 points)
      - <70%: 0 points
      - 70-84%: 1 point  
      - ≥85%: 2 points
    - White blood cell count: ×10⁹/L (0-2 points)
      - <10: 0 points
      - 10.0-14.9: 1 point
      - ≥15: 2 points
    - C-reactive protein: mg/L (0-2 points)
      - <10: 0 points
      - 10-49: 1 point
      - ≥50: 2 points
    
    Total score ranges from 0-12 points with interpretation:
    - 0-4 points: Low risk (outpatient management possible)
    - 5-8 points: Indeterminate risk (admit for observation)
    - 9-12 points: High risk (surgical consultation recommended)
    
    References (Vancouver style):
    1. Andersson M, Andersson RE. The appendicitis inflammatory response score: 
       a tool for the diagnosis of acute appendicitis that outperforms the Alvarado score. 
       World J Surg. 2008;32(8):1843-9.
    2. Sammalkorpi HE, Mentula P, Leppäniemi A. A new adult appendicitis score improves 
       diagnostic accuracy of acute appendicitis—a prospective study. BMC Gastroenterol. 
       2014;14:114.
    3. Scott AJ, Mason SE, Arunakirinathan M, et al. Risk stratification by the 
       Appendicitis Inflammatory Response score to guide decision-making in patients 
       with suspected appendicitis. Br J Surg. 2015;102(5):563-72.
    """
    
    vomiting: Literal["no", "yes"] = Field(
        ...,
        description="Presence of vomiting. Scores 0 points if no, 1 point if yes",
        example="no"
    )
    
    rif_pain: Literal["no", "yes"] = Field(
        ...,
        description="Right iliac fossa (RIF) pain. Scores 0 points if no, 1 point if yes",
        example="yes"
    )
    
    rebound_tenderness: Literal["none", "light", "medium", "strong"] = Field(
        ...,
        description="Rebound tenderness (percussion tenderness) reflecting peritoneal irritation. Graded as none (0 points), light (1 point), medium (2 points), or strong (3 points)",
        example="medium"
    )
    
    fever: Literal["no", "yes"] = Field(
        ...,
        description="Temperature ≥38.5°C (101.3°F). Scores 0 points if no, 1 point if yes",
        example="yes"
    )
    
    polymorphonuclear_percentage: Literal["under_70", "70_to_84", "85_or_over"] = Field(
        ...,
        description="Polymorphonuclear leukocytes (neutrophils) percentage. Under 70% scores 0 points, 70-84% scores 1 point, 85% or over scores 2 points. Advanced appendicitis often shows high neutrophil percentage due to lymphopenia",
        example="70_to_84"
    )
    
    wbc_count: Literal["under_10", "10_to_14_9", "15_or_over"] = Field(
        ...,
        description="White blood cell count (×10⁹/L). Under 10 scores 0 points, 10.0-14.9 scores 1 point, 15 or over scores 2 points",
        example="10_to_14_9"
    )
    
    crp_level: Literal["under_10", "10_to_49", "50_or_over"] = Field(
        ...,
        description="C-reactive protein level (mg/L). Under 10 scores 0 points, 10-49 scores 1 point, 50 or over scores 2 points",
        example="10_to_49"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "vomiting": "no",
                "rif_pain": "yes",
                "rebound_tenderness": "medium",
                "fever": "yes",
                "polymorphonuclear_percentage": "70_to_84",
                "wbc_count": "10_to_14_9",
                "crp_level": "10_to_49"
            }
        }


class AirScoreResponse(BaseModel):
    """
    Response model for Appendicitis Inflammatory Response (AIR) Score
    
    The AIR Score ranges from 0-12 points and stratifies patients into three risk categories:
    
    - Low Risk (0-4 points): Low probability of appendicitis
      * Outpatient follow-up if patient has unaltered general condition
      * Consider other diagnoses
      * Can be discharged with planned reexamination if clinically stable
    
    - Indeterminate Risk (5-8 points): Intermediate probability of appendicitis
      * Admit patient for observation and serial reassessment
      * Consider rescoring after 4-8 hours of observation
      * May require imaging studies or surgical consultation
    
    - High Risk (9-12 points): High probability of appendicitis
      * High suspicion for appendicitis
      * Surgical consultation recommended
      * Consider immediate surgical intervention, especially for advanced appendicitis
    
    Clinical pearls:
    - The score is designed with high sensitivity for advanced appendicitis
    - Works especially well in children and women
    - May be less specific in elderly patients (consider lower threshold for CT)
    - Patients with short symptom duration may have low scores initially
    - The neutrophil proportion is particularly important in advanced appendicitis
    
    Reference: Andersson M, Andersson RE. World J Surg. 2008;32(8):1843-9.
    """
    
    result: int = Field(
        ...,
        description="AIR Score calculated from clinical and laboratory variables (range: 0-12 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Admit patient for observation and serial reassessment. Consider rescoring after 4-8 hours of observation. May require imaging studies or surgical consultation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Indeterminate Risk, High Risk)",
        example="Indeterminate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate probability of appendicitis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Admit patient for observation and serial reassessment. Consider rescoring after 4-8 hours of observation. May require imaging studies or surgical consultation.",
                "stage": "Indeterminate Risk",
                "stage_description": "Intermediate probability of appendicitis"
            }
        }
