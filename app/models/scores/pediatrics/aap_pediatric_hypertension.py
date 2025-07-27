"""
AapPediatricHypertension calculation models
"""

from pydantic import BaseModel, Field
from app.models.shared import SexType

# AAP Pediatric Hypertension Models
class AapPediatricHypertensionRequest(BaseModel):
    """
    Request model for AAP Pediatric Hypertension Classification
    
    The AAP 2017 guidelines provide updated blood pressure classification for children and
    adolescents, incorporating height percentiles and age-specific thresholds.
    
    **Clinical Use**:
    - Pediatric blood pressure classification
    - Hypertension screening in children
    - Risk stratification for cardiovascular complications
    - Treatment decision-making
    - Long-term cardiovascular risk assessment
    - School and sports physical evaluations
    
    **Classification System**:
    - Normal: <90th percentile for age, sex, and height
    - Elevated: 90th to <95th percentile or 120/80 to <95th percentile
    - Stage 1 HTN: 95th percentile to <95th percentile + 12 mmHg or 130/80-139/89 mmHg
    - Stage 2 HTN: ≥95th percentile + 12 mmHg or ≥140/90 mmHg
    
    **Reference**: Flynn JT, et al. Clinical Practice Guideline for Screening and Management of High Blood Pressure in Children and Adolescents. Pediatrics. 2017;140(3):e20171904.
    """
    age: int = Field(
        ..., 
        ge=1, 
        le=17, 
        description="Patient's age in years (1-17 years). Age is crucial for determining appropriate percentile-based thresholds.",
        example=10
    )
    sex: SexType = Field(
        ..., 
        description="Patient's biological sex. Sex-specific percentile tables are used for accurate BP classification in pediatric patients.",
        example="male"
    )
    height: float = Field(
        ..., 
        ge=70.0, 
        le=200.0, 
        description="Patient's height in centimeters. Height percentile is essential for determining BP percentiles as taller children have higher normal BP values.",
        example=140.0
    )
    systolic_bp: int = Field(
        ..., 
        ge=60, 
        le=200, 
        description="Systolic blood pressure in mmHg. Should be measured with appropriate cuff size and after 5 minutes of rest.",
        example=110
    )
    diastolic_bp: int = Field(
        ..., 
        ge=30, 
        le=150, 
        description="Diastolic blood pressure in mmHg. For children <13 years, use Korotkoff phase IV; for ≥13 years, use phase V.",
        example=70
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 10,
                "sex": "male",
                "height": 140.0,
                "systolic_bp": 110,
                "diastolic_bp": 70
            }
        }


class AapPediatricHypertensionResponse(BaseModel):
    """
    Response model for AAP Pediatric Hypertension Classification
    
    Provides comprehensive pediatric blood pressure assessment with age-, sex-, and 
    height-adjusted percentiles and evidence-based management recommendations.
    
    **Management Guidelines**:
    - Normal: Routine screening, lifestyle counseling
    - Elevated: Lifestyle modifications, repeat measurements, annual follow-up
    - Stage 1 HTN: Lifestyle modifications, consider medication if target organ damage
    - Stage 2 HTN: Lifestyle modifications + antihypertensive medication
    
    **Follow-up Recommendations**:
    - Normal/Elevated: Annual screening
    - Stage 1: 1-2 week follow-up, then 3-month intervals
    - Stage 2: 1 week follow-up, then monthly until controlled
    
    **Lifestyle Modifications**:
    - Weight management if overweight/obese
    - DASH diet principles
    - Regular physical activity (60 min/day)
    - Limit sodium intake
    - Adequate sleep duration
    """
    result: str = Field(
        ..., 
        description="Pediatric blood pressure classification based on AAP 2017 guidelines (Normal, Elevated, Stage 1 Hypertension, Stage 2 Hypertension).",
        example="Normal"
    )
    unit: str = Field(
        ..., 
        description="Unit of the classification result",
        example="classification"
    )
    interpretation: str = Field(
        ..., 
        description="Evidence-based clinical interpretation with specific management recommendations including lifestyle modifications and follow-up guidance.",
        example="BP below the 90th percentile for age, sex, and height. No specific intervention required."
    )
    stage: str = Field(
        ..., 
        description="Blood pressure stage classification according to AAP guidelines",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Detailed description of the blood pressure stage with clinical implications",
        example="Normal blood pressure"
    )
    systolic_percentile: float = Field(
        ..., 
        description="Systolic blood pressure percentile for age, sex, and height. Values help determine exact classification and tracking over time.",
        example=75.2
    )
    diastolic_percentile: float = Field(
        ..., 
        description="Diastolic blood pressure percentile for age, sex, and height. Used in conjunction with systolic percentile for classification.",
        example=68.5
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": "Normal",
                "unit": "classification",
                "interpretation": "BP below the 90th percentile for age, sex, and height. No specific intervention required.",
                "stage": "Normal",
                "stage_description": "Normal blood pressure",
                "systolic_percentile": 75.2,
                "diastolic_percentile": 68.5
            }
        }