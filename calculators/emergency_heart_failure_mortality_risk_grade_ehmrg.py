"""
Emergency Heart Failure Mortality Risk Grade (EHMRG) Calculator

Estimates 7-day mortality risk in emergency department patients with acute heart failure
using clinical variables routinely collected on arrival.

The EHMRG score incorporates age, mode of presentation, vital signs, laboratory values,
and clinical comorbidities to provide personalized risk stratification for patients
presenting with acute heart failure.

References:
1. Lee DS, Stitt A, Austin PC, Stukel TA, Schull MJ, Charl G, et al. Prediction of 
   heart failure mortality in emergent care: a cohort study. Ann Intern Med. 
   2012;156(11):767-75.
2. Stiell IG, Clement CM, Brison RJ, Rowe BH, Borgundvaag B, Aaron SD, et al. A risk 
   scoring system to identify emergency department patients with heart failure at high 
   risk for serious adverse events. Acad Emerg Med. 2013;20(1):17-26.
"""

from typing import Dict, Any


class EmergencyHeartFailureMortalityRiskGradeEhmrgCalculator:
    """Calculator for Emergency Heart Failure Mortality Risk Grade (EHMRG)"""
    
    def __init__(self):
        # Scoring constants
        self.AGE_MULTIPLIER = 2
        self.EMS_POINTS = 60
        self.SBP_MULTIPLIER = -1
        self.SBP_CAP = 160
        self.HR_MULTIPLIER = 1
        self.HR_MIN = 80
        self.HR_MAX = 120
        self.O2SAT_MULTIPLIER = -2
        self.O2SAT_CAP = 92
        self.CREATININE_MULTIPLIER = 20
        self.TROPONIN_POINTS = 60
        self.CANCER_POINTS = 45
        self.METOLAZONE_POINTS = 60
        self.ADJUSTMENT_FACTOR = 12
        
        # Potassium scoring
        self.K_LOW_THRESHOLD = 3.9
        self.K_HIGH_THRESHOLD = 4.6
        self.K_LOW_POINTS = 5
        self.K_NORMAL_POINTS = 0
        self.K_HIGH_POINTS = 30
        
        # Risk group thresholds
        self.RISK_THRESHOLDS = {
            "group_1": -49.1,
            "group_2": -15.9,
            "group_3": 17.9,
            "group_4": 56.5,
            "group_5a": 89.3
        }
    
    def calculate(self, age: int, ems_transport: str, systolic_bp: int, heart_rate: int,
                 oxygen_saturation: int, creatinine: float, potassium: float,
                 troponin_elevated: str, active_cancer: str, metolazone_use: str) -> Dict[str, Any]:
        """
        Calculates the EHMRG score for 7-day mortality risk prediction
        
        Args:
            age (int): Patient age in years
            ems_transport (str): EMS transport ("yes" or "no")
            systolic_bp (int): Systolic blood pressure in mmHg
            heart_rate (int): Heart rate in bpm
            oxygen_saturation (int): Oxygen saturation percentage
            creatinine (float): Serum creatinine in mg/dL
            potassium (float): Serum potassium in mmol/L
            troponin_elevated (str): Troponin above upper limit ("yes" or "no")
            active_cancer (str): Presence of active cancer ("yes" or "no")
            metolazone_use (str): Current metolazone use ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, ems_transport, systolic_bp, heart_rate, oxygen_saturation,
                            creatinine, potassium, troponin_elevated, active_cancer, metolazone_use)
        
        # Calculate EHMRG score
        score = self._calculate_ehmrg_score(age, ems_transport, systolic_bp, heart_rate,
                                          oxygen_saturation, creatinine, potassium,
                                          troponin_elevated, active_cancer, metolazone_use)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": round(score, 1),
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age, ems_transport, systolic_bp, heart_rate, oxygen_saturation,
                        creatinine, potassium, troponin_elevated, active_cancer, metolazone_use):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 18 or age > 120:
            raise ValueError("Age must be an integer between 18 and 120 years")
        
        if ems_transport not in ["yes", "no"]:
            raise ValueError("EMS transport must be 'yes' or 'no'")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 40 or systolic_bp > 300:
            raise ValueError("Systolic blood pressure must be between 40 and 300 mmHg")
        
        if not isinstance(heart_rate, int) or heart_rate < 30 or heart_rate > 200:
            raise ValueError("Heart rate must be between 30 and 200 bpm")
        
        if not isinstance(oxygen_saturation, int) or oxygen_saturation < 50 or oxygen_saturation > 100:
            raise ValueError("Oxygen saturation must be between 50 and 100%")
        
        if not isinstance(creatinine, (int, float)) or creatinine < 0.1 or creatinine > 20.0:
            raise ValueError("Creatinine must be between 0.1 and 20.0 mg/dL")
        
        if not isinstance(potassium, (int, float)) or potassium < 2.0 or potassium > 8.0:
            raise ValueError("Potassium must be between 2.0 and 8.0 mmol/L")
        
        if troponin_elevated not in ["yes", "no"]:
            raise ValueError("Troponin elevated must be 'yes' or 'no'")
        
        if active_cancer not in ["yes", "no"]:
            raise ValueError("Active cancer must be 'yes' or 'no'")
        
        if metolazone_use not in ["yes", "no"]:
            raise ValueError("Metolazone use must be 'yes' or 'no'")
    
    def _calculate_ehmrg_score(self, age, ems_transport, systolic_bp, heart_rate,
                              oxygen_saturation, creatinine, potassium,
                              troponin_elevated, active_cancer, metolazone_use) -> float:
        """
        Calculates the EHMRG score using the validated formula
        
        Formula components:
        - Age: 2 × age
        - EMS transport: 60 points if yes
        - SBP: -1 × min(SBP, 160)
        - Heart rate: 1 × max(80, min(HR, 120))
        - O2 sat: -2 × min(O2sat, 92)
        - Creatinine: 20 × creatinine
        - Potassium: variable points based on range
        - Troponin: 60 points if elevated
        - Cancer: 45 points if active
        - Metolazone: 60 points if used
        - Adjustment: +12 points
        """
        
        score = 0
        
        # Age component
        score += self.AGE_MULTIPLIER * age
        
        # EMS transport component
        if ems_transport == "yes":
            score += self.EMS_POINTS
        
        # Systolic BP component (capped at 160)
        sbp_capped = min(systolic_bp, self.SBP_CAP)
        score += self.SBP_MULTIPLIER * sbp_capped
        
        # Heart rate component (range 80-120)
        hr_adjusted = max(self.HR_MIN, min(heart_rate, self.HR_MAX))
        score += self.HR_MULTIPLIER * hr_adjusted
        
        # Oxygen saturation component (capped at 92%)
        o2sat_capped = min(oxygen_saturation, self.O2SAT_CAP)
        score += self.O2SAT_MULTIPLIER * o2sat_capped
        
        # Creatinine component
        score += self.CREATININE_MULTIPLIER * creatinine
        
        # Potassium component
        score += self._get_potassium_points(potassium)
        
        # Troponin component
        if troponin_elevated == "yes":
            score += self.TROPONIN_POINTS
        
        # Active cancer component
        if active_cancer == "yes":
            score += self.CANCER_POINTS
        
        # Metolazone use component
        if metolazone_use == "yes":
            score += self.METOLAZONE_POINTS
        
        # Adjustment factor
        score += self.ADJUSTMENT_FACTOR
        
        return score
    
    def _get_potassium_points(self, potassium: float) -> int:
        """
        Determines potassium points based on level
        
        Args:
            potassium: Potassium level in mmol/L
            
        Returns:
            Points based on potassium range
        """
        
        if potassium <= self.K_LOW_THRESHOLD:
            return self.K_LOW_POINTS
        elif potassium >= self.K_HIGH_THRESHOLD:
            return self.K_HIGH_POINTS
        else:
            return self.K_NORMAL_POINTS
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the risk group and interpretation based on EHMRG score
        
        Args:
            score (float): Calculated EHMRG score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.RISK_THRESHOLDS["group_1"]:
            return {
                "stage": "Risk Group 1 (Very Low)",
                "description": "Very low 7-day mortality risk",
                "interpretation": "7-day mortality rate 0.5%. Very low risk for short-term mortality. Standard heart failure management with routine follow-up appropriate. Consider early discharge planning if clinically stable."
            }
        elif score <= self.RISK_THRESHOLDS["group_2"]:
            return {
                "stage": "Risk Group 2 (Low)",
                "description": "Low 7-day mortality risk",
                "interpretation": "7-day mortality rate 0.3%. Low risk for short-term mortality. Standard heart failure care with close outpatient follow-up. May be suitable for accelerated discharge pathway if appropriate support available."
            }
        elif score <= self.RISK_THRESHOLDS["group_3"]:
            return {
                "stage": "Risk Group 3 (Intermediate)",
                "description": "Intermediate 7-day mortality risk",
                "interpretation": "7-day mortality rate 0.7%. Intermediate risk requiring careful monitoring. Standard inpatient management with attention to optimization of heart failure therapy. Ensure adequate follow-up arrangements."
            }
        elif score <= self.RISK_THRESHOLDS["group_4"]:
            return {
                "stage": "Risk Group 4 (High)",
                "description": "High 7-day mortality risk",
                "interpretation": "7-day mortality rate 2.1%. High risk requiring intensive monitoring and aggressive management. Consider cardiology consultation, advanced heart failure therapies, and close inpatient observation."
            }
        elif score <= self.RISK_THRESHOLDS["group_5a"]:
            return {
                "stage": "Risk Group 5a (Very High)",
                "description": "Very high 7-day mortality risk",
                "interpretation": "7-day mortality rate 3.3%. Very high risk requiring immediate intensive intervention. Strong consideration for ICU-level care, advanced heart failure specialist consultation, and evaluation for advanced therapies."
            }
        else:
            return {
                "stage": "Risk Group 5b (Highest)",
                "description": "Highest 7-day mortality risk",
                "interpretation": "7-day mortality rate 8.0%. Highest risk category requiring immediate intensive care. Urgent cardiology/heart failure specialist consultation, ICU-level monitoring, and consideration of advanced mechanical support or palliative care discussions."
            }


def calculate_emergency_heart_failure_mortality_risk_grade_ehmrg(age: int, ems_transport: str, 
                                                              systolic_bp: int, heart_rate: int,
                                                              oxygen_saturation: int, creatinine: float,
                                                              potassium: float, troponin_elevated: str,
                                                              active_cancer: str, metolazone_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_emergency_heart_failure_mortality_risk_grade_ehmrg pattern
    """
    calculator = EmergencyHeartFailureMortalityRiskGradeEhmrgCalculator()
    return calculator.calculate(age, ems_transport, systolic_bp, heart_rate, oxygen_saturation,
                              creatinine, potassium, troponin_elevated, active_cancer, metolazone_use)