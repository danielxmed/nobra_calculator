"""
GRACE ACS Risk and Mortality Calculator

The GRACE (Global Registry of Acute Coronary Events) ACS Risk Score is a validated 
tool for estimating admission to 6-month mortality risk in patients with acute coronary 
syndrome. It uses 8 clinical variables to provide comprehensive risk stratification 
and guide treatment decisions for both ST-elevation and non-ST-elevation ACS patients.

The score helps clinicians:
- Identify high-risk patients who would benefit from intensive monitoring and aggressive interventions
- Guide decisions about early invasive strategies vs. conservative management
- Stratify patients for appropriate level of care and resource allocation
- Provide evidence-based prognostic information to patients and families
- Support clinical decision-making in acute coronary syndrome management

References (Vancouver style):
1. Fox KA, Dabbous OH, Goldberg RJ, Pieper KS, Eagle KA, Van de Werf F, et al. 
   Prediction of risk of death and myocardial infarction in the six months after 
   presentation with acute coronary syndrome: prospective multinational observational 
   study (GRACE). BMJ. 2006;333(7578):1091. doi: 10.1136/bmj.38985.646481.55.
2. Granger CB, Goldberg RJ, Dabbous O, Pieper KS, Eagle KA, Cannon CP, et al. 
   Predictors of hospital mortality in the global registry of acute coronary events. 
   Arch Intern Med. 2003;163(19):2345-53. doi: 10.1001/archinte.163.19.2345.
3. Abu-Assi E, Gracía-Acuña JM, Peña-Gil C, González-Juanatey JR. Validation of 
   the GRACE risk score for predicting death within 6 months of follow-up in a 
   contemporary cohort of patients with acute coronary syndrome. Rev Esp Cardiol 
   (Engl Ed). 2010;63(6):640-8. doi: 10.1016/s1885-5857(10)70139-4.
"""

import math
from typing import Dict, Any


class GraceAcsRiskCalculator:
    """Calculator for GRACE ACS Risk and Mortality Score"""
    
    def __init__(self):
        # Killip class points
        self.KILLIP_POINTS = {
            "class_1": 0,    # No CHF
            "class_2": 20,   # Pulmonary rales or JVD
            "class_3": 39,   # Pulmonary edema
            "class_4": 59    # Cardiogenic shock
        }
        
        # Binary risk factor points
        self.BINARY_POINTS = {
            "st_deviation": 28,
            "elevated_biomarkers": 14,
            "cardiac_arrest": 39
        }
        
        # Risk category thresholds and interpretations
        self.RISK_CATEGORIES = [
            {"min": 0, "max": 87, "risk": "Very Low Risk", "mortality": "0-2%", "description": "Excellent prognosis"},
            {"min": 88, "max": 128, "risk": "Low Risk", "mortality": "3-10%", "description": "Good prognosis"},
            {"min": 129, "max": 149, "risk": "Intermediate Risk", "mortality": "10-20%", "description": "Moderate prognosis"},
            {"min": 150, "max": 173, "risk": "High Risk", "mortality": "20-30%", "description": "Poor prognosis"},
            {"min": 174, "max": 284, "risk": "Very High Risk", "mortality": "40-90%", "description": "Very poor prognosis"},
            {"min": 285, "max": 400, "risk": "Extremely High Risk", "mortality": "≥99%", "description": "Critical prognosis"}
        ]
    
    def calculate(self, age: int, heart_rate: int, systolic_bp: int, creatinine: float,
                 killip_class: str, cardiac_arrest: str, st_deviation: str,
                 elevated_biomarkers: str) -> Dict[str, Any]:
        """
        Calculates GRACE ACS Risk Score from clinical parameters
        
        Args:
            age (int): Patient age in years
            heart_rate (int): Heart rate in beats per minute
            systolic_bp (int): Systolic blood pressure in mmHg
            creatinine (float): Serum creatinine in mg/dL
            killip_class (str): Killip class (class_1, class_2, class_3, class_4)
            cardiac_arrest (str): Cardiac arrest at admission (yes/no)
            st_deviation (str): ST segment deviation on ECG (yes/no)
            elevated_biomarkers (str): Elevated cardiac enzymes/biomarkers (yes/no)
            
        Returns:
            Dict with GRACE score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, heart_rate, systolic_bp, creatinine, killip_class,
                            cardiac_arrest, st_deviation, elevated_biomarkers)
        
        # Calculate component scores
        age_score = self._calculate_age_score(age)
        hr_score = self._calculate_heart_rate_score(heart_rate)
        bp_score = self._calculate_systolic_bp_score(systolic_bp)
        creat_score = self._calculate_creatinine_score(creatinine)
        killip_score = self.KILLIP_POINTS[killip_class]
        
        # Calculate binary risk factor scores
        st_score = self.BINARY_POINTS["st_deviation"] if st_deviation == "yes" else 0
        biomarker_score = self.BINARY_POINTS["elevated_biomarkers"] if elevated_biomarkers == "yes" else 0
        arrest_score = self.BINARY_POINTS["cardiac_arrest"] if cardiac_arrest == "yes" else 0
        
        # Calculate total GRACE score
        total_score = (age_score + hr_score + bp_score + creat_score + killip_score + 
                      st_score + biomarker_score + arrest_score)
        
        # Get clinical interpretation
        interpretation = self._get_interpretation(total_score, age, heart_rate, systolic_bp,
                                                creatinine, killip_class, cardiac_arrest,
                                                st_deviation, elevated_biomarkers)
        
        return {
            "result": int(total_score),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, heart_rate: int, systolic_bp: int, creatinine: float,
                        killip_class: str, cardiac_arrest: str, st_deviation: str,
                        elevated_biomarkers: str):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 20 or age > 100:
            raise ValueError("Age must be an integer between 20 and 100 years")
        
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 250:
            raise ValueError("Heart rate must be an integer between 30 and 250 bpm")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 50 or systolic_bp > 300:
            raise ValueError("Systolic BP must be an integer between 50 and 300 mmHg")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.3 or creatinine > 15.0:
            raise ValueError("Creatinine must be between 0.3 and 15.0 mg/dL")
        
        if killip_class not in self.KILLIP_POINTS:
            raise ValueError(f"Killip class must be one of: {list(self.KILLIP_POINTS.keys())}")
        
        binary_params = [
            ("cardiac_arrest", cardiac_arrest),
            ("st_deviation", st_deviation),
            ("elevated_biomarkers", elevated_biomarkers)
        ]
        
        for param_name, param_value in binary_params:
            if param_value not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _calculate_age_score(self, age: int) -> float:
        """
        Calculates age component score using GRACE algorithm
        
        Based on published GRACE scoring system where age contributes
        significantly to mortality risk in ACS patients
        """
        # GRACE age scoring: approximately 2.5 points per year over 40
        if age <= 40:
            return 0
        else:
            return (age - 40) * 2.5
    
    def _calculate_heart_rate_score(self, heart_rate: int) -> int:
        """
        Calculates heart rate component score
        
        Based on GRACE heart rate categories and their associated points
        """
        if heart_rate < 50:
            return 0
        elif heart_rate < 70:
            return 3
        elif heart_rate < 90:
            return 9
        elif heart_rate < 110:
            return 15
        elif heart_rate < 150:
            return 24
        elif heart_rate < 200:
            return 38
        else:
            return 46
    
    def _calculate_systolic_bp_score(self, systolic_bp: int) -> int:
        """
        Calculates systolic blood pressure component score
        
        Lower BP associated with higher mortality risk in ACS
        """
        if systolic_bp < 80:
            return 58
        elif systolic_bp < 100:
            return 53
        elif systolic_bp < 120:
            return 43
        elif systolic_bp < 140:
            return 34
        elif systolic_bp < 160:
            return 24
        elif systolic_bp < 200:
            return 10
        else:
            return 0
    
    def _calculate_creatinine_score(self, creatinine: float) -> int:
        """
        Calculates serum creatinine component score
        
        Renal dysfunction is associated with increased mortality in ACS
        """
        if creatinine < 0.40:
            return 1
        elif creatinine < 0.80:
            return 4
        elif creatinine < 1.20:
            return 7
        elif creatinine < 1.60:
            return 10
        elif creatinine < 2.00:
            return 13
        elif creatinine < 4.00:
            return 21
        else:
            return 28
    
    def _get_interpretation(self, score: int, age: int, heart_rate: int, systolic_bp: int,
                          creatinine: float, killip_class: str, cardiac_arrest: str,
                          st_deviation: str, elevated_biomarkers: str) -> Dict[str, str]:
        """
        Provides clinical interpretation based on GRACE score
        
        Returns:
            Dict with risk category, mortality estimate, and clinical recommendations
        """
        
        # Find appropriate risk category
        risk_category = None
        for category in self.RISK_CATEGORIES:
            if category["min"] <= score <= category["max"]:
                risk_category = category
                break
        
        if risk_category is None:
            # Handle scores outside expected range
            if score > 400:
                risk_category = self.RISK_CATEGORIES[-1]  # Use highest risk category
            else:
                risk_category = self.RISK_CATEGORIES[0]   # Use lowest risk category
        
        # Build parameter summary
        killip_descriptions = {
            "class_1": "Killip Class I (No CHF)",
            "class_2": "Killip Class II (Rales/JVD)",
            "class_3": "Killip Class III (Pulmonary edema)",
            "class_4": "Killip Class IV (Cardiogenic shock)"
        }
        
        parameter_summary = (
            f"Clinical parameters: Age {age} years, HR {heart_rate} bpm, "
            f"SBP {systolic_bp} mmHg, Creatinine {creatinine} mg/dL, "
            f"{killip_descriptions[killip_class]}, "
            f"Cardiac arrest: {cardiac_arrest}, ST deviation: {st_deviation}, "
            f"Elevated biomarkers: {elevated_biomarkers}. "
        )
        
        # Generate risk-specific recommendations
        if score <= 87:  # Very Low Risk
            recommendations = (
                "Very low mortality risk (0-2%). Patients may be suitable for early discharge "
                "and conservative management. Consider outpatient follow-up with cardiology. "
                "Standard medical therapy is appropriate. Monitor for clinical deterioration."
            )
        elif score <= 128:  # Low Risk
            recommendations = (
                "Low mortality risk (3-10%). Standard care with consideration for early invasive "
                "strategy based on other clinical factors. Appropriate for step-down unit care. "
                "Continue evidence-based medical therapy and monitor response to treatment."
            )
        elif score <= 149:  # Intermediate Risk
            recommendations = (
                "Intermediate mortality risk (10-20%). Requires careful monitoring and consideration "
                "for invasive management strategies. Consider early cardiology consultation. "
                "Intensive medical therapy and frequent reassessment recommended."
            )
        elif score <= 173:  # High Risk
            recommendations = (
                "High mortality risk (20-30%). Patients would benefit from intensive monitoring "
                "and aggressive interventional therapy. Consider immediate cardiology consultation "
                "and invasive strategy. ICU-level care may be appropriate."
            )
        elif score <= 284:  # Very High Risk
            recommendations = (
                "Very high mortality risk (40-90%). Requires immediate intensive care, aggressive "
                "interventional strategies, and close monitoring. Emergency cardiology consultation "
                "and immediate invasive management indicated. Consider transfer to tertiary center."
            )
        else:  # Extremely High Risk
            recommendations = (
                "Extremely high mortality risk (≥99%). Critical prognosis requiring maximum "
                "intensive care and immediate life-saving interventions. Emergency interventional "
                "cardiology consultation. Consider all available therapeutic options including "
                "mechanical circulatory support."
            )
        
        # Build comprehensive interpretation
        interpretation = (
            f"{parameter_summary}GRACE Score: {score} points. "
            f"Risk category: {risk_category['risk']} ({risk_category['mortality']} mortality). "
            f"Clinical recommendations: {recommendations} "
            f"Important note: Use in conjunction with clinical judgment and consider patient "
            f"comorbidities, preferences, and overall clinical picture when making treatment decisions."
        )
        
        return {
            "stage": risk_category["risk"],
            "description": risk_category["description"],
            "interpretation": interpretation
        }


def calculate_grace_acs_risk(age: int, heart_rate: int, systolic_bp: int, creatinine: float,
                           killip_class: str, cardiac_arrest: str, st_deviation: str,
                           elevated_biomarkers: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_grace_acs_risk pattern
    """
    calculator = GraceAcsRiskCalculator()
    return calculator.calculate(age, heart_rate, systolic_bp, creatinine, killip_class,
                              cardiac_arrest, st_deviation, elevated_biomarkers)