"""
HOMA-IR (Homeostatic Model Assessment for Insulin Resistance) Models

Request and response models for HOMA-IR calculation.

References (Vancouver style):
1. Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. 
   Homeostasis model assessment: insulin resistance and beta-cell function from 
   fasting plasma glucose and insulin concentrations in man. Diabetologia. 
   1985 Jul;28(7):412-9. doi: 10.1007/BF00280883.
2. Tohidi M, Ghasemi A, Hadaegh F, Derakhshan A, Chary A, Azizi F. Age- and 
   sex-specific reference values for fasting serum insulin levels and insulin 
   resistance/sensitivity indices in healthy Iranian adults: Tehran Lipid and 
   Glucose Study. Clin Biochem. 2014 Apr;47(6):432-8. 
   doi: 10.1016/j.clinbiochem.2014.02.007.

The HOMA-IR is a simple, non-invasive method to quantify insulin resistance using 
fasting glucose and insulin levels. It was developed as an alternative to the 
hyperinsulinemic-euglycemic clamp, which is the gold standard but resource-intensive. 
The HOMA-IR score helps identify individuals at risk for type 2 diabetes and 
metabolic syndrome.
"""

from pydantic import BaseModel, Field


class HomaIrRequest(BaseModel):
    """
    Request model for HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
    
    HOMA-IR requires two fasting laboratory values:
    
    1. Fasting insulin (μIU/mL):
    - Must be fasting for at least 8 hours
    - Normal range typically 2-25 μIU/mL
    - Values may vary by assay method
    
    2. Fasting glucose (mg/dL):
    - Must be fasting for at least 8 hours
    - Normal range typically 70-100 mg/dL
    
    The HOMA-IR formula: (Fasting Insulin × Fasting Glucose) / 405
    
    Important limitations:
    - Should NOT be used in patients on insulin therapy
    - May have reduced accuracy in impaired glucose tolerance
    - Normal ranges vary between populations and ethnicities

    References (Vancouver style):
    1. Matthews DR, Hosker JP, Rudenski AS, Naylor BA, Treacher DF, Turner RC. 
    Homeostasis model assessment: insulin resistance and beta-cell function from 
    fasting plasma glucose and insulin concentrations in man. Diabetologia. 
    1985 Jul;28(7):412-9.
    """
    
    fasting_insulin: float = Field(
        ...,
        description="Fasting insulin level in μIU/mL. Patient must be fasting for at least 8 hours. "
                    "Valid range: 0.1-300 μIU/mL",
        ge=0.1,
        le=300,
        example=10.5
    )
    
    fasting_glucose: float = Field(
        ...,
        description="Fasting glucose level in mg/dL. Patient must be fasting for at least 8 hours. "
                    "Valid range: 10-600 mg/dL",
        ge=10,
        le=600,
        example=95
    )
    
    class Config:
        schema_extra = {
            "example": {
                "fasting_insulin": 10.5,
                "fasting_glucose": 95
            }
        }


class HomaIrResponse(BaseModel):
    """
    Response model for HOMA-IR (Homeostatic Model Assessment for Insulin Resistance)
    
    The HOMA-IR score interpretation:
    - <0.7: Below normal range (possibly insulin sensitive)
    - 0.7-2.0: Normal insulin sensitivity
    - 2.0-2.5: Borderline insulin resistance  
    - 2.5-5.0: Moderate insulin resistance
    - >5.0: Severe insulin resistance
    
    The score is most useful for epidemiologic and population-based assessments 
    rather than individual clinical diagnosis.
    
    Reference: Matthews DR, et al. Diabetologia. 1985;28(7):412-9.
    """
    
    result: float = Field(
        ...,
        description="HOMA-IR score calculated from fasting insulin and glucose",
        example=2.47
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the HOMA-IR score",
        example="score"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation based on the HOMA-IR score",
        example="Borderline insulin resistance (2.0-2.5). Consider lifestyle modifications "
                "and monitoring for metabolic syndrome risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Insulin resistance category (Low, Normal, Borderline, Moderate, Severe)",
        example="Borderline"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the insulin resistance stage",
        example="Borderline insulin resistance"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.47,
                "unit": "score",
                "interpretation": "Borderline insulin resistance (2.0-2.5). Consider lifestyle "
                                "modifications and monitoring for metabolic syndrome risk factors.",
                "stage": "Borderline",
                "stage_description": "Borderline insulin resistance"
            }
        }