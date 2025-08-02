"""
Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis Models

Request and response models for Mayo DAI calculation.

References (Vancouver style):
1. Schroeder KW, Tremaine WJ, Ilstrup DM. Coated oral 5-aminosalicylic acid therapy 
   for mildly to moderately active ulcerative colitis. A randomized study. N Engl J Med. 
   1987 Dec 24;317(26):1625-9. doi: 10.1056/NEJM198712243172603.
2. D'Haens G, Sandborn WJ, Feagan BG, Geboes K, Hanauer SB, Irvine EJ, et al. 
   A review of activity indices and efficacy end points for clinical trials of medical 
   therapy in adults with ulcerative colitis. Gastroenterology. 2007 Feb;132(2):763-86. 
   doi: 10.1053/j.gastro.2006.12.038.
3. Lewis JD, Chuai S, Nessel L, Lichtenstein GR, Aberra FN, Ellenberg JH. Use of the 
   noninvasive components of the Mayo score to assess clinical response in ulcerative 
   colitis. Inflamm Bowel Dis. 2008 Dec;14(12):1660-6. doi: 10.1002/ibd.20520.
4. Feagan BG, Rutgeerts P, Sands BE, Hanauer S, Colombel JF, Sandborn WJ, et al. 
   Vedolizumab as induction and maintenance therapy for ulcerative colitis. N Engl J Med. 
   2013 Aug 22;369(8):699-710. doi: 10.1056/NEJMoa1215734.

The Mayo Score/Disease Activity Index (DAI) is the most widely adopted disease 
activity index for ulcerative colitis in clinical trials (49.5% adoption rate). 
It assesses disease severity using four parameters: stool frequency, rectal bleeding, 
mucosal appearance on endoscopy, and physician's global assessment. Each component 
is scored from 0-3 points, with total scores ranging from 0-12. Remission is defined 
as total score ≤2 with no individual component >1 point.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class MayoScoreDiseaseActivityIndexDaiUlcerativeColitisRequest(BaseModel):
    """
    Request model for Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis
    
    The Mayo DAI uses four clinical and endoscopic parameters to assess ulcerative colitis severity:
    
    **1. Stool Frequency (0-3 points):**
    - normal: Normal for patient (0 points)
    - 1_2_more_than_normal: 1-2 stools/day more than normal (1 point)
    - 3_4_more_than_normal: 3-4 stools/day more than normal (2 points)
    - more_than_4_more_than_normal: >4 stools/day more than normal (3 points)
    
    **2. Rectal Bleeding (0-3 points):**
    - none: No blood seen (0 points)
    - visible_blood_less_than_half_time: Visible blood with stool less than half of BMs (1 point)
    - visible_blood_half_time_or_more: Visible blood with stool half of BMs or more (2 points)
    - passing_blood_alone: Passing blood alone (3 points)
    
    **3. Mucosal Appearance - Endoscopic Assessment (0-3 points):**
    - normal_inactive: Normal or inactive disease (0 points)
    - mild_disease: Mild disease (erythema, decreased vascular pattern, mild friability) (1 point)
    - moderate_disease: Moderate disease (marked erythema, absent vascular pattern, friability, erosions) (2 points)
    - severe_disease: Severe disease (spontaneous bleeding, ulceration) (3 points)
    
    **4. Physician's Global Assessment (0-3 points):**
    - normal: Normal (0 points)
    - mild: Mild disease (1 point)
    - moderate: Moderate disease (2 points)
    - severe: Severe disease (3 points)
    
    **Scoring and Interpretation:**
    - **Remission (0-2 points)**: Minimal symptoms, therapeutic goal achieved
    - **Mild Disease (3-5 points)**: Mild symptoms, may need treatment optimization
    - **Moderate Disease (6-10 points)**: Active symptoms, requires intensive treatment
    - **Severe Disease (11-12 points)**: Severe symptoms, urgent aggressive treatment needed
    
    **Clinical Notes:**
    - Originally developed in 1987 during 5-ASA clinical trials
    - Most widely used activity index in UC clinical trials
    - Correlates closely with quality of life measures
    - Remission requires total score ≤2 AND no individual component >1
    - Mucosal healing defined as endoscopic subscore 0-1
    - Clinically meaningful change is ≥3 point reduction in total score
    
    References (Vancouver style):
    1. Schroeder KW, Tremaine WJ, Ilstrup DM. Coated oral 5-aminosalicylic acid therapy 
    for mildly to moderately active ulcerative colitis. A randomized study. N Engl J Med. 
    1987 Dec 24;317(26):1625-9. doi: 10.1056/NEJM198712243172603.
    2. D'Haens G, Sandborn WJ, Feagan BG, Geboes K, Hanauer SB, Irvine EJ, et al. 
    A review of activity indices and efficacy end points for clinical trials of medical 
    therapy in adults with ulcerative colitis. Gastroenterology. 2007 Feb;132(2):763-86. 
    doi: 10.1053/j.gastro.2006.12.038.
    3. Lewis JD, Chuai S, Nessel L, Lichtenstein GR, Aberra FN, Ellenberg JH. Use of the 
    noninvasive components of the Mayo score to assess clinical response in ulcerative 
    colitis. Inflamm Bowel Dis. 2008 Dec;14(12):1660-6. doi: 10.1002/ibd.20520.
    4. Feagan BG, Rutgeerts P, Sands BE, Hanauer S, Colombel JF, Sandborn WJ, et al. 
    Vedolizumab as induction and maintenance therapy for ulcerative colitis. N Engl J Med. 
    2013 Aug 22;369(8):699-710. doi: 10.1056/NEJMoa1215734.
    """
    
    stool_frequency: Literal["normal", "1_2_more_than_normal", "3_4_more_than_normal", "more_than_4_more_than_normal"] = Field(
        ...,
        description="Increase in stool frequency compared to patient's normal baseline. Assesses bowel movement frequency as indicator of disease activity and inflammation severity",
        example="1_2_more_than_normal"
    )
    
    rectal_bleeding: Literal["none", "visible_blood_less_than_half_time", "visible_blood_half_time_or_more", "passing_blood_alone"] = Field(
        ...,
        description="Presence and severity of rectal bleeding. Key indicator of mucosal inflammation and disease activity in ulcerative colitis",
        example="visible_blood_less_than_half_time"
    )
    
    mucosal_appearance: Literal["normal_inactive", "mild_disease", "moderate_disease", "severe_disease"] = Field(
        ...,
        description="Endoscopic findings of mucosal inflammation. Objective assessment of colonic mucosa appearance during endoscopy, critical for disease severity evaluation",
        example="mild_disease"
    )
    
    physician_global_assessment: Literal["normal", "mild", "moderate", "severe"] = Field(
        ...,
        description="Physician's overall clinical assessment of disease activity. Incorporates clinical judgment considering all aspects of patient's condition including extraintestinal manifestations",
        example="mild"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "stool_frequency": "1_2_more_than_normal",
                "rectal_bleeding": "visible_blood_less_than_half_time",
                "mucosal_appearance": "mild_disease",
                "physician_global_assessment": "mild"
            }
        }


class MayoScoreDiseaseActivityIndexDaiUlcerativeColitisResponse(BaseModel):
    """
    Response model for Mayo Score/Disease Activity Index (DAI) for Ulcerative Colitis
    
    The Mayo DAI score ranges from 0-12 points and classifies patients into:
    - **Remission (0-2 points)**: Disease remission, therapeutic goal achieved
    - **Mild Disease (3-5 points)**: Mildly active disease, may need optimization
    - **Moderate Disease (6-10 points)**: Moderately active disease, intensive treatment needed
    - **Severe Disease (11-12 points)**: Severely active disease, urgent intervention required
    
    Reference: Schroeder KW, et al. N Engl J Med. 1987;317(26):1625-9.
    """
    
    result: int = Field(
        ...,
        description="Mayo DAI score calculated from four clinical parameters (range: 0-12 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the score",
        example="Mayo DAI score 3-5 indicates mildly active ulcerative colitis. Patients have mild symptoms with some increase in stool frequency, intermittent bleeding, mild endoscopic changes with erythema and decreased vascular pattern. Treatment adjustment may be considered to achieve remission, with focus on optimizing current therapy or adding topical treatments."
    )
    
    stage: str = Field(
        ...,
        description="Disease activity category (Remission, Mild Disease, Moderate Disease, Severe Disease)",
        example="Mild Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease activity level",
        example="Mildly active disease"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Individual component scores for detailed assessment",
        example={
            "stool_frequency": 1,
            "rectal_bleeding": 1,
            "mucosal_appearance": 1,
            "physician_global_assessment": 1
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Mayo DAI score 3-5 indicates mildly active ulcerative colitis. Patients have mild symptoms with some increase in stool frequency, intermittent bleeding, mild endoscopic changes with erythema and decreased vascular pattern. Treatment adjustment may be considered to achieve remission, with focus on optimizing current therapy or adding topical treatments.",
                "stage": "Mild Disease",
                "stage_description": "Mildly active disease",
                "component_scores": {
                    "stool_frequency": 1,
                    "rectal_bleeding": 1,
                    "mucosal_appearance": 1,
                    "physician_global_assessment": 1
                }
            }
        }