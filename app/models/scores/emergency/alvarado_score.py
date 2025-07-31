"""
Alvarado Score for Acute Appendicitis Models

Request and response models for Alvarado Score calculation.

References (Vancouver style):
1. Alvarado A. A practical score for the early diagnosis of acute appendicitis. 
   Ann Emerg Med. 1986 May;15(5):557-64. doi: 10.1016/0196-0644(86)90014-6. PMID: 3963537.
2. Alvarado A. How to improve the clinical diagnosis of acute appendicitis in resource 
   limited settings. World J Emerg Surg. 2016 Apr 26;11:16. doi: 10.1186/s13017-016-0071-9. 
   PMID: 27123036; PMCID: PMC4845369.
3. Coleman JJ, Carr BW, Rogers T, Patel N, Krapohl GL, Hallbeck MS, Bartlett EK. 
   The Alvarado score should be used to reduce emergency department length of stay and 
   CT use in select patients with abdominal pain. J Trauma Acute Care Surg. 2018 
   Jun;84(6):946-950. doi: 10.1097/TA.0000000000001876. PMID: 29389735.

The Alvarado Score is a clinical decision rule that uses 8 clinical variables organized 
by the mnemonic MANTRELS to assess the probability of acute appendicitis. Originally 
developed by Dr. Alfredo Alvarado in 1986, it remains one of the most widely used and 
validated scoring systems for appendicitis diagnosis. The score ranges from 0-10 points, 
with higher scores indicating higher probability of appendicitis.

The MANTRELS mnemonic stands for:
- Migration of pain to right lower quadrant (1 point)
- Anorexia (1 point)  
- Nausea/vomiting (1 point)
- Tenderness in right lower quadrant (2 points)
- Rebound tenderness (1 point)
- Elevated temperature >37.3°C (1 point)
- Leukocytosis >10,000/μL (2 points)
- Left Shift of neutrophils >75% (1 point)

Clinical utility: Scores ≤3 suggest low probability (consider discharge), scores 4-6 
suggest intermediate probability (consider observation/imaging), scores 7-8 suggest 
high probability (surgical consultation), and scores 9-10 suggest very high probability 
(immediate surgical evaluation).
"""

from pydantic import BaseModel, Field
from typing import Literal


class AlvaradoScoreRequest(BaseModel):
    """
    Request model for Alvarado Score for Acute Appendicitis
    
    The Alvarado Score uses 8 clinical variables organized by the MANTRELS mnemonic 
    to assess probability of acute appendicitis:
    
    MANTRELS Components:
    M - Migration of pain to the right lower quadrant (right iliac fossa) - 1 point
    A - Anorexia (loss of appetite) - 1 point
    N - Nausea or vomiting - 1 point
    T - Tenderness in the right lower quadrant - 2 points (most important predictor)
    R - Rebound tenderness or indirect signs (Rovsing, Dunphy, Markle test) - 1 point
    E - Elevated temperature (fever >37.3°C or >99.1°F) - 1 point
    L - Leukocytosis (white blood cell count >10,000/μL) - 2 points (most important predictor)
    S - Left Shift of neutrophils (>75% neutrophils) - 1 point
    
    Clinical Application:
    - Originally developed as both a rule-out tool (low scores) and rule-in tool (high scores)
    - Best validated in men and children; higher false-positive rate in women of childbearing age
    - Can help guide decisions about discharge, observation, imaging, or surgical consultation
    - Should be used in conjunction with clinical judgment, not as sole decision-making tool
    
    Scoring Interpretation:
    - 0-3 points: Low probability (1-6% risk) - consider discharge with follow-up
    - 4-6 points: Intermediate probability (15-25% risk) - consider observation/imaging
    - 7-8 points: High probability (75-85% risk) - surgical consultation indicated
    - 9-10 points: Very high probability (>90% risk) - immediate surgery consultation
    
    References (Vancouver style):
    1. Alvarado A. A practical score for the early diagnosis of acute appendicitis. 
    Ann Emerg Med. 1986 May;15(5):557-64. doi: 10.1016/0196-0644(86)90014-6. PMID: 3963537.
    2. Alvarado A. How to improve the clinical diagnosis of acute appendicitis in resource 
    limited settings. World J Emerg Surg. 2016 Apr 26;11:16. doi: 10.1186/s13017-016-0071-9. 
    PMID: 27123036; PMCID: PMC4845369.
    """
    
    migration_to_rlq: Literal["yes", "no"] = Field(
        ...,
        description="Migration of pain to the right lower quadrant (right iliac fossa). Classic symptom where initial periumbilical or epigastric pain localizes to McBurney's point. Scores 1 point if present",
        example="yes"
    )
    
    anorexia: Literal["yes", "no"] = Field(
        ...,
        description="Anorexia (loss of appetite). Patient reports decreased desire to eat or inability to eat normally. In 2016 refinement, can be assessed by urine ketones >2+. Scores 1 point if present",
        example="yes"
    )
    
    nausea_vomiting: Literal["yes", "no"] = Field(
        ...,
        description="Nausea or vomiting. Either feeling of nausea or actual vomiting episodes. Common early symptom in appendicitis. Scores 1 point if present",
        example="no"
    )
    
    tenderness_rlq: Literal["yes", "no"] = Field(
        ...,
        description="Tenderness in the right lower quadrant (right iliac fossa). Localized tenderness at McBurney's point or surrounding area on palpation. Most important clinical predictor. Scores 2 points if present",
        example="yes"
    )
    
    rebound_tenderness: Literal["yes", "no"] = Field(
        ...,
        description="Rebound tenderness or indirect signs of peritoneal irritation. Can include classic rebound tenderness, Rovsing sign, Dunphy sign, Markle test, or percussion tenderness. Scores 1 point if present",
        example="no"
    )
    
    elevated_temperature: Literal["yes", "no"] = Field(
        ...,
        description="Elevated temperature (fever). Body temperature >37.3°C (99.1°F). May be low-grade initially but indicates inflammatory response. Scores 1 point if present",
        example="yes"
    )
    
    leukocytosis: Literal["yes", "no"] = Field(
        ...,
        description="Leukocytosis (elevated white blood cell count). WBC count >10,000/μL (>10.0 × 10⁹/L). Indicates systemic inflammatory response. Most important laboratory predictor. Scores 2 points if present",
        example="yes"
    )
    
    neutrophil_left_shift: Literal["yes", "no"] = Field(
        ...,
        description="Neutrophil left shift. >75% neutrophils on differential count. Indicates acute bacterial infection with release of immature neutrophils. Scores 1 point if present",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "migration_to_rlq": "yes",
                "anorexia": "yes", 
                "nausea_vomiting": "no",
                "tenderness_rlq": "yes",
                "rebound_tenderness": "no",
                "elevated_temperature": "yes",
                "leukocytosis": "yes",
                "neutrophil_left_shift": "no"
            }
        }


class AlvaradoScoreResponse(BaseModel):
    """
    Response model for Alvarado Score for Acute Appendicitis
    
    The Alvarado Score provides risk stratification for acute appendicitis:
    
    Score Interpretation:
    
    Low Risk (0-3 points):
    - 1-6% probability of appendicitis
    - Consider discharge with close follow-up instructions
    - No routine imaging needed
    - Return precautions for worsening symptoms
    
    Intermediate Risk (4-6 points):
    - 15-25% probability of appendicitis  
    - Consider active observation with serial examinations
    - May benefit from CT imaging for further evaluation
    - Surgical consultation may be appropriate
    
    High Risk (7-8 points):
    - 75-85% probability of appendicitis
    - Strong indication for surgical consultation
    - Likely candidate for appendectomy
    - Consider expedited surgical evaluation
    
    Very High Risk (9-10 points):
    - >90% probability of appendicitis
    - Very strong indication for immediate surgical consultation
    - High likelihood of requiring appendectomy
    - Imaging may unnecessarily delay surgery
    
    Clinical Considerations:
    - Performs better in men and children than women of childbearing age
    - Should complement, not replace, clinical judgment
    - Originally designed for emergency department triage and decision-making
    - Can help reduce unnecessary CT scans in very low-risk patients
    
    Reference: Alvarado A. Ann Emerg Med. 1986;15(5):557-64.
    """
    
    result: int = Field(
        ...,
        ge=0,
        le=10,
        description="Alvarado score calculated from MANTRELS criteria (range: 0-10 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with specific management recommendations based on the score",
        example="Intermediate probability of appendicitis (15-25% risk). Consider observation, serial exams, or imaging (CT scan). Surgical consultation may be warranted."
    )
    
    stage: str = Field(
        ...,
        description="Risk category classification (Low Risk, Intermediate Risk, High Risk, Very High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate probability of appendicitis"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Intermediate probability of appendicitis (15-25% risk). Consider observation, serial exams, or imaging (CT scan). Surgical consultation may be warranted.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate probability of appendicitis"
            }
        }