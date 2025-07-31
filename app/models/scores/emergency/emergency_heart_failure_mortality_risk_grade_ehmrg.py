"""
Emergency Heart Failure Mortality Risk Grade (EHMRG) Models

Request and response models for EHMRG calculation.

References (Vancouver style):
1. Lee DS, Stitt A, Austin PC, Stukel TA, Schull MJ, Charl G, et al. Prediction of 
   heart failure mortality in emergent care: a cohort study. Ann Intern Med. 
   2012;156(11):767-75, W-261, W-262. doi: 10.7326/0003-4819-156-11-201206050-00003.
2. Stiell IG, Clement CM, Brison RJ, Rowe BH, Borgundvaag B, Aaron SD, et al. A risk 
   scoring system to identify emergency department patients with heart failure at high 
   risk for serious adverse events. Acad Emerg Med. 2013;20(1):17-26. doi: 10.1111/acem.12056.
3. Chouihed T, Manzo-Silberman S, Peschanski N, Charpentier S, Gil-Jardrin E, Chkair B, et al. 
   Emergency Heart Failure Mortality Risk Grade score performance for 7-day mortality prediction 
   in patients with heart failure attended at the emergency department: validation in a Spanish 
   cohort. Eur J Emerg Med. 2017;24(3):169-177. doi: 10.1097/MEJ.0000000000000391.

The Emergency Heart Failure Mortality Risk Grade (EHMRG) is a validated risk prediction tool 
that estimates 7-day mortality risk in emergency department patients presenting with acute 
heart failure. The score uses ten clinical variables routinely collected on arrival to provide 
personalized risk stratification and guide clinical decision-making.

Clinical utility includes identifying patients at very low risk who may be suitable for 
accelerated discharge pathways, as well as high-risk patients who require intensive monitoring 
and advanced heart failure interventions.
"""

from pydantic import BaseModel, Field
from typing import Literal


class EmergencyHeartFailureMortalityRiskGradeEhmrgRequest(BaseModel):
    """
    Request model for Emergency Heart Failure Mortality Risk Grade (EHMRG)
    
    The EHMRG uses 10 clinical variables readily available in the emergency department
    to predict 7-day mortality risk in patients presenting with acute heart failure:
    
    Demographics and Presentation:
    - Age (continuous variable, multiplied by 2 in scoring)
    - EMS transport (60 points if arrived by ambulance)
    
    Vital Signs:
    - Systolic blood pressure (capped at 160 mmHg, negative multiplier)
    - Heart rate (constrained to 80-120 bpm range, positive multiplier)
    - Oxygen saturation (capped at 92%, negative multiplier of 2)
    
    Laboratory Values:
    - Creatinine (multiplied by 20 in scoring)
    - Potassium (categorical scoring: ≤3.9=5pts, 4.0-4.5=0pts, ≥4.6=30pts)
    - Troponin elevation above upper limit of normal (60 points if elevated)
    
    Clinical Factors:
    - Active cancer diagnosis (45 points if present)
    - Current metolazone use at home (60 points if used)
    
    Scoring Formula:
    Score = (2 × age) + (60 if EMS) + (-1 × min(SBP,160)) + (1 × max(80,min(HR,120))) 
            + (-2 × min(O2sat,92)) + (20 × creatinine) + K_points + (60 if troponin↑) 
            + (45 if cancer) + (60 if metolazone) + 12
    
    Risk Categories:
    - Risk Group 1 (≤-49.1): 7-day mortality 0.5%
    - Risk Group 2 (-49.0 to -15.9): 7-day mortality 0.3%
    - Risk Group 3 (-15.8 to 17.9): 7-day mortality 0.7%
    - Risk Group 4 (18.0 to 56.5): 7-day mortality 2.1%
    - Risk Group 5a (56.6 to 89.3): 7-day mortality 3.3%
    - Risk Group 5b (≥89.4): 7-day mortality 8.0%
    
    Clinical Applications:
    - Risk stratification for disposition decisions
    - Identification of candidates for accelerated discharge
    - Recognition of patients requiring intensive monitoring
    - Guide for cardiology consultation and advanced therapies
    - Objective tool to supplement clinical judgment
    
    Validation and Performance:
    - Derived and validated in large cohorts of ED heart failure patients
    - Superior performance compared to physician risk estimates
    - Validated internationally across different healthcare systems
    - C-statistic typically >0.70 for 7-day mortality prediction
    
    References (Vancouver style):
    1. Lee DS, Stitt A, Austin PC, Stukel TA, Schull MJ, Charl G, et al. Prediction of 
    heart failure mortality in emergent care: a cohort study. Ann Intern Med. 
    2012;156(11):767-75, W-261, W-262. doi: 10.7326/0003-4819-156-11-201206050-00003.
    2. Stiell IG, Clement CM, Brison RJ, Rowe BH, Borgundvaag B, Aaron SD, et al. A risk 
    scoring system to identify emergency department patients with heart failure at high 
    risk for serious adverse events. Acad Emerg Med. 2013;20(1):17-26. doi: 10.1111/acem.12056.
    3. Chouihed T, Manzo-Silberman S, Peschanski N, Charpentier S, Gil-Jardrin E, Chkair B, et al. 
    Emergency Heart Failure Mortality Risk Grade score performance for 7-day mortality prediction 
    in patients with heart failure attended at the emergency department: validation in a Spanish 
    cohort. Eur J Emerg Med. 2017;24(3):169-177. doi: 10.1097/MEJ.0000000000000391.
    """
    
    age: int = Field(
        ...,
        description="Patient age in years. Multiplied by 2 in the scoring formula",
        ge=18,
        le=120,
        example=75
    )
    
    ems_transport: Literal["yes", "no"] = Field(
        ...,
        description="Arrival by Emergency Medical Services (ambulance) transport. Adds 60 points if yes",
        example="yes"
    )
    
    systolic_bp: int = Field(
        ...,
        description="Systolic blood pressure on arrival in mmHg. Capped at 160 mmHg for calculation (negative multiplier)",
        ge=40,
        le=300,
        example=110
    )
    
    heart_rate: int = Field(
        ...,
        description="Heart rate on arrival in beats per minute. Constrained to 80-120 bpm range for calculation",
        ge=30,
        le=200,
        example=95
    )
    
    oxygen_saturation: int = Field(
        ...,
        description="Oxygen saturation on arrival as percentage. Capped at 92% for calculation (negative multiplier of 2)",
        ge=50,
        le=100,
        example=88
    )
    
    creatinine: float = Field(
        ...,
        description="Serum creatinine level in mg/dL. Multiplied by 20 in the scoring formula",
        ge=0.1,
        le=20.0,
        example=1.8
    )
    
    potassium: float = Field(
        ...,
        description="Serum potassium level in mmol/L. Categorical scoring: ≤3.9=5pts, 4.0-4.5=0pts, ≥4.6=30pts",
        ge=2.0,
        le=8.0,
        example=4.2
    )
    
    troponin_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Troponin level above the upper limit of normal. Adds 60 points if elevated",
        example="no"
    )
    
    active_cancer: Literal["yes", "no"] = Field(
        ...,
        description="Presence of active cancer diagnosis. Adds 45 points if present",
        example="no"
    )
    
    metolazone_use: Literal["yes", "no"] = Field(
        ...,
        description="Current home use of metolazone diuretic. Adds 60 points if used",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "age": 75,
                "ems_transport": "yes",
                "systolic_bp": 110,
                "heart_rate": 95,
                "oxygen_saturation": 88,
                "creatinine": 1.8,
                "potassium": 4.2,
                "troponin_elevated": "no",
                "active_cancer": "no",
                "metolazone_use": "no"
            }
        }


class EmergencyHeartFailureMortalityRiskGradeEhmrgResponse(BaseModel):
    """
    Response model for Emergency Heart Failure Mortality Risk Grade (EHMRG)
    
    The EHMRG score ranges from approximately -248 to 400+ points and classifies 
    patients into six risk groups for 7-day mortality prediction:
    
    Risk Group 1 (≤-49.1 points) - Very Low Risk:
    - 7-day mortality rate: 0.5%
    - Management: Standard heart failure care with routine follow-up
    - Consider early discharge planning if clinically stable
    
    Risk Group 2 (-49.0 to -15.9 points) - Low Risk:
    - 7-day mortality rate: 0.3%
    - Management: Standard care with close outpatient follow-up
    - May be suitable for accelerated discharge pathway
    
    Risk Group 3 (-15.8 to 17.9 points) - Intermediate Risk:
    - 7-day mortality rate: 0.7%
    - Management: Careful monitoring and standard inpatient care
    - Optimize heart failure therapy and ensure adequate follow-up
    
    Risk Group 4 (18.0 to 56.5 points) - High Risk:
    - 7-day mortality rate: 2.1%
    - Management: Intensive monitoring and aggressive treatment
    - Consider cardiology consultation and advanced therapies
    
    Risk Group 5a (56.6 to 89.3 points) - Very High Risk:
    - 7-day mortality rate: 3.3%
    - Management: Immediate intensive intervention required
    - Strong consideration for ICU-level care and specialist consultation
    
    Risk Group 5b (≥89.4 points) - Highest Risk:
    - 7-day mortality rate: 8.0%
    - Management: Immediate intensive care required
    - Urgent specialist consultation and advanced mechanical support consideration
    
    Clinical Decision Support:
    - Risk groups 1-2: Consider accelerated discharge with appropriate follow-up
    - Risk group 3: Standard inpatient management with careful monitoring
    - Risk groups 4-5: Intensive management, specialist consultation, advanced therapies
    - All groups: Clinical judgment should supplement risk score interpretation
    
    Performance Characteristics:
    - C-statistic typically >0.70 for 7-day mortality prediction
    - Superior to physician risk estimates for identifying high and low-risk patients
    - Validated across multiple international healthcare systems
    - Electronic calculation recommended to minimize computational errors
    
    Reference: Lee DS, et al. Ann Intern Med. 2012;156(11):767-75.
    """
    
    result: float = Field(
        ...,
        description="EHMRG score for 7-day mortality risk prediction (range approximately -248 to 400+ points)",
        example=45.2
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the risk score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on the EHMRG risk score",
        example="7-day mortality rate 2.1%. High risk requiring intensive monitoring and aggressive management. Consider cardiology consultation, advanced heart failure therapies, and close inpatient observation."
    )
    
    stage: str = Field(
        ...,
        description="Risk group classification (Risk Group 1-5b with descriptive risk level)",
        example="Risk Group 4 (High)"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk category",
        example="High 7-day mortality risk"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 45.2,
                "unit": "points",
                "interpretation": "7-day mortality rate 2.1%. High risk requiring intensive monitoring and aggressive management. Consider cardiology consultation, advanced heart failure therapies, and close inpatient observation.",
                "stage": "Risk Group 4 (High)",
                "stage_description": "High 7-day mortality risk"
            }
        }