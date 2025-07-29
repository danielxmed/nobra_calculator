"""
ARISCAT Score for Postoperative Pulmonary Complications Models

Request and response models for ARISCAT calculation.

References (Vancouver style):
1. Canet J, Gallart L, Gomar C, Paluzie G, Vallès J, Castillo J, et al. Prediction of 
   postoperative pulmonary complications in a population-based surgical cohort. 
   Anesthesiology. 2010;113(6):1338-50. doi: 10.1097/ALN.0b013e3181fc6e0a.
2. Mazo V, Sabaté S, Canet J, Gallart L, de Abreu MG, Belda J, et al. Prospective 
   external validation of a predictive score for postoperative pulmonary complications. 
   Anesthesiology. 2014;121(2):219-31. doi: 10.1097/ALN.0000000000000334.

The ARISCAT score is a validated tool for predicting postoperative pulmonary complications 
(PPC) including respiratory failure, respiratory infection, pleural effusion, atelectasis, 
pneumothorax, bronchospasm, or aspiration pneumonitis. It uses 7 preoperative variables 
to stratify patients into low (≤25 points), intermediate (26-44 points), or high (≥45 points) 
risk categories.
"""

from pydantic import BaseModel, Field
from typing import Literal


class AriscatScoreRequest(BaseModel):
    """
    Request model for ARISCAT Score for Postoperative Pulmonary Complications
    
    The ARISCAT score uses 7 preoperative variables to predict pulmonary complications:
    
    Age Categories:
    - 50_or_less: Age ≤50 years (0 points)
    - 51_to_80: Age 51-80 years (3 points)
    - over_80: Age >80 years (16 points)
    
    Preoperative SpO2:
    - 96_or_higher: SpO2 ≥96% (0 points)
    - 91_to_95: SpO2 91-95% (8 points)
    - 90_or_less: SpO2 ≤90% (24 points)
    
    Respiratory infection in last month:
    - no: No respiratory infection (0 points)
    - yes: Upper or lower respiratory infection with fever and antibiotic treatment (17 points)
    
    Preoperative anemia:
    - no: Hemoglobin >10 g/dL (0 points)
    - yes: Hemoglobin ≤10 g/dL (11 points)
    
    Surgical incision:
    - peripheral: Peripheral surgery (0 points)
    - upper_abdominal: Upper abdominal incision (15 points)
    - intrathoracic: Intrathoracic incision (24 points)
    
    Surgery duration:
    - less_than_2: Duration <2 hours (0 points)
    - 2_to_3: Duration 2-3 hours (16 points)
    - more_than_3: Duration >3 hours (23 points)
    
    Emergency procedure:
    - no: Elective surgery (0 points)
    - yes: Emergency surgery (8 points)

    References (Vancouver style):
    1. Canet J, Gallart L, Gomar C, Paluzie G, Vallès J, Castillo J, et al. Prediction of 
    postoperative pulmonary complications in a population-based surgical cohort. 
    Anesthesiology. 2010;113(6):1338-50. doi: 10.1097/ALN.0b013e3181fc6e0a.
    2. Mazo V, Sabaté S, Canet J, Gallart L, de Abreu MG, Belda J, et al. Prospective 
    external validation of a predictive score for postoperative pulmonary complications. 
    Anesthesiology. 2014;121(2):219-31. doi: 10.1097/ALN.0000000000000334.
    """
    
    age: Literal["50_or_less", "51_to_80", "over_80"] = Field(
        ...,
        description="Patient age category. ≤50 years scores 0 points, 51-80 years scores 3 points, >80 years scores 16 points",
        example="51_to_80"
    )
    
    preoperative_spo2: Literal["96_or_higher", "91_to_95", "90_or_less"] = Field(
        ...,
        description="Preoperative oxygen saturation on room air. ≥96% scores 0 points, 91-95% scores 8 points, ≤90% scores 24 points",
        example="96_or_higher"
    )
    
    respiratory_infection_last_month: Literal["no", "yes"] = Field(
        ...,
        description="Respiratory infection in the last month (upper or lower respiratory tract infection with fever and antibiotic treatment). Scores 17 points if yes",
        example="no"
    )
    
    preoperative_anemia: Literal["no", "yes"] = Field(
        ...,
        description="Preoperative anemia (hemoglobin ≤10 g/dL). Scores 11 points if yes",
        example="no"
    )
    
    surgical_incision: Literal["peripheral", "upper_abdominal", "intrathoracic"] = Field(
        ...,
        description="Type of surgical incision. Peripheral scores 0 points, upper abdominal scores 15 points, intrathoracic scores 24 points",
        example="upper_abdominal"
    )
    
    surgery_duration: Literal["less_than_2", "2_to_3", "more_than_3"] = Field(
        ...,
        description="Duration of surgery in hours. <2h scores 0 points, 2-3h scores 16 points, >3h scores 23 points",
        example="2_to_3"
    )
    
    emergency_procedure: Literal["no", "yes"] = Field(
        ...,
        description="Emergency surgical procedure. Scores 8 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": "51_to_80",
                "preoperative_spo2": "96_or_higher",
                "respiratory_infection_last_month": "no",
                "preoperative_anemia": "no",
                "surgical_incision": "upper_abdominal",
                "surgery_duration": "2_to_3",
                "emergency_procedure": "no"
            }
        }


class AriscatScoreResponse(BaseModel):
    """
    Response model for ARISCAT Score for Postoperative Pulmonary Complications
    
    The ARISCAT score ranges from 0 to 120 points and classifies patients into:
    - Low Risk (≤25 points): Low probability of postoperative pulmonary complications
    - Intermediate Risk (26-44 points): Intermediate probability requiring enhanced monitoring
    - High Risk (≥45 points): High probability requiring intensive monitoring and prophylaxis
    
    Reference: Canet J, et al. Anesthesiology. 2010;113(6):1338-50.
    """
    
    result: int = Field(
        ...,
        description="ARISCAT score calculated from preoperative variables (range: 0 to 120 points)",
        example=34
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended perioperative management based on the score",
        example="Intermediate risk of postoperative pulmonary complications. Enhanced respiratory monitoring and preventive measures should be considered."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Intermediate risk of postoperative pulmonary complications"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 34,
                "unit": "points",
                "interpretation": "Intermediate risk of postoperative pulmonary complications. Enhanced respiratory monitoring and preventive measures should be considered.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk of postoperative pulmonary complications"
            }
        }
