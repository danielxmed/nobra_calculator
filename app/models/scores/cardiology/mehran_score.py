"""
Mehran Score for Post-PCI Contrast Nephropathy Models

Request and response models for Mehran Score calculation.

References (Vancouver style):
1. Mehran R, Aymong ED, Nikolsky E, Lasic Z, Iakovou I, Fahy M, et al. A simple risk 
   score for prediction of contrast-induced nephropathy after percutaneous coronary 
   intervention: development and initial validation. J Am Coll Cardiol. 2004 Oct 
   6;44(7):1393-9. doi: 10.1016/j.jacc.2004.06.068.
2. Wi J, Ko YG, Kim JS, Kim BK, Choi D, Ha JW, et al. Impact of contrast-induced 
   acute kidney injury with transient or persistent renal dysfunction on long-term 
   outcomes of patients with acute myocardial infarction undergoing percutaneous 
   coronary intervention. Heart. 2011 Nov;97(21):1753-7. doi: 10.1136/hrt.2010.218677.
3. Narula A, Mehran R, Weisz G, Dangas GD, Yu J, Généreux P, et al. Contrast-induced 
   acute kidney injury after primary percutaneous coronary intervention: results from 
   the HORIZONS-AMI substudy. Eur Heart J. 2014 Jun 14;35(23):1533-40. 
   doi: 10.1093/eurheartj/ehu063.

The Mehran Score predicts the risk of contrast-induced nephropathy (CIN) after 
percutaneous coronary intervention (PCI) using 8 clinical variables. CIN is defined 
as an increase ≥0.5 mg/dL (or ≥25%) in serum creatinine at 48 hours post-PCI. The 
score stratifies patients into four risk categories to guide preventive strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal


class MehranScoreRequest(BaseModel):
    """
    Request model for Mehran Score for Post-PCI Contrast Nephropathy
    
    The Mehran Score uses 8 clinical variables to predict the risk of contrast-induced
    nephropathy (CIN) following percutaneous coronary intervention (PCI). The score
    helps identify patients who may benefit from preventive measures.
    
    Risk factors and point values:
    - Hypotension: 5 points
    - Intra-aortic balloon pump: 5 points
    - Congestive heart failure: 5 points
    - Age >75 years: 4 points
    - Anemia: 3 points
    - Diabetes: 3 points
    - Contrast volume: 1 point per 100 mL
    - eGFR <20: 6 points, 20-39: 4 points, 40-59: 2 points
    
    Exclusion criteria:
    - Pre-existing end-stage renal disease on dialysis
    - Contrast exposure within 1 week of the index procedure
    
    References (Vancouver style):
    1. Mehran R, Aymong ED, Nikolsky E, Lasic Z, Iakovou I, Fahy M, et al. A simple risk 
       score for prediction of contrast-induced nephropathy after percutaneous coronary 
       intervention: development and initial validation. J Am Coll Cardiol. 2004 Oct 
       6;44(7):1393-9. doi: 10.1016/j.jacc.2004.06.068.
    """
    
    hypotension: Literal["yes", "no"] = Field(
        ...,
        description="Systolic blood pressure <80 mmHg for ≥1 hour requiring inotropic support "
                    "or intra-aortic balloon pump within 24 hours of catheterization. Both "
                    "hypotension AND need for support are required for 'yes'. Scores 5 points.",
        example="no"
    )
    
    intra_aortic_balloon_pump: Literal["yes", "no"] = Field(
        ...,
        description="Use of intra-aortic balloon pump (IABP) for hemodynamic support. "
                    "Includes both prophylactic and rescue IABP use. Scores 5 points.",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="CHF class III/IV by New York Heart Association Classification (marked "
                    "limitation or symptoms at rest) and/or history of pulmonary edema. "
                    "Scores 5 points if present.",
        example="no"
    )
    
    age_over_75: Literal["yes", "no"] = Field(
        ...,
        description="Age greater than 75 years at time of procedure. Advanced age is an "
                    "independent risk factor for CIN. Scores 4 points.",
        example="yes"
    )
    
    anemia: Literal["yes", "no"] = Field(
        ...,
        description="Baseline hematocrit <39% for men and <36% for women. Pre-existing "
                    "anemia reduces renal oxygen delivery and increases CIN risk. "
                    "Scores 3 points.",
        example="no"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus (Type 1 or Type 2), regardless of "
                    "current glycemic control or treatment. Diabetic nephropathy "
                    "increases susceptibility to CIN. Scores 3 points.",
        example="yes"
    )
    
    contrast_volume_ml: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Total volume of contrast media used during the procedure in mL. "
                    "Higher volumes increase CIN risk. Each 100 mL scores 1 point "
                    "(e.g., 250 mL = 2 points, 300 mL = 3 points).",
        example=200.0
    )
    
    egfr: float = Field(
        ...,
        ge=0,
        le=200,
        description="Estimated glomerular filtration rate in mL/min/1.73 m². Calculate "
                    "using MDRD or CKD-EPI equation. Scores: <20 = 6 points, "
                    "20-39 = 4 points, 40-59 = 2 points, ≥60 = 0 points.",
        example=55.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hypotension": "no",
                "intra_aortic_balloon_pump": "no",
                "congestive_heart_failure": "no",
                "age_over_75": "yes",
                "anemia": "no",
                "diabetes": "yes",
                "contrast_volume_ml": 200.0,
                "egfr": 55.0
            }
        }


class MehranScoreResponse(BaseModel):
    """
    Response model for Mehran Score for Post-PCI Contrast Nephropathy
    
    The Mehran Score stratifies patients into four risk categories:
    - Low risk (≤5 points): 7.5% CIN risk, 0.04% dialysis risk
    - Moderate risk (6-10 points): 14% CIN risk, 0.12% dialysis risk
    - High risk (11-15 points): 26.1% CIN risk, 1.09% dialysis risk
    - Very high risk (≥16 points): 57.4% CIN risk, 12.6% dialysis risk
    
    Preventive measures based on risk:
    - Low risk: Standard hydration
    - Moderate risk: Enhanced prevention (N-acetylcysteine, sodium bicarbonate)
    - High risk: Aggressive prevention, minimize contrast
    - Very high risk: Consider alternative imaging, maximum prevention
    
    Reference: Mehran R, et al. J Am Coll Cardiol. 2004;44(7):1393-9.
    """
    
    result: int = Field(
        ...,
        description="Total Mehran score calculated from the 8 risk factors",
        example=11
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including CIN risk percentage, dialysis risk, "
                    "and recommended preventive measures based on risk category",
        example="26.1% risk of contrast-induced nephropathy. 1.09% risk of CIN requiring "
                "dialysis. Aggressive preventive measures recommended. Consider alternative "
                "imaging if possible or minimize contrast volume with careful monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, or Very High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="High risk of CIN"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11,
                "unit": "points",
                "interpretation": "26.1% risk of contrast-induced nephropathy. 1.09% risk of CIN "
                                "requiring dialysis. Aggressive preventive measures recommended. "
                                "Consider alternative imaging if possible or minimize contrast volume "
                                "with careful monitoring.",
                "stage": "High Risk",
                "stage_description": "High risk of CIN"
            }
        }