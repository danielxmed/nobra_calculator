"""
Brief Alcohol Withdrawal Scale (BAWS) Models

Request and response models for BAWS calculation.

References (Vancouver style):
1. Rastegar DA, Kuntz JL, Brower KJ, et al. Brief Alcohol Withdrawal Scale (BAWS): 
   A practical tool for the evaluation of alcohol withdrawal symptoms. Subst Abus. 
   2017;38(4):463-469. doi: 10.1080/08897077.2017.1323346.
2. Chaudhry RA, Schreck JS. Evaluation of the Brief Alcohol Withdrawal Scale Protocol 
   at an Academic Medical Center. J Intensive Care Med. 2020;35(3):268-272. 
   doi: 10.1177/0885066618815781.
3. Maldonado JR, Nguyen LH, Schader EM, Brooks JO 3rd. Dexmedetomidine and the 
   reduction of postoperative delirium after cardiac surgery. Psychosomatics. 
   2009;50(3):206-17. doi: 10.1176/appi.psy.50.3.206.

The BAWS is a 5-item assessment tool that evaluates alcohol withdrawal symptoms 
using tremor, sweats, agitation, orientation, and hallucinations. Each item is 
scored from 0-3 points, with higher scores indicating more severe withdrawal 
symptoms. It serves as a simplified alternative to the CIWA-Ar scale while 
maintaining good clinical correlation and requiring less administration time.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class BawsRequest(BaseModel):
    """
    Request model for Brief Alcohol Withdrawal Scale (BAWS)
    
    The BAWS uses 5 parameters to assess alcohol withdrawal severity:
    
    1. Tremor (0-3 points):
       - 0: No tremor
       - 1: Not visible, but can be felt
       - 2: Moderate, with arms extended
       - 3: At rest, without arms extended
    
    2. Sweats/Diaphoresis (0-3 points):
       - 0: No sweats
       - 1: Mild, barely visible
       - 2: Beads of sweat
       - 3: Drenching sweats
    
    3. Agitation based on RASS scale (0-3 points):
       - 0: Alert and calm (RASS = 0)
       - 1: Restless, anxious, apprehensive (RASS = 1)
       - 2: Agitated, frequent non-purposeful movement (RASS = 2)
       - 3: Very agitated or combative (RASS = 3 or 4)
    
    4. Orientation (0-3 points):
       - 0: Oriented to person, place, time
       - 1: Disoriented to time or place, but not both
       - 2: Disoriented to time and place
       - 3: Disoriented to person
    
    5. Hallucinations (0-3 points):
       - 0: None
       - 1: Mild (vague report, reality testing intact)
       - 2: Moderate (more defined hallucinations)
       - 3: Severe (responding to internal stimuli, poor reality testing)
    
    Score Interpretation:
    - 0-2: Mild withdrawal (minimal intervention)
    - 3-5: Moderate withdrawal (benzodiazepine treatment threshold)
    - 6-8: Severe withdrawal (increased intervention)
    - ≥9: Very severe withdrawal (immediate physician notification)
    
    References (Vancouver style):
    1. Rastegar DA, Kuntz JL, Brower KJ, et al. Brief Alcohol Withdrawal Scale (BAWS): 
    A practical tool for the evaluation of alcohol withdrawal symptoms. Subst Abus. 
    2017;38(4):463-469. doi: 10.1080/08897077.2017.1323346.
    2. Chaudhry RA, Schreck JS. Evaluation of the Brief Alcohol Withdrawal Scale Protocol 
    at an Academic Medical Center. J Intensive Care Med. 2020;35(3):268-272. 
    doi: 10.1177/0885066618815781.
    3. Maldonado JR, Nguyen LH, Schader EM, Brooks JO 3rd. Dexmedetomidine and the 
    reduction of postoperative delirium after cardiac surgery. Psychosomatics. 
    2009;50(3):206-17. doi: 10.1176/appi.psy.50.3.206.
    """
    
    tremor: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Tremor severity. 0=No tremor, 1=Not visible but can be felt, 2=Moderate with arms extended, 3=At rest without arms extended",
        example=1
    )
    
    sweats: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Diaphoresis/sweating severity. 0=No sweats, 1=Mild barely visible, 2=Beads of sweat, 3=Drenching sweats",
        example=2
    )
    
    agitation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Agitation level based on RASS scale. 0=Alert and calm (RASS=0), 1=Restless/anxious (RASS=1), 2=Agitated frequent movement (RASS=2), 3=Very agitated/combative (RASS=3-4)",
        example=1
    )
    
    orientation: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Orientation to person, place, and time. 0=Oriented to all three, 1=Disoriented to time OR place, 2=Disoriented to time AND place, 3=Disoriented to person",
        example=0
    )
    
    hallucinations: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Presence and severity of hallucinations. 0=None, 1=Mild with intact reality testing, 2=Moderate more defined, 3=Severe responding to internal stimuli",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "tremor": 1,
                "sweats": 2,
                "agitation": 1,
                "orientation": 0,
                "hallucinations": 0
            }
        }


class BawsResponse(BaseModel):
    """
    Response model for Brief Alcohol Withdrawal Scale (BAWS)
    
    The BAWS total score ranges from 0-15 points and categorizes withdrawal severity:
    - 0-2: Mild withdrawal (minimal intervention required)
    - 3-5: Moderate withdrawal (treatment threshold reached)
    - 6-8: Severe withdrawal (significant intervention required)
    - ≥9: Very severe withdrawal (immediate physician notification)
    
    A BAWS score ≥3 correlates with CIWA-Ar ≥8 (treatment threshold) with 
    90% sensitivity and 80% specificity, making it an effective screening tool.
    
    Reference: Rastegar DA, et al. Subst Abus. 2017;38(4):463-469.
    """
    
    result: int = Field(
        ...,
        description="Total BAWS score (range: 0-15 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended management based on the score",
        example="Moderate withdrawal symptoms. Moderate intervention required. Consider benzodiazepine treatment (e.g., diazepam 10mg PO q4h until BAWS <3). Monitor closely for progression."
    )
    
    stage: str = Field(
        ...,
        description="Withdrawal severity category (Mild, Moderate, Severe, Very Severe)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the withdrawal severity",
        example="Moderate withdrawal symptoms"
    )
    
    components: Dict[str, int] = Field(
        ...,
        description="Individual component scores for tremor, sweats, agitation, orientation, and hallucinations",
        example={
            "tremor": 1,
            "sweats": 2,
            "agitation": 1,
            "orientation": 0,
            "hallucinations": 0
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Moderate withdrawal symptoms. Moderate intervention required. Consider benzodiazepine treatment (e.g., diazepam 10mg PO q4h until BAWS <3). Monitor closely for progression. Ensure adequate hydration and electrolyte replacement.",
                "stage": "Moderate",
                "stage_description": "Moderate withdrawal symptoms",
                "components": {
                    "tremor": 1,
                    "sweats": 2,
                    "agitation": 1,
                    "orientation": 0,
                    "hallucinations": 0
                }
            }
        }