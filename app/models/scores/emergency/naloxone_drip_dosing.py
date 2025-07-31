"""
Naloxone Drip Dosing Models

Request and response models for Naloxone Drip Dosing calculation.

References (Vancouver style):
1. Boyer EW. Management of opioid analgesic overdose. N Engl J Med. 2012 Jul 12;367(2):146-55. 
   doi: 10.1056/NEJMra1202561.
2. Clarke SF, Dargan PI, Jones AL. Naloxone in opioid poisoning: walking the tightrope. 
   Emerg Med J. 2005 Sep;22(9):612-6. doi: 10.1136/emj.2003.009613.
3. Connors NJ, Nelson LS. The Evolution of Recommended Naloxone Dosing for Opioid Overdose 
   by Medical Specialty. J Med Toxicol. 2016 Sep;12(3):276-81. doi: 10.1007/s13181-016-0559-3.
4. Rzasa Lynn R, Galinkin JL. Naloxone dosage for opioid reversal: current evidence and 
   clinical implications. Ther Adv Drug Saf. 2018 Jan;9(1):63-88. 
   doi: 10.1177/2042098617744161.

The Naloxone Drip Dosing calculator determines the appropriate continuous IV infusion rate 
for naloxone in patients with acute opioid overdose who require sustained reversal. The 
formula uses two-thirds of the initial effective bolus dose per hour, maintaining the same 
level of opioid reversal achieved with the initial bolus while accounting for naloxone's 
shorter half-life compared to most opioids.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional


class NaloxoneDripDosingRequest(BaseModel):
    """
    Request model for Naloxone Drip Dosing
    
    The naloxone drip is indicated when:
    - Patient overdosed on long-acting opioids (methadone, sustained-release formulations)
    - Multiple bolus doses were required for initial reversal
    - Recurrent respiratory depression occurs after initial reversal
    - Synthetic opioids (fentanyl, carfentanil) are suspected
    
    Clinical Approach:
    1. Administer naloxone boluses until adequate reversal achieved
    2. Note total dose required in first hour (this is the bolus dose)
    3. Calculate infusion rate as 2/3 of bolus dose per hour
    4. Give half the bolus dose 15 minutes after starting infusion
    5. Titrate to maintain reversal without precipitating withdrawal
    
    References (Vancouver style):
    1. Boyer EW. Management of opioid analgesic overdose. N Engl J Med. 2012 Jul 12;367(2):146-55. 
       doi: 10.1056/NEJMra1202561.
    """
    
    bolus_dose: float = Field(
        ...,
        ge=0.1,
        le=10.0,
        description=(
            "Total naloxone dose required in the first hour to achieve adequate reversal (mg). "
            "This is the cumulative dose of all boluses needed to reverse respiratory depression "
            "and restore adequate ventilation. Common range is 0.4-2 mg for heroin, but may be "
            "much higher (4-10 mg) for synthetic opioids like fentanyl."
        ),
        example=2.0
    )
    
    @field_validator('bolus_dose')
    def validate_bolus_dose(cls, v):
        """Ensure bolus dose is within reasonable clinical range"""
        if v < 0.1:
            raise ValueError("Bolus dose must be at least 0.1 mg")
        if v > 10:
            raise ValueError(
                "Bolus dose exceeds 10 mg. While higher doses may occasionally be needed "
                "for synthetic opioids, please verify this extreme dose requirement."
            )
        return round(v, 2)  # Round to 2 decimal places for practical dosing
    
    class Config:
        json_schema_extra = {
            "example": {
                "bolus_dose": 2.0
            }
        }


class NaloxoneDripDosingResponse(BaseModel):
    """
    Response model for Naloxone Drip Dosing
    
    The continuous naloxone infusion maintains opioid reversal without repeated boluses.
    Naloxone's half-life (30-100 minutes) is shorter than most opioids, requiring 
    continuous administration to prevent recurrent respiratory depression.
    
    Monitoring Requirements:
    - Continuous pulse oximetry
    - Frequent vital signs (q15-30 min initially)
    - Level of consciousness assessment
    - Signs of opioid withdrawal
    - ICU-level monitoring recommended
    
    Titration Guidelines:
    - Increase rate if respiratory depression recurs
    - Decrease rate if withdrawal symptoms develop
    - Goal: RR >12/min, SpO2 >92%, responsive to verbal stimuli
    
    Reference: Clarke SF, et al. Emerg Med J. 2005;22(9):612-6.
    """
    
    result: float = Field(
        ...,
        description=(
            "Continuous IV infusion starting rate in mg/hr. This rate maintains "
            "the level of reversal achieved with the initial bolus dose."
        ),
        example=1.33
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the infusion rate",
        example="mg/hr"
    )
    
    interpretation: str = Field(
        ...,
        description=(
            "Clinical interpretation including infusion instructions, additional bolus "
            "timing, titration parameters, and monitoring requirements"
        ),
        example=(
            "Start continuous IV infusion at 1.33 mg/hr. Administer 1.0 mg bolus "
            "(half of initial dose) 15 minutes after starting the infusion to prevent "
            "drop in naloxone levels. Titrate infusion rate based on:\n"
            "- Respiratory rate (maintain >12/min)\n"
            "- Oxygen saturation\n"
            "- Level of consciousness\n\n"
            "Decrease rate if withdrawal symptoms occur. Monitor closely as naloxone "
            "half-life (30-100 min) is shorter than most opioids. Consider ICU "
            "admission for continuous monitoring."
        )
    )
    
    additional_bolus_at_15_min: float = Field(
        ...,
        description=(
            "Additional naloxone bolus dose to administer 15 minutes after starting "
            "the infusion (mg). This prevents the drop in naloxone levels that occurs "
            "when transitioning from bolus to infusion."
        ),
        example=1.0
    )
    
    additional_bolus_unit: str = Field(
        ...,
        description="Unit for the additional bolus dose",
        example="mg"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1.33,
                "unit": "mg/hr",
                "interpretation": (
                    "Start continuous IV infusion at 1.33 mg/hr. Administer 1.0 mg bolus "
                    "(half of initial dose) 15 minutes after starting the infusion to prevent "
                    "drop in naloxone levels. Titrate infusion rate based on:\n"
                    "- Respiratory rate (maintain >12/min)\n"
                    "- Oxygen saturation\n"
                    "- Level of consciousness\n\n"
                    "Decrease rate if withdrawal symptoms occur. Monitor closely as naloxone "
                    "half-life (30-100 min) is shorter than most opioids. Consider ICU "
                    "admission for continuous monitoring."
                ),
                "additional_bolus_at_15_min": 1.0,
                "additional_bolus_unit": "mg"
            }
        }