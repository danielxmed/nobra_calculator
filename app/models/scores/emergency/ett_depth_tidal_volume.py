"""
Endotracheal Tube (ETT) Depth and Tidal Volume Calculator Models

Request and response models for ETT depth and tidal volume calculation.

References (Vancouver style):
1. Techanivate A, Kumwilaisak K, Samranrean S. Estimation of the proper length 
   of orotracheal intubation by Chula formula. J Med Assoc Thai. 2005 Dec;88(12):1838-46. 
   PMID: 16518984.
2. Acute Respiratory Distress Syndrome Network, Brower RG, Matthay MA, Morris A, 
   Schoenfeld D, Thompson BT, Wheeler A. Ventilation with lower tidal volumes as 
   compared with traditional tidal volumes for acute lung injury and the acute 
   respiratory distress syndrome. N Engl J Med. 2000 May 4;342(18):1301-8. 
   doi: 10.1056/NEJM200005043421801.
3. Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974;8:650-655.
4. Roberts CM, Franklin JA, Morris AJ, Spiro SG, MacFarlane JT. Intravenous salbutamol 
   bolus compared with an aminophylline infusion in children with severe asthma: 
   a randomized controlled trial. Thorax. 2003 Jul;58(7):618-22. doi: 10.1136/thorax.58.7.618.

The ETT Depth and Tidal Volume Calculator estimates optimal endotracheal tube placement 
depth using the Chula formula and calculates target tidal volume based on ideal body 
weight for lung-protective ventilation. This tool helps prevent complications from 
improper ETT placement and supports evidence-based mechanical ventilation strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EttDepthTidalVolumeRequest(BaseModel):
    """
    Request model for Endotracheal Tube (ETT) Depth and Tidal Volume Calculator
    
    The calculator uses two validated formulas:
    
    1. Chula Formula for ETT Depth:
       ETT depth (cm) = 0.1 × Height (cm) + 4
       
       This formula estimates optimal ETT placement from front teeth to prevent:
       - Right mainstem intubation (too deep)
       - Vocal cord injury or accidental extubation (too shallow)
    
    2. Devine Formula for Ideal Body Weight (IBW):
       - Males: IBW = 50 kg + 2.3 × (height in inches - 60)
       - Females: IBW = 45.5 kg + 2.3 × (height in inches - 60)
       
       Tidal Volume = 6-8 mL/kg × IBW (lung-protective ventilation)
    
    Indications:
    - Emergency intubation guidance
    - Initial mechanical ventilation settings
    - Lung-protective ventilation strategies
    - Quick reference for optimal ETT placement
    
    Limitations:
    - Use for patients >20 years old
    - Minimum height requirement: 152.4 cm (60 inches)
    - Always verify placement with imaging/auscultation
    - Does not replace clinical assessment
    
    References (Vancouver style):
    1. Techanivate A, Kumwilaisak K, Samranrean S. Estimation of the proper length 
       of orotracheal intubation by Chula formula. J Med Assoc Thai. 2005 Dec;88(12):1838-46. 
       PMID: 16518984.
    2. Acute Respiratory Distress Syndrome Network, Brower RG, Matthay MA, Morris A, 
       Schoenfeld D, Thompson BT, Wheeler A. Ventilation with lower tidal volumes as 
       compared with traditional tidal volumes for acute lung injury and the acute 
       respiratory distress syndrome. N Engl J Med. 2000 May 4;342(18):1301-8. 
       doi: 10.1056/NEJM200005043421801.
    """
    
    height_cm: float = Field(
        ...,
        description="Patient height in centimeters. Must be ≥152.4 cm (60 inches). Used for both ETT depth calculation (Chula formula) and ideal body weight calculation (Devine formula)",
        ge=152.4,
        le=250.0,
        example=170.0
    )
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex for ideal body weight calculation using Devine formula. Males: IBW = 50 + 2.3 × (height in inches - 60). Females: IBW = 45.5 + 2.3 × (height in inches - 60)",
        example="male"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "height_cm": 170.0,
                "sex": "male"
            }
        }


class EttDepthTidalVolumeResponse(BaseModel):
    """
    Response model for Endotracheal Tube (ETT) Depth and Tidal Volume Calculator
    
    Provides calculated values for:
    
    1. ETT Depth: Distance from front teeth to optimal tracheal position (Chula formula)
    2. Ideal Body Weight: Used for tidal volume calculations (Devine formula)
    3. Tidal Volume Range: 6-8 mL/kg IBW for lung-protective ventilation
    
    Clinical Applications:
    - Emergency intubation guidance for immediate safe positioning
    - Initial mechanical ventilation settings
    - Prevention of ETT malposition complications
    - Evidence-based lung-protective ventilation strategies
    
    Important Notes:
    - Always verify ETT position with chest X-ray, auscultation, or ultrasound
    - Calculator provides estimates for initial placement guidance
    - Clinical assessment and imaging confirmation are essential
    - Particularly valuable in emergency scenarios for rapid decision-making
    
    Reference: Techanivate A, et al. J Med Assoc Thai. 2005;88(12):1838-46.
    """
    
    result: str = Field(
        ...,
        description="Calculation result status (normal_calculations)",
        example="normal_calculations"
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for results (various units)",
        example="various"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with calculated values and recommendations for ETT placement and mechanical ventilation",
        example="For a 170.0 cm tall male patient: Recommended ETT depth is 21.0 cm from front teeth (Chula formula). Ideal body weight is 73.0 kg (Devine formula). Target tidal volume for lung-protective ventilation is 438-584 mL (6-8 mL/kg IBW). Always verify ETT position with chest radiograph, auscultation, or ultrasound for extended intubation."
    )
    
    stage: str = Field(
        ...,
        description="Calculation stage (Calculated Values)",
        example="Calculated Values"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the calculations",
        example="ETT depth and tidal volume recommendations"
    )
    
    ett_depth_cm: float = Field(
        ...,
        description="Recommended ETT depth from front teeth in centimeters (Chula formula)",
        example=21.0
    )
    
    ideal_body_weight_kg: float = Field(
        ...,
        description="Calculated ideal body weight in kilograms (Devine formula)",
        example=73.0
    )
    
    tidal_volume_min_ml: int = Field(
        ...,
        description="Minimum recommended tidal volume in mL (6 mL/kg IBW)",
        example=438
    )
    
    tidal_volume_max_ml: int = Field(
        ...,
        description="Maximum recommended tidal volume in mL (8 mL/kg IBW)",
        example=584
    )
    
    height_inches: float = Field(
        ...,
        description="Patient height converted to inches for reference",
        example=66.9
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": "normal_calculations",
                "unit": "various",
                "interpretation": "For a 170.0 cm tall male patient: Recommended ETT depth is 21.0 cm from front teeth (Chula formula). Ideal body weight is 73.0 kg (Devine formula). Target tidal volume for lung-protective ventilation is 438-584 mL (6-8 mL/kg IBW). Always verify ETT position with chest radiograph, auscultation, or ultrasound for extended intubation.",
                "stage": "Calculated Values",
                "stage_description": "ETT depth and tidal volume recommendations",
                "ett_depth_cm": 21.0,
                "ideal_body_weight_kg": 73.0,
                "tidal_volume_min_ml": 438,
                "tidal_volume_max_ml": 584,
                "height_inches": 66.9
            }
        }