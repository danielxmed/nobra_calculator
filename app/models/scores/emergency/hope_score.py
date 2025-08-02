"""
Hypothermia Outcome Prediction after ECLS (HOPE) Score Models

Request and response models for HOPE Score calculation.

References (Vancouver style):
1. Pasquier M, Hugli O, Paal P, Darocha T, Blancher M, Husby P, et al. 
   Hypothermia outcome prediction after extracorporeal life support for hypothermic 
   cardiac arrest patients: The HOPE score. Resuscitation. 2018 May;126:58-64. 
   doi: 10.1016/j.resuscitation.2018.02.026.
2. Darocha T, Kosinski S, Jarosz A, Sobczyk D, Galazkowski R, Piątek J, et al. 
   The chain of survival in hypothermic circulatory arrest: encouraging preliminary 
   results when using early identification, risk stratification and extracorporeal 
   rewarming. Scand J Trauma Resusc Emerg Med. 2016 Jun 1;24:85. 
   doi: 10.1186/s13049-016-0281-9.
3. Lott C, Truhlář A, Alfonzo A, Barelli A, González-Salvado V, Hinkelbein J, et al. 
   European Resuscitation Council Guidelines 2021: Cardiac arrest in special circumstances. 
   Resuscitation. 2021 Apr;161:152-219. doi: 10.1016/j.resuscitation.2021.02.011.

The HOPE Score predicts survival probability for patients with hypothermic cardiac arrest 
undergoing extracorporeal life support (ECLS) rewarming. This validated tool guides clinical 
decision-making about initiating ECLS based on a 10% survival probability threshold. The score 
demonstrates superior discrimination compared to serum potassium alone (AUC 0.895 vs 0.774) 
and has been externally validated with excellent performance (AUC 0.825).
"""

from pydantic import BaseModel, Field
from typing import Literal


class HopeScoreRequest(BaseModel):
    """
    Request model for Hypothermia Outcome Prediction after ECLS (HOPE) Score
    
    The HOPE Score uses six clinical parameters to predict survival probability in 
    hypothermic cardiac arrest patients undergoing ECLS rewarming:
    
    1. Sex: Male patients have slightly lower survival probability
       - Male: Associated with decreased survival (coefficient -1.55)
       - Female: Reference category with better outcomes
    
    2. Hypothermia with Asphyxia: Mechanism of cooling affects outcomes
       - Yes: Asphyxial hypothermia (drowning, avalanche burial) has worse prognosis
       - No: Non-asphyxial hypothermia (exposure) has better outcomes
    
    3. Age: Advanced age negatively impacts survival
       - Each year increases mortality risk (coefficient -0.0191)
       - Pediatric and young adult patients have better outcomes
    
    4. Serum Potassium: Strong predictor of outcome (hyperkalemia indicates cellular death)
       - Higher potassium levels indicate worse cellular damage
       - Traditional cutoff was 12 mmol/L, but HOPE score provides more nuanced assessment
       - Logarithmic relationship with survival (coefficient -2.07)
    
    5. CPR Duration: Prolonged resuscitation decreases survival probability
       - Each minute of CPR reduces chances of good outcome
       - Logarithmic relationship (coefficient -0.573)
       - Extended CPR acceptable in hypothermia due to neuroprotective effects
    
    6. Core Temperature: Degree of hypothermia affects outcome
       - Optimal protective temperature range exists
       - Quadratic relationship (linear coefficient +0.937, squared coefficient -0.0247)
       - Severe hypothermia may indicate prolonged exposure
    
    Clinical Decision Making:
    - Survival probability ≥10%: ECLS rewarming recommended
    - Survival probability <10%: ECLS unlikely to benefit, consider comfort care
    - The 10% threshold provides 97% negative predictive value
    
    Formula:
    HOPE Score = 2.44 - 1.55*(Sex: Male=1) - 1.95*(Asphyxia: Yes=1) - 0.0191*(Age) 
                - 2.07*log₂(Potassium) - 0.573*log₂(CPR duration) + 0.937*(Temperature) 
                - 0.0247*(Temperature)²
    
    Survival Probability = e^(HOPE Score) / (1 + e^(HOPE Score)) * 100%
    
    References (Vancouver style):
    1. Pasquier M, Hugli O, Paal P, Darocha T, Blancher M, Husby P, et al. 
       Hypothermia outcome prediction after extracorporeal life support for hypothermic 
       cardiac arrest patients: The HOPE score. Resuscitation. 2018 May;126:58-64. 
       doi: 10.1016/j.resuscitation.2018.02.026.
    2. Darocha T, Kosinski S, Jarosz A, Sobczyk D, Galazkowski R, Piątek J, et al. 
       The chain of survival in hypothermic circulatory arrest: encouraging preliminary 
       results when using early identification, risk stratification and extracorporeal 
       rewarming. Scand J Trauma Resusc Emerg Med. 2016 Jun 1;24:85. 
       doi: 10.1186/s13049-016-0281-9.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Male sex is associated with slightly decreased survival probability "
                   "in hypothermic cardiac arrest (coefficient -1.55 in HOPE score calculation). "
                   "This may reflect physiological differences in cold tolerance or exposure patterns.",
        example="male"
    )
    
    hypothermia_with_asphyxia: Literal["yes", "no"] = Field(
        ...,
        description="Hypothermia with asphyxia (drowning, avalanche burial with airway obstruction). "
                   "yes: Asphyxial hypothermia has worse prognosis due to combined hypoxic and hypothermic injury. "
                   "no: Non-asphyxial hypothermia (environmental exposure) has better outcomes due to preserved "
                   "oxygenation during cooling. This is a strong negative prognostic factor (coefficient -1.95).",
        example="no"
    )
    
    age_years: int = Field(
        ...,
        ge=0,
        le=120,
        description="Patient age in years. Advanced age is associated with decreased survival probability "
                   "in hypothermic cardiac arrest. Each year of age decreases survival odds (coefficient -0.0191). "
                   "Pediatric and young adult patients have significantly better outcomes due to greater "
                   "physiological reserve and cold tolerance.",
        example=45
    )
    
    potassium_mmol_l: float = Field(
        ...,
        ge=1.0,
        le=20.0,
        description="Serum potassium level in mmol/L. Hyperkalemia reflects degree of cellular damage "
                   "and tissue death during hypothermic arrest. Higher potassium levels indicate worse "
                   "cellular integrity and decreased survival probability. The HOPE score uses logarithmic "
                   "transformation (coefficient -2.07*log₂(K⁺)) to account for non-linear relationship. "
                   "Traditional cutoff was 12 mmol/L, but HOPE provides more nuanced risk assessment.",
        example=6.5
    )
    
    cpr_duration_minutes: int = Field(
        ...,
        ge=1,
        le=600,
        description="Duration of cardiopulmonary resuscitation in minutes from arrest to ECLS initiation. "
                   "Prolonged CPR duration decreases survival probability, but extended resuscitation is "
                   "acceptable in hypothermia due to neuroprotective effects of cooling. Uses logarithmic "
                   "relationship (coefficient -0.573*log₂(CPR duration)) to reflect diminishing returns "
                   "of prolonged resuscitation efforts.",
        example=45
    )
    
    core_temperature_celsius: float = Field(
        ...,
        ge=10.0,
        le=35.0,
        description="Core body temperature in degrees Celsius at hospital arrival. The relationship "
                   "with survival is complex and quadratic - moderate hypothermia may be protective "
                   "while severe hypothermia indicates prolonged exposure. Formula uses both linear "
                   "(+0.937*T) and quadratic (-0.0247*T²) terms to capture optimal protective range "
                   "around 20-25°C. Temperatures <15°C or >30°C may indicate poor prognosis.",
        example=22.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "hypothermia_with_asphyxia": "no",
                "age_years": 45,
                "potassium_mmol_l": 6.5,
                "cpr_duration_minutes": 45,
                "core_temperature_celsius": 22.5
            }
        }


class HopeScoreResponse(BaseModel):
    """
    Response model for Hypothermia Outcome Prediction after ECLS (HOPE) Score
    
    The HOPE Score provides survival probability prediction for hypothermic cardiac arrest 
    patients undergoing ECLS rewarming, with a critical decision threshold at 10% survival probability:
    
    Clinical Decision Framework:
    - Survival probability ≥10%: ECLS rewarming recommended
      * Immediately notify ECLS-capable center
      * Activate rewarming protocol
      * Maintain high-quality CPR during transport
      * Most survivors (84%) achieve good neurological outcomes
    
    - Survival probability <10%: ECLS unlikely to benefit
      * Consider withholding ECLS
      * Focus on compassionate end-of-life care
      * Discuss goals of care with family
      * 97% negative predictive value for poor outcome
    
    Clinical Validation:
    - Derived from 286 patients with 37% overall survival
    - Superior discrimination vs. potassium alone (AUC 0.895 vs 0.774)
    - External validation confirmed excellent performance (AUC 0.825)
    - Negative predictive value 97% for HOPE <10%
    - Recommended in 2021 European Resuscitation Council Guidelines
    
    Implementation Considerations:
    - Not validated for mild hypothermia or non-accidental arrests
    - Primarily validated in adult populations
    - Clinical judgment should complement score interpretation
    - Available online calculator: https://www.hypothermiascore.org
    
    Reference: Pasquier M, et al. Resuscitation. 2018;126:58-64.
    """
    
    result: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Predicted survival probability as percentage (0-100%)",
        example=25.7
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for survival probability",
        example="percentage"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with ECLS recommendation and next steps based on survival probability",
        example="Survival probability is 25.7%, which meets the threshold for ECLS initiation. ECLS rewarming is recommended."
    )
    
    stage: str = Field(
        ...,
        description="Clinical decision category (Low Survival Probability or Favorable for ECLS)",
        example="Favorable for ECLS"
    )
    
    stage_description: str = Field(
        ...,
        description="Description of survival probability range relative to 10% threshold",
        example="≥10% survival probability"
    )
    
    hope_score: float = Field(
        ...,
        description="Raw HOPE score value used in logistic transformation to calculate survival probability",
        example=-1.234
    )
    
    ecls_recommended: bool = Field(
        ...,
        description="Boolean indicating whether ECLS rewarming is recommended (true if survival probability ≥10%)",
        example=True
    )
    
    clinical_recommendation: str = Field(
        ...,
        description="Specific clinical recommendation based on survival probability threshold",
        example="ECLS recommended - Proceed with extracorporeal rewarming"
    )
    
    decision_threshold: str = Field(
        ...,
        description="The clinical decision threshold used for ECLS recommendation",
        example="10%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 25.7,
                "unit": "percentage",
                "interpretation": "Survival probability is 25.7%, which meets the threshold for ECLS initiation. ECLS rewarming is recommended. Immediately notify ECLS-capable center and activate rewarming protocol while maintaining high-quality CPR. Patient has reasonable chance of survival with good neurological outcome.",
                "stage": "Favorable for ECLS",
                "stage_description": "≥10% survival probability",
                "hope_score": -1.234,
                "ecls_recommended": True,
                "clinical_recommendation": "ECLS recommended - Proceed with extracorporeal rewarming",
                "decision_threshold": "10%"
            }
        }