"""
HCM Risk-SCD Models

Request and response models for HCM Risk-SCD calculation.

References (Vancouver style):
1. O'Mahony C, Jichi F, Pavlou M, Monserrat L, Anastasakis A, Rapezzi C, et al. A novel 
   clinical risk prediction model for sudden cardiac death in hypertrophic cardiomyopathy 
   (HCM risk-SCD). Eur Heart J. 2014 Aug 7;35(30):2010-20. doi: 10.1093/eurheartj/eht439.
2. Elliott PM, Anastasakis A, Borger MA, Borggrefe M, Cecchi F, Charron P, et al. 
   2014 ESC Guidelines on diagnosis and management of hypertrophic cardiomyopathy: 
   the Task Force for the Diagnosis and Management of Hypertrophic Cardiomyopathy 
   of the European Society of Cardiology (ESC). Eur Heart J. 2014 Oct 14;35(39):2733-79. 
   doi: 10.1093/eurheartj/ehu284.
3. O'Mahony C, Jichi F, Ommen SR, Christiaans I, Arbustini E, Garcia-Pavia P, et al. 
   International External Validation Study of the 2014 European Society of Cardiology 
   Guidelines on Sudden Cardiac Death Prevention in Hypertrophic Cardiomyopathy 
   (EVIDENCE-HCM). Circulation. 2018 Mar 6;137(10):1015-1023. 
   doi: 10.1161/CIRCULATIONAHA.117.030437.

The HCM Risk-SCD calculator estimates the 5-year risk of sudden cardiac death in 
patients with hypertrophic cardiomyopathy. It was developed using a multicenter 
retrospective cohort of 3,675 patients and validated both internally and externally. 
The model uses readily available clinical parameters to provide individualized risk 
estimates that guide decisions regarding prophylactic ICD implantation.
"""

from pydantic import BaseModel, Field, validator
from typing import Literal


class HcmRiskScdRequest(BaseModel):
    """
    Request model for HCM Risk-SCD
    
    The HCM Risk-SCD calculator uses 7 clinical parameters to estimate 5-year 
    sudden cardiac death risk in HCM patients:
    
    1. Age: Younger patients generally have higher SCD risk
    2. Family history of SCD: Genetic predisposition indicator
    3. Maximum wall thickness: Extent of hypertrophy correlates with risk
    4. Left atrial diameter: Marker of diastolic dysfunction and filling pressures
    5. Maximum LVOT gradient: Obstruction increases hemodynamic stress
    6. Non-sustained VT: Strong arrhythmic risk marker
    7. Unexplained syncope: May indicate arrhythmic events
    
    The model provides superior risk stratification compared to previous approaches
    that relied on counting risk factors.
    
    References (Vancouver style):
    1. O'Mahony C, Jichi F, Pavlou M, Monserrat L, Anastasakis A, Rapezzi C, et al. 
       A novel clinical risk prediction model for sudden cardiac death in hypertrophic 
       cardiomyopathy (HCM risk-SCD). Eur Heart J. 2014 Aug 7;35(30):2010-20. 
       doi: 10.1093/eurheartj/eht439.
    2. Elliott PM, Anastasakis A, Borger MA, Borggrefe M, Cecchi F, Charron P, et al. 
       2014 ESC Guidelines on diagnosis and management of hypertrophic cardiomyopathy. 
       Eur Heart J. 2014 Oct 14;35(39):2733-79. doi: 10.1093/eurheartj/ehu284.
    """
    
    age: int = Field(
        ...,
        description="Age at evaluation in years. Younger age is associated with higher SCD risk "
                    "in HCM due to the progressive nature of the disease.",
        example=45,
        ge=16,
        le=110
    )
    
    family_history_scd: Literal["no", "yes"] = Field(
        ...,
        description="History of sudden cardiac death in ≥1 first degree relatives <40 years of age "
                    "OR SCD in any relative with confirmed HCM at any age. Suggests genetic "
                    "predisposition to malignant arrhythmias.",
        example="no"
    )
    
    max_wall_thickness: float = Field(
        ...,
        description="Maximum left ventricular wall thickness in mm, measured by echocardiography. "
                    "Greatest thickness in anterior septum, posterior septum, lateral wall, and "
                    "posterior wall. Severe hypertrophy (≥30 mm) significantly increases risk.",
        example=18.0,
        ge=10,
        le=40
    )
    
    left_atrial_diameter: float = Field(
        ...,
        description="Left atrial diameter in mm, determined by M-Mode or 2-D echocardiography "
                    "in parasternal long axis view. LA enlargement reflects chronically elevated "
                    "LV filling pressures and diastolic dysfunction.",
        example=40.0,
        ge=15,
        le=70
    )
    
    max_lvot_gradient: float = Field(
        ...,
        description="Maximum left ventricular outflow tract gradient in mmHg, determined at rest "
                    "AND with Valsalva provocation (use higher value). Peak instantaneous gradient "
                    "by continuous wave Doppler. Obstruction increases wall stress and ischemia risk.",
        example=20.0,
        ge=0,
        le=200
    )
    
    nsvt: Literal["no", "yes"] = Field(
        ...,
        description="Non-sustained ventricular tachycardia on Holter monitoring. Defined as ≥3 "
                    "consecutive ventricular beats at rate ≥120 bpm and <30 seconds duration. "
                    "Strong marker of electrical instability.",
        example="no"
    )
    
    unexplained_syncope: Literal["no", "yes"] = Field(
        ...,
        description="History of unexplained syncope at or prior to evaluation. Excludes syncope "
                    "with clear vasovagal features or identifiable trigger. May represent "
                    "aborted sudden cardiac death.",
        example="no"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "age": 45,
                "family_history_scd": "no",
                "max_wall_thickness": 18.0,
                "left_atrial_diameter": 40.0,
                "max_lvot_gradient": 20.0,
                "nsvt": "no",
                "unexplained_syncope": "no"
            }
        }


class HcmRiskScdResponse(BaseModel):
    """
    Response model for HCM Risk-SCD
    
    The calculator provides individualized 5-year SCD risk estimates:
    - Low Risk (<4%): ICD generally not indicated
    - Intermediate Risk (4-6%): ICD may be considered 
    - High Risk (≥6%): ICD should be considered
    
    Risk should be reassessed every 1-2 years or when clinical changes occur.
    Additional risk modifiers (e.g., LV aneurysm, extensive LGE) may influence
    decisions in borderline cases.
    
    Reference: O'Mahony C, et al. Eur Heart J. 2014;35(30):2010-20.
    """
    
    result: float = Field(
        ...,
        description="5-year risk of sudden cardiac death as a percentage (0-100%)",
        example=2.5,
        ge=0,
        le=100
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk",
        example="%"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with risk percentage, category, and ICD recommendations",
        example="5-year risk of SCD is 2.5% (Low Risk). ICD generally not indicated. "
                "Continue regular follow-up and reassess risk every 1-2 years or if "
                "clinical change occurs."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low 5-year SCD risk"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": 2.5,
                "unit": "%",
                "interpretation": "5-year risk of SCD is 2.5% (Low Risk). ICD generally not indicated. "
                                  "Continue regular follow-up and reassess risk every 1-2 years or if "
                                  "clinical change occurs.",
                "stage": "Low Risk",
                "stage_description": "Low 5-year SCD risk"
            }
        }