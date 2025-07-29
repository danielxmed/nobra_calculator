"""
BeAM Value Models

Request and response models for BeAM Value calculation.

References (Vancouver style):
1. Raz I, Wilson PW, Strojek K, Kowalska I, Bozikov V, Gitt AK, et al. Effects of 
   prandial versus fasting glycemia on cardiovascular outcomes in type 2 diabetes: 
   the HEART2D trial. Diabetes Care. 2009 Mar;32(3):381-6.
2. Blonde L, Merilainen M, Karwe V, Raskin P; TITRATE Study Group. Patient-directed 
   titration for achieving glycaemic goals using a once-daily basal insulin analogue: 
   an assessment of two different fasting plasma glucose targets - the TITRATE study. 
   Diabetes Obes Metab. 2009 Jun;11(6):623-31.
3. Garber AJ, King AB, Del Prato S, Sreenan S, Balci MK, Muñoz-Torres M, et al. 
   Insulin degludec, an ultra-longacting basal insulin, versus insulin glargine in 
   basal-bolus treatment with mealtime insulin aspart in type 2 diabetes (BEGIN 
   Basal-Bolus Type 2): a phase 3, randomised, open-label, treat-to-target 
   non-inferiority trial. Lancet. 2012 Apr 21;379(9825):1498-507.

The BeAM Value calculates the difference between bedtime and morning fasting blood glucose 
to guide prandial insulin therapy decisions in patients with type 2 diabetes. A high BeAM 
value (≥30 mg/dL) indicates the need for prandial insulin supplementation, while a negative 
BeAM value is a contraindication for intensification of prandial insulin therapy.
"""

from pydantic import BaseModel, Field


class BeamValueRequest(BaseModel):
    """
    Request model for BeAM Value calculation
    
    The BeAM Value is calculated as: Bedtime glucose - Morning fasting glucose
    
    Clinical Context:
    The BeAM value helps identify patients with type 2 diabetes using basal insulin 
    who need targeting of postprandial control rather than advancing basal insulin dose.
    
    Interpretation Guidelines:
    - High BeAM (≥30 mg/dL): Indicates postprandial glucose excursions and need for 
      prandial insulin supplementation
    - Medium/Low BeAM (0-29 mg/dL): Prandial insulin may be of little benefit; 
      focus on basal insulin optimization
    - Negative BeAM (<0 mg/dL): Contraindication for prandial insulin intensification; 
      suggests dawn phenomenon or inadequate basal insulin coverage
    
    References (Vancouver style):
    1. Raz I, Wilson PW, Strojek K, Kowalska I, Bozikov V, Gitt AK, et al. Effects of 
    prandial versus fasting glycemia on cardiovascular outcomes in type 2 diabetes: 
    the HEART2D trial. Diabetes Care. 2009 Mar;32(3):381-6.
    2. Blonde L, Merilainen M, Karwe V, Raskin P; TITRATE Study Group. Patient-directed 
    titration for achieving glycaemic goals using a once-daily basal insulin analogue: 
    an assessment of two different fasting plasma glucose targets - the TITRATE study. 
    Diabetes Obes Metab. 2009 Jun;11(6):623-31.
    3. Garber AJ, King AB, Del Prato S, Sreenan S, Balci MK, Muñoz-Torres M, et al. 
    Insulin degludec, an ultra-longacting basal insulin, versus insulin glargine in 
    basal-bolus treatment with mealtime insulin aspart in type 2 diabetes (BEGIN 
    Basal-Bolus Type 2): a phase 3, randomised, open-label, treat-to-target 
    non-inferiority trial. Lancet. 2012 Apr 21;379(9825):1498-507.
    """
    
    bedtime_glucose: float = Field(
        ...,
        description="Bedtime blood glucose level (SMBG measurement taken before sleep). Should be measured consistently at the same time each night",
        ge=40,
        le=600,
        example=180.0
    )
    
    morning_glucose: float = Field(
        ...,
        description="Morning fasting blood glucose level (SMBG measurement taken before breakfast after overnight fast). Should be measured consistently upon waking",
        ge=40,
        le=600,
        example=120.0
    )
    
    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "title": "High BeAM Value (indicates need for prandial insulin)",
                    "value": {
                        "bedtime_glucose": 200.0,
                        "morning_glucose": 140.0
                    }
                },
                {
                    "title": "Medium BeAM Value (prandial insulin may not be beneficial)",
                    "value": {
                        "bedtime_glucose": 160.0,
                        "morning_glucose": 145.0
                    }
                },
                {
                    "title": "Negative BeAM Value (contraindication for prandial insulin)",
                    "value": {
                        "bedtime_glucose": 140.0,
                        "morning_glucose": 160.0
                    }
                }
            ]
        }


class BeamValueResponse(BaseModel):
    """
    Response model for BeAM Value calculation
    
    Returns the calculated BeAM value with detailed clinical interpretation including:
    - Classification (High BeAM ≥30 mg/dL, Medium/Low BeAM 0-29 mg/dL, Negative BeAM <0 mg/dL)
    - Clinical recommendations for insulin therapy management
    - Guidance on whether to add prandial insulin or optimize basal insulin
    
    The BeAM value helps clinicians decide between advancing basal insulin dose or 
    adding prandial insulin therapy in patients with type 2 diabetes.
    
    Reference: The BeAM value described in clinical studies is a simple, easy-to-calculate 
    value that may identify patients with T2DM using basal insulin that need targeting of 
    postprandial control rather than advancing basal insulin dose.
    """
    
    result: float = Field(
        ...,
        description="BeAM value calculated as bedtime glucose minus morning glucose (mg/dL)",
        example=60.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the BeAM value",
        example="mg/dL"
    )
    
    interpretation: str = Field(
        ...,
        description="Detailed clinical interpretation including BeAM category, clinical significance, and management recommendations",
        example="BeAM value: 60.0 mg/dL (bedtime 200.0 mg/dL - morning 140.0 mg/dL). High BeAM value (≥30 mg/dL) suggests postprandial glucose excursions during the day leading to high bedtime glucose and well-controlled fasting glucose. This is an indicator for prandial insulin supplementation rather than advancing basal insulin dose. Clinical recommendation: Consider adding rapid-acting insulin before meals to target postprandial hyperglycemia. Monitor HbA1c and adjust therapy accordingly. The BeAM value helps identify patients who would benefit from targeting postprandial control rather than continuing to increase basal insulin."
    )
    
    stage: str = Field(
        ...,
        description="BeAM value category (High BeAM, Medium/Low BeAM, or Negative BeAM)",
        example="High BeAM"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BeAM category with threshold information",
        example="Large BeAM value (≥30 mg/dL)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 60.0,
                "unit": "mg/dL",
                "interpretation": "BeAM value: 60.0 mg/dL (bedtime 200.0 mg/dL - morning 140.0 mg/dL). High BeAM value (≥30 mg/dL) suggests postprandial glucose excursions during the day leading to high bedtime glucose and well-controlled fasting glucose. This is an indicator for prandial insulin supplementation rather than advancing basal insulin dose. Clinical recommendation: Consider adding rapid-acting insulin before meals to target postprandial hyperglycemia. Monitor HbA1c and adjust therapy accordingly. The BeAM value helps identify patients who would benefit from targeting postprandial control rather than continuing to increase basal insulin.",
                "stage": "High BeAM",
                "stage_description": "Large BeAM value (≥30 mg/dL)"
            }
        }