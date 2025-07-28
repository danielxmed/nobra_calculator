"""ACEF II Risk Score models"""

from pydantic import BaseModel, Field


class AcefIiRequest(BaseModel):
    """Request model for ACEF II Risk Score

    The ACEF II score predicts 30-day mortality after cardiac surgery using
    patient age, left ventricular ejection fraction, serum creatinine, urgency
    of the procedure, and pre-operative anemia. The equation is parsimonious
    yet well validated in contemporary cohorts.

    **Reference**: Ranucci M, Pistuddi V, Scolletta S, de Vincentiis C,
    Menicanti L. The ACEF II Risk Score for cardiac surgery: updated but still
    parsimonious. Eur Heart J. 2018;39(23):2183-2189.
    """

    age: int = Field(..., ge=18, le=100,
                     description="Patient age in years")
    ejection_fraction: float = Field(..., ge=10, le=80,
                                     description="Left ventricular ejection fraction percentage")
    serum_creatinine: float = Field(..., ge=0.1, le=20.0,
                                    description="Serum creatinine in mg/dL")
    emergency_surgery: bool = Field(..., description="Emergency surgery indicator")
    hematocrit: float = Field(..., ge=15, le=60,
                              description="Pre-operative hematocrit percentage")

    class Config:
        schema_extra = {
            "example": {
                "age": 70,
                "ejection_fraction": 45.0,
                "serum_creatinine": 1.2,
                "emergency_surgery": False,
                "hematocrit": 38.0
            }
        }


class AcefIiResponse(BaseModel):
    """Response model for ACEF II Risk Score"""

    result: float = Field(..., description="ACEF II score")
    unit: str = Field(..., description="Unit of the result")
    interpretation: str = Field(..., description="Clinical interpretation")
    stage: str = Field(..., description="Risk category")
    stage_description: str = Field(..., description="Risk description")

    class Config:
        schema_extra = {
            "example": {
                "result": 1.8,
                "unit": "points",
                "interpretation": "Standard perioperative management.",
                "stage": "Low Risk",
                "stage_description": "Estimated mortality <2%"
            }
        }

