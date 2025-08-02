"""
Truelove and Witts Severity Index for Ulcerative Colitis Models

Request and response models for the Truelove and Witts Severity Index calculation.

References (Vancouver style):
1. Truelove SC, Witts LJ. Cortisone in ulcerative colitis; final report on a therapeutic trial. 
   Br Med J. 1955;2(4947):1041-8. doi: 10.1136/bmj.2.4947.1041. PMID: 13260656; PMCID: PMC2061071.
2. Danese S, Fiocchi C. Ulcerative colitis. N Engl J Med. 2011 Nov 3;365(18):1713-25. 
   doi: 10.1056/NEJMra1102942. PMID: 22047562.
3. Rubin DT, Ananthakrishnan AN, Siegel CA, Sauer BG, Long MD. ACG Clinical Guideline: 
   Ulcerative Colitis in Adults. Am J Gastroenterol. 2019 Mar;114(3):384-413. 
   doi: 10.14309/ajg.0000000000000152. PMID: 30840605.

The Truelove and Witts Severity Index is a classic clinical tool developed in 1955 for 
stratifying ulcerative colitis severity. It evaluates six parameters (bowel movements, 
blood in stool, fever, tachycardia, anemia, and ESR) to classify disease as mild, 
moderate, or severe, guiding treatment decisions and prognosis assessment.
"""

from pydantic import BaseModel, Field
from typing import Literal


class TrueloveWittsSeverityIndexRequest(BaseModel):
    """
    Request model for Truelove and Witts Severity Index for Ulcerative Colitis
    
    The Truelove and Witts Severity Index evaluates six clinical and laboratory 
    parameters to classify ulcerative colitis severity:
    
    Clinical Parameters:
    - Bowel movements per day: Frequency of bowel movements in 24-hour period
    - Blood in stool: Visual assessment of rectal bleeding severity
    - Pyrexia: Fever ≥100.04°F (37.8°C)
    - Tachycardia: Heart rate >90 beats per minute
    
    Laboratory Parameters:
    - Anemia: Hemoglobin ≤10.5 g/dL (105 g/L)
    - ESR: Erythrocyte sedimentation rate >30 mm/hr
    
    Severity Classification:
    - Mild: All criteria for mild severity are met (minimal symptoms, no systemic features)
    - Severe: ≥6 bowel movements AND ≥1 systemic feature (fever, tachycardia, or anemia)
    - Moderate: Between mild and severe criteria
    
    Clinical Significance:
    The index helps guide treatment decisions - mild disease may be managed outpatient 
    with aminosalicylates, while severe disease requires hospitalization and intensive 
    medical therapy.
    
    References (Vancouver style):
    1. Truelove SC, Witts LJ. Cortisone in ulcerative colitis; final report on a 
       therapeutic trial. Br Med J. 1955;2(4947):1041-8. doi: 10.1136/bmj.2.4947.1041.
    2. Danese S, Fiocchi C. Ulcerative colitis. N Engl J Med. 2011 Nov 3;365(18):1713-25. 
       doi: 10.1056/NEJMra1102942.
    """
    
    bowel_movements: Literal["less_than_4", "4_to_5", "6_or_more"] = Field(
        ...,
        description="Number of bowel movements per day. Count all bowel movements in a 24-hour period. "
                    "Less than 4 suggests mild disease, 4-5 suggests moderate, and 6 or more suggests "
                    "severe disease when combined with systemic features.",
        example="4_to_5"
    )
    
    blood_in_stool: Literal["none_or_small", "between_mild_severe", "visible_blood"] = Field(
        ...,
        description="Presence and severity of blood in stool. 'None or small amounts' indicates "
                    "minimal or no visible blood, 'between mild and severe' indicates moderate "
                    "bleeding, and 'visible blood' indicates frank blood in stool.",
        example="between_mild_severe"
    )
    
    pyrexia: Literal["no", "yes"] = Field(
        ...,
        description="Presence of fever defined as temperature ≥100.04°F (37.8°C). Fever is a "
                    "systemic sign that, when present with frequent bowel movements, indicates "
                    "severe disease requiring immediate medical attention.",
        example="no"
    )
    
    tachycardia: Literal["no", "yes"] = Field(
        ...,
        description="Pulse rate greater than 90 beats per minute. Tachycardia is a systemic "
                    "sign that may indicate severe disease, especially when combined with "
                    "frequent bowel movements and other systemic features.",
        example="no"
    )
    
    anemia: Literal["no", "yes"] = Field(
        ...,
        description="Presence of anemia defined as hemoglobin ≤10.5 g/dL (105 g/L). Anemia "
                    "in ulcerative colitis may result from chronic blood loss and indicates "
                    "more severe disease when present with other criteria.",
        example="no"
    )
    
    esr_elevated: Literal["no", "yes"] = Field(
        ...,
        description="Erythrocyte sedimentation rate (ESR) greater than 30 mm/hr. Elevated ESR "
                    "indicates systemic inflammation and is associated with more active disease. "
                    "ESR >30 mm/hr suggests moderate to severe disease activity.",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "bowel_movements": "4_to_5",
                "blood_in_stool": "between_mild_severe",
                "pyrexia": "no",
                "tachycardia": "no",
                "anemia": "no",
                "esr_elevated": "yes"
            }
        }


class TrueloveWittsSeverityIndexResponse(BaseModel):
    """
    Response model for Truelove and Witts Severity Index for Ulcerative Colitis
    
    Returns the severity classification (mild, moderate, or severe) with appropriate 
    clinical interpretation and management recommendations.
    
    Severity Categories:
    - Mild: Minimal symptoms, no systemic features, can often be managed outpatient
    - Moderate: Some systemic symptoms, may require hospitalization for optimization
    - Severe: Significant systemic symptoms, requires immediate hospitalization and 
      intensive therapy
    
    Clinical Management:
    - Mild: Topical or oral aminosalicylates, close monitoring
    - Moderate: Oral corticosteroids, immunomodulators, consider hospitalization
    - Severe: IV corticosteroids, biologics, surgical consultation, monitor for complications
    
    Reference: Truelove SC, Witts LJ. Br Med J. 1955;2(4947):1041-8.
    """
    
    result: str = Field(
        ...,
        description="Severity classification of ulcerative colitis (mild, moderate, or severe)",
        example="moderate"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (empty for categorical result)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on severity classification",
        example="Moderate disease with some systemic symptoms. Consider oral corticosteroids or immunomodulators. May require hospitalization for monitoring and treatment optimization."
    )
    
    stage: str = Field(
        ...,
        description="Severity classification category (Mild, Moderate, Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the severity category",
        example="Moderate ulcerative colitis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "moderate",
                "unit": "",
                "interpretation": "Moderate disease with some systemic symptoms. Consider oral corticosteroids or immunomodulators. May require hospitalization for monitoring and treatment optimization.",
                "stage": "Moderate",
                "stage_description": "Moderate ulcerative colitis"
            }
        }