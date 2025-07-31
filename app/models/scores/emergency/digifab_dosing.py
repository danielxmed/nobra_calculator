"""
DigiFab (Digibind) Dosing for Digoxin Poisoning Models

Request and response models for DigiFab dosing calculation.

References (Vancouver style):
1. Lapostolle F, Borron SW, Verdier C, et al. Digoxin-specific Fab fragments as single 
   first-line therapy in digitalis poisoning. Crit Care Med. 2008;36(11):3014-8. 
   doi: 10.1097/CCM.0b013e31818b341c.
2. Antman EM, Wenger TL, Butler VP Jr, Haber E, Smith TW. Treatment of 150 cases of 
   life-threatening digitalis intoxication with digoxin-specific Fab antibody fragments. 
   Final report of a multicenter study. Circulation. 1990;81(6):1744-52. 
   doi: 10.1161/01.cir.81.6.1744.
3. Bismuth C, Gaultier M, Conso F, Efthymiou ML. Hyperkalemia in acute digitalis poisoning: 
   prognostic significance and therapeutic implications. Clin Toxicol. 1973;6(2):153-62. 
   doi: 10.3109/15563657308990513.

DigiFab (Digibind) is the definitive antidote for digoxin toxicity. This calculator determines 
the appropriate number of vials based on either serum digoxin levels or the amount ingested. 
Each vial contains approximately 40 mg of digoxin-specific antibody fragments that bind and 
neutralize digoxin, rapidly reversing toxicity.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal, Optional


class DigifabDosingRequest(BaseModel):
    """
    Request model for DigiFab (Digibind) Dosing for Digoxin Poisoning
    
    The calculator offers two methods for determining DigiFab dosing:
    
    1. Serum Level Method (preferred when available):
       - Uses patient weight and measured serum digoxin level
       - Formula: Number of vials = (serum level × weight) / 100
       - Most accurate when level drawn ≥6 hours after last dose
    
    2. Amount Ingested Method (when serum level unavailable):
       - Uses total amount of digoxin ingested
       - Formula: Number of vials = (amount ingested / 0.5) × 0.8
       - Accounts for 80% oral bioavailability
    
    Indications for DigiFab administration:
    - Life-threatening dysrhythmias (ventricular arrhythmias, high-grade AV block)
    - Potassium >5 mEq/L in acute poisoning
    - Serum digoxin level >15 ng/mL (>19 nmol/L)
    - Acute ingestion >10 mg in adults or >4 mg in children
    
    References (Vancouver style):
    1. Lapostolle F, Borron SW, Verdier C, et al. Digoxin-specific Fab fragments as single 
    first-line therapy in digitalis poisoning. Crit Care Med. 2008;36(11):3014-8.
    2. Antman EM, Wenger TL, Butler VP Jr, Haber E, Smith TW. Treatment of 150 cases of 
    life-threatening digitalis intoxication with digoxin-specific Fab antibody fragments. 
    Final report of a multicenter study. Circulation. 1990;81(6):1744-52.
    """
    
    method: Literal["serum_level", "amount_ingested"] = Field(
        ...,
        description="Calculation method. Use 'serum_level' when digoxin level is available (preferred), or 'amount_ingested' when only ingestion amount is known",
        example="serum_level"
    )
    
    weight_kg: Optional[float] = Field(
        None,
        ge=0.5,
        le=620,
        description="Patient body weight in kilograms. Required for serum level method. Range: 0.5-620 kg",
        example=75.0
    )
    
    serum_digoxin_level: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Serum digoxin level in ng/mL. Required for serum level method. Therapeutic range: 0.8-2.0 ng/mL. Should be drawn ≥6 hours after last dose for accuracy",
        example=5.5
    )
    
    amount_ingested_mg: Optional[float] = Field(
        None,
        ge=0,
        le=100,
        description="Total amount of digoxin ingested in mg. Required for amount ingested method. Note: 0.25 mg tablet is common dose",
        example=10.0
    )
    
    @field_validator('weight_kg')
    def validate_weight_for_serum_method(cls, v, values):
        if values.get('method') == 'serum_level' and v is None:
            raise ValueError('Weight is required when using serum level method')
        return v
    
    @field_validator('serum_digoxin_level')
    def validate_serum_level_for_method(cls, v, values):
        if values.get('method') == 'serum_level' and v is None:
            raise ValueError('Serum digoxin level is required when using serum level method')
        return v
    
    @field_validator('amount_ingested_mg')
    def validate_amount_for_ingested_method(cls, v, values):
        if values.get('method') == 'amount_ingested' and v is None:
            raise ValueError('Amount ingested is required when using amount ingested method')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "method": "serum_level",
                "weight_kg": 75.0,
                "serum_digoxin_level": 5.5,
                "amount_ingested_mg": None
            }
        }


class DigifabDosingResponse(BaseModel):
    """
    Response model for DigiFab (Digibind) Dosing for Digoxin Poisoning
    
    The calculator returns the number of DigiFab vials needed, always rounded up to the 
    next whole number. Each vial contains approximately 40 mg of digoxin-specific antibody 
    fragments.
    
    Administration guidelines:
    - Slow infusion over 2 hours improves efficacy when dysrhythmias are not life-threatening
    - Rapid infusion may be necessary for life-threatening dysrhythmias
    - Monitor for improvement in symptoms, ECG changes, and potassium levels
    
    Important considerations:
    - Post-DigiFab digoxin levels will be falsely elevated (bound digoxin)
    - Hyperkalemia indicates severity of poisoning
    - Avoid calcium salts which may worsen dysrhythmias
    - Consider empiric dosing in severe cases: 10-20 vials for acute, 3-6 vials for chronic
    
    Reference: Lapostolle F, et al. Crit Care Med. 2008;36(11):3014-8.
    """
    
    result: int = Field(
        ...,
        description="Number of DigiFab vials to administer (always rounded up to next whole number)",
        example=5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (vials)",
        example="vials"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with administration guidance based on calculated dose",
        example="Administer calculated number of vials. Typical dose for chronic toxicity in adults. Monitor patient closely for response."
    )
    
    stage: str = Field(
        ...,
        description="Dose category (Low dose, Moderate dose, High dose, Very high dose, Extreme dose)",
        example="Moderate dose"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the dose requirement",
        example="Moderate dose requirement"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 5,
                "unit": "vials",
                "interpretation": "Administer calculated number of vials. Typical dose for chronic toxicity in adults. Monitor patient closely for response.",
                "stage": "Moderate dose",
                "stage_description": "Moderate dose requirement"
            }
        }