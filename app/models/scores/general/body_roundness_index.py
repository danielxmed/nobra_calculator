"""
Body Roundness Index (BRI) Models

Request and response models for BRI calculation.

References (Vancouver style):
1. Thomas DM, Bredlau C, Bosy-Westphal A, Mueller M, Shen W, Gallagher D, et al. 
   Relationships between body roundness with body fat and visceral adipose tissue 
   emerging from a new geometrical model. Obesity (Silver Spring). 2013 Nov;21(11):2264-71. 
   doi: 10.1002/oby.20408.
2. Zhang X, Ma N, Lin Q, Chen K, Zheng F, Wu J, et al. Body Roundness Index and 
   All-Cause Mortality Among US Adults. JAMA Netw Open. 2024 Jun 3;7(6):e2415051. 
   doi: 10.1001/jamanetworkopen.2024.15051.
3. Chang Y, Guo X, Chen Y, Guo L, Li Z, Yu S, et al. A body shape index and body 
   roundness index: two new body indices to identify diabetes mellitus among rural 
   populations in northeast China. BMC Public Health. 2015 Aug 19;15:794. 
   doi: 10.1186/s12889-015-2150-2.

The Body Roundness Index (BRI) is a geometric assessment of body shape based on the 
principle of body eccentricity. It estimates body fat percentage and visceral adipose 
tissue using only waist circumference and height measurements. Unlike BMI, BRI accounts 
for central adiposity and has shown superior predictive ability for cardiometabolic 
risk and all-cause mortality. The index demonstrates a U-shaped mortality curve, with 
both very low and very high values associated with increased mortality risk.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class BodyRoundnessIndexRequest(BaseModel):
    """
    Request model for Body Roundness Index (BRI)
    
    The BRI is calculated using a mathematical formula based on the geometric principle 
    of body eccentricity. It models the human body as an ellipse to estimate body fat 
    and visceral adipose tissue distribution.
    
    **Measurement Guidelines:**
    
    **Waist Circumference:**
    - Measured at the level of the umbilicus (navel)
    - Patient should be standing with feet together
    - Arms should be at the sides
    - Measurement taken at the end of normal expiration
    - Tape measure should be snug but not compressing the skin
    - Parallel to the floor
    
    **Height:**
    - Measured without shoes
    - Standing against a wall or stadiometer
    - Head in Frankfurt plane (looking straight ahead)
    - Heels together, touching the wall
    
    **Clinical Applications:**
    
    **Metabolic Risk Assessment:**
    - BRI correlates with insulin resistance and diabetes risk
    - Better predictor than BMI for metabolic syndrome
    - Accounts for visceral adiposity distribution
    
    **Cardiovascular Risk:**
    - Associated with hypertension and dyslipidemia
    - Predicts cardiovascular events
    - U-shaped curve for mortality risk
    
    **Body Composition:**
    - Estimates percentage body fat
    - Correlates with DEXA scan measurements
    - Reflects central obesity patterns
    
    **Advantages over BMI:**
    - Accounts for body shape, not just weight
    - Better correlation with visceral fat
    - More accurate in muscular individuals
    - Considers fat distribution patterns
    
    **Limitations:**
    - Relatively new index requiring validation
    - May not apply equally to all ethnicities
    - Does not differentiate muscle from fat mass
    - Requires accurate waist measurement
    
    References (Vancouver style):
    1. Thomas DM, Bredlau C, Bosy-Westphal A, Mueller M, Shen W, Gallagher D, et al. 
    Relationships between body roundness with body fat and visceral adipose tissue 
    emerging from a new geometrical model. Obesity (Silver Spring). 2013 Nov;21(11):2264-71. 
    doi: 10.1002/oby.20408.
    2. Zhang X, Ma N, Lin Q, Chen K, Zheng F, Wu J, et al. Body Roundness Index and 
    All-Cause Mortality Among US Adults. JAMA Netw Open. 2024 Jun 3;7(6):e2415051. 
    doi: 10.1001/jamanetworkopen.2024.15051.
    """
    
    waist_circumference: float = Field(
        ...,
        ge=40,
        le=200,
        description="Waist circumference in centimeters, measured at the level of the umbilicus (navel). Normal range typically 60-120 cm for adults.",
        example=85.0
    )
    
    height: float = Field(
        ...,
        ge=100,
        le=250,
        description="Height in centimeters, measured without shoes. Typical adult range 150-200 cm.",
        example=175.0
    )
    
    class Config:
        schema_extra = {
            "example": {
                "waist_circumference": 85.0,
                "height": 175.0
            }
        }


class BodyRoundnessIndexResponse(BaseModel):
    """
    Response model for Body Roundness Index (BRI)
    
    The BRI value represents the degree of body roundness, with higher values 
    indicating a more spherical body shape and increased health risks. The index 
    typically ranges from 1 to 20, with most adults falling between 3 and 7.
    
    **Interpretation Guidelines:**
    
    **BRI < 3.41 (Low):**
    - May indicate lower body fat
    - Paradoxically associated with moderate mortality risk
    - Consider assessment for malnutrition or muscle wasting
    - HR 0.57 (95% CI 0.49-0.67) vs reference
    
    **BRI 3.41-4.45 (Below Average):**
    - Generally favorable body composition
    - No significant increase in health risks
    - HR 0.81 (95% CI 0.69-0.95) vs reference
    
    **BRI 4.45-5.46 (Average/Reference):**
    - Reference range for mortality comparisons
    - Low risk for visceral obesity complications
    - Baseline hazard ratio (HR 1.0)
    
    **BRI 5.46-6.91 (Above Average):**
    - Increased body roundness and health risks
    - Consider lifestyle interventions
    - HR 1.48 (95% CI 1.30-1.69) vs reference
    
    **BRI ≥6.91 (High):**
    - Significantly increased health risks
    - Strong recommendation for intervention
    - HR 1.62 (95% CI 1.42-1.85) vs reference
    
    **Clinical Decision Making:**
    
    **Risk Stratification:**
    - Use alongside other metabolic markers
    - Consider family history and comorbidities
    - Account for age and ethnicity factors
    
    **Intervention Thresholds:**
    - BRI >5.46: Consider lifestyle counseling
    - BRI >6.91: Aggressive risk factor modification
    - Monitor trends over time
    
    **Follow-up Recommendations:**
    - Low/High BRI: Reassess in 6 months
    - Average BRI: Annual screening
    - Track changes with interventions
    
    Reference: Zhang X, et al. JAMA Netw Open. 2024;7(6):e2415051.
    """
    
    result: float = Field(
        ...,
        description="Body Roundness Index value, typically ranging from 1 to 20",
        example=4.85
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for BRI",
        example="index"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the BRI value with risk assessment",
        example="BRI between 4.45-5.46 represents the reference range for average body roundness. This is used as the baseline for mortality risk comparisons (HR 1.0). Generally indicates low risk for health problems related to visceral obesity."
    )
    
    stage: str = Field(
        ...,
        description="BRI category (Low, Below Average, Average, Above Average, High)",
        example="Average BRI"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BRI category",
        example="Average body roundness (reference)"
    )
    
    additional_metrics: Dict[str, Any] = Field(
        None,
        description="Additional calculated metrics including waist-to-height ratio and eccentricity",
        example={
            "waist_to_height_ratio": 0.486,
            "eccentricity": 0.9856
        }
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4.85,
                "unit": "index",
                "interpretation": "BRI between 4.45-5.46 represents the reference range for average body roundness. This is used as the baseline for mortality risk comparisons (HR 1.0). Generally indicates low risk for health problems related to visceral obesity.",
                "stage": "Average BRI",
                "stage_description": "Average body roundness (reference)",
                "additional_metrics": {
                    "waist_to_height_ratio": 0.486,
                    "eccentricity": 0.9856
                }
            }
        }