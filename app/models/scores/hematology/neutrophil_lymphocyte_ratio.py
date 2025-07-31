"""
Neutrophil-Lymphocyte Ratio (NLR) Calculator Models

Request and response models for Neutrophil-Lymphocyte Ratio calculation.

References (Vancouver style):
1. Zahorec R. Ratio of neutrophil to lymphocyte counts--rapid and simple parameter 
   of systemic inflammation and stress in critically ill. Bratisl Lek Listy. 
   2001;102(1):5-14.
2. Yang AP, Liu JP, Tao WQ, Li HM. The diagnostic and predictive role of NLR, 
   d-NLR and PLR in COVID-19 patients. Int Immunopharmacol. 2020 Jul;84:106504.

The Neutrophil-Lymphocyte Ratio (NLR) is a simple biomarker of systemic inflammation 
and physiological stress. It is calculated by dividing the absolute neutrophil count 
by the absolute lymphocyte count, or by using the respective percentages from a 
complete blood count (CBC) with differential.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Literal


class NeutrophilLymphocyteRatioRequest(BaseModel):
    """
    Request model for Neutrophil-Lymphocyte Ratio (NLR) Calculator
    
    The NLR is a readily available biomarker that reflects the balance between 
    neutrophil and lymphocyte levels in the blood. It serves as an indicator of:
    - Systemic inflammation
    - Physiological stress
    - Immune system activation
    - Disease severity and prognosis
    
    The ratio can be calculated using either:
    1. Absolute counts (cells/μL) from CBC with differential
    2. Percentage values if absolute counts are not available
    
    Normal NLR range: 1-3
    Interpretation:
    - Normal (1-3): No significant physiological stress
    - Mildly elevated (3-6): Low-level stress
    - Mild stress (6-9): Early infection or inflammation
    - Moderate stress (9-18): Significant infection or inflammation
    - Severe stress (>18): Critical illness, sepsis, or severe inflammation
    
    Important considerations:
    - Results can be affected by steroid use
    - May be skewed in hematologic disorders
    - HIV can cause chronic lymphopenia affecting the ratio
    - Should be interpreted in clinical context
    
    References (Vancouver style):
    1. Zahorec R. Ratio of neutrophil to lymphocyte counts--rapid and simple parameter 
       of systemic inflammation and stress in critically ill. Bratisl Lek Listy. 
       2001;102(1):5-14.
    2. Yang AP, Liu JP, Tao WQ, Li HM. The diagnostic and predictive role of NLR, 
       d-NLR and PLR in COVID-19 patients. Int Immunopharmacol. 2020 Jul;84:106504.
    """
    
    count_type: Literal["absolute", "percentage"] = Field(
        ...,
        description="Type of counts being provided. Use 'absolute' for cells/μL or 'percentage' for % from differential",
        example="absolute"
    )
    
    neutrophil_count: float = Field(
        ...,
        gt=0,
        description="Neutrophil count. If count_type is 'absolute': cells/μL (normal: 2000-7500). If 'percentage': % from differential (normal: 50-70%)",
        example=5000
    )
    
    lymphocyte_count: float = Field(
        ...,
        gt=0,
        description="Lymphocyte count. If count_type is 'absolute': cells/μL (normal: 1000-4000). If 'percentage': % from differential (normal: 20-40%). Must be >0 to avoid division by zero",
        example=2000
    )
    
    @field_validator('neutrophil_count')
    def validate_neutrophil_count(cls, v, values):
        """Validate neutrophil count based on count type"""
        if 'count_type' in values:
            if values['count_type'] == 'percentage' and v > 100:
                raise ValueError('Neutrophil percentage cannot exceed 100%')
            elif values['count_type'] == 'absolute' and v > 50000:
                raise ValueError('Neutrophil count seems too high (>50,000 cells/μL). Please verify.')
        return v
    
    @field_validator('lymphocyte_count')
    def validate_lymphocyte_count(cls, v, values):
        """Validate lymphocyte count based on count type"""
        if v <= 0:
            raise ValueError('Lymphocyte count must be greater than 0')
        if 'count_type' in values:
            if values['count_type'] == 'percentage' and v > 100:
                raise ValueError('Lymphocyte percentage cannot exceed 100%')
            elif values['count_type'] == 'absolute' and v > 50000:
                raise ValueError('Lymphocyte count seems too high (>50,000 cells/μL). Please verify.')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "count_type": "absolute",
                "neutrophil_count": 5000,
                "lymphocyte_count": 2000
            }
        }


class NeutrophilLymphocyteRatioResponse(BaseModel):
    """
    Response model for Neutrophil-Lymphocyte Ratio (NLR) Calculator
    
    The NLR provides a simple, readily available marker of physiological stress 
    that is more informative than white blood cell count alone. Higher values 
    generally correlate with:
    - Increased disease severity
    - Poorer prognosis
    - Higher mortality risk
    - Greater inflammatory burden
    
    The ratio can be trended over time to monitor:
    - Treatment response
    - Disease progression
    - Recovery from illness
    - Stress response resolution
    
    Reference: Zahorec R. Bratisl Lek Listy. 2001;102(1):5-14.
    """
    
    result: float = Field(
        ...,
        description="Calculated neutrophil-lymphocyte ratio",
        example=2.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement (always 'ratio' for NLR)",
        example="ratio"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the NLR with context and recommendations",
        example="NLR of 2.5 is within normal range (1-3), indicating no significant physiological stress. This is a reassuring finding suggesting adequate immune balance."
    )
    
    stage: str = Field(
        ...,
        description="Stress level category (Normal, Mildly Elevated, Mild Stress, Moderate Stress, or Severe Stress)",
        example="Normal"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the stress level",
        example="Normal NLR"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "ratio",
                "interpretation": "NLR of 2.5 is within normal range (1-3), indicating no significant physiological stress. This is a reassuring finding suggesting adequate immune balance.",
                "stage": "Normal",
                "stage_description": "Normal NLR"
            }
        }