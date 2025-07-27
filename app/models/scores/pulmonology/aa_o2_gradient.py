"""
AAO2Gradient calculation models
"""

from pydantic import BaseModel, Field
from typing import Optional
from app.models.shared import YesNoType

class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"



class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable responses"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"



# A-a O2 Gradient Models
class AAO2GradientRequest(BaseModel):
    """
    Request model for Alveolar-Arterial Oxygen Gradient calculation
    
    The A-a O₂ gradient assesses pulmonary gas exchange efficiency by comparing
    alveolar and arterial oxygen partial pressures, helping diagnose lung disease.
    
    **Clinical Use**:
    - Pulmonary gas exchange assessment
    - Differential diagnosis of hypoxemia
    - Monitoring lung disease progression
    - Ventilator management guidance
    - Pulmonary embolism evaluation
    - Interstitial lung disease assessment
    
    **Physiology**:
    - Normal gradient increases with age: ~2.5 + (0.21 × age)
    - Elevated gradient suggests V/Q mismatch, shunt, or diffusion limitation
    - Normal gradient with hypoxemia suggests hypoventilation or low FiO₂
    
    **Reference**: Mellemgaard K. The alveolar-arterial oxygen difference: its size and components in normal man. Acta Physiol Scand. 1966;67(1):10-20.
    """
    age: int = Field(
        ..., 
        ge=1, 
        le=120, 
        description="Patient's age in years. Age is crucial for interpreting A-a gradient as normal values increase with aging due to physiological changes in lung mechanics.",
        example=45
    )
    fio2: float = Field(
        ..., 
        ge=0.21, 
        le=1.0, 
        description="Fraction of inspired oxygen (0.21 for room air, up to 1.0 for 100% oxygen). Higher FiO₂ increases alveolar oxygen and affects gradient calculation.",
        example=0.21
    )
    paco2: float = Field(
        ..., 
        ge=10.0, 
        le=100.0, 
        description="Arterial carbon dioxide partial pressure in mmHg from arterial blood gas. Used to calculate alveolar oxygen pressure via the alveolar gas equation.",
        example=40.0
    )
    pao2: float = Field(
        ..., 
        ge=30.0, 
        le=600.0, 
        description="Arterial oxygen partial pressure in mmHg from arterial blood gas. This is subtracted from calculated alveolar oxygen to determine the gradient.",
        example=90.0
    )
    patm: Optional[float] = Field(
        760.0, 
        ge=500.0, 
        le=800.0, 
        description="Atmospheric pressure in mmHg. Standard is 760 mmHg at sea level, but adjustments needed for altitude (decreases ~19 mmHg per 1000 feet elevation).",
        example=760.0
    )
    respiratory_quotient: Optional[float] = Field(
        0.8, 
        ge=0.7, 
        le=1.0, 
        description="Respiratory quotient (CO₂ production/O₂ consumption ratio). Typically 0.8 on mixed diet, 0.7 on fat diet, 1.0 on carbohydrate diet.",
        example=0.8
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "fio2": 0.21,
                "paco2": 40.0,
                "pao2": 90.0,
                "patm": 760.0,
                "respiratory_quotient": 0.8
            }
        }


class AAO2GradientResponse(BaseModel):
    """
    Response model for Alveolar-Arterial Oxygen Gradient calculation
    
    Provides comprehensive pulmonary gas exchange assessment with age-adjusted
    interpretation and clinical guidance for hypoxemia evaluation.
    
    **Normal Values**:
    - Young adults (20-30 years): 5-10 mmHg
    - Middle age (40-50 years): 10-15 mmHg  
    - Elderly (>70 years): 15-25 mmHg
    - Formula: Expected A-a gradient = 2.5 + (0.21 × age)
    
    **Clinical Interpretation**:
    - Normal gradient + hypoxemia = hypoventilation or low FiO₂
    - Elevated gradient + hypoxemia = lung disease (V/Q mismatch, shunt, diffusion defect)
    - Massive elevation (>50 mmHg on room air) suggests severe lung pathology
    """
    result: float = Field(
        ..., 
        description="Calculated alveolar-arterial oxygen gradient in mmHg. Normal values increase with age, typically 5-10 mmHg in young adults, up to 25 mmHg in elderly.",
        example=15.2
    )
    unit: str = Field(
        ..., 
        description="Unit of measurement for the oxygen gradient",
        example="mmHg"
    )
    interpretation: str = Field(
        ..., 
        description="Clinical interpretation of the A-a gradient with age-adjusted normal values and assessment of pulmonary gas exchange efficiency.",
        example="Preserved alveolar function. Normal values for young adults are 5-10 mmHg, which may increase with age."
    )
    stage: str = Field(
        ..., 
        description="Gradient classification (Normal, Mildly Elevated, Moderately Elevated, Severely Elevated)",
        example="Normal"
    )
    stage_description: str = Field(
        ..., 
        description="Description of the A-a gradient status",
        example="Normal A-a gradient"
    )
    pao2_alveolar: float = Field(
        ..., 
        description="Calculated alveolar oxygen partial pressure in mmHg using the alveolar gas equation: PAO₂ = (FiO₂ × (Patm - 47)) - (PaCO₂ / RQ).",
        example=105.2
    )
    age_adjusted_normal: float = Field(
        ..., 
        description="Age-adjusted upper limit of normal A-a gradient in mmHg using the formula: 2.5 + (0.21 × age).",
        example=15.25
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 15.2,
                "unit": "mmHg",
                "interpretation": "Preserved alveolar function. Normal values for young adults are 5-10 mmHg, which may increase with age.",
                "stage": "Normal",
                "stage_description": "Normal A-a gradient",
                "pao2_alveolar": 105.2,
                "age_adjusted_normal": 15.25
            }
        }


# AAS Models
class YesNoType(str, Enum):
    """Enum for yes/no responses"""
    YES = "yes"
    NO = "no"


class YesNoNAType(str, Enum):
    """Enum for yes/no/not applicable responses"""
    YES = "yes"
    NO = "no"
    NOT_APPLICABLE = "not_applicable"