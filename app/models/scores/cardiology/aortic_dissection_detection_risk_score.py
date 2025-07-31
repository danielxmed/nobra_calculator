"""
Aortic Dissection Detection Risk Score (ADD-RS) Models

Request and response models for ADD-RS calculation.

References (Vancouver style):
1. Rogers AM, Hermann LK, Booher AM, Nienaber CA, Williams DM, Kazerooni EA, et al. 
   Sensitivity of the aortic dissection detection risk score, a novel guideline-based tool 
   for identification of acute aortic dissection at initial presentation: results from the 
   International Registry of Acute Aortic Dissection. Circulation. 2011;123(20):2213-2218. 
   doi: 10.1161/CIRCULATIONAHA.110.988568

2. Hiratzka LF, Bakris GL, Beckman JA, Bersin RM, Carr VF, Casey DE, et al. 2010 
   ACCF/AHA/AATS/ACR/ASA/SCA/SCAI/SIR/STS/SVM guidelines for the diagnosis and management 
   of patients with thoracic aortic disease: a report of the American College of Cardiology 
   Foundation/American Heart Association Task Force on Practice Guidelines. Circulation. 
   2010;121(13):e266-e369. doi: 10.1161/CIR.0b013e3181d4739e

The ADD-RS is a clinical screening tool that stratifies patients with suspected acute aortic 
dissection into low, intermediate, and high-risk categories based on the presence of high-risk 
features in three categories: predisposing conditions, pain features, and examination findings. 
The score ranges from 0-3 points and was validated on 2538 patients with confirmed acute aortic 
dissection from the International Registry of Acute Aortic Dissection (IRAD), showing 95.7% 
sensitivity for detecting acute aortic dissection when any high-risk feature is present.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AorticDissectionDetectionRiskScoreRequest(BaseModel):
    """
    Request model for Aortic Dissection Detection Risk Score (ADD-RS)
    
    The ADD-RS evaluates three categories of high-risk features for aortic dissection:
    
    1. High-Risk Predisposing Conditions:
       - Marfan syndrome
       - Family history of aortic disease
       - Known aortic valve disease
       - Recent aortic manipulation (surgery, catheterization)
       - Known thoracic aortic aneurysm
    
    2. High-Risk Pain Features:
       - Abrupt onset of pain (sudden, instantaneous)
       - Severe pain intensity (worst pain ever experienced)
       - Ripping or tearing pain quality (described as "tearing" or "ripping")
    
    3. High-Risk Examination Features:
       - Pulse deficit or systolic blood pressure differential >20 mmHg between extremities
       - Focal neurological deficit occurring in conjunction with pain
       - New murmur of aortic insufficiency occurring in conjunction with pain
       - Hypotension or shock state
    
    Each category contributes 1 point if ANY high-risk feature within that category is present.
    Total score ranges from 0-3 points.
    
    Risk Stratification:
    - Score 0: Low risk (4.3% of confirmed dissections in IRAD had score 0)
    - Score 1: Intermediate risk (36.5% of confirmed dissections)
    - Score 2-3: High risk (59.2% of confirmed dissections)
    
    References (Vancouver style):
    1. Rogers AM, Hermann LK, Booher AM, Nienaber CA, Williams DM, Kazerooni EA, et al. 
    Sensitivity of the aortic dissection detection risk score, a novel guideline-based tool 
    for identification of acute aortic dissection at initial presentation: results from the 
    International Registry of Acute Aortic Dissection. Circulation. 2011;123(20):2213-2218. 
    doi: 10.1161/CIRCULATIONAHA.110.988568
    """
    
    predisposing_conditions: Literal["none", "present"] = Field(
        ...,
        description="Presence of any high-risk predisposing condition: Marfan syndrome, family history of aortic disease, known aortic valve disease, recent aortic manipulation, or known thoracic aortic aneurysm",
        example="none"
    )
    
    pain_features: Literal["none", "present"] = Field(
        ...,
        description="Presence of any high-risk pain feature: abrupt onset, severe intensity, or ripping/tearing quality",
        example="present"
    )
    
    examination_features: Literal["none", "present"] = Field(
        ...,
        description="Presence of any high-risk examination finding: pulse deficit/BP differential, focal neurological deficit with pain, new aortic insufficiency murmur with pain, or hypotension/shock",
        example="none"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "predisposing_conditions": "none",
                "pain_features": "present", 
                "examination_features": "none"
            }
        }


class AorticDissectionDetectionRiskScoreResponse(BaseModel):
    """
    Response model for Aortic Dissection Detection Risk Score (ADD-RS)
    
    The ADD-RS provides risk stratification for acute aortic dissection:
    
    - Score 0 (Low Risk): Consider chest X-ray; if widened mediastinum or no alternative 
      diagnosis, consider aortic imaging
    - Score 1 (Intermediate Risk): Consider D-dimer testing or proceed to aortic imaging 
      based on clinical judgment
    - Score 2-3 (High Risk): Proceed immediately to definitive aortic imaging
    
    The score showed 95.7% sensitivity for detecting acute aortic dissection in the IRAD 
    validation study of 2538 confirmed cases.
    
    Reference: Rogers AM, et al. Circulation. 2011;123(20):2213-2218.
    """
    
    result: int = Field(
        ...,
        description="ADD-RS score based on number of high-risk categories present (range: 0-3 points)",
        example=1
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on risk stratification",
        example="Intermediate risk for aortic dissection. Consider D-dimer testing or proceed to aortic imaging based on clinical judgment. If D-dimer available and negative (<500 ng/mL), may help rule out dissection in appropriate clinical context."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="One high-risk category present"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Intermediate risk for aortic dissection. Consider D-dimer testing or proceed to aortic imaging based on clinical judgment. If D-dimer available and negative (<500 ng/mL), may help rule out dissection in appropriate clinical context.",
                "stage": "Intermediate Risk",
                "stage_description": "One high-risk category present"
            }
        }