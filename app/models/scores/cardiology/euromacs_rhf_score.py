"""
EUROMACS-RHF Score Models

Request and response models for EUROMACS-RHF Score calculator for predicting right heart failure 
after left ventricular assist device (LVAD) implantation.

References (Vancouver style):
1. Soliman OII, Akin S, Muslem R, Boersma E, Manintveld OC, Krabatsch T, et al. Derivation and 
   Validation of a Novel Right-Sided Heart Failure Model After Implantation of Continuous Flow 
   Left Ventricular Assist Devices: The EUROMACS (European Registry for Patients with Mechanical 
   Circulatory Support) Right-Sided Heart Failure Risk Score. Circulation. 2018 Mar 6;137(9):891-906. 
   doi: 10.1161/CIRCULATIONAHA.117.030543.
2. Bellavia D, Iacovoni A, Scardulla C, Moja L, Pilato M, Kushwaha SS, et al. Prediction of right 
   heart failure after left ventricular assist device implantation. Eur Heart J Acute Cardiovasc Care. 
   2017 Dec;6(8):668-676. doi: 10.1177/2048872615612455.
3. Kormos RL, Cowger J, Pagani FD, Teuteberg JJ, Goldstein DJ, Jacobs JP, et al. The Society of 
   Thoracic Surgeons Intermacs database annual report: evolving indications, outcomes, and scientific 
   partnerships. J Heart Lung Transplant. 2019 Feb;38(2):114-126. doi: 10.1016/j.healun.2018.11.013.

The EUROMACS-RHF Score is a validated risk prediction tool for early (<30 days) severe 
postoperative right heart failure after continuous-flow LVAD implantation. It was derived 
from 2,988 adult patients and validated in separate cohorts with good discriminative ability.
"""

from pydantic import BaseModel, Field
from typing import Literal, Dict


class EuromacsRhfScoreRequest(BaseModel):
    """
    Request model for EUROMACS-RHF Score Calculator
    
    The EUROMACS-RHF Score predicts the risk of early (<30 days) severe right heart failure 
    after left ventricular assist device (LVAD) implantation using five key clinical variables:
    
    Scoring System:
    1. RA/PCWP ratio >0.54: 2 points
       - Right atrial pressure to pulmonary capillary wedge pressure ratio
       - Indicates elevated right-sided filling pressures relative to left-sided pressures
       - Suggests right ventricular dysfunction or increased pulmonary vascular resistance
    
    2. Hemoglobin ≤10 g/dL: 1 point
       - Low hemoglobin levels associated with increased RHF risk
       - May reflect chronic disease, malnutrition, or bleeding
       - Anemia can compromise oxygen delivery and cardiac function
    
    3. Multiple intravenous inotropes: 2.5 points (highest weighted factor)
       - Use of multiple IV inotropic agents pre-operatively
       - Indicates severe heart failure requiring maximal medical support
       - Strongest predictor of post-LVAD right heart failure
    
    4. INTERMACS Class 1-3: 2 points
       - Class 1: Critical cardiogenic shock
       - Class 2: Progressive decline on inotropes
       - Class 3: Stable but inotrope dependent
       - Lower INTERMACS classes indicate more severe heart failure
    
    5. Severe right ventricular dysfunction: 2 points
       - Assessed by echocardiography
       - Indicates pre-existing RV impairment
       - Strong predictor of post-operative RV failure
    
    Risk Stratification:
    - Low Risk (0-2 points): 11% RHF incidence
    - Intermediate Risk (2.5-4 points): Intermediate incidence
    - High Risk (4.5-9.5 points): 43.1% RHF incidence
    
    Clinical Definition of RHF:
    Early severe postoperative RHF defined as receiving:
    - Short- or long-term right-sided circulatory support, OR
    - Continuous inotropic support for ≥14 days, OR
    - Nitric oxide ventilation for ≥48 hours
    
    Clinical Applications:
    - Preoperative risk assessment for LVAD candidates
    - Surgical planning and device selection
    - Perioperative monitoring intensity determination
    - Patient and family counseling
    - Resource allocation and ICU planning
    
    Key Study Characteristics:
    - Derived from 2,988 adult patients (derivation n=2000, validation n=988)
    - Primarily White (68%) and male (82%) population
    - C-index: 0.70 (derivation), 0.67 (validation)
    - Outperformed other existing risk scores
    
    References (Vancouver style):
    1. Soliman OII, et al. Circulation. 2018 Mar 6;137(9):891-906.
    2. Bellavia D, et al. Eur Heart J Acute Cardiovasc Care. 2017 Dec;6(8):668-676.
    """
    
    ra_pcwp_ratio_elevated: Literal["yes", "no"] = Field(
        ...,
        description="Right atrial pressure to pulmonary capillary wedge pressure ratio >0.54. Elevated ratio indicates right-sided pressure elevation relative to left-sided pressures, suggesting RV dysfunction or increased PVR. Worth 2 points if yes",
        example="no"
    )
    
    hemoglobin_low: Literal["yes", "no"] = Field(
        ...,
        description="Hemoglobin level ≤10 g/dL (≤100 g/L). Low hemoglobin associated with increased RHF risk, may reflect chronic disease, malnutrition, or bleeding. Worth 1 point if yes",
        example="no"
    )
    
    multiple_inotropes: Literal["yes", "no"] = Field(
        ...,
        description="Multiple intravenous inotropes pre-operatively. Use of multiple IV inotropic agents indicates severe heart failure requiring maximal medical support. Strongest predictor of post-LVAD RHF. Worth 2.5 points if yes (highest weight)",
        example="no"
    )
    
    intermacs_class_low: Literal["yes", "no"] = Field(
        ...,
        description="INTERMACS Class 1-3 (critical cardiogenic shock to stable but inotrope dependent). Lower classes indicate more severe heart failure: Class 1 (critical shock), Class 2 (progressive decline), Class 3 (stable on inotropes). Worth 2 points if yes",
        example="yes"
    )
    
    severe_rv_dysfunction: Literal["yes", "no"] = Field(
        ...,
        description="Severe right ventricular dysfunction by echocardiography. Pre-existing RV impairment assessed by echo parameters (RV function, tricuspid regurgitation, TAPSE, etc.). Strong predictor of post-operative RV failure. Worth 2 points if yes",
        example="no"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "ra_pcwp_ratio_elevated": "no",
                "hemoglobin_low": "no", 
                "multiple_inotropes": "no",
                "intermacs_class_low": "yes",
                "severe_rv_dysfunction": "no"
            }
        }


class EuromacsRhfScoreResponse(BaseModel):
    """
    Response model for EUROMACS-RHF Score Calculator
    
    Provides comprehensive risk assessment for right heart failure after LVAD implantation:
    
    Score Interpretation:
    
    Low Risk (0-2 points):
    - 11% incidence of RHF
    - Standard perioperative monitoring
    - Routine hemodynamic assessment
    - Expected shorter ICU stay
    - Better 1-year and 2-year survival
    
    Intermediate Risk (2.5-4 points):
    - Intermediate RHF incidence
    - Enhanced monitoring recommended
    - Closer hemodynamic surveillance
    - Optimization of RV support
    - More frequent RV function assessment
    
    High Risk (4.5-9.5 points):
    - 43.1% incidence of RHF
    - Intensive monitoring required
    - Proactive management strategies
    - Consider biventricular assist device
    - Consider total heart support
    - Optimize hemodynamics pre-operatively
    - Advanced RV support strategies
    - Expect prolonged ICU stay (median 24 vs 7 days)
    - Reduced survival (53% vs 71% at 1 year)
    
    Clinical Outcomes Associated with RHF:
    - Prolonged ICU stay: 24 days (IQR 14-38) vs 7 days (IQR 4-15)
    - Reduced 1-year survival: 53% vs 71%
    - Reduced 2-year survival: 45% vs 58%
    - Increased healthcare resource utilization
    - Higher complication rates
    
    Management Strategies by Risk Level:
    
    Low Risk:
    - Standard LVAD implantation protocols
    - Routine post-operative monitoring
    - Standard weaning protocols
    
    Intermediate Risk:
    - Enhanced hemodynamic monitoring
    - Closer surveillance in early post-op period
    - Optimize RV function pre-operatively
    - Consider delayed weaning
    
    High Risk:
    - Consider biventricular assist device (BiVAD)
    - Consider total artificial heart
    - Intensive hemodynamic optimization
    - Advanced RV support planning
    - Extended ICU monitoring
    - Multidisciplinary team approach
    
    External Validation:
    - Variable performance in external cohorts
    - AUC ranges from 0.58-0.67 in validation studies
    - Should be combined with clinical judgment
    - Most useful as part of comprehensive assessment
    
    Important Limitations:
    - Derived primarily from White, male population
    - External validation shows variable performance
    - Should not be used as sole decision-making tool
    - Requires clinical correlation and judgment
    - Performance may vary across institutions and populations
    
    Reference: Soliman OII, et al. Circulation. 2018;137(9):891-906.
    """
    
    result: float = Field(
        ...,
        description="EUROMACS-RHF Score total points (range: 0-9.5 points)",
        example=2.0
    )
    
    unit: str = Field(
        ...,
        description="Unit of measurement for the score (points)",
        example="points"
    )
    
    interpretation: str = Field(
        ...,
        description="Clinical interpretation including risk level, RHF incidence, and management recommendations",
        example="EUROMACS-RHF Score: 2.0 points. LOW RISK of right heart failure after LVAD implantation (11% incidence). Standard perioperative monitoring and management recommended. Consider routine hemodynamic assessment post-LVAD implantation with standard protocols."
    )
    
    stage: str = Field(
        ...,
        description="Risk stratification level (Low Risk, Intermediate Risk, High Risk)",
        example="Low Risk"
    )
    
    stage_description: str = Field(
        ...,
        description="Brief description of the risk level",
        example="Low risk for RHF"
    )
    
    risk_category: str = Field(
        ...,
        description="Risk category classification based on score",
        example="Low Risk"
    )
    
    rhf_incidence: str = Field(
        ...,
        description="Expected incidence of right heart failure for this risk level",
        example="11%"
    )
    
    score_breakdown: Dict[str, float] = Field(
        ...,
        description="Detailed breakdown of score components showing individual contributions",
        example={
            "ra_pcwp_ratio_elevated": 0,
            "hemoglobin_low": 0,
            "multiple_inotropes": 0,
            "intermacs_class_low": 2.0,
            "severe_rv_dysfunction": 0
        }
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "result": 2.0,
                "unit": "points",
                "interpretation": "EUROMACS-RHF Score: 2.0 points. LOW RISK of right heart failure after LVAD implantation (11% incidence). Standard perioperative monitoring and management recommended. Consider routine hemodynamic assessment post-LVAD implantation with standard protocols.",
                "stage": "Low Risk",
                "stage_description": "Low risk for RHF",
                "risk_category": "Low Risk",
                "rhf_incidence": "11%",
                "score_breakdown": {
                    "ra_pcwp_ratio_elevated": 0,
                    "hemoglobin_low": 0,
                    "multiple_inotropes": 0,
                    "intermacs_class_low": 2.0,
                    "severe_rv_dysfunction": 0
                }
            }
        }