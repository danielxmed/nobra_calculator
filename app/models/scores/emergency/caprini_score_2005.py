"""
Caprini Score for Venous Thromboembolism (2005) Models

Request and response models for Caprini Score calculation.

References (Vancouver style):
1. Caprini JA. Thrombosis risk assessment as a guide to quality patient care. 
   Dis Mon. 2005 Feb-Mar;51(2-3):70-8. doi: 10.1016/j.disamonth.2005.02.003.
2. Pannucci CJ, Laird S, Dimick JB, Campbell DA, Henke PK. A validated risk model 
   to predict 90-day VTE events in postsurgical patients. Chest. 2014 Mar;145(3):567-73. 
   doi: 10.1378/chest.13-1553.
3. Bahl V, Hu HM, Henke PK, Wakefield TW, Campbell DA Jr, Caprini JA. A validation 
   study of a retrospective venous thromboembolism risk scoring method. Ann Surg. 
   2010 Feb;251(2):344-50. doi: 10.1097/SLA.0b013e3181b7fca6.

The Caprini Score stratifies risk of venous thromboembolism (VTE) in surgical and 
medical patients, guiding prophylaxis decisions. It is the most widely validated 
VTE risk assessment tool and is recommended by ACCP guidelines for surgical patients.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CapriniScore2005Request(BaseModel):
    """
    Request model for Caprini Score for Venous Thromboembolism (2005)
    
    The Caprini Score is the most widely validated VTE risk assessment tool that 
    stratifies patients into risk categories based on multiple clinical factors.
    
    Risk Factors and Point Values:
    
    Age Categories:
    - Under 41 years: 0 points
    - 41-60 years: 1 point
    - 61-74 years: 2 points
    - 75+ years: 3 points
    
    Surgery Types:
    - Minor surgery (<45 minutes): 1 point
    - Major surgery (>45 minutes): 2 points
    - Hip/knee arthroplasty: 5 points
    - Hip/pelvis/leg fracture: 5 points
    - Acute spinal cord injury: 5 points
    
    Medical Conditions (1 point each):
    - Varicose veins
    - Current swollen legs (edema)
    - Central venous access
    - Inflammatory bowel disease
    - BMI >25 kg/m²
    
    Medical Conditions (2 points each):
    - Acute myocardial infarction
    - Congestive heart failure (<1 month)
    - Sepsis (<1 month)
    - Serious lung disease (<1 month)
    - Abnormal pulmonary function (COPD)
    - Medical patient at bed rest
    - Plaster cast or brace
    
    Thrombophilia/History (3 points each):
    - History of DVT/PE
    - Family history of thrombosis
    - Factor V Leiden
    - Prothrombin 20210A
    - Lupus anticoagulant
    - Anticardiolipin antibodies
    - Heparin-induced thrombocytopenia
    - Other thrombophilia
    
    Malignancy: 5 points
    
    Risk Stratification:
    - 0 points: Lowest risk - early ambulation
    - 1-2 points: Low risk - mechanical prophylaxis
    - 3-4 points: Moderate risk (0.7% VTE) - consider chemoprophylaxis
    - 5-6 points: High risk (1.8% VTE) - chemoprophylaxis recommended
    - 7-8 points: High risk (4.0% VTE) - extended prophylaxis
    - ≥9 points: Highest risk (10.7% VTE) - aggressive prophylaxis
    
    References (Vancouver style):
    1. Caprini JA. Thrombosis risk assessment as a guide to quality patient care. 
    Dis Mon. 2005 Feb-Mar;51(2-3):70-8.
    """
    
    age_category: Literal["under_41", "41_to_60", "61_to_74", "75_or_older"] = Field(
        ...,
        description="Patient age category: under 41 (0 pts), 41-60 (1 pt), 61-74 (2 pts), 75+ (3 pts)",
        example="41_to_60"
    )
    
    minor_surgery: Literal["yes", "no"] = Field(
        ...,
        description="Minor surgery (planned procedure <45 minutes). Scores +1 point if yes",
        example="no"
    )
    
    major_surgery: Literal["yes", "no"] = Field(
        ...,
        description="Major surgery (>45 minutes, laparoscopic >45 min, or arthroscopic >45 min). Scores +2 points if yes",
        example="yes"
    )
    
    hip_knee_arthroplasty: Literal["yes", "no"] = Field(
        ...,
        description="Elective major lower extremity arthroplasty (hip or knee replacement). Scores +5 points if yes",
        example="no"
    )
    
    hip_pelvis_leg_fracture: Literal["yes", "no"] = Field(
        ...,
        description="Hip, pelvis, or leg fracture. Scores +5 points if yes",
        example="no"
    )
    
    acute_spinal_cord_injury: Literal["yes", "no"] = Field(
        ...,
        description="Acute spinal cord injury (paralysis). Scores +5 points if yes",
        example="no"
    )
    
    varicose_veins: Literal["yes", "no"] = Field(
        ...,
        description="Varicose veins. Scores +1 point if yes",
        example="no"
    )
    
    current_swollen_legs: Literal["yes", "no"] = Field(
        ...,
        description="Current swollen legs (edema). Scores +1 point if yes",
        example="no"
    )
    
    central_venous_access: Literal["yes", "no"] = Field(
        ...,
        description="Central venous access (central line, port, etc.). Scores +1 point if yes",
        example="no"
    )
    
    inflammatory_bowel_disease: Literal["yes", "no"] = Field(
        ...,
        description="Inflammatory bowel disease (Crohn's disease, ulcerative colitis). Scores +1 point if yes",
        example="no"
    )
    
    bmi_over_25: Literal["yes", "no"] = Field(
        ...,
        description="BMI >25 kg/m². Scores +1 point if yes",
        example="yes"
    )
    
    acute_myocardial_infarction: Literal["yes", "no"] = Field(
        ...,
        description="Acute myocardial infarction. Scores +2 points if yes",
        example="no"
    )
    
    congestive_heart_failure: Literal["yes", "no"] = Field(
        ...,
        description="Congestive heart failure (<1 month). Scores +2 points if yes",
        example="no"
    )
    
    sepsis: Literal["yes", "no"] = Field(
        ...,
        description="Sepsis (<1 month). Scores +2 points if yes",
        example="no"
    )
    
    serious_lung_disease: Literal["yes", "no"] = Field(
        ...,
        description="Serious lung disease including pneumonia (<1 month). Scores +2 points if yes",
        example="no"
    )
    
    abnormal_pulmonary_function: Literal["yes", "no"] = Field(
        ...,
        description="Abnormal pulmonary function (COPD). Scores +2 points if yes",
        example="no"
    )
    
    medical_patient_bed_rest: Literal["yes", "no"] = Field(
        ...,
        description="Medical patient currently at bed rest. Scores +2 points if yes",
        example="no"
    )
    
    cast_or_brace: Literal["yes", "no"] = Field(
        ...,
        description="Plaster cast or brace. Scores +2 points if yes",
        example="no"
    )
    
    history_of_vte: Literal["yes", "no"] = Field(
        ...,
        description="History of DVT/PE. Scores +3 points if yes",
        example="no"
    )
    
    family_history_thrombosis: Literal["yes", "no"] = Field(
        ...,
        description="Family history of thrombosis. Scores +3 points if yes",
        example="no"
    )
    
    factor_v_leiden: Literal["yes", "no"] = Field(
        ...,
        description="Factor V Leiden mutation. Scores +3 points if yes",
        example="no"
    )
    
    prothrombin_20210a: Literal["yes", "no"] = Field(
        ...,
        description="Prothrombin 20210A mutation. Scores +3 points if yes",
        example="no"
    )
    
    lupus_anticoagulant: Literal["yes", "no"] = Field(
        ...,
        description="Lupus anticoagulant. Scores +3 points if yes",
        example="no"
    )
    
    anticardiolipin_antibodies: Literal["yes", "no"] = Field(
        ...,
        description="Anticardiolipin antibodies. Scores +3 points if yes",
        example="no"
    )
    
    heparin_induced_thrombocytopenia: Literal["yes", "no"] = Field(
        ...,
        description="Heparin-induced thrombocytopenia (HIT). Scores +3 points if yes",
        example="no"
    )
    
    other_congenital_thrombophilia: Literal["yes", "no"] = Field(
        ...,
        description="Other congenital or acquired thrombophilia. Scores +3 points if yes",
        example="no"
    )
    
    malignancy: Literal["yes", "no"] = Field(
        ...,
        description="Malignancy (present or previous). Scores +5 points if yes",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age_category": "41_to_60",
                "minor_surgery": "no",
                "major_surgery": "yes",
                "hip_knee_arthroplasty": "no",
                "hip_pelvis_leg_fracture": "no",
                "acute_spinal_cord_injury": "no",
                "varicose_veins": "no",
                "current_swollen_legs": "no",
                "central_venous_access": "no",
                "inflammatory_bowel_disease": "no",
                "bmi_over_25": "yes",
                "acute_myocardial_infarction": "no",
                "congestive_heart_failure": "no",
                "sepsis": "no",
                "serious_lung_disease": "no",
                "abnormal_pulmonary_function": "no",
                "medical_patient_bed_rest": "no",
                "cast_or_brace": "no",
                "history_of_vte": "no",
                "family_history_thrombosis": "no",
                "factor_v_leiden": "no",
                "prothrombin_20210a": "no",
                "lupus_anticoagulant": "no",
                "anticardiolipin_antibodies": "no",
                "heparin_induced_thrombocytopenia": "no",
                "other_congenital_thrombophilia": "no",
                "malignancy": "no"
            }
        }


class CapriniScore2005Response(BaseModel):
    """
    Response model for Caprini Score for Venous Thromboembolism (2005)
    
    The Caprini Score provides evidence-based VTE risk stratification and 
    prophylaxis recommendations:
    
    Risk Categories and Clinical Management:
    - Lowest Risk (0 points): Early ambulation, compression stockings
    - Low Risk (1-2 points): Mechanical prophylaxis (IPC)
    - Moderate Risk (3-4 points): 0.7% VTE risk - consider chemoprophylaxis
    - High Risk (5-6 points): 1.8% VTE risk - IPC + LMWH recommended
    - High Risk (7-8 points): 4.0% VTE risk - IPC + LMWH + extended prophylaxis
    - Highest Risk (≥9 points): 10.7% VTE risk - aggressive prophylaxis mandatory
    
    Clinical Applications:
    - Most widely validated VTE risk assessment tool
    - Recommended by ACCP guidelines for surgical patients
    - Guides duration and intensity of prophylaxis
    - Cost-effective approach to VTE prevention
    
    Prophylaxis Options:
    - Mechanical: Early ambulation, compression stockings, IPC
    - Pharmacologic: LMWH, UFH, fondaparinux, warfarin, DOACs
    - Extended: 30-day post-operative prophylaxis for high-risk patients
    - Special considerations: IVC filter if anticoagulation contraindicated
    
    Performance:
    - Validated in >250,000 patients across >100 studies
    - 14-fold variation in VTE risk across score categories
    - Benefit of chemoprophylaxis demonstrated for scores ≥7
    - No increased bleeding risk identified across score ranges
    
    Reference: Caprini JA. Dis Mon. 2005;51(2-3):70-8.
    """
    
    result: int = Field(
        ...,
        description="Caprini Score calculated from clinical risk factors (range: 0 to >20 points)",
        example=4
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and prophylaxis recommendations based on VTE risk category",
        example="Moderate risk of VTE. Consider intermittent pneumatic compression or low molecular weight heparin. Risk-benefit assessment for chemoprophylaxis recommended."
    )
    
    stage: str = Field(
        ...,
        description="VTE risk category (Lowest Risk, Low Risk, Moderate Risk, High Risk, or Highest Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="VTE risk percentage or description for the risk category",
        example="0.7% VTE risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 4,
                "unit": "points",
                "interpretation": "Moderate risk of VTE. Consider intermittent pneumatic compression or low molecular weight heparin. Risk-benefit assessment for chemoprophylaxis recommended.",
                "stage": "Moderate Risk",
                "stage_description": "0.7% VTE risk"
            }
        }