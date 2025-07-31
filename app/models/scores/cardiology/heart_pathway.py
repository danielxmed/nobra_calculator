"""
HEART Pathway for Early Discharge in Acute Chest Pain Models

Request and response models for HEART Pathway calculation.

References (Vancouver style):
1. Mahler SA, Riley RF, Hiestand BC, Russell GB, Hoekstra JW, Lefebvre CW, et al. The 
   HEART Pathway randomized trial: identifying emergency department patients with acute 
   chest pain for early discharge. Circ Cardiovasc Qual Outcomes. 2015 Mar;8(2):195-203. 
   doi: 10.1161/CIRCOUTCOMES.114.001384.
2. Mahler SA, Stopyra JP, Apple FS, Riley RF, Russell GB, Hiestand BC, et al. Use of 
   the HEART Pathway with high sensitivity cardiac troponins: a secondary analysis. 
   Clin Biochem. 2017 May;50(7-8):401-407. doi: 10.1016/j.clinbiochem.2016.11.018.
3. Backus BE, Six AJ, Kelder JC, Bosschaert MA, Mast EG, Mosterd A, et al. A prospective 
   validation of the HEART score for chest pain patients at the emergency department. 
   Int J Cardiol. 2013 Oct 3;168(3):2153-8. doi: 10.1016/j.ijcard.2013.01.255.

The HEART Pathway combines the HEART score (History, ECG, Age, Risk factors, Troponin) 
with serial troponin measurements at 0 and 3 hours to identify low-risk chest pain 
patients safe for early discharge. Patients with HEART score ≤3 and negative serial 
troponins have <2% 30-day MACE risk and can be safely discharged.
"""

from pydantic import BaseModel, Field
from typing import Literal, Optional


class HeartPathwayRequest(BaseModel):
    """
    Request model for HEART Pathway for Early Discharge in Acute Chest Pain
    
    The HEART Pathway decision tool combines:
    1. HEART score calculation (0-10 points total)
    2. Serial troponin measurements at 0 and 3 hours
    
    Risk factors for scoring include:
    - Hypertension
    - Hypercholesterolemia  
    - Diabetes mellitus
    - Obesity (BMI >30 kg/m²)
    - Smoking (current or quit <3 months)
    - Positive family history (parent or sibling with CVD <65 years)
    - Atherosclerotic disease (prior MI, PCI/CABG, CVA/TIA, or PAD)
    
    Clinical outcomes:
    - Low risk pathway (HEART ≤3 + negative troponins): 0.9-1.7% 30-day MACE
    - High risk pathway (HEART ≥4 or positive troponin): 12-65% 30-day MACE
    
    References (Vancouver style):
    1. Mahler SA, Riley RF, Hiestand BC, Russell GB, Hoekstra JW, Lefebvre CW, et al. The 
       HEART Pathway randomized trial: identifying emergency department patients with acute 
       chest pain for early discharge. Circ Cardiovasc Qual Outcomes. 2015 Mar;8(2):195-203. 
       doi: 10.1161/CIRCOUTCOMES.114.001384.
    2. Backus BE, Six AJ, Kelder JC, Bosschaert MA, Mast EG, Mosterd A, et al. A prospective 
       validation of the HEART score for chest pain patients at the emergency department. 
       Int J Cardiol. 2013 Oct 3;168(3):2153-8. doi: 10.1016/j.ijcard.2013.01.255.
    """
    
    history: int = Field(
        ...,
        ge=0,
        le=2,
        description="Clinical history assessment. 0 = Slightly suspicious (nonspecific history), "
                    "1 = Moderately suspicious (mixed features), "
                    "2 = Highly suspicious (primarily high-risk features)",
        example=1
    )
    
    ecg: int = Field(
        ...,
        ge=0,
        le=2,
        description="ECG findings. 0 = Normal (completely normal), "
                    "1 = Non-specific repolarization disturbance (no significant ST depression), "
                    "2 = Significant ST depression (≥1mm in ≥2 contiguous leads)",
        example=0
    )
    
    age: int = Field(
        ...,
        ge=0,
        le=2,
        description="Patient age category. 0 = <45 years, "
                    "1 = 45-64 years, "
                    "2 = ≥65 years",
        example=1
    )
    
    risk_factors: int = Field(
        ...,
        ge=0,
        le=2,
        description="Number of cardiovascular risk factors. 0 = No known risk factors, "
                    "1 = 1-2 risk factors, "
                    "2 = ≥3 risk factors OR history of atherosclerotic disease "
                    "(prior MI, PCI/CABG, CVA/TIA, PAD)",
        example=1
    )
    
    initial_troponin: int = Field(
        ...,
        ge=0,
        le=2,
        description="Initial troponin level at presentation. 0 = ≤normal limit (negative), "
                    "1 = 1-3x normal limit (borderline elevation), "
                    "2 = >3x normal limit (significantly elevated)",
        example=0
    )
    
    repeat_troponin_negative: Literal["yes", "no", "not_done"] = Field(
        "not_done",
        description="3-hour repeat troponin result (only relevant for low-risk patients). "
                    "'yes' = Negative at 3 hours, 'no' = Positive at 3 hours, "
                    "'not_done' = Not performed yet or not applicable",
        example="not_done"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "history": 1,
                "ecg": 0,
                "age": 1,
                "risk_factors": 1,
                "initial_troponin": 0,
                "repeat_troponin_negative": "not_done"
            }
        }


class HeartPathwayResponse(BaseModel):
    """
    Response model for HEART Pathway for Early Discharge in Acute Chest Pain
    
    The HEART Pathway provides risk stratification for 30-day major adverse 
    cardiac events (MACE) including MI, PCI, CABG, or death:
    - Low risk pathway: 0.9-1.7% 30-day MACE (safe for discharge)
    - High risk pathway: 12-65% 30-day MACE (requires admission)
    
    Clinical implementation has shown >20% of chest pain patients can be 
    safely discharged with >99% NPV for 30-day MACE.
    
    Reference: Mahler SA, et al. Circ Cardiovasc Qual Outcomes. 2015;8(2):195-203.
    """
    
    result: int = Field(
        ...,
        description="HEART score (0-10 points). Sum of all 5 components",
        example=3
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with pathway recommendations based on score and troponin status",
        example="Low risk HEART score with negative initial troponin. Repeat troponin at 3 hours required to complete HEART Pathway. If 3-hour troponin is also negative, safe for early discharge."
    )
    
    stage: str = Field(
        ...,
        description="Risk classification (Low Risk, Low Risk (Pending), or High Risk)",
        example="Low Risk (Pending)"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of the risk category with MACE percentage",
        example="0.9-1.7% 30-day MACE risk"
    )
    
    risk_category: str = Field(
        ...,
        description="Overall risk category (Low or High)",
        example="Low"
    )
    
    mace_risk: str = Field(
        ...,
        description="30-day major adverse cardiac event risk percentage",
        example="0.9-1.7% 30-day MACE risk"
    )
    
    recommendation: str = Field(
        ...,
        description="Specific clinical recommendation based on pathway results",
        example="Obtain 3-hour troponin to complete pathway"
    )
    
    initial_troponin_elevated: bool = Field(
        ...,
        description="Whether initial troponin was elevated (score 1-2)",
        example=False
    )
    
    pathway_complete: bool = Field(
        ...,
        description="Whether the HEART Pathway assessment is complete or awaiting 3-hour troponin",
        example=False
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Low risk HEART score with negative initial troponin. Repeat troponin at 3 hours required to complete HEART Pathway. If 3-hour troponin is also negative, safe for early discharge.",
                "stage": "Low Risk (Pending)",
                "stage_description": "0.9-1.7% 30-day MACE risk",
                "risk_category": "Low",
                "mace_risk": "0.9-1.7% 30-day MACE risk",
                "recommendation": "Obtain 3-hour troponin to complete pathway",
                "initial_troponin_elevated": False,
                "pathway_complete": False
            }
        }