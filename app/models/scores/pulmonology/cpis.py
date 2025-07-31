"""
Clinical Pulmonary Infection Score (CPIS) Models

Request and response models for CPIS calculation.

References (Vancouver style):
1. Pugin J, Auckenthaler R, Mili N, Janssens JP, Lew PD, Suter PM. Diagnosis of 
   ventilator-associated pneumonia by bacteriologic analysis of bronchoscopic and 
   nonbronchoscopic 'blind' bronchoalveolar lavage fluid. Am Rev Respir Dis. 
   1991 May;143(5 Pt 1):1121-9. doi: 10.1164/ajrccm/143.5_Pt_1.1121.
2. Singh N, Rogers P, Atwood CW, Wagener MM, Yu VL. Short-course empiric antibiotic 
   therapy for patients with pulmonary infiltrates in the intensive care unit. A 
   proposed solution for indiscriminate antibiotic prescription. Am J Respir Crit 
   Care Med. 2000 Aug;162(2 Pt 1):505-11. doi: 10.1164/ajrccm.162.2.9909095.
3. Schurink CA, Van Nieuwenhoven CA, Jacobs JA, Rozenberg-Arska M, Joore HC, 
   Buskens E, et al. Clinical pulmonary infection score for ventilator-associated 
   pneumonia: accuracy and inter-observer variability. Intensive Care Med. 2004 
   Feb;30(2):217-24. doi: 10.1007/s00134-003-2018-2.

The CPIS assists in diagnosing ventilator-associated pneumonia (VAP) by evaluating 
six clinical parameters to stratify risk and guide antibiotic management decisions.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class CpisRequest(BaseModel):
    """
    Request model for Clinical Pulmonary Infection Score (CPIS)
    
    The CPIS evaluates six clinical parameters in mechanically ventilated patients:
    
    1. Temperature (0-2 points)
    2. White blood cell count (0-2 points)
    3. Tracheal secretions (0-2 points)
    4. Oxygenation PaO2/FiO2 ratio (0-2 points)
    5. Chest radiograph (0-2 points)
    6. Tracheal aspirate culture (0-2 points)
    
    Total score ranges from 0-12 points, with scores ≥7 suggesting higher 
    likelihood of VAP.
    
    Note: CPIS has limited sensitivity and specificity with substantial 
    inter-observer variability. Should be used in conjunction with clinical judgment.
    
    References (Vancouver style):
    1. Pugin J, Auckenthaler R, Mili N, Janssens JP, Lew PD, Suter PM. Diagnosis of 
       ventilator-associated pneumonia by bacteriologic analysis of bronchoscopic and 
       nonbronchoscopic 'blind' bronchoalveolar lavage fluid. Am Rev Respir Dis. 
       1991 May;143(5 Pt 1):1121-9.
    """
    
    temperature: Literal["36.5-38.4", "38.5-38.9", "≥39.0 or ≤36.0"] = Field(
        ...,
        description="Core body temperature in degrees Celsius. Normal range (36.5-38.4°C) scores 0 points, mild elevation (38.5-38.9°C) scores 1 point, high fever or hypothermia (≥39.0°C or ≤36.0°C) scores 2 points",
        example="36.5-38.4"
    )
    
    white_blood_cells: Literal["4-11", "<4 or >11", "<4 or >11 plus band forms ≥500"] = Field(
        ...,
        description="White blood cell count (×10³/μL). Normal (4-11) scores 0 points, abnormal (<4 or >11) scores 1 point, abnormal with significant band forms (≥500) scores 2 points",
        example="4-11"
    )
    
    tracheal_secretions: Literal["<14+", "≥14+", "≥14+ plus purulent"] = Field(
        ...,
        description="Volume and character of tracheal secretions where + indicates suction frequency. Minimal secretions (<14+ per day) scores 0 points, moderate (≥14+) scores 1 point, abundant and purulent scores 2 points",
        example="<14+"
    )
    
    oxygenation: Literal[">240 or ARDS", "≤240 and no ARDS"] = Field(
        ...,
        description="PaO₂/FiO₂ ratio in mm Hg. Good oxygenation (>240) or presence of ARDS scores 0 points, impaired oxygenation (≤240) without ARDS scores 2 points",
        example=">240 or ARDS"
    )
    
    chest_radiograph: Literal["No infiltrate", "Diffuse or patchy infiltrate", "Localized infiltrate"] = Field(
        ...,
        description="Chest radiograph findings. No infiltrate scores 0 points, diffuse/patchy infiltrate scores 1 point, localized infiltrate scores 2 points",
        example="No infiltrate"
    )
    
    tracheal_aspirate_culture: Literal["Pathogenic bacteria ≤1+ or no growth", "Pathogenic bacteria >1+", "Pathogenic bacteria >1+ plus same on gram stain >1+"] = Field(
        ...,
        description="Tracheal aspirate culture and gram stain results. Minimal/no growth scores 0 points, moderate growth (>1+) scores 1 point, significant growth with gram stain correlation scores 2 points",
        example="Pathogenic bacteria ≤1+ or no growth"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "temperature": "38.5-38.9",
                "white_blood_cells": "<4 or >11",
                "tracheal_secretions": "≥14+",
                "oxygenation": "≤240 and no ARDS",
                "chest_radiograph": "Localized infiltrate",
                "tracheal_aspirate_culture": "Pathogenic bacteria >1+"
            }
        }


class CpisResponse(BaseModel):
    """
    Response model for Clinical Pulmonary Infection Score (CPIS)
    
    The CPIS score ranges from 0-12 points and stratifies VAP risk:
    - Score ≤6: Low likelihood of VAP
    - Score ≥7: High likelihood of VAP
    
    The score guides decisions regarding:
    - Empirical antibiotic therapy
    - Need for pulmonary cultures (BAL or PSB)
    - Continuation vs discontinuation of antibiotics
    
    Reference: Singh N, et al. Am J Respir Crit Care Med. 2000;162(2 Pt 1):505-11.
    """
    
    result: int = Field(
        ...,
        description="CPIS score (0-12 points)",
        example=7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations",
        example="Score ≥7 may indicate higher likelihood of ventilator-associated pneumonia. Consider obtaining pulmonary cultures (quantitative BAL or PSB) and continuing empirical antimicrobial therapy pending culture results."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low likelihood or High likelihood)",
        example="High likelihood"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of VAP likelihood",
        example="High likelihood of VAP"
    )
    
    component_scores: Dict[str, int] = Field(
        ...,
        description="Individual component scores for each parameter",
        example={
            "temperature": 1,
            "white_blood_cells": 1,
            "tracheal_secretions": 1,
            "oxygenation": 2,
            "chest_radiograph": 2,
            "tracheal_aspirate_culture": 1
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 8,
                "unit": "points",
                "interpretation": "Score ≥7 may indicate higher likelihood of ventilator-associated pneumonia. Consider obtaining pulmonary cultures (quantitative BAL or PSB) and continuing empirical antimicrobial therapy pending culture results.",
                "stage": "High likelihood",
                "stage_description": "High likelihood of VAP",
                "component_scores": {
                    "temperature": 1,
                    "white_blood_cells": 1,
                    "tracheal_secretions": 1,
                    "oxygenation": 2,
                    "chest_radiograph": 2,
                    "tracheal_aspirate_culture": 1
                }
            }
        }