"""
Infective Endocarditis (IE) Mortality Risk Score Models

Request and response models for IE Mortality Risk Score calculation.

References (Vancouver style):
1. Gunes M, Gecmen C, Beker Evans M, et al. Validated Risk Score for Predicting 
   6-Month Mortality in Infective Endocarditis. J Am Heart Assoc. 2017 Apr 7;6(4):e003016. 
   doi: 10.1161/JAHA.115.003016.
2. Murdoch DR, Corey GR, Hoen B, et al. Clinical presentation, etiology, and outcome 
   of infective endocarditis in the 21st century: the International Collaboration on 
   Endocarditis-Prospective Cohort Study. Arch Intern Med. 2009 Mar 9;169(5):463-73. 
   doi: 10.1001/archinternmed.2008.603.
3. Cahill TJ, Baddour LM, Habib G, et al. Challenges in Infective Endocarditis. 
   J Am Coll Cardiol. 2017 Jul 25;70(3):325-335. doi: 10.1016/j.jacc.2017.06.007.

The IE Mortality Risk Score predicts 6-month mortality in patients with infective 
endocarditis using validated clinical parameters from the International Collaboration 
on Endocarditis (ICE) Prospective Cohort Study. The score incorporates host factors 
(age, dialysis history), IE characteristics (pathogen, vegetation location), and 
complications (heart failure, stroke, paravalvular involvement) to provide mortality 
risk stratification. This tool helps clinicians assess prognosis and guide treatment 
decisions in patients with definite infective endocarditis.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IeMortalityRiskScoreRequest(BaseModel):
    """
    Request model for Infective Endocarditis (IE) Mortality Risk Score
    
    Predicts 6-month mortality in patients with infective endocarditis using 14 clinical 
    parameters from the validated ICE study. The score incorporates:
    
    Host Factors:
    - Age categories: ≤45 years (0 points), 46-60 years (2 points), 61-70 years (3 points), >70 years (4 points)
    - History of dialysis: No (0 points), Yes (3 points)
    
    IE Characteristics:
    - Nosocomial IE: Healthcare-associated infection (0 or 2 points)
    - Prosthetic IE: Prosthetic valve involvement (0 or 1 point)
    - Symptoms >1 month: Longer symptom duration before admission (0 or -1 point - protective)
    - Staphylococcus aureus: Causative pathogen (0 or 1 point)
    - Viridans group streptococci: Causative pathogen (0 or -2 points - protective)
    - Aortic vegetation: Aortic valve involvement (0 or 1 point)
    - Mitral vegetation: Mitral valve involvement (0 or 1 point)
    
    IE Complications:
    - NYHA Class 3-4 heart failure: Severe heart failure (0 or 3 points)
    - Stroke: Embolic complication (0 or 2 points)  
    - Paravalvular complication: Abscess, fistula, pseudoaneurysm (0 or 2 points)
    - Persistent bacteremia: Continued positive cultures despite treatment (0 or 2 points)
    - Surgical treatment: Surgery during hospitalization (0 or -2 points - protective)
    
    Formula: Probability (%) = 100 × [1 / (1 + exp(-(2.416×score + 0.109×score² - 4.849)))]
    
    References (Vancouver style):
    1. Gunes M, Gecmen C, Beker Evans M, et al. Validated Risk Score for Predicting 
       6-Month Mortality in Infective Endocarditis. J Am Heart Assoc. 2017 Apr 7;6(4):e003016. 
       doi: 10.1161/JAHA.115.003016.
    2. Murdoch DR, Corey GR, Hoen B, et al. Clinical presentation, etiology, and outcome 
       of infective endocarditis in the 21st century: the International Collaboration on 
       Endocarditis-Prospective Cohort Study. Arch Intern Med. 2009 Mar 9;169(5):463-73.
    """
    
    age_category: Literal["45_or_under", "46_to_60", "61_to_70", "over_70"] = Field(
        ...,
        description="Patient age category. Older age associated with increased mortality risk. Scores: ≤45 years (0), 46-60 years (2), 61-70 years (3), >70 years (4)",
        example="61_to_70"
    )
    
    history_of_dialysis: Literal["no", "yes"] = Field(
        ...,
        description="History of chronic dialysis treatment. Dialysis patients have significantly higher mortality risk due to comorbidities and complications. Scores: No (0), Yes (3)",
        example="no"
    )
    
    nosocomial_ie: Literal["no", "yes"] = Field(
        ...,
        description="Healthcare-associated infective endocarditis. Nosocomial IE is associated with worse outcomes due to resistant organisms and patient comorbidities. Scores: No (0), Yes (2)",
        example="no"
    )
    
    prosthetic_ie: Literal["no", "yes"] = Field(
        ...,
        description="Prosthetic valve infective endocarditis. Prosthetic valve IE has higher mortality due to surgical complexity and biofilm formation. Scores: No (0), Yes (1)",
        example="no"
    )
    
    symptoms_over_1_month: Literal["no", "yes"] = Field(
        ...,
        description="Symptoms present for more than 1 month before admission. Longer symptom duration may indicate lower acuity subacute disease. Scores: No (0), Yes (-1 - protective)",
        example="yes"
    )
    
    staphylococcus_aureus: Literal["no", "yes"] = Field(
        ...,
        description="Staphylococcus aureus as causative pathogen. S. aureus IE is associated with more aggressive disease and complications. Scores: No (0), Yes (1)",
        example="yes"
    )
    
    viridans_group_streptococci: Literal["no", "yes"] = Field(
        ...,
        description="Viridans group streptococci as causative pathogen. Viridans strep is generally associated with better prognosis and indolent course. Scores: No (0), Yes (-2 - protective)",
        example="no"
    )
    
    aortic_vegetation: Literal["no", "yes"] = Field(
        ...,
        description="Presence of aortic valve vegetation on echocardiography. Aortic involvement carries higher risk for embolism and valve destruction. Scores: No (0), Yes (1)",
        example="yes"
    )
    
    mitral_vegetation: Literal["no", "yes"] = Field(
        ...,
        description="Presence of mitral valve vegetation on echocardiography. Mitral involvement may lead to severe regurgitation and heart failure. Scores: No (0), Yes (1)",
        example="no"
    )
    
    nyha_class_3_or_4_hf: Literal["no", "yes"] = Field(
        ...,
        description="NYHA Class 3 or 4 heart failure. Severe heart failure is a major predictor of poor prognosis in IE. Scores: No (0), Yes (3)",
        example="no"
    )
    
    stroke: Literal["no", "yes"] = Field(
        ...,
        description="Stroke complication during IE episode. Embolic stroke is a major complication indicating high-risk disease. Scores: No (0), Yes (2)",
        example="no"
    )
    
    paravalvular_complication: Literal["no", "yes"] = Field(
        ...,
        description="Paravalvular complications including abscess, fistula, or pseudoaneurysm. Indicates severe local tissue destruction requiring surgical intervention. Scores: No (0), Yes (2)",
        example="no"
    )
    
    persistent_bacteremia: Literal["no", "yes"] = Field(
        ...,
        description="Persistent bacteremia despite appropriate antibiotic treatment. Indicates treatment failure and uncontrolled infection. Scores: No (0), Yes (2)",
        example="no"
    )
    
    surgical_treatment: Literal["no", "yes"] = Field(
        ...,
        description="Surgical treatment performed during index hospitalization. Surgery is associated with improved survival when appropriately selected. Scores: No (0), Yes (-2 - protective)",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "61_to_70",
                "history_of_dialysis": "no",
                "nosocomial_ie": "no",
                "prosthetic_ie": "no",
                "symptoms_over_1_month": "yes",
                "staphylococcus_aureus": "yes",
                "viridans_group_streptococci": "no",
                "aortic_vegetation": "yes",
                "mitral_vegetation": "no",
                "nyha_class_3_or_4_hf": "no",
                "stroke": "no",
                "paravalvular_complication": "no",
                "persistent_bacteremia": "no",
                "surgical_treatment": "no"
            }
        }


class IeMortalityRiskScoreResponse(BaseModel):
    """
    Response model for Infective Endocarditis (IE) Mortality Risk Score
    
    Returns the predicted 6-month mortality probability with risk stratification:
    - Low Risk (≤10%): Standard medical management with monitoring
    - Moderate Risk (10-25%): Intensive medical management, consider surgery
    - High Risk (25-50%): Aggressive treatment, surgical evaluation, prognosis discussion
    - Very High Risk (>50%): Palliative care consideration, goals of care discussion
    
    The IE Mortality Risk Score provides validated prognostic information to guide 
    clinical decision-making, including surgical timing, intensity of treatment, 
    and discussions with patients and families about prognosis. The score incorporates 
    14 clinical variables from the largest prospective study of IE outcomes.
    
    Reference: Gunes M, et al. J Am Heart Assoc. 2017;6(4):e003016.
    """
    
    result: float = Field(
        ...,
        description="Predicted 6-month mortality probability percentage calculated from IE risk score",
        example=18.5,
        ge=0.0,
        le=100.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for mortality probability",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on mortality risk category",
        example="Moderate risk of 6-month mortality. Consider intensive medical management and evaluation for surgical intervention if indicated."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category with probability range",
        example="Mortality probability 18.5% (10-25%)"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 18.5,
                "unit": "%",
                "interpretation": "Moderate risk of 6-month mortality. Consider intensive medical management and evaluation for surgical intervention if indicated.",
                "stage": "Moderate Risk",
                "stage_description": "Mortality probability 18.5% (10-25%)"
            }
        }