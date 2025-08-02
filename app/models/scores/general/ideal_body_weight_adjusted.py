"""
Ideal Body Weight and Adjusted Body Weight Models

Request and response models for Ideal Body Weight and Adjusted Body Weight calculation.

References (Vancouver style):
1. Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974;8:650-655.
2. Pai MP, Paloucek FP. The origin of the "ideal" body weight equations. Ann Pharmacother. 
   2000 Sep;34(9):1066-9. doi: 10.1345/aph.19381.
3. Robinson JD, Lupkiewicz SM, Palenik L, Lopez LM, Ariet M. Determination of ideal body 
   weight for drug dosage calculations. Am J Hosp Pharm. 1983 Jun;40(6):1016-9. 
   doi: 10.1093/ajhp/40.6.1016.

The Ideal Body Weight and Adjusted Body Weight calculator uses the Devine formula to calculate 
ideal body weight and provides adjusted body weight for overweight/obese patients. Originally 
developed for medication dosing, these calculations are widely used in clinical practice for 
drug dosing, mechanical ventilation parameters, and nutritional assessments. The Devine formula 
is the most commonly used method for ideal body weight calculation in clinical settings.
"""

from pydantic import BaseModel, Field
from typing import Literal, List, Optional, Dict, Any


class IdealBodyWeightAdjustedRequest(BaseModel):
    """
    Request model for Ideal Body Weight and Adjusted Body Weight Calculator
    
    The calculator uses the Devine formula to determine ideal body weight and calculates 
    adjusted body weight for clinical applications, particularly medication dosing:
    
    1. Sex: Different baseline weights for calculation
       - Male: Base weight 50 kg (higher muscle mass and frame size)
       - Female: Base weight 45.5 kg (smaller average frame size)
    
    2. Height: Used in linear calculation above 60 inches (152.4 cm)
       - Standard formula assumes height ≥60 inches (5 feet)
       - For shorter patients, consider adjusting final result downward
       - Height increment: 2.3 kg per inch above 60 inches
    
    3. Actual Weight (Optional): Used for adjusted body weight calculation
       - Required only if adjusted body weight needed
       - Useful for overweight/obese patients where ideal weight may underestimate dosing needs
       - Not needed for ideal body weight calculation alone
    
    Devine Formula:
    - Men: IBW = 50 kg + 2.3 kg × (height in inches - 60)
    - Women: IBW = 45.5 kg + 2.3 kg × (height in inches - 60)
    
    Adjusted Body Weight Formula:
    - AdjBW = IBW + 0.4 × (Actual Weight - IBW)
    - Only calculated when actual weight > ideal weight
    - Uses 40% of excess weight above ideal weight
    
    Clinical Applications:
    - Medication dosing (especially antibiotics, anesthetics, chemotherapy)
    - Mechanical ventilation tidal volume calculation (6-8 mL/kg IBW)
    - Nutritional assessment and caloric needs estimation
    - Research calculations and clinical trials
    
    Limitations:
    - Developed for heights ≥60 inches (consider adjustment for shorter patients)
    - Not suitable for athletes with high muscle mass
    - Population-based averages may not fit individual body composition
    - Clinical judgment needed for specific medication classes
    
    References (Vancouver style):
    1. Devine BJ. Gentamicin therapy. Drug Intell Clin Pharm. 1974;8:650-655.
    2. Pai MP, Paloucek FP. The origin of the "ideal" body weight equations. Ann Pharmacother. 
       2000 Sep;34(9):1066-9. doi: 10.1345/aph.19381.
    """
    
    sex: Literal["male", "female"] = Field(
        ...,
        description="Patient sex. Male patients have higher baseline weight (50 kg) compared to "
                   "female patients (45.5 kg) in the Devine formula, reflecting average differences "
                   "in body composition and frame size.",
        example="male"
    )
    
    height_inches: float = Field(
        ...,
        ge=48.0,
        le=84.0,
        description="Patient height in inches. The Devine formula was developed for heights ≥60 inches "
                   "(5 feet). For patients shorter than 60 inches, consider subtracting 2-5 lbs per inch "
                   "below the 60-inch threshold from the calculated ideal weight. Range: 48-84 inches "
                   "(approximately 4-7 feet) for practical clinical use.",
        example=70.0
    )
    
    actual_weight_kg: Optional[float] = Field(
        None,
        ge=20.0,
        le=300.0,
        description="Patient's actual body weight in kg (optional). Required only for adjusted body weight "
                   "calculation. When provided, allows calculation of adjusted body weight for overweight/obese "
                   "patients. If actual weight ≤ ideal weight, actual weight is used for dosing. If actual weight "
                   "> ideal weight, adjusted body weight provides intermediate value between ideal and actual.",
        example=85.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "sex": "male",
                "height_inches": 70.0,
                "actual_weight_kg": 85.0
            }
        }


class IdealBodyWeightAdjustedResponse(BaseModel):
    """
    Response model for Ideal Body Weight and Adjusted Body Weight Calculator
    
    The calculator provides ideal body weight using the validated Devine formula and, 
    when actual weight is provided, calculates adjusted body weight for clinical use:
    
    Clinical Decision Making:
    - Ideal Body Weight: Use for most medication dosing, especially hydrophilic drugs
    - Adjusted Body Weight: Consider for lipophilic drugs in overweight/obese patients
    - Tidal Volume: Always use ideal body weight (6-8 mL/kg IBW)
    - Nutritional Assessment: May use either depending on clinical context
    
    Medication Dosing Guidelines:
    - Hydrophilic medications (aminoglycosides, vancomycin): Use ideal body weight
    - Lipophilic medications (propofol, some anesthetics): Consider adjusted body weight
    - Chemotherapy: Often uses body surface area, but weight-based doses may use adjusted weight
    - Always confirm specific medication dosing guidelines with pharmacy
    
    Height Considerations:
    - Standard formula accurate for heights ≥60 inches (152.4 cm)
    - For shorter patients: Consider reducing calculated weight by 2-5 lbs per inch below 60 inches
    - Very tall patients (>84 inches): Formula may overestimate, use clinical judgment
    
    Limitations and Considerations:
    - Population-based formula may not reflect individual body composition
    - Not validated for extreme body weights or heights
    - Athletes with high muscle mass may require actual weight for some calculations
    - Elderly patients may have different body composition requiring clinical adjustment
    
    Reference: Devine BJ. Drug Intell Clin Pharm. 1974;8:650-655.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Dictionary containing calculated body weights and height conversions",
        example={
            "ideal_body_weight": 72.7,
            "adjusted_body_weight": 77.6,
            "height_inches": 70.0,
            "height_cm": 177.8
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for body weights",
        example="kg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with dosing recommendations based on calculated weights",
        example="Ideal body weight: 72.7 kg. Patient is 12.3 kg above ideal weight. Consider using adjusted body weight (77.6 kg) for certain medications and calculations."
    )
    
    stage: str = Field(
        ...,
        description="Height category classification (Normal Height or Short Stature)",
        example="Normal Height"
    )
    
    stage_description: str = Field(
        ...,
        description="Height range description relative to formula validation",
        example="≥60 inches (5 feet)"
    )
    
    clinical_applications: List[str] = Field(
        ...,
        description="List of clinical applications for the calculated weights",
        example=[
            "Medication dosing in overweight/obese patients",
            "Tidal volume calculation (use ideal body weight)",
            "Nutritional assessment and planning",
            "Clinical research calculations"
        ]
    )
    
    dosing_considerations: List[str] = Field(
        ...,
        description="Specific dosing considerations and guidelines for medication use",
        example=[
            "Hydrophilic drugs: typically use ideal body weight",
            "Lipophilic drugs: may use adjusted body weight",
            "Confirm specific medication dosing guidelines",
            "Adjusted body weight = IBW + 0.4 × (actual weight - IBW)"
        ]
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "ideal_body_weight": 72.7,
                    "adjusted_body_weight": 77.6,
                    "height_inches": 70.0,
                    "height_cm": 177.8
                },
                "unit": "kg",
                "interpretation": "Ideal body weight: 72.7 kg. Patient is 12.3 kg above ideal weight. Consider using adjusted body weight (77.6 kg) for certain medications and calculations. Standard Devine formula applies.",
                "stage": "Normal Height",
                "stage_description": "≥60 inches (5 feet)",
                "clinical_applications": [
                    "Medication dosing in overweight/obese patients",
                    "Tidal volume calculation (use ideal body weight)",
                    "Nutritional assessment and planning",
                    "Clinical research calculations"
                ],
                "dosing_considerations": [
                    "Hydrophilic drugs: typically use ideal body weight",
                    "Lipophilic drugs: may use adjusted body weight",
                    "Confirm specific medication dosing guidelines",
                    "Adjusted body weight = IBW + 0.4 × (actual weight - IBW)"
                ]
            }
        }