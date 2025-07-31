"""
4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) Models

Request and response models for 4PEPS calculation.

References (Vancouver style):
1. Roy PM, Friou E, Germeau B, Douillet D, Kline JA, Righini M, et al. Derivation and 
   Validation of a 4-Level Clinical Pretest Probability Score for Suspected Pulmonary 
   Embolism to Safely Decrease Imaging Testing. JAMA Cardiol. 2021 Jun 1;6(6):669-677. 
   doi: 10.1001/jamacardio.2021.0064.
2. Stals MAM, Beenen LFM, Coppens M, Faber LM, Hofstee HMA, Hovens MMC, et al. 
   Performance of the 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) 
   in the diagnostic management of pulmonary embolism: An external validation study. 
   Thromb Res. 2023 Nov;231:65-75. doi: 10.1016/j.thromres.2023.09.010.
3. Chiang P, Robert-Ebadi H, Perrier A, Roy PM, Sanchez O, Righini M, et al. 
   Pulmonary embolism risk stratification: external validation of the 4-level Clinical 
   Pretest Probability Score (4PEPS). Res Pract Thromb Haemost. 2024 Feb 15;8(1):102348. 
   doi: 10.1016/j.rpth.2024.102348.

The 4PEPS is a clinical decision tool that uses 13 clinical variables to stratify 
patients with suspected pulmonary embolism into four probability categories, allowing 
for safe reduction of imaging studies in low-risk patients. This score can safely 
rule out PE in 58% of patients without imaging while maintaining a failure rate of 1.3%.
"""

from pydantic import BaseModel, Field
from typing import Literal


class FourPepsRequest(BaseModel):
    """
    Request model for 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)
    
    The 4PEPS uses 13 clinical variables to assess pulmonary embolism probability:
    
    Age Categories:
    - under_50: Age <50 years (-2 points)
    - 50_to_64: Age 50-64 years (-1 point)  
    - 65_or_over: Age ≥65 years (0 points)
    
    Clinical Variables (each yes/no):
    - Chronic respiratory disease (-1 point if yes)
    - Heart rate <80 bpm (-1 point if yes)
    - Chest pain AND acute dyspnea (+1 point if yes)
    - Male gender (+2 points if yes)
    - Hormonal estrogenic treatment (+2 points if yes)
    - Personal history of VTE (+2 points if yes)
    - Syncope (+2 points if yes)
    - Immobility within 4 weeks (+2 points if yes)
    - Pulse oxygen saturation <95% (+3 points if yes)
    - Calf pain/unilateral lower limb edema (+3 points if yes)
    - PE is most likely diagnosis (+5 points if yes)

    References (Vancouver style):
    1. Roy PM, Friou E, Germeau B, Douillet D, Kline JA, Righini M, et al. Derivation and 
    Validation of a 4-Level Clinical Pretest Probability Score for Suspected Pulmonary 
    Embolism to Safely Decrease Imaging Testing. JAMA Cardiol. 2021 Jun 1;6(6):669-677. 
    doi: 10.1001/jamacardio.2021.0064.
    2. Stals MAM, Beenen LFM, Coppens M, Faber LM, Hofstee HMA, Hovens MMC, et al. 
    Performance of the 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS) 
    in the diagnostic management of pulmonary embolism: An external validation study. 
    Thromb Res. 2023 Nov;231:65-75. doi: 10.1016/j.thromres.2023.09.010.
    3. Chiang P, Robert-Ebadi H, Perrier A, Roy PM, Sanchez O, Righini M, et al. 
    Pulmonary embolism risk stratification: external validation of the 4-level Clinical 
    Pretest Probability Score (4PEPS). Res Pract Thromb Haemost. 2024 Feb 15;8(1):102348. 
    doi: 10.1016/j.rpth.2024.102348.
    """
    
    age_category: Literal["under_50", "50_to_64", "65_or_over"] = Field(
        ...,
        description="Patient age category. Under 50 years scores -2 points, 50-64 years scores -1 point, 65 or over scores 0 points",
        example="50_to_64"
    )
    
    chronic_respiratory_disease: Literal["yes", "no"] = Field(
        ...,
        description="Presence of chronic respiratory disease (COPD, asthma, pulmonary fibrosis, etc.). Scores -1 point if yes",
        example="no"
    )
    
    heart_rate_under_80: Literal["yes", "no"] = Field(
        ...,
        description="Heart rate less than 80 beats per minute. Scores -1 point if yes",
        example="no"
    )
    
    chest_pain_dyspnea: Literal["yes", "no"] = Field(
        ...,
        description="Presence of BOTH chest pain AND acute dyspnea (not just one). Scores +1 point if yes",
        example="yes"
    )
    
    male_gender: Literal["yes", "no"] = Field(
        ...,
        description="Patient is male. Scores +2 points if yes",
        example="yes"
    )
    
    hormonal_treatment: Literal["yes", "no"] = Field(
        ...,
        description="Current hormonal estrogenic treatment (oral contraceptives, hormone replacement therapy). Scores +2 points if yes",
        example="no"
    )
    
    personal_history_vte: Literal["yes", "no"] = Field(
        ...,
        description="Personal history of venous thromboembolism (previous DVT or PE). Scores +2 points if yes",
        example="no"
    )
    
    syncope: Literal["yes", "no"] = Field(
        ...,
        description="Recent syncope (fainting episode). Scores +2 points if yes",
        example="no"
    )
    
    immobility_4_weeks: Literal["yes", "no"] = Field(
        ...,
        description="Immobility within the last 4 weeks (bed rest, wheelchair, cast, surgery, etc.). Scores +2 points if yes",
        example="no"
    )
    
    oxygen_saturation_under_95: Literal["yes", "no"] = Field(
        ...,
        description="Pulse oxygen saturation less than 95% on room air. Scores +3 points if yes",
        example="no"
    )
    
    calf_pain_edema: Literal["yes", "no"] = Field(
        ...,
        description="Calf pain and/or unilateral lower limb edema suggesting DVT. Scores +3 points if yes",
        example="no"
    )
    
    pe_most_likely: Literal["yes", "no"] = Field(
        ...,
        description="PE is the most likely diagnosis based on clinician's overall assessment. Scores +5 points if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age_category": "50_to_64",
                "chronic_respiratory_disease": "no",
                "heart_rate_under_80": "no",
                "chest_pain_dyspnea": "yes",
                "male_gender": "yes",
                "hormonal_treatment": "no",
                "personal_history_vte": "no",
                "syncope": "no",
                "immobility_4_weeks": "no",
                "oxygen_saturation_under_95": "no",
                "calf_pain_edema": "no",
                "pe_most_likely": "no"
            }
        }


class FourPepsResponse(BaseModel):
    """
    Response model for 4-Level Pulmonary Embolism Clinical Probability Score (4PEPS)
    
    The 4PEPS score ranges from -5 to +20 points and classifies patients into:
    - Very Low (<0 points): PE ruled out, no testing needed
    - Low (0-5 points): Use D-dimer with 1000 μg/L cut-off
    - Moderate (6-12 points): Use age-adjusted D-dimer cut-off
    - High (>12 points): Proceed directly to imaging
    
    Reference: Roy PM, et al. JAMA Cardiol. 2021;6(6):669-677.
    """
    
    result: int = Field(
        ...,
        description="4PEPS score calculated from clinical variables (range: -5 to +20 points)",
        example=2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended next steps based on the score",
        example="Low probability of PE. Use D-dimer with 1000 μg/L cut-off. If D-dimer <1000 μg/L, PE is ruled out."
    )
    
    stage: str = Field(
        ...,
        description="Clinical probability category (Very Low, Low, Moderate, High)",
        example="Low"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the probability category",
        example="Low clinical probability"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2,
                "unit": "points",
                "interpretation": "Low probability of PE. Use D-dimer with 1000 μg/L cut-off. If D-dimer <1000 μg/L, PE is ruled out.",
                "stage": "Low",
                "stage_description": "Low clinical probability"
            }
        }