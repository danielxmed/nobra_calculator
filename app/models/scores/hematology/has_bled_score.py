"""
HAS-BLED Score for Major Bleeding Risk Models

Request and response models for HAS-BLED calculation.

References (Vancouver style):
1. Pisters R, Lane DA, Nieuwlaat R, de Vos CB, Crijns HJ, Lip GY. A novel user-friendly 
   score (HAS-BLED) to assess 1-year risk of major bleeding in patients with atrial 
   fibrillation: the Euro Heart Survey. Chest. 2010 Nov;138(5):1093-100. 
   doi: 10.1378/chest.10-0134.
2. Lip GY, Frison L, Halperin JL, Lane DA. Comparative validation of a novel risk score 
   for predicting bleeding risk in anticoagulated patients with atrial fibrillation: 
   the HAS-BLED (Hypertension, Abnormal Renal/Liver Function, Stroke, Bleeding History 
   or Predisposition, Labile INR, Elderly, Drugs/Alcohol Concomitantly) score. 
   J Am Coll Cardiol. 2011 Jan 11;57(2):173-80. doi: 10.1016/j.jacc.2010.09.024.
3. Apostolakis S, Lane DA, Guo Y, Buller H, Lip GY. Performance of the HEMORR(2)HAGES, 
   ATRIA, and HAS-BLED bleeding risk-prediction scores in patients with atrial fibrillation 
   undergoing anticoagulation: the AMADEUS (evaluating the use of SR34006 compared to 
   warfarin or acenocoumarol in patients with atrial fibrillation) study. J Am Coll Cardiol. 
   2012 Aug 28;60(9):861-7. doi: 10.1016/j.jacc.2012.06.019.

The HAS-BLED score estimates the 1-year risk of major bleeding in patients with atrial 
fibrillation on anticoagulation therapy. Major bleeding is defined as intracranial hemorrhage, 
bleeding requiring hospitalization, hemoglobin decrease >2 g/L, or bleeding requiring 
transfusion. The score is used alongside CHA2DS2-VASc to balance stroke and bleeding risks.
"""

from pydantic import BaseModel, Field
from typing import Literal


class HasBledScoreRequest(BaseModel):
    """
    Request model for HAS-BLED Score for Major Bleeding Risk
    
    The HAS-BLED score assesses 1-year major bleeding risk in anticoagulated AF patients:
    
    H - Hypertension: Uncontrolled, systolic BP >160 mmHg (1 point)
    A - Abnormal renal/liver function (1 point each, max 2 points):
        - Renal: Dialysis, transplant, or Cr >2.26 mg/dL (>200 μmol/L)
        - Liver: Cirrhosis or bilirubin >2x normal with AST/ALT/AP >3x normal
    S - Stroke: Previous stroke history (1 point)
    B - Bleeding: Prior major bleeding or predisposition (1 point)
    L - Labile INR: Unstable/high INRs, TTR <60% (1 point)
    E - Elderly: Age >65 years (1 point)
    D - Drugs/Alcohol (1 point each, max 2 points):
        - Drugs: Antiplatelet agents, NSAIDs
        - Alcohol: ≥8 drinks per week
    
    Total score ranges from 0-9 points. Score ≥3 indicates high bleeding risk.
    
    References (Vancouver style):
    1. Pisters R, Lane DA, Nieuwlaat R, de Vos CB, Crijns HJ, Lip GY. A novel user-friendly 
       score (HAS-BLED) to assess 1-year risk of major bleeding in patients with atrial 
       fibrillation: the Euro Heart Survey. Chest. 2010 Nov;138(5):1093-100. 
       doi: 10.1378/chest.10-0134.
    2. Lip GY, Frison L, Halperin JL, Lane DA. Comparative validation of a novel risk score 
       for predicting bleeding risk in anticoagulated patients with atrial fibrillation: 
       the HAS-BLED score. J Am Coll Cardiol. 2011 Jan 11;57(2):173-80. 
       doi: 10.1016/j.jacc.2010.09.024.
    """
    
    hypertension: Literal["no", "yes"] = Field(
        ...,
        description="Uncontrolled hypertension with systolic blood pressure >160 mmHg. "
                    "Scores 1 point if present. Modifiable risk factor that should be addressed.",
        example="no"
    )
    
    abnormal_renal_function: Literal["no", "yes"] = Field(
        ...,
        description="Chronic dialysis, renal transplant, or serum creatinine >2.26 mg/dL (>200 μmol/L). "
                    "Scores 1 point if present. Indicates significantly impaired kidney function.",
        example="no"
    )
    
    abnormal_liver_function: Literal["no", "yes"] = Field(
        ...,
        description="Chronic hepatic disease (e.g., cirrhosis) or biochemical evidence of significant "
                    "hepatic derangement (bilirubin >2x upper limit of normal in association with "
                    "AST/ALT/AP >3x upper limit normal). Scores 1 point if present.",
        example="no"
    )
    
    stroke_history: Literal["no", "yes"] = Field(
        ...,
        description="Previous stroke of any type (ischemic or hemorrhagic). "
                    "Scores 1 point if present. Non-modifiable risk factor.",
        example="no"
    )
    
    bleeding_history: Literal["no", "yes"] = Field(
        ...,
        description="Prior major bleeding event or predisposition to bleeding (e.g., bleeding diathesis, "
                    "anemia). Major bleeding includes intracranial, hospitalization for bleeding, "
                    "hemoglobin drop >2 g/L, or transfusion. Scores 1 point if present.",
        example="no"
    )
    
    labile_inr: Literal["no", "yes"] = Field(
        ...,
        description="Unstable/high INRs or poor time in therapeutic range (e.g., <60% of time in "
                    "therapeutic range). Scores 1 point if present. Modifiable risk factor - consider "
                    "improved INR monitoring or switching to DOAC.",
        example="no"
    )
    
    elderly: Literal["no", "yes"] = Field(
        ...,
        description="Age >65 years. Scores 1 point if present. Non-modifiable risk factor "
                    "but requires careful monitoring.",
        example="yes"
    )
    
    drugs: Literal["no", "yes"] = Field(
        ...,
        description="Concomitant use of drugs that promote bleeding such as antiplatelet agents "
                    "(aspirin, clopidogrel) or non-steroidal anti-inflammatory drugs (NSAIDs). "
                    "Scores 1 point if present. Modifiable risk factor - consider discontinuation.",
        example="no"
    )
    
    alcohol: Literal["no", "yes"] = Field(
        ...,
        description="Excessive alcohol use defined as ≥8 drinks per week. "
                    "Scores 1 point if present. Modifiable risk factor.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "hypertension": "no",
                "abnormal_renal_function": "no",
                "abnormal_liver_function": "no",
                "stroke_history": "no",
                "bleeding_history": "no",
                "labile_inr": "no",
                "elderly": "yes",
                "drugs": "no",
                "alcohol": "no"
            }
        }


class HasBledScoreResponse(BaseModel):
    """
    Response model for HAS-BLED Score for Major Bleeding Risk
    
    The HAS-BLED score provides bleeding risk stratification:
    - 0-1 points: Low risk (0.9-3.4% annual major bleeding risk)
    - 2 points: Moderate risk (4.1% annual major bleeding risk)
    - ≥3 points: High risk (5.8% to >10% annual major bleeding risk)
    
    High-risk patients (≥3 points) require regular clinical review and careful monitoring.
    The score should not be used alone to withhold anticoagulation but to identify 
    modifiable risk factors and ensure appropriate monitoring.
    
    Reference: Pisters R, et al. Chest. 2010;138(5):1093-100.
    """
    
    result: int = Field(
        ...,
        description="HAS-BLED score calculated from clinical parameters (range: 0-9 points)",
        example=1,
        ge=0,
        le=9
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation of bleeding risk with estimated annual percentage "
                    "and recommendations for anticoagulation management",
        example="Low risk of major bleeding (0.9-3.4% per year, estimated 1.3-3.4%). "
                "Anticoagulation should be considered if indicated. Regular monitoring "
                "and attention to modifiable risk factors recommended."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (Low Risk, Moderate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding risk level",
        example="Low bleeding risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 1,
                "unit": "points",
                "interpretation": "Low risk of major bleeding (0.9-3.4% per year, estimated 1.3-3.4%). "
                                  "Anticoagulation should be considered if indicated. Regular monitoring "
                                  "and attention to modifiable risk factors recommended.",
                "stage": "Low Risk",
                "stage_description": "Low bleeding risk"
            }
        }