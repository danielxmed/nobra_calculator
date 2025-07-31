"""
SixMinuteWalk calculation models
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.models.shared import SexType

# 6 Minute Walk Distance Models
class SixMinuteWalkRequest(BaseModel):
    """
    Request model for 6-Minute Walk Distance calculation
    
    The 6-minute walk test (6MWT) is a standardized exercise test that assesses functional
    capacity and cardiopulmonary fitness, providing reference values for comparison.
    
    **Clinical Use**:
    - Functional capacity assessment
    - Cardiopulmonary disease monitoring
    - Pre-operative risk stratification
    - Pulmonary rehabilitation outcomes
    - Heart failure assessment
    - Disability evaluation
    - Treatment response monitoring
    
    **Test Protocol**:
    - 30-meter flat corridor
    - Patient walks at own pace for 6 minutes
    - Encouragement every 2 minutes
    - Oxygen saturation and symptoms monitored
    - Distance measured in meters
    
    **Reference**: ATS Committee on Proficiency Standards for Clinical Pulmonary Function Laboratories. ATS statement: guidelines for the six-minute walk test. Am J Respir Crit Care Med. 2002;166(1):111-7.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=100, 
        description="Patient's age in years. Age significantly affects predicted walking distance, with progressive decline expected with aging.",
        example=65
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Men typically have higher predicted walking distances than women due to differences in muscle mass and cardiovascular capacity.",
        example="male"
    )
    height: float = Field(
        ..., 
        ge=120.0, 
        le=220.0, 
        description="Patient's height in centimeters. Taller individuals typically have longer stride length and higher predicted distances.",
        example=175.0
    )
    weight: float = Field(
        ..., 
        ge=30.0, 
        le=200.0, 
        description="Patient's weight in kilograms. Higher weight may limit walking distance due to increased metabolic demand.",
        example=80.0
    )
    observed_distance: Optional[float] = Field(
        None, 
        ge=0.0, 
        le=1000.0, 
        description="Optional: Actual distance walked in meters during the 6MWT. If provided, percentage of predicted will be calculated for comparison with reference values.",
        example=450.0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "sex": "male",
                "height": 175.0,
                "weight": 80.0,
                "observed_distance": 450.0
            }
        }


class SixMinuteWalkResponse(BaseModel):
    """
    Response model for 6-Minute Walk Distance calculation
    
    Provides predicted walking distance with comprehensive functional capacity interpretation
    and comparison with age-, sex-, and anthropometry-matched reference values.
    
    **Interpretation Guidelines**:
    - >80% of predicted: Normal functional capacity
    - 60-80% of predicted: Mild functional limitation
    - 40-60% of predicted: Moderate functional limitation
    - <40% of predicted: Severe functional limitation
    
    **Clinical Significance**:
    - Distances <350m associated with increased mortality in heart failure
    - >50m improvement clinically significant in pulmonary rehabilitation
    - Lower limit of normal helps identify pathological reduction
    """
    result: float = Field(
        ..., 
        description="Predicted 6-minute walk distance in meters based on age, sex, height, and weight using validated reference equations.",
        example=485.3
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for walking distance",
        example="meters"
    )
    interpretation: str = Field(
        ..., 
        description="Comprehensive interpretation of functional capacity based on predicted values and observed performance if provided.",
        example="Distance within expected values for age, sex, height, and weight. Indicates preserved functional capacity."
    )
    stage: str = Field(
        ..., 
        description="Functional capacity classification (Normal, Mild Limitation, Moderate Limitation, Severe Limitation)",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the functional capacity level",
        example="Normal functional capacity"
    )
    lower_limit_normal: float = Field(
        ..., 
        description="Lower limit of normal walking distance in meters (typically predicted distance minus 1.96 × standard error). Values below this suggest pathological limitation.",
        example=332.3
    )
    percentage_predicted: Optional[float] = Field(
        None, 
        description="Percentage of predicted distance achieved (only calculated if observed distance is provided). Values >80% are typically considered normal.",
        example=92.7
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 485.3,
                "unit": "meters",
                "interpretation": "Distance within expected values for age, sex, height, and weight. Indicates preserved functional capacity.",
                "stage": "Normal",
                "stage_description": "Normal functional capacity",
                "lower_limit_normal": 332.3,
                "percentage_predicted": 92.7
            }
        }