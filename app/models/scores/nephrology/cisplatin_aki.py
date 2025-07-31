"""
Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk Calculator Models

Request and response models for CP-AKI calculation.

References (Vancouver style):
1. Gupta S, Portales-Castillo I, Daher A, Kitchlu A. Derivation and external 
   validation of a simple risk score for predicting severe acute kidney injury 
   after intravenous cisplatin: cohort study. BMJ. 2024 Mar 27;384:e077169. 
   doi: 10.1136/bmj-2023-077169.
2. Motwani SS, McMahon GM, Humphreys BD, Partridge AH, Waikar SS, Curhan GC. 
   Development and Validation of a Risk Prediction Model for Acute Kidney Injury 
   After the First Course of Cisplatin. J Clin Oncol. 2018 Mar 1;36(7):682-688. 
   doi: 10.1200/JCO.2017.75.7161.
3. Kitchlu A, McArthur E, Amir E, Booth CM, Sutradhar R, Majeed H, et al. 
   Acute Kidney Injury in Patients Receiving Systemic Treatment for Cancer: 
   A Population-Based Cohort Study. J Natl Cancer Inst. 2019 Jul 1;111(7):727-736. 
   doi: 10.1093/jnci/djy167.

The CP-AKI Risk Calculator predicts the risk of moderate to severe acute kidney 
injury (≥2-fold rise in serum creatinine or need for kidney replacement therapy 
within 14 days) in patients treated with intravenous cisplatin. This tool helps 
clinicians identify high-risk patients who may benefit from closer monitoring or 
alternative treatment strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal


class CisplatinAkiRequest(BaseModel):
    """
    Request model for Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk Calculator
    
    The CP-AKI calculator uses 9 clinical variables to assess kidney injury risk:
    
    Patient Demographics:
    - Age: Risk increases with age, particularly >60 years
    
    Comorbidities (each yes/no):
    - Hypertension: Independent risk factor for AKI
    - Type 2 Diabetes: Associated with increased AKI risk
    
    Cisplatin Dosing:
    - Total dose: Higher doses (>100 mg) increase risk
    
    Laboratory Values:
    - Hemoglobin: Anemia is a risk factor
    - WBC count: Both low and high counts increase risk
    - Platelet count: Thrombocytopenia increases risk
    - Albumin: Hypoalbuminemia strongly predictive
    - Magnesium: Hypomagnesemia increases risk

    References (Vancouver style):
    1. Gupta S, Portales-Castillo I, Daher A, Kitchlu A. Derivation and external 
    validation of a simple risk score for predicting severe acute kidney injury 
    after intravenous cisplatin: cohort study. BMJ. 2024 Mar 27;384:e077169. 
    doi: 10.1136/bmj-2023-077169.
    2. Motwani SS, McMahon GM, Humphreys BD, Partridge AH, Waikar SS, Curhan GC. 
    Development and Validation of a Risk Prediction Model for Acute Kidney Injury 
    After the First Course of Cisplatin. J Clin Oncol. 2018 Mar 1;36(7):682-688. 
    doi: 10.1200/JCO.2017.75.7161.
    """
    
    age: int = Field(
        ...,
        ge=18,
        le=110,
        description="Patient age in years. Age is a strong predictor, with risk increasing significantly after 60 years",
        example=65
    )
    
    hypertension: Literal["yes", "no"] = Field(
        ...,
        description="History of hypertension. Hypertension is an independent risk factor for cisplatin-induced AKI",
        example="yes"
    )
    
    diabetes: Literal["yes", "no"] = Field(
        ...,
        description="History of type 2 diabetes mellitus. Diabetes increases risk of AKI through pre-existing kidney damage",
        example="no"
    )
    
    cisplatin_dose: float = Field(
        ...,
        ge=1,
        le=1000,
        description="Total cisplatin dose in mg. Higher doses (>100 mg) significantly increase AKI risk",
        example=120
    )
    
    hemoglobin: float = Field(
        ...,
        ge=2.0,
        le=20.0,
        description="Hemoglobin level in g/dL. Anemia (Hgb <10 g/dL) is associated with increased AKI risk",
        example=11.5
    )
    
    wbc_count: float = Field(
        ...,
        ge=1.0,
        le=300.0,
        description="White blood cell count in ×10³/µL. Both leukopenia and leukocytosis increase risk",
        example=7.2
    )
    
    platelet_count: float = Field(
        ...,
        ge=1,
        le=1500,
        description="Platelet count in ×10³/µL. Thrombocytopenia (<150 ×10³/µL) increases AKI risk",
        example=180
    )
    
    albumin: float = Field(
        ...,
        ge=0.5,
        le=8.0,
        description="Serum albumin level in g/dL. Hypoalbuminemia (<3.5 g/dL) is a strong predictor of AKI",
        example=3.8
    )
    
    magnesium: float = Field(
        ...,
        ge=0.5,
        le=5.0,
        description="Serum magnesium level in mg/dL. Hypomagnesemia (<1.6 mg/dL) increases cisplatin nephrotoxicity",
        example=1.8
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 65,
                "hypertension": "yes",
                "diabetes": "no",
                "cisplatin_dose": 120,
                "hemoglobin": 11.5,
                "wbc_count": 7.2,
                "platelet_count": 180,
                "albumin": 3.8,
                "magnesium": 1.8
            }
        }


class CisplatinAkiResponse(BaseModel):
    """
    Response model for Cisplatin-Associated Acute Kidney Injury (CP-AKI) Risk Calculator
    
    The CP-AKI calculator predicts risk of moderate to severe AKI, defined as:
    - ≥2-fold rise in serum creatinine within 14 days, OR
    - Need for kidney replacement therapy within 14 days
    
    Risk categories guide clinical management:
    - Low (<5%): Standard monitoring
    - Moderate (5-15%): Enhanced monitoring, prophylactic measures
    - High (15-30%): Close monitoring, consider alternatives
    - Very High (≥30%): Strong consideration for alternative therapy
    
    Reference: Gupta S, et al. BMJ. 2024;384:e077169.
    """
    
    result: float = Field(
        ...,
        description="Estimated risk of moderate to severe acute kidney injury as a percentage",
        example=12.5
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on risk level",
        example="Moderate risk of cisplatin-associated acute kidney injury (5-15%). Enhanced monitoring recommended. Consider prophylactic measures such as aggressive hydration and electrolyte repletion."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low, Moderate, High, Very High)",
        example="Moderate"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="Moderate risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 12.5,
                "unit": "%",
                "interpretation": "Moderate risk of cisplatin-associated acute kidney injury (5-15%). Enhanced monitoring recommended. Consider prophylactic measures such as aggressive hydration and electrolyte repletion.",
                "stage": "Moderate",
                "stage_description": "Moderate risk"
            }
        }