"""
Duke Treadmill Score Models

Request and response models for Duke Treadmill Score calculation.

References (Vancouver style):
1. Mark DB, Shaw L, Harrell FE Jr, Hlatky MA, Lee KL, Bengtson JR, et al. Prognostic 
   value of a treadmill exercise score in outpatients with suspected coronary artery 
   disease. N Engl J Med. 1991;325(12):849-53. doi: 10.1056/NEJM199109193251204.
2. Mark DB, Hlatky MA, Harrell FE Jr, Lee KL, Califf RM, Pryor DB. Exercise treadmill 
   score for predicting prognosis in coronary artery disease. Ann Intern Med. 1987;106(6):793-800. 
   doi: 10.7326/0003-4819-106-6-793.
3. Shaw LJ, Peterson ED, Shaw LK, Kesler KL, DeLong ER, Harrell FE Jr, et al. Use of 
   a prognostic treadmill score in identifying diagnostic coronary disease subgroups. 
   Circulation. 1998;98(16):1622-30. doi: 10.1161/01.cir.98.16.1622.

The Duke Treadmill Score (DTS) is a prognostic tool that combines exercise capacity, 
electrocardiographic response, and symptom response during exercise testing to predict 
the likelihood of significant coronary artery disease and long-term prognosis. 
Developed in 1987, it remains one of the most validated and widely used exercise 
testing scores for risk stratification in patients with suspected CAD.
"""

from pydantic import BaseModel, Field
from typing import Literal


class DukeTreadmillScoreRequest(BaseModel):
    """
    Request model for Duke Treadmill Score
    
    The Duke Treadmill Score uses three key parameters from exercise stress testing:
    
    Exercise Time (Bruce Protocol):
    - Standard Bruce protocol with increasing speed and grade every 3 minutes
    - Stage 1: 1.7 mph, 10% grade (1.7 METs)
    - Stage 2: 2.5 mph, 12% grade (4.0 METs)
    - Stage 3: 3.4 mph, 14% grade (7.0 METs)
    - Stage 4: 4.2 mph, 16% grade (10.0 METs)
    - Stage 5: 5.0 mph, 18% grade (13.0 METs)
    - Longer exercise time indicates better functional capacity and lower risk
    
    ST Deviation:
    - Maximum ST segment change (elevation or depression) during exercise or recovery
    - Measured in any lead except aVR (which is typically ignored)
    - ST depression ≥1mm (0.1mV) horizontal or downsloping is considered positive
    - ST elevation may indicate transmural ischemia or previous MI with wall motion abnormality
    - Greater ST deviation indicates higher likelihood of significant CAD
    
    Angina Index:
    - 0 = No angina during exercise (best prognosis)
    - 1 = Non-limiting angina (typical or atypical chest pain that doesn't stop exercise)
    - 2 = Exercise-limiting angina (chest pain that forces termination of exercise)
    - Higher angina index indicates greater symptom burden and higher risk
    
    Formula: DTS = Exercise time (minutes) - (5 × ST deviation in mm) - (4 × angina index)
    
    Risk Stratification:
    - Low risk (DTS > 5): 5-year survival 97%, mostly no CAD or single-vessel disease
    - Intermediate risk (DTS -10 to 4): 5-year survival 90%, variable CAD severity
    - High risk (DTS < -11): 5-year survival 65%, 74% have 3-vessel or left main CAD
    
    Clinical Applications:
    - Initial risk assessment in patients with suspected CAD
    - Prognostic evaluation after acute coronary syndromes
    - Guidance for further testing (stress imaging, coronary angiography)
    - Preoperative risk assessment for non-cardiac surgery
    - Exercise prescription and cardiac rehabilitation planning
    
    Limitations:
    - Requires interpretable baseline ECG (not reliable with LBBB, paced rhythm)
    - May be less accurate in women and elderly patients
    - Cannot assess viability or localize ischemia
    - Limited by patient's ability to achieve adequate exercise workload
    - Less reliable in presence of significant valvular disease
    
    References (Vancouver style):
    1. Mark DB, Shaw L, Harrell FE Jr, Hlatky MA, Lee KL, Bengtson JR, et al. Prognostic 
       value of a treadmill exercise score in outpatients with suspected coronary artery 
       disease. N Engl J Med. 1991;325(12):849-53.
    2. Mark DB, Hlatky MA, Harrell FE Jr, Lee KL, Califf RM, Pryor DB. Exercise treadmill 
       score for predicting prognosis in coronary artery disease. Ann Intern Med. 1987;106(6):793-800.
    3. Shaw LJ, Peterson ED, Shaw LK, Kesler KL, DeLong ER, Harrell FE Jr, et al. Use of 
       a prognostic treadmill score in identifying diagnostic coronary disease subgroups. 
       Circulation. 1998;98(16):1622-30.
    """
    
    exercise_time: float = Field(
        ...,
        description="Exercise time in minutes using standard Bruce protocol. Reflects functional capacity and cardiopulmonary fitness",
        example=9.0,
        ge=0.0,
        le=30.0
    )
    
    st_deviation: float = Field(
        ...,
        description="Maximum ST segment change (elevation or depression) in mm in any lead except aVR during exercise or recovery. Positive values indicate ST elevation, negative values indicate ST depression",
        example=2.0,
        ge=-10.0,
        le=10.0
    )
    
    angina_index: Literal[0, 1, 2] = Field(
        ...,
        description="Angina severity during exercise: 0 = no angina, 1 = non-limiting angina (doesn't stop exercise), 2 = exercise-limiting angina (forces exercise termination)",
        example=0
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "exercise_time": 9.0,
                "st_deviation": 2.0,
                "angina_index": 0
            }
        }


class DukeTreadmillScoreResponse(BaseModel):
    """
    Response model for Duke Treadmill Score
    
    The Duke Treadmill Score provides prognostic information and guides clinical 
    decision-making in patients with suspected coronary artery disease:
    
    Low Risk (DTS > 5):
    - 5-year survival: 97%
    - CAD prevalence: Most patients have no CAD or single-vessel disease
    - Management: Conservative approach with medical therapy and risk factor modification
    - Follow-up: Routine clinical follow-up, repeat testing if symptoms change
    - Prognosis: Excellent long-term prognosis with low cardiac event rate
    
    Intermediate Risk (DTS -10 to 4):
    - 5-year survival: 90%
    - CAD prevalence: Variable, may have single or multi-vessel disease
    - Management: Consider further non-invasive testing based on clinical context
    - Testing options: Stress echocardiography, nuclear perfusion imaging, coronary CT angiography
    - Decision factors: Clinical presentation, risk factors, patient preferences
    
    High Risk (DTS < -11):
    - 5-year survival: 65%
    - CAD prevalence: 74% have 3-vessel or left main coronary artery disease
    - Management: Strong indication for coronary angiography per ACC/AHA guidelines
    - Urgent evaluation: Consider cardiology consultation and invasive assessment
    - Treatment: High likelihood of benefit from revascularization (PCI or CABG)
    
    Clinical Decision Making:
    - Integrates functional capacity, ischemic response, and symptom severity
    - Correlates with coronary anatomy and need for revascularization
    - Guides resource utilization and cost-effective care
    - Provides objective risk assessment for patient counseling
    - Supports shared decision-making regarding further testing and treatment
    
    Important Considerations:
    - Score should be interpreted with clinical context and other risk factors
    - Results may be less reliable in certain populations (women, elderly, diabetes)
    - Submaximal exercise testing may underestimate risk
    - Consider alternative testing if baseline ECG is uninterpretable
    - Combine with other clinical data for comprehensive risk assessment
    
    Prognostic Value:
    - Validated in large patient cohorts with long-term follow-up
    - Correlates with cardiac mortality and major adverse events
    - Maintains prognostic value across different patient populations
    - Cost-effective tool for initial risk stratification
    - Widely accepted standard for exercise testing interpretation
    
    Reference: Mark DB, et al. N Engl J Med. 1991;325(12):849-53.
    """
    
    result: float = Field(
        ...,
        description="Duke Treadmill Score calculated using the formula: Exercise time - (5 × ST deviation) - (4 × angina index)",
        example=1.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation and management recommendations based on risk stratification",
        example="Intermediate risk for coronary artery disease (DTS = 1.0) with 5-year survival of 90%. Consider further non-invasive testing (stress imaging, coronary CT angiography) or cardiology consultation based on clinical context and risk factors."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Intermediate Risk, High Risk)",
        example="Intermediate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Intermediate risk for coronary artery disease"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 1.0,
                "unit": "points",
                "interpretation": "Intermediate risk for coronary artery disease (DTS = 1.0) with 5-year survival of 90%. Consider further non-invasive testing (stress imaging, coronary CT angiography) or cardiology consultation based on clinical context and risk factors.",
                "stage": "Intermediate Risk",
                "stage_description": "Intermediate risk for coronary artery disease"
            }
        }