"""
Mentzer Index Models

Request and response models for Mentzer Index calculation.

References (Vancouver style):
1. Mentzer WC Jr. Differentiation of iron deficiency from thalassaemia trait. 
   Lancet. 1973 Apr 21;1(7808):882. doi: 10.1016/s0140-6736(73)91446-3.
2. Vehapoglu A, Ozgurhan G, Demir AD, Uzuner S, Nursoy MA, Turkmen S, et al. 
   Hematological indices for differential diagnosis of Beta thalassemia trait 
   and iron deficiency anemia. Anemia. 2014;2014:576738. doi: 10.1155/2014/576738.
3. Zaghloul A, Al-Bukhari TAMA, Bajuaifer N, Shalaby M, Al-Pakistani HA, 
   Halawani SH, et al. Introduction of new formulas and evaluation of the 
   previous red blood cell indices and formulas in the differentiation between 
   beta thalassemia trait and iron deficiency anemia in the Makkah region. 
   Hematology. 2016 Jul;21(6):351-8. doi: 10.1080/10245332.2015.1133753.

The Mentzer Index is a simple screening tool that uses the ratio of MCV to RBC count 
to differentiate between beta thalassemia trait and iron deficiency anemia, two common 
causes of microcytic anemia. The index was first described in 1973 and remains widely 
used due to its simplicity and effectiveness as an initial screening tool.
"""

from pydantic import BaseModel, Field, validator


class MentzerIndexRequest(BaseModel):
    """
    Request model for Mentzer Index calculation
    
    The Mentzer Index differentiates beta thalassemia trait from iron deficiency anemia 
    using a simple ratio of Mean Corpuscular Volume (MCV) to Red Blood Cell (RBC) count.
    
    Formula: Mentzer Index = MCV (fL) / RBC count (10⁶/µL)
    
    Pathophysiology:
    - Beta Thalassemia Trait: Normal RBC production but cells are smaller and more fragile
      → Normal RBC count, Low MCV → Low Mentzer Index (<13)
    - Iron Deficiency Anemia: Reduced RBC production and small cells
      → Low RBC count, Low MCV → High Mentzer Index (>13)
    
    Clinical Context:
    This index serves as a screening tool for patients with microcytic anemia (low MCV).
    While definitive diagnosis requires hemoglobin electrophoresis and iron studies,
    the Mentzer Index provides a quick initial assessment to guide further testing.
    
    Performance Characteristics:
    - Sensitivity for beta thalassemia trait: 74-98.7% (varies by study)
    - Specificity for beta thalassemia trait: 63-82.3% (varies by study)
    
    References (Vancouver style):
    1. Mentzer WC Jr. Differentiation of iron deficiency from thalassaemia trait. 
       Lancet. 1973 Apr 21;1(7808):882. doi: 10.1016/s0140-6736(73)91446-3.
    """
    
    mcv: float = Field(
        ...,
        description="Mean Corpuscular Volume - the average volume of red blood cells. "
                    "Normal range is typically 80-100 fL. In microcytic anemias, MCV is "
                    "reduced (<80 fL). This value is obtained from a complete blood count (CBC).",
        ge=0,
        le=200,
        example=65.0
    )
    
    rbc_count: float = Field(
        ...,
        description="Red Blood Cell count in millions per microliter (10⁶/µL). Normal range "
                    "is typically 4.0-6.0 × 10⁶/µL for adults. In iron deficiency anemia, "
                    "this count is often reduced, while in beta thalassemia trait it tends "
                    "to be normal or even elevated. Obtained from a complete blood count (CBC).",
        ge=0.001,
        le=15,
        example=5.5
    )
    
    @validator('mcv')
    def validate_mcv(cls, v):
        """Validate MCV is within reasonable physiological range"""
        if v <= 0:
            raise ValueError("MCV must be greater than 0")
        if v > 200:
            raise ValueError("MCV must be less than or equal to 200 fL")
        return v
    
    @validator('rbc_count')
    def validate_rbc_count(cls, v):
        """Validate RBC count is within reasonable physiological range"""
        if v < 0.001:
            raise ValueError("RBC count must be at least 0.001 × 10⁶/µL")
        if v > 15:
            raise ValueError("RBC count must be less than or equal to 15 × 10⁶/µL")
        return v
    
    class Config:
        schema_extra = {
            "example": {
                "mcv": 65.0,
                "rbc_count": 5.5
            }
        }


class MentzerIndexResponse(BaseModel):
    """
    Response model for Mentzer Index calculation
    
    The Mentzer Index provides a quick screening tool to differentiate between beta 
    thalassemia trait and iron deficiency anemia:
    
    - Index < 13: Suggests beta thalassemia trait
    - Index = 13: Indeterminate result
    - Index > 13: Suggests iron deficiency anemia
    
    Important Limitations:
    - This is a screening tool only and should not be used for definitive diagnosis
    - Results can be affected by concurrent conditions (e.g., combined iron deficiency 
      and thalassemia trait)
    - False results may occur in other conditions causing microcytosis
    - Confirmatory testing with iron studies and hemoglobin electrophoresis is essential
    
    Reference: Mentzer WC Jr. Lancet. 1973;1(7808):882.
    """
    
    result: float = Field(
        ...,
        description="The calculated Mentzer Index value (MCV/RBC count). Values <13 suggest "
                    "beta thalassemia trait, while values >13 suggest iron deficiency anemia.",
        example=11.8
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the index (dimensionless ratio)",
        example=""
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of the index value, including likely diagnosis "
                    "and recommended confirmatory testing",
        example="Beta thalassemia trait is more likely. In thalassemia, RBC production is "
                "normal but cells are smaller and more fragile, resulting in normal RBC "
                "count with low MCV. Consider hemoglobin electrophoresis for confirmation."
    )
    
    stage: str = Field(
        ...,
        description="Diagnostic category based on the index value",
        example="Beta Thalassemia Trait Likely"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the index range",
        example="Index < 13"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 11.8,
                "unit": "",
                "interpretation": "Beta thalassemia trait is more likely. In thalassemia, RBC "
                                "production is normal but cells are smaller and more fragile, "
                                "resulting in normal RBC count with low MCV. Consider hemoglobin "
                                "electrophoresis for confirmation.",
                "stage": "Beta Thalassemia Trait Likely",
                "stage_description": "Index < 13"
            }
        }