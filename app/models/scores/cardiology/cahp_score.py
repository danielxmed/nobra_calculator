"""
CAHP (Cardiac Arrest Hospital Prognosis) Score Models

Request and response models for CAHP Score calculation.

References (Vancouver style):
1. Maupain C, Bougouin W, Lamhaut L, Deye N, Diehl JL, Geri G, et al. The CAHP 
   (Cardiac Arrest Hospital Prognosis) score: a tool for risk stratification 
   after out-of-hospital cardiac arrest. Eur Heart J. 2016 Nov 1;37(42):3222-3228. 
   doi: 10.1093/eurheartj/ehv556.
2. Bougouin W, Dumas F, Karam N, Maupain C, Marijon E, Lamhaut L, et al. Should 
   We Perform an Immediate Coronary Angiography in All Patients After Cardiac 
   Arrest?: Insights From a Large French Registry. JACC Cardiovasc Interv. 2018 
   Feb 12;11(3):249-256. doi: 10.1016/j.jcin.2017.09.011.
3. Maupain C, Bougouin W, Lamhaut L, Deye N, Diehl JL, Geri G, et al. The CAHP 
   (cardiac arrest hospital prognosis) score: A tool for risk stratification 
   after out-of-hospital cardiac arrest in elderly patients. Resuscitation. 
   2020 Mar;148:200-206. doi: 10.1016/j.resuscitation.2020.01.011.

The CAHP score is a prognostic tool designed to predict neurological outcome 
after out-of-hospital cardiac arrest (OHCA). It helps guide clinical decisions 
including the utility of cardiac catheterization and aggressive treatment in 
the post-arrest period.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CahpScoreRequest(BaseModel):
    """
    Request model for CAHP (Cardiac Arrest Hospital Prognosis) Score
    
    The CAHP score incorporates seven variables independently associated with 
    poor neurological outcome (defined as Cerebral Performance Category 3-5):
    
    Age: Older age is associated with worse outcomes. Each year above 10 years 
    contributes points to the score (1.1 points per year).
    
    Setting: Location where cardiac arrest occurred
    - Public setting: Better prognosis (0 points) - includes witnessed arrests 
      with rapid response
    - Home: Worse prognosis (24 points) - often unwitnessed with delayed response
    
    Initial Rhythm: First recorded cardiac rhythm
    - Shockable (VF/VT): Better prognosis (0 points) - indicates cardiac etiology
    - Non-shockable (PEA/Asystole): Worse prognosis (27 points)
    
    Collapse to CPR: Time from witnessed collapse to initiation of CPR
    - Each minute delay adds 2.8 points
    - Reflects importance of early CPR initiation
    
    CPR to ROSC: Duration of resuscitation efforts
    - Each minute adds 0.8 points
    - Longer resuscitation associated with worse outcomes
    
    Admission pH: Arterial pH on hospital admission
    - Lower pH indicates more severe metabolic acidosis
    - Calculated as: 585 - (77 × pH)
    
    Epinephrine Dose: Total epinephrine during resuscitation
    - Higher doses indicate more refractory arrest
    - 0 mg: 0 points, 1-2 mg: 27 points, ≥3 mg: 43 points
    
    Important Notes:
    - Validated for medical/cardiac arrests only
    - Not applicable to traumatic arrests, drowning, hanging, or overdose
    - High scores do not mandate withdrawal of care
    - Guides but does not replace clinical judgment
    
    References (Vancouver style):
    1. Maupain C, et al. Eur Heart J. 2016;37(42):3222-3228.
    2. Bougouin W, et al. JACC Cardiovasc Interv. 2018;11(3):249-256.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=120,
        description="Patient age in years. Each year above 10 contributes 1.1 points to the score.",
        example=65
    )
    
    setting: Literal["public", "home"] = Field(
        ...,
        description="Setting where cardiac arrest occurred. Public settings (0 points) have better outcomes than home arrests (24 points).",
        example="home"
    )
    
    initial_rhythm: Literal["shockable", "non_shockable"] = Field(
        ...,
        description="Initial cardiac rhythm. Shockable rhythms (VF/VT, 0 points) have better prognosis than non-shockable (PEA/Asystole, 27 points).",
        example="non_shockable"
    )
    
    collapse_to_cpr: float = Field(
        ...,
        ge=0,
        le=60,
        description="Duration from collapse to CPR initiation in minutes. Each minute adds 2.8 points. Early CPR is critical for survival.",
        example=5.0
    )
    
    cpr_to_rosc: float = Field(
        ...,
        ge=0,
        le=120,
        description="Duration from CPR start to return of spontaneous circulation (ROSC) in minutes. Each minute adds 0.8 points.",
        example=20.0
    )
    
    admission_ph: float = Field(
        ...,
        ge=6.5,
        le=7.8,
        description="Arterial pH on admission. Lower pH indicates more severe acidosis and worse prognosis. Normal: 7.35-7.45.",
        example=7.15
    )
    
    epinephrine_dose: Literal["0mg", "1-2mg", ">=3mg"] = Field(
        ...,
        description="Total epinephrine dose during resuscitation. Higher doses (≥3mg: 43 points) indicate more refractory arrest.",
        example="1-2mg"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "setting": "home",
                "initial_rhythm": "non_shockable",
                "collapse_to_cpr": 5.0,
                "cpr_to_rosc": 20.0,
                "admission_ph": 7.15,
                "epinephrine_dose": "1-2mg"
            }
        }


class CahpScoreResponse(BaseModel):
    """
    Response model for CAHP (Cardiac Arrest Hospital Prognosis) Score
    
    The CAHP score ranges from 0 to approximately 350 points and stratifies 
    patients into three risk categories:
    
    Low Risk (<150 points):
    - 39% risk of poor neurological outcome (CPC 3-5)
    - Consider aggressive treatment including cardiac catheterization
    - Good candidates for all interventions
    
    Moderate Risk (150-200 points):
    - 81% risk of poor neurological outcome
    - Individualized decisions based on clinical context
    - Consider patient/family wishes and pre-arrest function
    
    High Risk (>200 points):
    - 100% risk of poor neurological outcome in validation cohort
    - Consider goals of care discussion
    - High scores alone do not warrant withdrawal of care
    
    CPC Categories:
    - CPC 1: Good cerebral performance (normal life)
    - CPC 2: Moderate cerebral disability (disabled but independent)
    - CPC 3: Severe cerebral disability (dependent)
    - CPC 4: Coma or vegetative state
    - CPC 5: Brain death
    
    Clinical Applications:
    - Early risk stratification in ICU
    - Guide cardiac catheterization decisions
    - Inform family discussions
    - Resource allocation in pandemic situations
    
    Reference: Maupain C, et al. Eur Heart J. 2016;37(42):3222-3228.
    """
    
    result: int = Field(
        ...,
        description="CAHP score calculated from clinical variables (range: 0-350 points)",
        example=175
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the score",
        example="81% risk of poor neurological outcome (CPC 3-5) at hospital discharge. Individualized treatment decisions should be made based on clinical context."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk of poor neurological outcome"
    )
    
    details: Dict[str, Any] = Field(
        ...,
        description="Breakdown of score components for transparency",
        example={
            "age_points": 60.5,
            "setting_points": 24,
            "rhythm_points": 27,
            "collapse_cpr_points": 14.0,
            "cpr_rosc_points": 16.0,
            "ph_points": 30.5,
            "epinephrine_points": 27
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 175,
                "unit": "points",
                "interpretation": "81% risk of poor neurological outcome (CPC 3-5) at hospital discharge. Individualized treatment decisions should be made based on clinical context.",
                "stage": "Moderate Risk",
                "stage_description": "Moderate risk of poor neurological outcome",
                "details": {
                    "age_points": 60.5,
                    "setting_points": 24,
                    "rhythm_points": 27,
                    "collapse_cpr_points": 14.0,
                    "cpr_rosc_points": 16.0,
                    "ph_points": 30.5,
                    "epinephrine_points": 27
                }
            }
        }