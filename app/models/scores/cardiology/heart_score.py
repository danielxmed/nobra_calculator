"""
HEART Score for Major Cardiac Events Models

Request and response models for HEART Score calculation.

References (Vancouver style):
1. Six AJ, Backus BE, Kelder JC. Chest pain in the emergency room: value of the 
   HEART score. Neth Heart J. 2008 Jun;16(6):191-6. doi: 10.1007/BF03086144.
2. Backus BE, Six AJ, Kelder JC, Bosschaert MA, Mast EG, Mosterd A, et al. A 
   prospective validation of the HEART score for chest pain patients at the 
   emergency department. Int J Cardiol. 2013 Oct 3;168(3):2153-8. doi: 
   10.1016/j.ijcard.2013.01.255.
3. Poldervaart JM, Reitsma JB, Backus BE, Koffijberg H, Veldkamp RF, Ten Haaf ME, 
   et al. Effect of Using the HEART Score in Patients With Chest Pain in the 
   Emergency Department: A Stepped-Wedge, Cluster Randomized Trial. Ann Intern Med. 
   2017 May 16;166(10):689-697. doi: 10.7326/M16-1600.

The HEART Score is a clinical decision tool that helps predict the 6-week risk of 
major adverse cardiac events (MACE) including all-cause mortality, myocardial 
infarction, or coronary revascularization in patients presenting to the emergency 
department with chest pain. It outperforms TIMI and GRACE scores with a c-statistic 
of 0.83.
"""

from pydantic import BaseModel, Field


class HeartScoreRequest(BaseModel):
    """
    Request model for HEART Score for Major Cardiac Events
    
    The HEART Score evaluates 5 components (History, EKG, Age, Risk factors, Troponin)
    to stratify chest pain patients in the emergency department.
    
    Risk factors for scoring include:
    - Hypertension
    - Hypercholesterolemia
    - Diabetes mellitus
    - Obesity (BMI >30 kg/m²)
    - Smoking (current or cessation ≤3 months)
    - Positive family history (CVD before age 65)
    - Atherosclerotic disease (prior MI, PCI/CABG, CVA/TIA, or PAD)
    
    Clinical outcomes by risk category:
    - Low risk (0-3 points): 0.9-1.7% 6-week MACE rate
    - Moderate risk (4-6 points): 12-16.6% 6-week MACE rate
    - High risk (7-10 points): 50-65% 6-week MACE rate
    
    References (Vancouver style):
    1. Six AJ, Backus BE, Kelder JC. Chest pain in the emergency room: value of the 
       HEART score. Neth Heart J. 2008 Jun;16(6):191-6. doi: 10.1007/BF03086144.
    2. Backus BE, Six AJ, Kelder JC, Bosschaert MA, Mast EG, Mosterd A, et al. A 
       prospective validation of the HEART score for chest pain patients at the 
       emergency department. Int J Cardiol. 2013 Oct 3;168(3):2153-8. doi: 
       10.1016/j.ijcard.2013.01.255.
    """
    
    history: int = Field(
        ...,
        ge=0,
        le=2,
        description="Clinical history assessment. 0 = Slightly suspicious (nonspecific or "
                    "inconsistent with ACS), 1 = Moderately suspicious (mixed features), "
                    "2 = Highly suspicious (classic presentation for ACS)",
        example=1
    )
    
    ekg: int = Field(
        ...,
        ge=0,
        le=2,
        description="EKG findings. 0 = Normal (completely normal), "
                    "1 = Non-specific repolarization disturbance (LBBB, LVH, digoxin effect, "
                    "unchanged known repolarization disorders), "
                    "2 = Significant ST deviation (new or not known to be old, "
                    "not explained by LBBB/LVH/digoxin)",
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
                    "2 = ≥3 risk factors OR history of atherosclerotic disease. "
                    "Risk factors: HTN, hypercholesterolemia, DM, obesity (BMI >30), "
                    "smoking (current or quit ≤3 months), family history (CVD <65 years), "
                    "prior atherosclerotic disease",
        example=1
    )
    
    troponin: int = Field(
        ...,
        ge=0,
        le=2,
        description="Initial troponin level. 0 = ≤normal limit (within normal range), "
                    "1 = 1-3× normal limit (borderline elevation), "
                    "2 = >3× normal limit (significantly elevated)",
        example=0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "history": 1,
                "ekg": 0,
                "age": 1,
                "risk_factors": 1,
                "troponin": 0
            }
        }


class HeartScoreResponse(BaseModel):
    """
    Response model for HEART Score for Major Cardiac Events
    
    The HEART Score provides risk stratification for 6-week major adverse 
    cardiac events (MACE) including all-cause mortality, MI, or coronary 
    revascularization.
    
    Superior performance compared to other risk scores:
    - HEART Score c-statistic: 0.83
    - TIMI Score c-statistic: 0.75
    - GRACE Score c-statistic: 0.70
    
    Reference: Six AJ, et al. Neth Heart J. 2008;16(6):191-6.
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
        description="Clinical interpretation with management recommendations based on risk category",
        example="Low risk for major adverse cardiac events. Safe for discharge from the emergency department with outpatient follow-up. Consider stress testing within 72 hours if clinically indicated."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, or High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of 6-week MACE risk percentage",
        example="0.9-1.7% 6-week MACE risk"
    )
    
    mace_risk: str = Field(
        ...,
        description="6-week major adverse cardiac event risk percentage",
        example="0.9-1.7%"
    )
    
    disposition: str = Field(
        ...,
        description="Recommended disposition based on risk stratification",
        example="Discharge with outpatient follow-up"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 3,
                "unit": "points",
                "interpretation": "Low risk for major adverse cardiac events. Safe for discharge from the emergency department with outpatient follow-up. Consider stress testing within 72 hours if clinically indicated.",
                "stage": "Low Risk",
                "stage_description": "0.9-1.7% 6-week MACE risk",
                "mace_risk": "0.9-1.7%",
                "disposition": "Discharge with outpatient follow-up"
            }
        }