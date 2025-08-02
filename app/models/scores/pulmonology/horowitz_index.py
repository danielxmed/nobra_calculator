"""
Horowitz Index for Lung Function (P/F Ratio) Models

Request and response models for Horowitz Index calculation.

References (Vancouver style):
1. Horovitz JH, Carrico CJ, Shires GT. Pulmonary response to major injury. 
   Arch Surg. 1974 Mar;108(3):349-55. doi: 10.1001/archsurg.1974.01350270079015.
2. Bernard GR, Artigas A, Brigham KL, Carlet J, Falke K, Hudson L, et al. 
   The American-European Consensus Conference on ARDS. Definitions, mechanisms, 
   relevant outcomes, and clinical trial coordination. Am J Respir Crit Care Med. 
   1994 Mar;149(3 Pt 1):818-24. doi: 10.1164/ajrccm.149.3.7509706.
3. ARDS Definition Task Force, Ranieri VM, Rubenfeld GD, Thompson BT, Ferguson ND, 
   Caldwell E, et al. Acute respiratory distress syndrome: the Berlin Definition. 
   JAMA. 2012 Jun 20;307(23):2526-33. doi: 10.1001/jama.2012.5669.

The Horowitz Index, also known as the P/F ratio or Carrico Index, is a widely used 
measure of lung function that assesses oxygenation status by calculating the ratio 
of arterial oxygen partial pressure (PaO2) to fraction of inspired oxygen (FiO2). 
It is particularly useful in critically ill patients and is a key component in 
diagnosing and stratifying the severity of acute respiratory distress syndrome (ARDS).
"""

from pydantic import BaseModel, Field, validator


class HorowitzIndexRequest(BaseModel):
    """
    Request model for Horowitz Index for Lung Function (P/F Ratio)
    
    The Horowitz Index requires two parameters:
    
    1. PaO2 (Partial pressure of oxygen in arterial blood):
    - Obtained from arterial blood gas (ABG) analysis
    - Normal range at sea level: 75-100 mmHg
    - Measured in mmHg
    
    2. FiO2 (Fraction of inspired oxygen):
    - Must be expressed as a decimal fraction, NOT percentage
    - Room air = 0.21 (21%)
    - 100% oxygen = 1.0
    - Range: 0.21-1.0
    
    The P/F ratio formula: PaO2 / FiO2
    
    Normal P/F ratio at sea level is typically 400-500 mmHg.

    References (Vancouver style):
    1. Horovitz JH, Carrico CJ, Shires GT. Pulmonary response to major injury. 
    Arch Surg. 1974 Mar;108(3):349-55.
    2. ARDS Definition Task Force. Acute respiratory distress syndrome: the Berlin 
    Definition. JAMA. 2012;307(23):2526-33.
    """
    
    pao2: float = Field(
        ...,
        description="Partial pressure of oxygen in arterial blood from ABG in mmHg. "
                    "Valid range: 10-700 mmHg",
        ge=10,
        le=700,
        example=75
    )
    
    fio2: float = Field(
        ...,
        description="Fraction of inspired oxygen as decimal (NOT percentage). "
                    "Room air = 0.21, 100% oxygen = 1.0. Valid range: 0.21-1.0",
        ge=0.21,
        le=1.0,
        example=0.5
    )
    
    @validator('fio2')
    def validate_fio2_format(cls, v):
        """Ensure FiO2 is in fraction format, not percentage"""
        if v > 1.0:
            raise ValueError("FiO2 must be expressed as a fraction (0.21-1.0), not percentage. "
                           "For example, use 0.5 for 50% oxygen, not 50.")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "pao2": 75,
                "fio2": 0.5
            }
        }


class HorowitzIndexResponse(BaseModel):
    """
    Response model for Horowitz Index for Lung Function (P/F Ratio)
    
    The P/F ratio interpretation according to Berlin Definition:
    - >400: Normal lung function
    - 300-400: Mild impairment (not ARDS)
    - 200-300: Mild ARDS (27% mortality)
    - 100-200: Moderate ARDS (32% mortality)
    - ≤100: Severe ARDS (45% mortality)
    
    Note: The Berlin Definition also requires PEEP ≥5 cm H2O for ARDS diagnosis.
    
    Reference: ARDS Definition Task Force. JAMA. 2012;307(23):2526-33.
    """
    
    result: float = Field(
        ...,
        description="P/F ratio (Horowitz Index) calculated as PaO2/FiO2 in mmHg",
        example=150.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the P/F ratio",
        example="mmHg"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on the P/F ratio and Berlin criteria",
        example="Moderate ARDS according to Berlin criteria. Associated with approximately "
                "32% mortality. Implement lung protective ventilation and consider prone positioning."
    )
    
    stage: str = Field(
        ...,
        description="Severity category (Normal, Mild Impairment, Mild ARDS, Moderate ARDS, Severe ARDS)",
        example="Moderate ARDS"
    )
    
    stage_description: str = Field(
        ...,
        description="P/F ratio range for the severity category",
        example="P/F ratio 100-200"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 150.0,
                "unit": "mmHg",
                "interpretation": "Moderate ARDS according to Berlin criteria. Associated with "
                                "approximately 32% mortality. Implement lung protective ventilation "
                                "and consider prone positioning.",
                "stage": "Moderate ARDS",
                "stage_description": "P/F ratio 100-200"
            }
        }