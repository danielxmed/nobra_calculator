"""
IV Drip Rate Calculator Models

Request and response models for IV drip rate calculator.

References (Vancouver style):
1. Phillips LD, Gorski LA. Manual of I.V. therapeutics: evidence-based practice 
   for infusion therapy. 6th ed. Philadelphia, PA: F.A. Davis Company; 2014.
2. Weinstein SM, Hagle ME. Plumer's principles and practice of infusion therapy. 
   9th ed. Philadelphia, PA: Wolters Kluwer/Lippincott Williams & Wilkins; 2014.
3. Alexander M, Corrigan A, Gorski L, Hankins J, Perucca R. Infusion nursing: 
   an evidence-based approach. 3rd ed. St. Louis, MO: Saunders Elsevier; 2010.
4. Hadaway L. Short peripheral intravenous catheters and infections. J Infus Nurs. 
   2012;35(4):230-40.

The IV Drip Rate Calculator determines the correct drops per minute needed to deliver 
a specified volume of intravenous fluid over a given time period using gravity-fed 
IV administration sets. This tool is essential in resource-limited settings or when 
electronic infusion pumps are not available, providing healthcare providers with 
accurate manual infusion rates for safe patient care.
"""

from pydantic import BaseModel, Field
from typing import Literal


class IvDripRateCalculatorRequest(BaseModel):
    """
    Request model for IV Drip Rate Calculator
    
    The IV drip rate calculation uses three essential parameters to determine the correct 
    drops per minute for gravity-fed intravenous administration:
    
    Formula: IV Drip Rate (gtts/min) = (Volume in mL × Drop factor in gtts/mL) / Time in minutes
    
    Parameters:
    
    1. Volume (mL): Total amount of IV fluid to be administered
       - Range: 1-10,000 mL to accommodate various clinical scenarios
       - Common volumes: 50-1000 mL for medications, up to 3000+ mL for resuscitation
       - Includes maintenance fluids, blood products, medications, and resuscitation fluids
    
    2. Time (minutes): Duration over which the infusion should be completed
       - Range: 1-14,400 minutes (up to 10 days for extended infusions)
       - Common timeframes: 15-60 minutes for medications, 2-8 hours for maintenance fluids
       - Consider patient condition, medication requirements, and clinical urgency
    
    3. Drop Factor (gtts/mL): Number of drops per milliliter delivered by the IV tubing
    
    Drop Factor Types and Clinical Applications:
    
    Microdrip/Minidrip Tubing (60 gtts/mL):
    - Used for: Pediatric patients, critical medications, precise dosing
    - Advantages: Most accurate for small volumes and slow rates
    - Clinical use: Vasoactive drips, chemotherapy, neonatal care
    - Counting: Easier to count due to smaller, more frequent drops
    
    Macrodrip/Regular Tubing (10-20 gtts/mL):
    - 10 gtts/mL: Large volume, rapid infusion (trauma, surgery)
    - 15 gtts/mL: Standard fluid administration (most common)
    - 20 gtts/mL: Moderate volume infusions
    - Advantages: Faster delivery, good for maintenance fluids
    - Clinical use: Crystalloids, blood products, routine medications
    
    Safety Considerations:
    - Always verify drop factor on IV tubing packaging
    - Monitor patient for fluid overload or inadequate infusion
    - Consider patient factors: age, cardiac status, renal function
    - Count drops for 15 seconds and multiply by 4 to verify rate
    - Adjust using roller clamp on IV tubing
    
    Clinical Applications:
    - Resource-limited settings without electronic pumps
    - Backup method when pumps malfunction
    - Field medicine and emergency situations
    - Educational purposes for understanding infusion principles
    
    References (Vancouver style):
    1. Phillips LD, Gorski LA. Manual of I.V. therapeutics: evidence-based practice 
    for infusion therapy. 6th ed. Philadelphia, PA: F.A. Davis Company; 2014.
    2. Alexander M, Corrigan A, Gorski L, Hankins J, Perucca R. Infusion nursing: 
    an evidence-based approach. 3rd ed. St. Louis, MO: Saunders Elsevier; 2010.
    """
    
    volume_ml: float = Field(
        ...,
        ge=1,
        le=10000,
        description="Total volume of IV fluid to be administered in milliliters. Range includes small medication volumes (1-50 mL) to large resuscitation volumes (up to 10,000 mL). Consider patient size, clinical condition, and indication for infusion",
        example=1000.0
    )
    
    time_minutes: float = Field(
        ...,
        ge=1,
        le=14400,
        description="Total time for infusion in minutes (1 minute to 10 days). Consider medication requirements, patient tolerance, clinical urgency, and safety parameters. Common ranges: 15-60 min for medications, 2-8 hours for maintenance fluids",
        example=480.0
    )
    
    drop_factor: Literal["10", "15", "20", "60"] = Field(
        ...,
        description="Drop factor of IV tubing in drops per mL. 60 gtts/mL = microdrip for precise delivery (pediatrics, critical meds). 10-20 gtts/mL = macrodrip for routine fluids. Always verify on tubing packaging - critical for patient safety",
        example="15"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "volume_ml": 1000.0,
                "time_minutes": 480.0,
                "drop_factor": "15"
            }
        }


class IvDripRateCalculatorResponse(BaseModel):
    """
    Response model for IV Drip Rate Calculator
    
    The IV drip rate result provides the calculated drops per minute with clinical interpretation 
    and safety guidance based on the infusion parameters:
    
    Drip Rate Categories and Clinical Implications:
    
    Slow Infusion (<30 gtts/min):
    - Clinical use: Maintenance fluids, careful medication titration, fluid-sensitive patients
    - Advantages: Easy to count manually, low risk of fluid overload
    - Monitoring: Standard vital signs, less frequent rate verification needed
    - Patient types: CHF, renal failure, elderly, pediatric maintenance
    
    Moderate Infusion (30-100 gtts/min):
    - Clinical use: Standard fluid resuscitation, blood products, routine medications
    - Monitoring: Regular rate checks every 15-30 minutes, careful counting required
    - Patient care: Standard IV monitoring protocols, watch for infiltration
    - Rate verification: Count for 15 seconds × 4 or 30 seconds × 2
    
    Fast Infusion (100-200 gtts/min):
    - Clinical use: Rapid resuscitation, urgent medication delivery, trauma protocols
    - Challenges: Difficult to count accurately, requires frequent monitoring
    - Safety measures: Consider larger bore tubing, multiple IV sites if available
    - Patient monitoring: Continuous assessment for fluid overload, electrolyte changes
    
    Very Fast Infusion (>200 gtts/min):
    - Clinical use: Emergency resuscitation, critical volume replacement
    - Limitations: Extremely difficult to count manually, high error risk
    - Alternatives: Pressure bags, multiple IV lines, electronic pumps if available
    - Monitoring: Continuous patient assessment, frequent vital signs
    
    Safety Guidelines:
    - Always double-check drop factor on IV tubing packaging
    - Start infusion slowly and gradually increase to calculated rate
    - Monitor for signs of infiltration, phlebitis, or fluid overload
    - Document infusion rate, patient response, and any adjustments made
    - Have alternative delivery methods available for very fast rates
    
    Clinical Considerations:
    - Patient tolerance may require rate adjustment regardless of calculation
    - Consider patient's cardiovascular and renal status
    - Some medications require specific infusion rates regardless of volume
    - Environmental factors (temperature, movement) can affect drip consistency
    
    Quality Assurance:
    - Verify calculation independently before starting infusion
    - Use consistent counting method (15 seconds × 4 recommended)
    - Document actual counted rate vs. calculated rate
    - Adjust roller clamp carefully to achieve target rate
    - Re-verify rate after any adjustments
    
    Reference: Phillips LD, Gorski LA. Manual of I.V. therapeutics. 6th ed. 2014.
    """
    
    result: float = Field(
        ...,
        description="Calculated IV drip rate in drops per minute using the formula: (Volume × Drop factor) / Time",
        example=31.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the drip rate",
        example="gtts/min"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including infusion category, safety considerations, monitoring requirements, and practical guidance for manual drip rate management",
        example="Moderate infusion rate of 31.2 gtts/min using macrodrip (15 gtts/mL) tubing. Delivering 1000 mL over 8.0 hours at 125.0 mL/hr. This rate is appropriate for standard fluid resuscitation, blood products, or routine medication administration. Requires careful counting and frequent monitoring. Adjust roller clamp as needed to maintain consistent rate."
    )
    
    stage: str = Field(
        ...,
        description="Infusion rate category (Slow, Moderate, Fast, Very Fast Infusion)",
        example="Moderate Infusion"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the infusion rate category",
        example="Moderate drip rate infusion"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 31.2,
                "unit": "gtts/min",
                "interpretation": "Moderate infusion rate of 31.2 gtts/min using macrodrip (15 gtts/mL) tubing. Delivering 1000 mL over 8.0 hours at 125.0 mL/hr. This rate is appropriate for standard fluid resuscitation, blood products, or routine medication administration. Requires careful counting and frequent monitoring. Adjust roller clamp as needed to maintain consistent rate.",
                "stage": "Moderate Infusion",
                "stage_description": "Moderate drip rate infusion"
            }
        }