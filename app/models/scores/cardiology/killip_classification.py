"""
Killip Classification for Heart Failure Models

Request and response models for Killip Classification calculation.

References (Vancouver style):
1. Killip T 3rd, Kimball JT. Treatment of myocardial infarction in a coronary 
   care unit. A two year experience with 250 patients. Am J Cardiol. 1967 
   Oct;20(4):457-64.
2. Khot UN, Jia G, Moliterno DJ, Lincoff AM, Khot MB, Harrington RA, Topol EJ. 
   Prognostic importance of physical examination for heart failure in non-ST-elevation 
   acute coronary syndromes: the enduring value of Killip classification. JAMA. 
   2003 Oct 22;290(16):2174-81.
3. Mello BH, Oliveira GB, Ramos RF, Lopes BB, Barros CB, Carvalho Ede O, et al. 
   Validation of the Killip-Kimball classification and late mortality after acute 
   myocardial infarction. Arq Bras Cardiol. 2014 Aug;103(2):107-17.
4. DeGeare VS, Boura JA, Grines LL, O'Neill WW, Grines CL. Predictive value of 
   the Killip classification in patients undergoing primary percutaneous coronary 
   intervention for acute myocardial infarction. Am J Cardiol. 2001 May 1;87(9):1035-8.

The Killip Classification is a bedside clinical tool that stratifies patients with 
acute coronary syndrome (both STEMI and NSTEMI) based on physical examination findings 
of heart failure. Developed in 1967, it remains one of the most powerful predictors 
of mortality in ACS patients, even in the modern era of reperfusion therapy.

The classification uses simple physical examination findings to categorize patients 
into four classes:
- Class I: No signs of heart failure
- Class II: Mild-moderate heart failure (S3, rales, elevated JVP)
- Class III: Frank pulmonary edema
- Class IV: Cardiogenic shock

This tool is particularly valuable for rapid bedside risk stratification in emergency 
settings and can guide treatment decisions including the urgency of revascularization, 
use of mechanical circulatory support, and intensity of monitoring.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class KillipClassificationRequest(BaseModel):
    """
    Request model for Killip Classification for Heart Failure
    
    The Killip Classification requires only a single parameter based on clinical 
    examination findings at presentation:
    
    Class Definitions:
    - Class I: No clinical signs of heart failure
    - Class II: Presence of S3 gallop and/or basal lung rales  
    - Class III: Frank acute pulmonary edema
    - Class IV: Cardiogenic shock (SBP <90 mmHg with signs of hypoperfusion)
    
    Clinical Applications:
    - Risk stratification in acute coronary syndrome (STEMI and NSTEMI)
    - Guide treatment urgency and intensity
    - Predict short-term and long-term mortality
    - Help determine need for mechanical circulatory support
    
    Important Notes:
    - Assessment should be performed at initial presentation
    - Serial assessments can track response to treatment
    - Higher Killip class is associated with larger infarct size
    - Remains predictive even in the era of primary PCI
    
    References (Vancouver style):
    1. Killip T 3rd, Kimball JT. Treatment of myocardial infarction in a coronary 
       care unit. A two year experience with 250 patients. Am J Cardiol. 1967 
       Oct;20(4):457-64.
    2. Khot UN, Jia G, Moliterno DJ, Lincoff AM, Khot MB, Harrington RA, Topol EJ. 
       Prognostic importance of physical examination for heart failure in non-ST-elevation 
       acute coronary syndromes: the enduring value of Killip classification. JAMA. 
       2003 Oct 22;290(16):2174-81.
    """
    
    killip_class: Literal["class_i", "class_ii", "class_iii", "class_iv"] = Field(
        ...,
        description="Killip class based on clinical examination findings. "
                   "Class I: No signs of heart failure (no S3, clear lungs). "
                   "Class II: S3 gallop and/or basal rales on auscultation. "
                   "Class III: Acute pulmonary edema with rales throughout lung fields. "
                   "Class IV: Cardiogenic shock with hypotension and signs of hypoperfusion.",
        example="class_ii"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "killip_class": "class_ii"
            }
        }


class KillipClassificationResponse(BaseModel):
    """
    Response model for Killip Classification for Heart Failure
    
    Provides the Killip class with associated mortality risk estimates based on 
    both historical and contemporary data. Mortality rates have decreased since 
    the original 1967 study due to advances in reperfusion therapy and medical 
    management, but the relative risk stratification remains valid.
    
    Risk Categories:
    - Class I (Low Risk): No heart failure, excellent prognosis
    - Class II (Moderate Risk): Mild-moderate heart failure
    - Class III (High Risk): Severe heart failure with pulmonary edema
    - Class IV (Very High Risk): Cardiogenic shock, highest mortality
    
    Clinical Implications:
    - Higher Killip class indicates need for more aggressive therapy
    - Class III-IV often require mechanical circulatory support consideration
    - Serial assessment can track response to treatment
    - Helps determine appropriate level of care (CCU vs. step-down)
    
    Modern Era Considerations:
    - Mortality rates are lower than original study due to reperfusion therapy
    - Early revascularization particularly benefits higher Killip classes
    - Still one of the strongest predictors of outcomes in ACS
    
    Reference: Killip T 3rd, Kimball JT. Am J Cardiol. 1967;20(4):457-64.
    """
    
    result: Dict[str, str] = Field(
        ...,
        description="Killip classification result containing class, description, and mortality estimates",
        example={
            "class": "II",
            "description": "S3 and basal rales on auscultation",
            "mortality_30_day": "5-12%",
            "in_hospital_mortality": "<17%"
        }
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the classification",
        example="classification"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk assessment, expected outcomes, "
                   "and management recommendations based on the Killip class",
        example="Killip Class II: S3 and basal rales on auscultation. 30-day mortality: 5-12%, In-hospital mortality: <17%. Moderate risk with evidence of mild to moderate heart failure. Consider diuretics for congestion, optimize medical therapy, and maintain close hemodynamic monitoring. May benefit from early invasive strategy if NSTEMI."
    )
    
    stage: str = Field(
        ...,
        description="Risk category (Low Risk, Moderate Risk, High Risk, Very High Risk)",
        example="Moderate Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the heart failure severity",
        example="Mild-moderate heart failure"
    )
    
    class Config:
        schema_extra = {
            "example": {
                "result": {
                    "class": "II",
                    "description": "S3 and basal rales on auscultation",
                    "mortality_30_day": "5-12%",
                    "in_hospital_mortality": "<17%"
                },
                "unit": "classification",
                "interpretation": "Killip Class II: S3 and basal rales on auscultation. 30-day mortality: 5-12%, In-hospital mortality: <17%. Moderate risk with evidence of mild to moderate heart failure. Consider diuretics for congestion, optimize medical therapy, and maintain close hemodynamic monitoring. May benefit from early invasive strategy if NSTEMI.",
                "stage": "Moderate Risk",
                "stage_description": "Mild-moderate heart failure"
            }
        }