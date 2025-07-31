"""
Eosinophilic Esophagitis Endoscopic Reference Score (EREFS) Models

Request and response models for EREFS calculation.

References (Vancouver style):
1. Hirano I, Moy N, Heckman MG, Thomas CS, Gonsalves N, Achem SR. Endoscopic 
   assessment of the oesophageal features of eosinophilic oesophagitis: validation 
   of a novel classification and grading system. Gut. 2013 Apr;62(4):489-95. 
   doi: 10.1136/gutjnl-2011-301817.
2. van Rhijn BD, Verheij J, van den Bergh Weerman MA, Verseijden C, van den Wijngaard RM, 
   de Jonge WJ, et al. The Endoscopic Reference Score shows modest accuracy to predict 
   either clinical or histological activity in adult patients with eosinophilic oesophagitis. 
   Aliment Pharmacol Ther. 2016 Aug;44(3):300-9. doi: 10.1111/apt.13698.
3. Dellon ES, Cotton CC, Gebhart JH, Higgins LL, Beitia R, Woosley JT, et al. 
   Accuracy of the Eosinophilic Esophagitis Endoscopic Reference Score in Diagnosis 
   and Determining Response to Treatment. Clin Gastroenterol Hepatol. 2016 Jan;14(1):31-9. 
   doi: 10.1016/j.cgh.2015.08.040.
4. Safroneeva E, Straumann A, Coslovsky M, Zwahlen M, Kuehni CE, Panczak R, et al. 
   Symptoms Have Modest Accuracy in Detecting Endoscopic and Histologic Remission in 
   Adults With Eosinophilic Esophagitis. Gastroenterology. 2016 Sep;151(3):446-57.e5. 
   doi: 10.1053/j.gastro.2016.05.040.

The EREFS is a standardized endoscopic scoring system for eosinophilic esophagitis 
that evaluates five major endoscopic features: edema, rings, exudates, furrows, 
and strictures. This tool helps clinicians assess disease severity, track treatment 
response, and standardize endoscopic evaluation of EoE patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class ErefsRequest(BaseModel):
    """
    Request model for Eosinophilic Esophagitis Endoscopic Reference Score (EREFS)
    
    The EREFS evaluates five major endoscopic features of eosinophilic esophagitis:
    
    1. Edema (0-1 points):
       - 0: Absent
       - 1: Present (loss of normal vascular markings; pallor or decreased transparency)
    
    2. Rings (0-3 points):
       - 0: None
       - 1: Mild (subtle, circumferential ridges)
       - 2: Moderate (distinct rings that don't impair scope passage)
       - 3: Severe (fixed rings that impair scope passage)
    
    3. Exudates (0-2 points):
       - 0: None
       - 1: Mild (≤10% of mucosal surface covered by white plaques)
       - 2: Severe (>10% of mucosal surface covered)
    
    4. Furrows (0-1 points):
       - 0: Absent
       - 1: Present (vertical lines or creases along esophageal wall)
    
    5. Strictures (0-1 points):
       - 0: None
       - 1: Present (fixed narrowings requiring small-caliber scope or causing resistance)
    
    Clinical Application:
    - Standardizes endoscopic assessment of EoE
    - Tracks disease progression and treatment response
    - Should be used in conjunction with histologic assessment
    - Recommended to score the segment with worst findings
    
    References (Vancouver style):
    1. Hirano I, Moy N, Heckman MG, Thomas CS, Gonsalves N, Achem SR. Endoscopic 
       assessment of the oesophageal features of eosinophilic oesophagitis: validation 
       of a novel classification and grading system. Gut. 2013 Apr;62(4):489-95. 
       doi: 10.1136/gutjnl-2011-301817.
    2. Dellon ES, Cotton CC, Gebhart JH, Higgins LL, Beitia R, Woosley JT, et al. 
       Accuracy of the Eosinophilic Esophagitis Endoscopic Reference Score in Diagnosis 
       and Determining Response to Treatment. Clin Gastroenterol Hepatol. 2016 Jan;14(1):31-9. 
       doi: 10.1016/j.cgh.2015.08.040.
    """
    
    edema: Literal[0, 1] = Field(
        ...,
        description="Edema: Loss of normal vascular markings, pallor, or decreased transparency. 0 = Absent, 1 = Present",
        example=1
    )
    
    rings: Literal[0, 1, 2, 3] = Field(
        ...,
        description="Rings: Trachealization/feline esophagus appearance with concentric rings. 0 = None, 1 = Mild (subtle), 2 = Moderate, 3 = Severe (fixed rings)",
        example=2
    )
    
    exudates: Literal[0, 1, 2] = Field(
        ...,
        description="Exudates: White plaques on esophageal mucosa. 0 = None, 1 = Mild (≤10% surface), 2 = Severe (>10% surface)",
        example=1
    )
    
    furrows: Literal[0, 1] = Field(
        ...,
        description="Furrows: Vertical lines or creases along the esophageal wall. 0 = Absent, 1 = Present",
        example=1
    )
    
    strictures: Literal[0, 1] = Field(
        ...,
        description="Strictures: Fixed narrowings requiring small-caliber scope or causing resistance. 0 = None, 1 = Present",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "edema": 1,
                "rings": 2,
                "exudates": 1,
                "furrows": 1,
                "strictures": 0
            }
        }


class ErefsResponse(BaseModel):
    """
    Response model for Eosinophilic Esophagitis Endoscopic Reference Score (EREFS)
    
    The EREFS score ranges from 0-9 points and provides standardized assessment of 
    endoscopic severity in eosinophilic esophagitis:
    
    Score Interpretation:
    - 0 points: No endoscopic features (normal endoscopy doesn't exclude EoE)
    - 1-2 points: Mild disease (monitor and correlate with histology)
    - 3-5 points: Moderate disease (established disease, consider treatment)
    - 6-9 points: Severe disease (advanced disease, aggressive treatment needed)
    
    Clinical Applications:
    - Standardizes endoscopic assessment across providers
    - Tracks treatment response over time
    - Guides management decisions based on severity
    - Research tool for clinical studies
    
    Important Limitations:
    - Should be used with histological assessment (gold standard)
    - 12-21% misclassification rate for treatment response
    - Normal endoscopy doesn't exclude EoE diagnosis
    - Interobserver agreement varies by feature
    
    Reference: Hirano I, et al. Gut. 2013;62(4):489-95.
    """
    
    result: int = Field(
        ...,
        description="Total EREFS score calculated from five endoscopic features (range: 0-9 points)",
        ge=0,
        le=9,
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including individual feature findings and overall disease severity assessment",
        example="EREFS score: 5/9. Edema: Present (loss of vascular markings); Rings: Moderate; Exudates: Mild (≤10% mucosal surface); Furrows: Present. Moderate endoscopic evidence of eosinophilic esophagitis. Multiple features present suggest established disease. Correlate with histology and consider appropriate anti-inflammatory treatment."
    )
    
    stage: str = Field(
        ...,
        description="Disease severity stage based on total score (No Endoscopic Features, Mild Disease, Moderate Disease, Severe Disease)",
        example="Moderate Disease"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the disease severity stage",
        example="Moderate endoscopic features"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5,
                "unit": "points",
                "interpretation": "EREFS score: 5/9. Edema: Present (loss of vascular markings); Rings: Moderate; Exudates: Mild (≤10% mucosal surface); Furrows: Present. Moderate endoscopic evidence of eosinophilic esophagitis. Multiple features present suggest established disease. Correlate with histology and consider appropriate anti-inflammatory treatment.",
                "stage": "Moderate Disease",
                "stage_description": "Moderate endoscopic features"
            }
        }