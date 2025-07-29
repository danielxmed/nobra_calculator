"""
Apfel Score for Postoperative Nausea and Vomiting Models

Request and response models for Apfel Score calculation.

References (Vancouver style):
1. Apfel CC, Läärä E, Koivuranta M, Greim CA, Roewer N. A simplified risk score 
   for predicting postoperative nausea and vomiting: conclusions from cross-validations 
   between two centers. Anesthesiology. 1999;91(3):693-700.
2. Gan TJ, Belani KG, Bergese S, et al. Fourth Consensus Guidelines for the Management 
   of Postoperative Nausea and Vomiting. Anesth Analg. 2020;131(2):411-448.
3. Apfel CC, Heidrich FM, Jukar-Rao S, et al. Evidence-based analysis of risk factors 
   for postoperative nausea and vomiting. Br J Anaesth. 2012;109(5):742-753.

The Apfel Score is one of the most widely validated and used risk assessment tools for 
postoperative nausea and vomiting (PONV). It uses four simple clinical risk factors:
1. Female gender (1 point)
2. Non-smoking status (1 point) 
3. History of motion sickness or PONV (1 point)
4. Use of postoperative opioids (1 point)

The score helps guide prophylactic antiemetic therapy decisions in the perioperative period.
Each risk factor contributes equally (1 point) to the total score (0-4 points).
"""

from pydantic import BaseModel, Field
from typing import Literal


class ApfelScorePonvRequest(BaseModel):
    """
    Request model for Apfel Score for Postoperative Nausea and Vomiting
    
    The Apfel Score predicts PONV risk using four equally weighted clinical factors:
    
    Risk Factors (each contributes 1 point):
    - Female gender: Women have approximately twice the risk of PONV compared to men
    - Non-smoking status: Non-smokers have higher PONV risk than smokers
    - History of motion sickness or PONV: Previous episodes predict future risk
    - Use of postoperative opioids: Opioids increase PONV risk through central mechanisms
    
    Score Interpretation:
    - 0 points: ~10% PONV risk (Very Low Risk)
    - 1 point: ~20% PONV risk (Low Risk)
    - 2 points: ~40% PONV risk (Moderate Risk) 
    - 3 points: ~60% PONV risk (High Risk)
    - 4 points: ~80% PONV risk (Very High Risk)
    
    References (Vancouver style):
    1. Apfel CC, Läärä E, Koivuranta M, Greim CA, Roewer N. A simplified risk score 
    for predicting postoperative nausea and vomiting: conclusions from cross-validations 
    between two centers. Anesthesiology. 1999;91(3):693-700.
    2. Gan TJ, Belani KG, Bergese S, et al. Fourth Consensus Guidelines for the Management 
    of Postoperative Nausea and Vomiting. Anesth Analg. 2020;131(2):411-448.
    3. Apfel CC, Heidrich FM, Jukar-Rao S, et al. Evidence-based analysis of risk factors 
    for postoperative nausea and vomiting. Br J Anaesth. 2012;109(5):742-753.
    """
    
    gender: Literal["male", "female"] = Field(
        ...,
        description="Patient gender. Female gender is a significant risk factor for PONV (1 point if female)",
        example="female"
    )
    
    smoking_status: Literal["smoker", "nonsmoker"] = Field(
        ...,
        description="Current smoking status. Non-smoking is a risk factor for PONV (1 point if nonsmoker)",
        example="nonsmoker"
    )
    
    history_motion_sickness_ponv: Literal["no", "yes"] = Field(
        ...,
        description="Previous history of motion sickness or postoperative nausea and vomiting (1 point if yes)",
        example="yes"
    )
    
    postoperative_opioids: Literal["no", "yes"] = Field(
        ...,
        description="Planned use of postoperative opioids for pain management (1 point if yes)",
        example="yes"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "gender": "female",
                "smoking_status": "nonsmoker",
                "history_motion_sickness_ponv": "yes",
                "postoperative_opioids": "yes"
            }
        }


class ApfelScorePonvResponse(BaseModel):
    """
    Response model for Apfel Score for Postoperative Nausea and Vomiting
    
    The Apfel Score ranges from 0-4 points and predicts 24-hour PONV risk:
    - 0 points: ~10% risk (Very Low Risk) - Prophylactic antiemetics generally not recommended
    - 1 point: ~20% risk (Low Risk) - Consider single prophylactic antiemetic agent
    - 2 points: ~40% risk (Moderate Risk) - Recommend combination of 2 prophylactic antiemetic agents
    - 3 points: ~60% risk (High Risk) - Recommend combination of 2-3 prophylactic antiemetic agents
    - 4 points: ~80% risk (Very High Risk) - Multiple prophylactic agents + consider TIVA
    
    Reference: Apfel CC, et al. Anesthesiology. 1999;91(3):693-700.
    """
    
    result: int = Field(
        ...,
        description="Apfel Score for PONV risk assessment (0-4 points)",
        ge=0,
        le=4,
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and recommended prophylactic antiemetic strategy based on the score",
        example="Approximately 80% risk of PONV within 24 hours. Recommend combination of multiple prophylactic antiemetic agents and consider total intravenous anesthesia (TIVA)."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Very High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="4 risk factors"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Approximately 80% risk of PONV within 24 hours. Recommend combination of multiple prophylactic antiemetic agents and consider total intravenous anesthesia (TIVA).",
                "stage": "Very High Risk",
                "stage_description": "4 risk factors"
            }
        }
