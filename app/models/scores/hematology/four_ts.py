"""
FourTs calculation models
"""

from pydantic import BaseModel, Field

class UreaUnitType(str, Enum):
    """Enum for urea measurement units"""
    MMOL_L = "mmol_L"
    MG_DL = "mg_dL"



class FourTsRequest(BaseModel):
    """
    Request model for 4Ts Score calculation
    
    The 4Ts score assesses the probability of heparin-induced thrombocytopenia (HIT),
    a serious immune-mediated adverse reaction to heparin therapy.
    
    **Clinical Use**:
    - HIT probability assessment in heparin-exposed patients
    - Decision-making for heparin discontinuation
    - Alternative anticoagulation selection
    - Laboratory testing prioritization
    - Risk stratification for thrombotic complications
    
    **Score Components**:
    - Thrombocytopenia: Magnitude of platelet count fall and nadir
    - Timing: Onset timing relative to heparin exposure
    - Thrombosis: New thrombotic events or other sequelae
    - Other causes: Alternative explanations for thrombocytopenia
    
    **Reference**: Lo GK, et al. Evaluation of pretest clinical score (4 T's) for the diagnosis of heparin-induced thrombocytopenia in two clinical settings. J Thromb Haemost. 2006;4(4):759-65.
    """
    thrombocytopenia_severity: ThrombocytopeniaSeverityType = Field(
        ..., 
        description="Severity of thrombocytopenia based on platelet count fall and nadir. Greater falls and lower nadirs suggest higher HIT probability (2 points: >50% fall and nadir >20k; 1 point: 30-50% fall or nadir 10-19k; 0 points: <30% fall or nadir <10k).",
        example="fall_greater_50_nadir_greater_20"
    )
    timing_onset: TimingOnsetType = Field(
        ..., 
        description="Timing of platelet fall onset relative to heparin exposure. Classic HIT timing is 5-10 days after first exposure (2 points: typical timing; 1 point: possible timing; 0 points: unlikely timing).",
        example="onset_5_10_days_or_fall_1_day_heparin_30_days"
    )
    thrombosis_sequelae: ThrombosisSequelaeType = Field(
        ..., 
        description="Presence of thrombotic complications or other HIT sequelae. New thrombosis strongly suggests HIT (2 points: new thrombosis/skin necrosis/systemic reaction; 1 point: progressive/suspected thrombosis; 0 points: no thrombosis).",
        example="new_thrombosis_or_skin_necrosis_or_systemic_reaction"
    )
    other_causes: OtherCausesType = Field(
        ..., 
        description="Alternative explanations for thrombocytopenia. Absence of other causes increases HIT probability (2 points: no other cause; 1 point: possible other cause; 0 points: definitive other cause).",
        example="no_other_apparent_cause"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "thrombocytopenia_severity": "fall_greater_50_nadir_greater_20",
                "timing_onset": "onset_5_10_days_or_fall_1_day_heparin_30_days",
                "thrombosis_sequelae": "new_thrombosis_or_skin_necrosis_or_systemic_reaction",
                "other_causes": "no_other_apparent_cause"
            }
        }


class FourTsResponse(BaseModel):
    """
    Response model for 4Ts Score calculation
    
    Provides HIT probability assessment with specific management recommendations
    based on current hematology and thrombosis guidelines.
    
    **Probability & Management**:
    - Score 0-3: Low probability (<5%) - continue heparin, HIT testing not routinely needed
    - Score 4-5: Intermediate probability (~14%) - stop heparin, start alternative anticoagulant, HIT testing recommended
    - Score 6-8: High probability (~64%) - stop heparin immediately, start non-heparin anticoagulant, urgent HIT testing
    
    **Alternative Anticoagulants**:
    - Direct thrombin inhibitors: argatroban, bivalirudin
    - Factor Xa inhibitors: fondaparinux
    - Direct oral anticoagulants (DOACs) in select cases
    
    **Important**: Never use warfarin alone in acute HIT due to risk of venous limb gangrene
    """
    result: int = Field(
        ..., 
        description="Total 4Ts score ranging from 0-8 points. Higher scores indicate increased probability of heparin-induced thrombocytopenia.",
        example=7
    )
    unit: str = Field(
        ..., 
        description="Unit of the score result",
        example="points"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific HIT management recommendations including heparin discontinuation and alternative anticoagulation guidance.",
        example="HIT probability ~64%. Immediately discontinue all heparin. Start non-heparin anticoagulant. Perform confirmatory tests for HIT."
    )
    stage: str = Field(
        ..., 
        description="HIT probability classification (Low Probability, Intermediate Probability, High Probability)",
        example="High Probability"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the HIT probability level",
        example="High probability of HIT"
    )
    hit_probability: str = Field(
        ..., 
        description="Estimated HIT probability percentage based on validation studies",
        example="64%"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 7,
                "unit": "points",
                "interpretation": "HIT probability ~64%. Immediately discontinue all heparin. Start non-heparin anticoagulant. Perform confirmatory tests for HIT.",
                "stage": "High Probability",
                "stage_description": "High probability of HIT",
                "hit_probability": "64%"
            }
        }


# 4C Mortality Score Models
class UreaUnitType(str, Enum):
    """Enum for urea measurement units"""
    MMOL_L = "mmol_L"
    MG_DL = "mg_dL"