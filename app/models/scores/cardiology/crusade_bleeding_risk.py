"""
CRUSADE Score for Post-MI Bleeding Risk Models

Request and response models for CRUSADE bleeding risk calculation.

References (Vancouver style):
1. Subherwal S, Bach RG, Chen AY, et al. Baseline risk of major bleeding in 
   non-ST-segment-elevation myocardial infarction: the CRUSADE (Can Rapid risk 
   stratification of Unstable angina patients Suppress ADverse outcomes with Early 
   implementation of the ACC/AHA Guidelines) Bleeding Score. Circulation. 
   2009;119(14):1873-1882.
2. Abu-Assi E, Raposeiras-Roubin S, Lear P, et al. The risk of bleeding according 
   to the CRUSADE, ACUITY and HAS-BLED scores in acute coronary syndrome patients 
   treated with prasugrel: insights from a four-year registry. Thromb Res. 
   2013;132(6):652-658.
3. Ariza-Solé A, Sánchez-Elvira G, Sánchez-Salado JC, et al. CRUSADE bleeding 
   score validation for ST-segment-elevation myocardial infarction undergoing 
   primary percutaneous coronary intervention. Thromb Res. 2013;132(6):652-658.

The CRUSADE bleeding risk score is a validated tool for stratifying major bleeding 
risk in patients with acute coronary syndromes undergoing antithrombotic therapy. 
Developed from the CRUSADE Quality Improvement Initiative, it incorporates 8 baseline 
clinical variables to predict in-hospital major bleeding risk with scores ranging 
from 1-100 points.

The score was originally developed and validated in NSTEMI patients but has been 
subsequently validated in STEMI patients as well. It helps clinicians balance 
the competing risks of thrombosis and bleeding when selecting antithrombotic 
regimens and monitoring strategies.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict, Any


class CrusadeBleedingRiskRequest(BaseModel):
    """
    Request model for CRUSADE Score for Post-MI Bleeding Risk
    
    The CRUSADE bleeding risk score incorporates 8 clinical variables:
    
    **1. Baseline Hematocrit (%)**:
    - <31%: 9 points
    - 31-33.9%: 7 points
    - 34-36.9%: 3 points
    - 37-39.9%: 2 points
    - ≥40%: 0 points
    
    **2. Creatinine Clearance (mL/min)**:
    - ≤15: 39 points
    - 15-30: 35 points
    - 30-60: 28 points
    - 60-90: 17 points
    - 90-120: 7 points
    - >120: 0 points
    
    **3. Heart Rate (bpm)**:
    - ≤70: 0 points
    - 71-80: 1 point
    - 81-90: 3 points
    - 91-100: 6 points
    - 101-110: 8 points
    - 111-120: 10 points
    - ≥121: 11 points
    
    **4. Sex**:
    - Male: 0 points
    - Female: 8 points
    
    **5. Signs of CHF at Presentation**:
    - No: 0 points
    - Yes: 7 points
    
    **6. Diabetes Mellitus**:
    - No: 0 points
    - Yes: 6 points
    
    **7. Prior Vascular Disease**:
    - No: 0 points
    - Yes: 6 points
    
    **8. Systolic Blood Pressure (mmHg)**:
    - ≤90: 10 points
    - 91-100: 8 points
    - 101-120: 5 points
    - 121-180: 1 point
    - 181-200: 3 points
    - ≥201: 5 points
    
    **Risk Stratification**:
    - ≤20 points: Very low risk (3.1% bleeding rate)
    - 21-30 points: Low risk (5.5% bleeding rate)
    - 31-40 points: Moderate risk (8.6% bleeding rate)
    - 41-50 points: High risk (11.9% bleeding rate)
    - >50 points: Very high risk (19.5% bleeding rate)
    
    **Major Bleeding Definition**:
    - Hematocrit drop ≥12%
    - RBC transfusion when baseline hematocrit ≥28%
    - RBC transfusion with witnessed bleeding when baseline hematocrit <28%
    
    **Clinical Applications**:
    - Risk stratification for antithrombotic therapy selection
    - Monitoring intensity determination
    - Duration of dual antiplatelet therapy guidance
    - Bleeding prevention strategy development
    
    References (Vancouver style):
    1. Subherwal S, Bach RG, Chen AY, et al. Baseline risk of major bleeding in 
    non-ST-segment-elevation myocardial infarction: the CRUSADE (Can Rapid risk 
    stratification of Unstable angina patients Suppress ADverse outcomes with Early 
    implementation of the ACC/AHA Guidelines) Bleeding Score. Circulation. 
    2009;119(14):1873-1882.
    2. Abu-Assi E, Raposeiras-Roubin S, Lear P, et al. The risk of bleeding according 
    to the CRUSADE, ACUITY and HAS-BLED scores in acute coronary syndrome patients 
    treated with prasugrel: insights from a four-year registry. Thromb Res. 
    2013;132(6):652-658.
    3. Ariza-Solé A, Sánchez-Elvira G, Sánchez-Salado JC, et al. CRUSADE bleeding 
    score validation for ST-segment-elevation myocardial infarction undergoing 
    primary percutaneous coronary intervention. Thromb Res. 2013;132(6):652-658.
    """
    
    baseline_hematocrit: float = Field(
        ...,
        ge=15.0,
        le=55.0,
        description="Baseline hematocrit percentage on admission. Lower values indicate higher bleeding risk due to existing anemia",
        example=35.2
    )
    
    creatinine_clearance: float = Field(
        ...,
        ge=5.0,
        le=200.0,
        description="Calculated creatinine clearance using Cockcroft-Gault equation in mL/min. Reduced kidney function affects drug clearance and bleeding risk",
        example=65.8
    )
    
    heart_rate: int = Field(
        ...,
        ge=30,
        le=200,
        description="Heart rate on admission in beats per minute. Elevated heart rate may indicate hemodynamic instability and higher bleeding risk",
        example=88
    )
    
    patient_sex: Literal["male", "female"] = Field(
        ...,
        description="Patient biological sex. Female sex is independently associated with increased bleeding risk in acute coronary syndromes",
        example="female"
    )
    
    signs_chf: Literal["yes", "no"] = Field(
        ...,
        description="Signs of congestive heart failure at presentation (dyspnea, rales, elevated JVP, S3 gallop). Indicates higher disease severity and comorbidity burden",
        example="no"
    )
    
    diabetes_mellitus: Literal["yes", "no"] = Field(
        ...,
        description="History of diabetes mellitus (Type 1 or Type 2). Associated with vascular complications and increased bleeding risk",
        example="yes"
    )
    
    prior_vascular_disease: Literal["yes", "no"] = Field(
        ...,
        description="History of prior vascular disease including peripheral arterial disease, cerebrovascular disease, or aortic aneurysm. Indicates systemic atherosclerosis",
        example="no"
    )
    
    systolic_blood_pressure: int = Field(
        ...,
        ge=60,
        le=250,
        description="Systolic blood pressure on admission in mmHg. Both low and very high blood pressure are associated with bleeding complications",
        example=142
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "baseline_hematocrit": 35.2,
                "creatinine_clearance": 65.8,
                "heart_rate": 88,
                "patient_sex": "female",
                "signs_chf": "no",
                "diabetes_mellitus": "yes",
                "prior_vascular_disease": "no",
                "systolic_blood_pressure": 142
            }
        }


class CrusadeBleedingRiskResponse(BaseModel):
    """
    Response model for CRUSADE Score for Post-MI Bleeding Risk
    
    The CRUSADE bleeding risk score provides risk stratification for major bleeding 
    in patients with acute coronary syndromes undergoing antithrombotic therapy. 
    Scores range from 1-100 points with higher scores indicating greater bleeding risk.
    
    **Risk Categories**:
    - **≤20 points**: Very low risk (3.1% bleeding rate)
    - **21-30 points**: Low risk (5.5% bleeding rate)  
    - **31-40 points**: Moderate risk (8.6% bleeding rate)
    - **41-50 points**: High risk (11.9% bleeding rate)
    - **>50 points**: Very high risk (19.5% bleeding rate)
    
    **Clinical Applications**:
    - Selection of appropriate antithrombotic regimens
    - Determination of monitoring intensity
    - Duration of dual antiplatelet therapy guidance
    - Bleeding prevention strategy development
    
    **Major Bleeding Definition**:
    Major bleeding is defined as hematocrit drop ≥12%, RBC transfusion when 
    baseline hematocrit ≥28%, or RBC transfusion with witnessed bleeding when 
    baseline hematocrit <28%.
    
    Reference: Subherwal S, et al. Circulation. 2009;119(14):1873-1882.
    """
    
    result: int = Field(
        ...,
        ge=1,
        le=100,
        description="Total CRUSADE bleeding risk score calculated from 8 clinical variables (range: 1-100 points)",
        example=42
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the CRUSADE score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation with bleeding risk assessment and management recommendations",
        example="CRUSADE score of 42 indicates high bleeding risk (11.9% major bleeding rate). Consider reduced-dose antithrombotic regimens, shorter duration therapy, and intensive bleeding monitoring."
    )
    
    stage: str = Field(
        ...,
        description="Bleeding risk category (Very Low Risk, Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="High Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the bleeding risk category",
        example="High bleeding risk"
    )
    
    component_breakdown: Dict[str, Dict[str, Any]] = Field(
        ...,
        description="Detailed breakdown of scores for each CRUSADE component with clinical rationale",
        example={
            "hematocrit": {
                "score": 3,
                "description": "Baseline hematocrit level",
                "rationale": "Lower hematocrit indicates bleeding risk and anemia"
            },
            "creatinine_clearance": {
                "score": 17,
                "description": "Kidney function assessment",
                "rationale": "Reduced kidney function affects drug clearance and bleeding risk"
            },
            "heart_rate": {
                "score": 3,
                "description": "Heart rate on admission",
                "rationale": "Elevated heart rate may indicate hemodynamic instability"
            },
            "sex": {
                "score": 8,
                "description": "Patient biological sex",
                "rationale": "Female sex independently associated with increased bleeding risk"
            },
            "chf": {
                "score": 0,
                "description": "Signs of congestive heart failure",
                "rationale": "CHF indicates higher severity and comorbidity burden"
            },
            "diabetes": {
                "score": 6,
                "description": "History of diabetes mellitus",
                "rationale": "Diabetes associated with vascular complications and bleeding risk"
            },
            "vascular_disease": {
                "score": 0,
                "description": "Prior vascular disease history",
                "rationale": "Previous vascular disease indicates systemic atherosclerosis"
            },
            "systolic_bp": {
                "score": 1,
                "description": "Systolic blood pressure",
                "rationale": "Both low and very high BP associated with bleeding complications"
            }
        }
    )
    
    bleeding_risk_percentage: Dict[str, Any] = Field(
        ...,
        description="Estimated bleeding risk percentage based on validation studies",
        example={
            "estimated_bleeding_risk": "11.9%",
            "definition": "Major bleeding defined as hematocrit drop ≥12%, RBC transfusion (if baseline Hct ≥28%), or RBC transfusion with witnessed bleeding (if baseline Hct <28%)",
            "timeframe": "During hospitalization for acute coronary syndrome"
        }
    )
    
    clinical_recommendations: Dict[str, Any] = Field(
        ...,
        description="Evidence-based clinical recommendations for antithrombotic therapy and monitoring",
        example={
            "antithrombotic_therapy": "Reduced dose regimens preferred",
            "monitoring": "Intensive bleeding monitoring",
            "duration": "Shorter duration therapy when possible",
            "special_considerations": [
                "Consider alternative antithrombotic strategies",
                "Intensive monitoring protocols",
                "Proton pump inhibitor recommended",
                "Frequent clinical assessments",
                "Early intervention for bleeding"
            ]
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 42,
                "unit": "points",
                "interpretation": "CRUSADE score of 42 indicates high bleeding risk (11.9% major bleeding rate). Consider reduced-dose antithrombotic regimens, shorter duration therapy, and intensive bleeding monitoring.",
                "stage": "High Risk",
                "stage_description": "High bleeding risk",
                "component_breakdown": {
                    "hematocrit": {
                        "score": 3,
                        "description": "Baseline hematocrit level",
                        "rationale": "Lower hematocrit indicates bleeding risk and anemia"
                    },
                    "creatinine_clearance": {
                        "score": 17,
                        "description": "Kidney function assessment",
                        "rationale": "Reduced kidney function affects drug clearance and bleeding risk"
                    },
                    "heart_rate": {
                        "score": 3,
                        "description": "Heart rate on admission",
                        "rationale": "Elevated heart rate may indicate hemodynamic instability"
                    },
                    "sex": {
                        "score": 8,
                        "description": "Patient biological sex",
                        "rationale": "Female sex independently associated with increased bleeding risk"
                    },
                    "chf": {
                        "score": 0,
                        "description": "Signs of congestive heart failure",
                        "rationale": "CHF indicates higher severity and comorbidity burden"
                    },
                    "diabetes": {
                        "score": 6,
                        "description": "History of diabetes mellitus",
                        "rationale": "Diabetes associated with vascular complications and bleeding risk"
                    },
                    "vascular_disease": {
                        "score": 0,
                        "description": "Prior vascular disease history",
                        "rationale": "Previous vascular disease indicates systemic atherosclerosis"
                    },
                    "systolic_bp": {
                        "score": 1,
                        "description": "Systolic blood pressure",
                        "rationale": "Both low and very high BP associated with bleeding complications"
                    }
                },
                "bleeding_risk_percentage": {
                    "estimated_bleeding_risk": "11.9%",
                    "definition": "Major bleeding defined as hematocrit drop ≥12%, RBC transfusion (if baseline Hct ≥28%), or RBC transfusion with witnessed bleeding (if baseline Hct <28%)",
                    "timeframe": "During hospitalization for acute coronary syndrome"
                },
                "clinical_recommendations": {
                    "antithrombotic_therapy": "Reduced dose regimens preferred",
                    "monitoring": "Intensive bleeding monitoring",
                    "duration": "Shorter duration therapy when possible",
                    "special_considerations": [
                        "Consider alternative antithrombotic strategies",
                        "Intensive monitoring protocols",
                        "Proton pump inhibitor recommended",
                        "Frequent clinical assessments",
                        "Early intervention for bleeding"
                    ]
                }
            }
        }