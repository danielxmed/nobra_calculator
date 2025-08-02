"""
ISTH Criteria for Disseminated Intravascular Coagulation (DIC) Models

Request and response models for ISTH DIC criteria calculation.

References (Vancouver style):
1. Taylor FB Jr, Toh CH, Hoots WK, Wada H, Levi M; Scientific Subcommittee on 
   Disseminated Intravascular Coagulation (DIC) of the International Society on 
   Thrombosis and Haemostasis (ISTH). Towards definition, clinical and laboratory 
   criteria, and a scoring system for disseminated intravascular coagulation. 
   Thromb Haemost. 2001 Nov;86(5):1327-30.
2. Toh CH, Hoots WK; SSC on Disseminated Intravascular Coagulation of the ISTH. 
   The scoring system of the Scientific and Standardisation Committee on 
   Disseminated Intravascular Coagulation of the International Society on 
   Thrombosis and Haemostasis: a 5-year overview. J Thromb Haemost. 2007 Mar;5(3):604-6.
3. Bakhtiari K, Meijers JC, de Jonge E, Levi M. Prospective validation of the 
   International Society of Thrombosis and Haemostasis scoring system for 
   disseminated intravascular coagulation. Crit Care Med. 2004 Dec;32(12):2416-21.
4. Levi M, Toh CH, Thachil J, Watson HG. Guidelines for the diagnosis and management 
   of disseminated intravascular coagulation. British Committee for Standards in 
   Haematology. Br J Haematol. 2009 Apr;145(1):24-33.

The ISTH DIC scoring system diagnoses overt disseminated intravascular coagulation 
using readily available laboratory parameters. Developed by the International Society 
on Thrombosis and Haemostasis as a standardized diagnostic approach with 91-93% 
sensitivity and 97-98% specificity. Use only in patients with clinical suspicion 
for DIC in appropriate settings (sepsis, malignancy, obstetric complications, trauma).
"""

from pydantic import BaseModel, Field
from typing import Literal


class IsthDicCriteriaRequest(BaseModel):
    """
    Request model for ISTH DIC Criteria
    
    The ISTH DIC scoring system uses four laboratory parameters to diagnose overt DIC:
    
    Laboratory Parameters:
    
    1. Platelet Count (×10^9/L):
       - ≥100: 0 points (normal or mild decrease)
       - 50-99: 1 point (moderate thrombocytopenia)
       - <50: 2 points (severe thrombocytopenia)
    
    2. Fibrin-Related Marker Elevation:
       - D-dimer is most commonly used, but fibrin monomers or FDP are acceptable
       - no_increase: 0 points (normal levels)
       - moderate_increase: 2 points (elevated but not severely)
       - severe_increase: 3 points (markedly elevated levels)
    
    3. Prothrombin Time (PT) Prolongation:
       - <3_seconds: 0 points (normal or minimally prolonged)
       - 3-5_seconds: 1 point (moderate prolongation)
       - ≥6_seconds: 2 points (severe prolongation beyond normal range)
    
    4. Fibrinogen Level (g/L):
       - ≥1_g_L: 0 points (normal fibrinogen levels)
       - <1_g_L: 1 point (hypofibrinogenemia)
    
    Clinical Context Requirements:
    - Must have underlying disorder associated with DIC (sepsis, malignancy, trauma, obstetric complications)
    - Clinical suspicion of DIC based on bleeding, thrombosis, or organ dysfunction
    - Not recommended for screening asymptomatic patients
    
    Interpretation Guidelines:
    - Score ≥5: Compatible with overt DIC (high likelihood, proceed with treatment)
    - Score <5: Not suggestive of overt DIC (may indicate non-overt DIC or absence)
    - Serial measurements often more informative than single assessment
    - Consider clinical context when interpreting borderline scores
    
    References (Vancouver style):
    1. Taylor FB Jr, Toh CH, Hoots WK, Wada H, Levi M; Scientific Subcommittee on 
    Disseminated Intravascular Coagulation (DIC) of the International Society on 
    Thrombosis and Haemostasis (ISTH). Towards definition, clinical and laboratory 
    criteria, and a scoring system for disseminated intravascular coagulation. 
    Thromb Haemost. 2001 Nov;86(5):1327-30.
    2. Bakhtiari K, Meijers JC, de Jonge E, Levi M. Prospective validation of the 
    International Society of Thrombosis and Haemostasis scoring system for 
    disseminated intravascular coagulation. Crit Care Med. 2004 Dec;32(12):2416-21.
    """
    
    platelet_count: Literal["≥100", "50-99", "<50"] = Field(
        ...,
        description="Platelet count category in ×10^9/L. ≥100 scores 0 points, 50-99 scores 1 point, <50 scores 2 points. Thrombocytopenia in DIC results from platelet consumption and microangiopathic destruction",
        example="50-99"
    )
    
    fibrin_marker: Literal["no_increase", "moderate_increase", "severe_increase"] = Field(
        ...,
        description="Fibrin-related marker elevation (D-dimer most common, fibrin monomers or FDP acceptable). No increase scores 0 points, moderate increase scores 2 points, severe increase scores 3 points. Reflects fibrin formation and breakdown in DIC",
        example="severe_increase"
    )
    
    pt_prolongation: Literal["<3_seconds", "3-5_seconds", "≥6_seconds"] = Field(
        ...,
        description="Prothrombin time prolongation beyond normal range in seconds. <3 seconds scores 0 points, 3-5 seconds scores 1 point, ≥6 seconds scores 2 points. Reflects consumption of coagulation factors",
        example="3-5_seconds"
    )
    
    fibrinogen_level: Literal["≥1_g_L", "<1_g_L"] = Field(
        ...,
        description="Fibrinogen level in grams per liter. ≥1 g/L scores 0 points, <1 g/L scores 1 point. Hypofibrinogenemia results from consumption and impaired synthesis in severe DIC",
        example="≥1_g_L"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "platelet_count": "50-99",
                "fibrin_marker": "severe_increase",
                "pt_prolongation": "3-5_seconds",
                "fibrinogen_level": "≥1_g_L"
            }
        }


class IsthDicCriteriaResponse(BaseModel):
    """
    Response model for ISTH DIC Criteria
    
    The ISTH DIC score ranges from 0-8 points and classifies patients as:
    
    Score Interpretation:
    - ≥5 points: Compatible with overt DIC (91-93% sensitivity, 97-98% specificity)
    - <5 points: Not suggestive of overt DIC (may indicate non-overt DIC)
    
    Clinical Management by Score:
    
    Compatible with Overt DIC (≥5 points):
    - High likelihood of overt disseminated intravascular coagulation
    - Consider immediate treatment of underlying condition
    - Supportive care: platelet and plasma transfusions as needed
    - Monitor closely with serial laboratory studies
    - Address precipitating factors (sepsis, trauma, malignancy)
    
    Not Suggestive of Overt DIC (<5 points):
    - Does not rule out DIC completely
    - May indicate non-overt or subclinical DIC
    - Consider serial measurements if clinical suspicion persists
    - Monitor for progression especially if underlying condition worsens
    - Reassess with clinical changes or deterioration
    
    Follow-up Recommendations:
    - Repeat scoring with clinical or laboratory changes
    - Monitor trend rather than single time point
    - Consider alternative diagnoses if score remains low
    - Assess response to treatment of underlying condition
    
    Reference: Taylor FB Jr, et al. Thromb Haemost. 2001;86(5):1327-30.
    """
    
    result: int = Field(
        ...,
        description="ISTH DIC score calculated from laboratory parameters (range: 0-8 points)",
        example=6
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the DIC score and likelihood of overt DIC",
        example="Score ≥5 points (6 points): Compatible with overt DIC. Strong likelihood of overt disseminated intravascular coagulation based on ISTH criteria. This finding has 91-93% sensitivity and 97-98% specificity for overt DIC. Consider immediate treatment and management of underlying condition. Monitor closely with serial laboratory studies and address precipitating factors such as sepsis, malignancy, obstetric complications, or trauma."
    )
    
    stage: str = Field(
        ...,
        description="DIC likelihood category (Compatible with Overt DIC, Not Suggestive)",
        example="Compatible with Overt DIC"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the DIC likelihood category",
        example="Compatible with overt DIC"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 6,
                "unit": "points",
                "interpretation": "Score ≥5 points (6 points): Compatible with overt DIC. Strong likelihood of overt disseminated intravascular coagulation based on ISTH criteria. This finding has 91-93% sensitivity and 97-98% specificity for overt DIC. Consider immediate treatment and management of underlying condition. Monitor closely with serial laboratory studies and address precipitating factors such as sepsis, malignancy, obstetric complications, or trauma.",
                "stage": "Compatible with Overt DIC",
                "stage_description": "Compatible with overt DIC"
            }
        }