"""
Harmless Acute Pancreatitis Score (HAPS) Models

Request and response models for HAPS calculation.

References (Vancouver style):
1. Lankisch PG, Weber-Dany B, Hebel K, Maisonneuve P, Lowenfels AB. The harmless acute 
   pancreatitis score: a clinical algorithm for rapid initial stratification of nonsevere 
   disease. Clin Gastroenterol Hepatol. 2009 Jun;7(6):702-5; quiz 607. doi: 10.1016/j.cgh.2009.02.020.
2. Oskarsson V, Mehrabi M, Orsini N, Hammarqvist F, Segersvärd R, Andrén-Sandberg Å, et al. 
   Validation of the harmless acute pancreatitis score in predicting nonsevere course of 
   acute pancreatitis. Pancreatology. 2011;11(5):464-8. doi: 10.1159/000331502.
3. Ma X, Li L, Jin T, Xia Q. Harmless acute pancreatitis score on admission can accurately 
   predict mild acute pancreatitis. Nan Fang Yi Ke Da Xue Xue Bao. 2021 Oct 20;41(10):1546-1550. 
   doi: 10.12122/j.issn.1673-4254.2021.10.14.
4. Tang J, Kong L, Wu J, Chen X, Liu L, Zhu X. The harmless acute pancreatitis score 
   (HAPS) identifies non-severe patients: A systematic review and meta-analysis. 
   Pancreatology. 2021 Dec;21(8):1419-1427. doi: 10.1016/j.pan.2021.09.017.

The Harmless Acute Pancreatitis Score (HAPS) is a simple clinical scoring system designed to 
identify patients with acute pancreatitis who will have a mild disease course and do not require 
intensive care unit admission. The score assesses three parameters at admission: absence of 
peritonitis, normal creatinine, and normal hematocrit. A HAPS score of 0 (all parameters normal) 
has 97% specificity and 98% positive predictive value for identifying non-severe acute pancreatitis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HapsRequest(BaseModel):
    """
    Request model for Harmless Acute Pancreatitis Score (HAPS)
    
    The HAPS uses three simple clinical parameters assessed at admission to identify 
    patients with acute pancreatitis who will have a mild disease course:
    
    1. Peritonitis: Absence of rebound tenderness or guarding (0 points if absent, 1 if present)
    2. Creatinine: Serum creatinine <2 mg/dL (0 points if <2, 1 point if ≥2)
    3. Hematocrit: Below threshold values (0 points if normal, 1 point if elevated)
       - Male: <43%
       - Female: <39.6%
    
    A total score of 0 indicates "harmless" acute pancreatitis with high specificity 
    for predicting a non-severe disease course without need for ICU admission.
    
    References (Vancouver style):
    1. Lankisch PG, Weber-Dany B, Hebel K, Maisonneuve P, Lowenfels AB. The harmless acute 
       pancreatitis score: a clinical algorithm for rapid initial stratification of nonsevere 
       disease. Clin Gastroenterol Hepatol. 2009 Jun;7(6):702-5; quiz 607. doi: 10.1016/j.cgh.2009.02.020.
    2. Oskarsson V, Mehrabi M, Orsini N, Hammarqvist F, Segersvärd R, Andrén-Sandberg Å, et al. 
       Validation of the harmless acute pancreatitis score in predicting nonsevere course of 
       acute pancreatitis. Pancreatology. 2011;11(5):464-8. doi: 10.1159/000331502.
    """
    
    peritonitis: Literal["absent", "present"] = Field(
        ...,
        description="Presence of peritonitis (rebound tenderness or guarding) on abdominal examination. "
                    "Absent scores 0 points (favorable), present scores 1 point. Peritonitis indicates "
                    "potential complications and excludes a 'harmless' course.",
        example="absent"
    )
    
    creatinine_elevated: Literal["no", "yes"] = Field(
        ...,
        description="Whether serum creatinine is ≥2 mg/dL (177 µmol/L). 'No' (<2 mg/dL) scores 0 points, "
                    "'Yes' (≥2 mg/dL) scores 1 point. Elevated creatinine may indicate renal dysfunction "
                    "or severe dehydration from pancreatitis.",
        example="no"
    )
    
    hematocrit_elevated: Literal["no", "yes"] = Field(
        ...,
        description="Whether hematocrit is elevated based on sex-specific thresholds. 'No' scores 0 points, "
                    "'Yes' scores 1 point. Thresholds: Male ≥43%, Female ≥39.6%. Elevated hematocrit "
                    "suggests hemoconcentration and potential for severe pancreatitis.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "peritonitis": "absent",
                "creatinine_elevated": "no",
                "hematocrit_elevated": "no"
            }
        }


class HapsResponse(BaseModel):
    """
    Response model for Harmless Acute Pancreatitis Score (HAPS)
    
    The HAPS score ranges from 0-3 points:
    - 0 points: Harmless acute pancreatitis - 97% specificity and 98% PPV for non-severe course
    - 1-3 points: Cannot rule out severe pancreatitis - standard management required
    
    The score helps identify low-risk patients who may not require ICU admission within 
    30-60 minutes of presentation, potentially allowing for management on general wards 
    or early discharge with outpatient follow-up.
    
    Reference: Lankisch PG, et al. Clin Gastroenterol Hepatol. 2009;7(6):702-5.
    """
    
    result: int = Field(
        ...,
        description="HAPS score calculated from clinical parameters (range: 0-3 points)",
        example=0,
        ge=0,
        le=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the HAPS score with management recommendations",
        example="Patient has a harmless acute pancreatitis. Absence of pancreatic necrosis, "
                "need for dialysis, artificial ventilation, or fatal outcome with 97% specificity "
                "and 98% positive predictive value. Patient may not require ICU admission and could "
                "potentially be managed on a general ward or even at home after short observation."
    )
    
    stage: str = Field(
        ...,
        description="Risk category based on HAPS score (Harmless or Not Harmless)",
        example="Harmless"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Low risk for severe pancreatitis"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 0,
                "unit": "points",
                "interpretation": "Patient has a harmless acute pancreatitis. Absence of pancreatic necrosis, "
                                  "need for dialysis, artificial ventilation, or fatal outcome with 97% specificity "
                                  "and 98% positive predictive value. Patient may not require ICU admission and could "
                                  "potentially be managed on a general ward or even at home after short observation.",
                "stage": "Harmless",
                "stage_description": "Low risk for severe pancreatitis"
            }
        }