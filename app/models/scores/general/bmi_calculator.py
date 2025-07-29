"""
BMI Calculator (Body Mass Index and BSA) Models

Request and response models for BMI and BSA calculation.

References (Vancouver style):
1. World Health Organization. Obesity: preventing and managing the global epidemic. 
   Report of a WHO consultation. World Health Organ Tech Rep Ser. 2000;894:i-xii, 1-253.
2. Mosteller RD. Simplified calculation of body-surface area. N Engl J Med. 1987 Oct 22;317(17):1098. 
   doi: 10.1056/NEJM198710223171717.
3. National Institutes of Health. Clinical Guidelines on the Identification, Evaluation, 
   and Treatment of Overweight and Obesity in Adults--The Evidence Report. Obes Res. 1998 Sep;6 Suppl 2:51S-209S.
4. Rubino F, Puhl RM, Cummings DE, et al. Joint international consensus statement for ending stigma of obesity. 
   Nat Med. 2020 Apr;26(4):485-497. doi: 10.1038/s41591-020-0803-x.

The BMI Calculator computes Body Mass Index and Body Surface Area using validated medical formulas. 
BMI serves as a screening tool for weight-related health risks and is defined as weight in kilograms 
divided by the square of height in meters. The calculation provides classification according to WHO 
standards ranging from underweight to obese classes.

BSA is calculated using the Mosteller formula, which is widely used in clinical practice for 
medication dosing (particularly chemotherapy) and cardiac index calculations. The formula is: 
BSA (m²) = √[height (cm) × weight (kg) / 3600].

Both measurements are essential tools in clinical practice, though they should be interpreted 
alongside other assessments including waist circumference, body composition analysis, and 
overall clinical evaluation.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any


class BmiCalculatorRequest(BaseModel):
    """
    Request model for BMI Calculator (Body Mass Index and BSA)
    
    This calculator computes two fundamental anthropometric measurements used extensively 
    in clinical practice:
    
    **Body Mass Index (BMI):**
    A measure of body mass relative to height, calculated as weight in kilograms divided 
    by the square of height in meters (kg/m²). BMI serves as a screening tool for 
    weight-related health risks and provides standardized classification according to 
    World Health Organization guidelines.
    
    **BMI Classification (WHO Standards):**
    - **Underweight**: <18.5 kg/m² - May indicate malnutrition or underlying conditions
    - **Normal weight**: 18.5-24.9 kg/m² - Healthy weight range with lowest health risks
    - **Overweight**: 25.0-29.9 kg/m² - Increased risk of cardiovascular and metabolic diseases
    - **Obese Class 1**: 30.0-34.9 kg/m² - Moderate obesity requiring medical intervention
    - **Obese Class 2**: 35.0-39.9 kg/m² - Severe obesity with high complication risk
    - **Obese Class 3**: ≥40.0 kg/m² - Extreme obesity requiring intensive treatment
    
    **Body Surface Area (BSA):**
    An estimate of the total surface area of the human body, calculated using the 
    Mosteller formula: BSA (m²) = √[height (cm) × weight (kg) / 3600]. BSA is more 
    accurate than weight alone for many physiological and pharmacological calculations.
    
    **Clinical Applications:**
    
    **BMI Applications:**
    - Population health screening and epidemiological studies
    - Risk assessment for cardiovascular disease, diabetes, and metabolic syndrome
    - Surgical risk stratification and anesthesia planning
    - Insurance and clinical guideline assessments
    - Public health policy development and intervention targeting
    
    **BSA Applications:**
    - Chemotherapy and oncology drug dosing (most common use)
    - Cardiac index calculations (cardiac output/BSA)
    - Physiological research and metabolic studies
    - Some medication dosing in pediatrics and critical care
    - Burn treatment surface area calculations
    
    **Important Limitations:**
    
    **BMI Limitations:**
    - Does not distinguish between muscle mass and fat mass
    - May overestimate body fat in highly muscular individuals (athletes)
    - May underestimate body fat in older adults with reduced muscle mass
    - Less accurate in certain ethnic populations (different thresholds may apply)
    - Does not account for fat distribution (central vs. peripheral obesity)
    
    **BSA Limitations:**
    - Less accurate at extremes of height and weight
    - May not be appropriate for all medications with narrow therapeutic indices
    - Different formulas (Mosteller, Du Bois, Haycock) may yield different results
    - Not validated for all patient populations and clinical scenarios
    
    **Clinical Interpretation Guidelines:**
    - BMI should be used in conjunction with other assessments including waist circumference
    - Consider ethnic-specific BMI thresholds when appropriate
    - Evaluate clinical context including muscle mass, age, and comorbidities
    - BSA-based dosing should be verified against weight-based dosing when appropriate
    - Both measurements require clinical judgment and should not be used in isolation
    
    References (Vancouver style):
    1. World Health Organization. Obesity: preventing and managing the global epidemic. 
    Report of a WHO consultation. World Health Organ Tech Rep Ser. 2000;894:i-xii, 1-253.
    2. Mosteller RD. Simplified calculation of body-surface area. N Engl J Med. 1987 Oct 22;317(17):1098. 
    doi: 10.1056/NEJM198710223171717.
    3. National Institutes of Health. Clinical Guidelines on the Identification, Evaluation, 
    and Treatment of Overweight and Obesity in Adults--The Evidence Report. Obes Res. 1998 Sep;6 Suppl 2:51S-209S.
    4. Rubino F, Puhl RM, Cummings DE, et al. Joint international consensus statement for ending stigma of obesity. 
    Nat Med. 2020 Apr;26(4):485-497. doi: 10.1038/s41591-020-0803-x.
    """
    
    weight: float = Field(
        ...,
        ge=0.5,
        le=500,
        description="Patient weight in kilograms. Range: 0.5-500 kg to accommodate pediatric to adult populations",
        example=70.0
    )
    
    height: float = Field(
        ...,
        ge=30,
        le=250,
        description="Patient height in centimeters. Range: 30-250 cm to accommodate pediatric to adult populations",
        example=175.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "weight": 70.0,
                "height": 175.0
            }
        }


class BmiCalculatorResponse(BaseModel):
    """
    Response model for BMI Calculator (Body Mass Index and BSA)
    
    Returns calculated BMI and BSA values with comprehensive clinical interpretation 
    based on established medical guidelines.
    
    **BMI Interpretation:**
    Results are classified according to World Health Organization standards with 
    specific recommendations for each category. The interpretation includes health 
    risk assessment and clinical management recommendations.
    
    **BSA Clinical Application:**
    Body surface area results are provided for use in medication dosing calculations, 
    particularly for chemotherapy agents and cardiac index measurements.
    
    **Result Components:**
    - **BMI**: Calculated value in kg/m² with one decimal precision
    - **BSA**: Calculated value in m² with two decimal precision using Mosteller formula
    - **Height in meters**: Converted height for reference
    - **Weight**: Input weight for verification
    
    **Clinical Context:**
    Results should be interpreted within the broader clinical context including patient 
    age, sex, ethnicity, muscle mass, and comorbidity profile. BMI categories may require 
    adjustment for certain populations, and BSA calculations should be verified for 
    critical applications.
    
    Reference: World Health Organization. Obesity guidelines. 2000.
    """
    
    result: Dict[str, Any] = Field(
        ...,
        description="BMI and BSA calculation results including values and measurements",
        example={
            "bmi": 22.9,
            "bsa": 1.85,
            "height_meters": 1.75,
            "weight_kg": 70.0
        }
    )
    
    unit: str = Field(
        ...,
        description="Units of measurement for the calculated values",
        example="BMI: kg/m², BSA: m²"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with BMI classification, BSA applications, and medical recommendations",
        example="BMI: 22.9 kg/m² (Normal weight). BSA: 1.85 m² (Mosteller formula). Height: 1.75 m, Weight: 70.0 kg. Healthy weight range. Associated with lowest risk of weight-related health problems. Continue current lifestyle and eating habits. BSA is used for medication dosing calculations (especially chemotherapy) and cardiac index measurements. BMI should be interpreted alongside other clinical assessments including waist circumference and body composition."
    )
    
    stage: str = Field(
        ...,
        description="BMI weight classification category",
        example="Normal weight"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the BMI classification",
        example="BMI 18.5-24.9"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": {
                    "bmi": 22.9,
                    "bsa": 1.85,
                    "height_meters": 1.75,
                    "weight_kg": 70.0
                },
                "unit": "BMI: kg/m², BSA: m²",
                "interpretation": "BMI: 22.9 kg/m² (Normal weight). BSA: 1.85 m² (Mosteller formula). Height: 1.75 m, Weight: 70.0 kg. Healthy weight range. Associated with lowest risk of weight-related health problems. Continue current lifestyle and eating habits. BSA is used for medication dosing calculations (especially chemotherapy) and cardiac index measurements. BMI should be interpreted alongside other clinical assessments including waist circumference and body composition.",
                "stage": "Normal weight",
                "stage_description": "BMI 18.5-24.9"
            }
        }