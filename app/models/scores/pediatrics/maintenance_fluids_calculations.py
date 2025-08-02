"""
Maintenance Fluids Calculations (Holliday-Segar Method) Models

Request and response models for maintenance fluids calculation.

References (Vancouver style):
1. Holliday MA, Segar WE. The maintenance need for water in parenteral fluid therapy. 
   Pediatrics. 1957 May;19(5):823-32.
2. Moritz ML, Ayus JC. Prevention of hospital-acquired hyponatremia: a case for using 
   isotonic saline. Pediatrics. 2003 Feb;111(2):227-30. doi: 10.1542/peds.111.2.227.
3. Friedman JN, Beck CE, DeGroot J, Geary DF, Sklansky DJ, Freedman SB. Comparison of 
   isotonic and hypotonic intravenous maintenance fluids: a randomized clinical trial. 
   JAMA Pediatr. 2015 May;169(5):445-51. doi: 10.1001/jamapediatrics.2015.0012.

The Holliday-Segar method is the gold standard for calculating maintenance fluid 
requirements in pediatric and adult patients. Developed in 1957, this weight-based 
formula provides a systematic approach to determining appropriate fluid replacement 
rates. The method is based on metabolic demands and has been validated across different 
age groups and clinical conditions.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class MaintenanceFluidsCalculationsRequest(BaseModel):
    """
    Request model for Maintenance Fluids Calculations using Holliday-Segar Method
    
    The Holliday-Segar method calculates maintenance fluid requirements based on weight:
    
    Weight Categories and Calculations:
    - 0-10 kg: 100 mL/kg/day
      • Provides 100 mL of fluid per kilogram of body weight per day
      • Example: 8 kg patient = 8 × 100 = 800 mL/day
    
    - 10-20 kg: 1000 mL/day + 50 mL/kg for each kg over 10
      • First 10 kg calculated at 100 mL/kg = 1000 mL/day
      • Additional weight over 10 kg calculated at 50 mL/kg/day
      • Example: 15 kg patient = 1000 + (5 × 50) = 1250 mL/day
    
    - >20 kg: 1500 mL/day + 20 mL/kg for each kg over 20
      • First 20 kg calculated as above = 1500 mL/day
      • Additional weight over 20 kg calculated at 20 mL/kg/day
      • Example: 30 kg patient = 1500 + (10 × 20) = 1700 mL/day
    
    Clinical Applications:
    - Maintenance IV fluid calculation for hospitalized patients
    - Post-operative fluid management
    - Replacement of normal daily fluid losses
    - Baseline for adjusting additional fluid needs
    - NPO (nothing by mouth) patients requiring IV hydration
    
    Important Considerations:
    - Formula assumes normal renal function and no excessive losses
    - Does not include replacement of ongoing losses (fever, diarrhea, drainage)
    - Consider using isotonic solutions to prevent hyponatremia
    - Adjust for clinical conditions (heart failure, renal disease, liver disease)
    - Monitor electrolytes and fluid balance regularly
    - Neonates and premature infants may require different calculations

    References (Vancouver style):
    1. Holliday MA, Segar WE. The maintenance need for water in parenteral fluid therapy. 
    Pediatrics. 1957 May;19(5):823-32.
    2. Moritz ML, Ayus JC. Prevention of hospital-acquired hyponatremia: a case for using 
    isotonic saline. Pediatrics. 2003 Feb;111(2):227-30. doi: 10.1542/peds.111.2.227.
    3. Friedman JN, Beck CE, DeGroot J, Geary DF, Sklansky DJ, Freedman SB. Comparison of 
    isotonic and hypotonic intravenous maintenance fluids: a randomized clinical trial. 
    JAMA Pediatr. 2015 May;169(5):445-51. doi: 10.1001/jamapediatrics.2015.0012.
    """
    
    weight: float = Field(
        ...,
        ge=0.5,
        le=200.0,
        description="Patient weight in kilograms. Used to calculate maintenance fluid requirements using the Holliday-Segar method. Range: 0.5-200.0 kg",
        example=25.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "weight": 25.0
            }
        }


class MaintenanceFluidsCalculationsResponse(BaseModel):
    """
    Response model for Maintenance Fluids Calculations using Holliday-Segar Method
    
    Returns calculated maintenance fluid requirements including:
    - Daily maintenance fluid volume in mL/day
    - Hourly maintenance fluid rate in mL/hr
    - Weight category with applicable formula
    - Clinical interpretation and recommendations
    
    The response provides practical fluid management guidance including:
    - Specific volume and rate calculations
    - Clinical considerations for different patient populations
    - Recommendations for fluid type and monitoring
    - Adjustments for clinical conditions and ongoing losses
    
    Reference: Holliday MA, Segar WE. Pediatrics. 1957;19(5):823-32.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="Maintenance fluid calculation results including daily volume, hourly rate, and weight category",
        example={
            "daily_maintenance": 1600.0,
            "hourly_rate": 66.7,
            "weight_category": ">20 kg (1500 mL + 20 mL/kg for each kg >20)"
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for fluid volumes",
        example="mL"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with fluid management recommendations and considerations for patient safety",
        example="Maintenance fluid requirement: 1600.0 mL/day (66.7 mL/hr). This calculation uses the Holliday-Segar method for adult patients. Consider using isotonic solutions (normal saline or lactated Ringer's) to prevent hyponatremia. Adjust for clinical condition, ongoing losses (fever, diarrhea, drainage), and fluid balance status. Monitor electrolytes and urine output regularly."
    )
    
    stage: str = Field(
        ...,
        description="Stage classification for the calculation result",
        example="Maintenance Requirements"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the calculation stage",
        example="Standard maintenance fluid calculation"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "daily_maintenance": 1600.0,
                    "hourly_rate": 66.7,
                    "weight_category": ">20 kg (1500 mL + 20 mL/kg for each kg >20)"
                },
                "unit": "mL",
                "interpretation": "Maintenance fluid requirement: 1600.0 mL/day (66.7 mL/hr). This calculation uses the Holliday-Segar method for adult patients. Consider using isotonic solutions (normal saline or lactated Ringer's) to prevent hyponatremia. Adjust for clinical condition, ongoing losses (fever, diarrhea, drainage), and fluid balance status. Monitor electrolytes and urine output regularly.",
                "stage": "Maintenance Requirements",
                "stage_description": "Standard maintenance fluid calculation"
            }
        }