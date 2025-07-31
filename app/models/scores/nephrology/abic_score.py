"""
ABIC Score calculation models
"""

from pydantic import BaseModel, Field


class AbicScoreRequest(BaseModel):
    """
    Request model for ABIC Score calculation
    
    The ABIC (Age, serum Bilirubin, INR, serum Creatinine) score predicts 90-day and 
    1-year survival in patients with alcoholic hepatitis, helping guide treatment decisions.
    
    **Clinical Use**:
    - Prognosis assessment in alcoholic hepatitis
    - Treatment intensity decision-making
    - Patient counseling regarding outcomes
    - Clinical trial stratification
    - Resource allocation decisions
    - Liver transplant evaluation timing
    
    **Score Components**:
    - Age (years)
    - Serum bilirubin (mg/dL)
    - INR (International Normalized Ratio)
    - Serum creatinine (mg/dL)
    
    **Reference**: Dominguez M, et al. A new scoring system for prognostic stratification of patients with alcoholic hepatitis. Am J Gastroenterol. 2008;103(11):2747-56.
    """
    age: int = Field(
        ..., 
        ge=18, 
        le=100, 
        description="Patient's age in years. Older age is associated with worse prognosis in alcoholic hepatitis.",
        example=50
    )
    serum_bilirubin: float = Field(
        ..., 
        ge=0.1, 
        le=50.0, 
        description="Total serum bilirubin concentration in mg/dL. Elevated bilirubin reflects severity of hepatic dysfunction and cholestasis.",
        example=8.5
    )
    serum_creatinine: float = Field(
        ..., 
        ge=0.1, 
        le=20.0, 
        description="Serum creatinine concentration in mg/dL. Elevated creatinine indicates renal dysfunction, often hepatorenal syndrome in severe cases.",
        example=1.2
    )
    inr: float = Field(
        ..., 
        ge=0.5, 
        le=10.0, 
        description="International Normalized Ratio reflecting coagulation status. Elevated INR indicates impaired hepatic synthetic function.",
        example=2.1
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 50,
                "serum_bilirubin": 8.5,
                "serum_creatinine": 1.2,
                "inr": 2.1
            }
        }


class AbicScoreResponse(BaseModel):
    """Response model for ABIC Score"""
    result: float = Field(..., description="Total ABIC score")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Prognostic interpretation")
    stage: str = Field(..., description="Risk classification")
    stage_description: str = Field(..., description="Prognosis description")
    survival_90_days: str = Field(..., description="90-day survival")
    survival_1_year: str = Field(..., description="1-year survival")
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 7.5,
                "unit": "points",
                "interpretation": "90-day survival: 70%. 1-year survival: 64.3%.",
                "stage": "Intermediate Risk",
                "stage_description": "Moderate survival",
                "survival_90_days": "70%",
                "survival_1_year": "64.3%"
            }
        }