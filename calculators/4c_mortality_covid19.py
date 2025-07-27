"""
4C Mortality Score for COVID-19 Calculator

Predicts in-hospital mortality in patients admitted with COVID-19.
Reference: Knight SR et al., BMJ 2020;370:m3339
"""

from typing import Dict, Any


class FourCMortalityCovid19Calculator:
    """Calculator for the 4C Mortality Score for COVID-19"""
    
    def calculate(self, age: int, sex: str, comorbidities: int, respiratory_rate: int,
                 oxygen_saturation: float, glasgow_coma_scale: int, urea_unit: str,
                 urea_value: float, crp: float) -> Dict[str, Any]:
        """
        Calculates the 4C Mortality Score for COVID-19
        
        Args:
            age: Age in years
            sex: "male" or "female"
            comorbidities: Number of comorbidities (0-20)
            respiratory_rate: Respiratory rate (breaths/min)
            oxygen_saturation: O2 saturation (%)
            glasgow_coma_scale: Glasgow Coma Scale (3-15)
            urea_unit: "mmol_L" or "mg_dL"
            urea_value: Serum urea value
            crp: C-reactive protein (mg/L)
            
        Returns:
            Dict with result, interpretation, and risk classification
        """
        
        # Validations
        self._validate_inputs(age, sex, comorbidities, respiratory_rate,
                            oxygen_saturation, glasgow_coma_scale, urea_unit,
                            urea_value, crp)
        
        # Calculate score
        score = 0
        
        # Age (0-7 points)
        score += self._score_age(age)
        
        # Sex (0-1 point)
        score += self._score_sex(sex)
        
        # Comorbidities (0-2 points)
        score += self._score_comorbidities(comorbidities)
        
        # Respiratory rate (0-2 points)
        score += self._score_respiratory_rate(respiratory_rate)
        
        # Oxygen saturation (0-2 points)
        score += self._score_oxygen_saturation(oxygen_saturation)
        
        # Glasgow Coma Scale (0-2 points)
        score += self._score_glasgow_coma_scale(glasgow_coma_scale)
        
        # Urea (0-3 points)
        score += self._score_urea(urea_value, urea_unit)
        
        # CRP (0-2 points)
        score += self._score_crp(crp)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "mortality_risk": interpretation["mortality_risk"]
        }
    
    def _validate_inputs(self, age: int, sex: str, comorbidities: int,
                        respiratory_rate: int, oxygen_saturation: float,
                        glasgow_coma_scale: int, urea_value: float, urea_unit: str,
                        crp: float):
        """Validates input parameters"""
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        if sex not in ["male", "female"]:
            raise ValueError("Sex must be 'male' or 'female'")
        
        if not isinstance(comorbidities, int) or comorbidities < 0 or comorbidities > 20:
            raise ValueError("Number of comorbidities must be an integer between 0 and 20")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 5 or respiratory_rate > 60:
            raise ValueError("Respiratory rate must be an integer between 5 and 60 breaths/min")
        
        if not isinstance(oxygen_saturation, (int, float)) or oxygen_saturation < 50.0 or oxygen_saturation > 100.0:
            raise ValueError("Oxygen saturation must be between 50.0 and 100.0%")
        
        if not isinstance(glasgow_coma_scale, int) or glasgow_coma_scale < 3 or glasgow_coma_scale > 15:
            raise ValueError("Glasgow Coma Scale must be an integer between 3 and 15")
        
        if urea_unit not in ["mmol_L", "mg_dL"]:
            raise ValueError("Urea unit must be 'mmol_L' or 'mg_dL'")
        
        if not isinstance(urea_value, (int, float)) or urea_value < 0.1 or urea_value > 300.0:
            raise ValueError("Urea value must be between 0.1 and 300.0")
        
        if not isinstance(crp, (int, float)) or crp < 0.0 or crp > 1000.0:
            raise ValueError("CRP must be between 0.0 and 1000.0 mg/L")
    
    def _score_age(self, age: int) -> int:
        """Calculates points for age"""
        if age < 50:
            return 0
        elif age < 60:
            return 2
        elif age < 70:
            return 4
        elif age < 80:
            return 6
        else:  # ≥80
            return 7
    
    def _score_sex(self, sex: str) -> int:
        """Calculates points for sex"""
        return 1 if sex == "male" else 0
    
    def _score_comorbidities(self, comorbidities: int) -> int:
        """Calculates points for comorbidities"""
        if comorbidities == 0:
            return 0
        elif comorbidities == 1:
            return 1
        else:  # ≥2
            return 2
    
    def _score_respiratory_rate(self, respiratory_rate: int) -> int:
        """Calculates points for respiratory rate"""
        if respiratory_rate < 20:
            return 0
        elif respiratory_rate < 30:
            return 1
        else:  # ≥30
            return 2
    
    def _score_oxygen_saturation(self, oxygen_saturation: float) -> int:
        """Calculates points for oxygen saturation"""
        return 0 if oxygen_saturation >= 92.0 else 2
    
    def _score_glasgow_coma_scale(self, glasgow_coma_scale: int) -> int:
        """Calculates points for Glasgow Coma Scale"""
        return 0 if glasgow_coma_scale == 15 else 2
    
    def _score_urea(self, urea_value: float, urea_unit: str) -> int:
        """Calculates points for urea"""
        if urea_unit == "mmol_L":
            # Conversion to mmol/L
            if urea_value < 7.0:
                return 0
            elif urea_value <= 14.0:
                return 1
            else:  # >14
                return 3
        else:  # mg_dL (BUN)
            # Conversion to mg/dL
            if urea_value < 19.6:
                return 0
            elif urea_value <= 39.2:
                return 1
            else:  # >39.2
                return 3
    
    def _score_crp(self, crp: float) -> int:
        """Calculates points for CRP"""
        if crp < 50.0:
            return 0
        elif crp < 100.0:
            return 1
        else:  # ≥100
            return 2
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score: Calculated score (0-21)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 3:
            return {
                "stage": "Low Risk",
                "description": "Low mortality risk",
                "interpretation": f"Score of {score} points indicates low risk with in-hospital mortality of 1.2-1.7%. Patients may be considered for early discharge or outpatient management if clinically stable.",
                "mortality_risk": "1.2-1.7%"
            }
        elif score <= 8:
            return {
                "stage": "Intermediate Risk",
                "description": "Intermediate mortality risk",
                "interpretation": f"Score of {score} points indicates intermediate risk with in-hospital mortality of 9.1-9.9%. Patients require standard hospital monitoring with vigilance for clinical deterioration.",
                "mortality_risk": "9.1-9.9%"
            }
        elif score <= 14:
            return {
                "stage": "High Risk",
                "description": "High mortality risk",
                "interpretation": f"Score of {score} points indicates high risk with in-hospital mortality of 31.4-34.9%. Patients require intensive care or high-dependency unit monitoring.",
                "mortality_risk": "31.4-34.9%"
            }
        else:  # ≥15
            return {
                "stage": "Very High Risk",
                "description": "Very high mortality risk",
                "interpretation": f"Score of {score} points indicates very high risk with in-hospital mortality of 61.5-66.2%. Patients require immediate intensive care and consideration of support limitation if appropriate.",
                "mortality_risk": "61.5-66.2%"
            }


def calculate_4c_mortality_covid19(age: int, sex: str, comorbidities: int,
                                   respiratory_rate: int, oxygen_saturation: float,
                                   glasgow_coma_scale: int, urea_unit: str,
                                   urea_value: float, crp: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FourCMortalityCovid19Calculator()
    return calculator.calculate(age, sex, comorbidities, respiratory_rate,
                              oxygen_saturation, glasgow_coma_scale, urea_unit,
                              urea_value, crp)
