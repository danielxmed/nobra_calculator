"""
CURB-65 Score Calculator

Assesses the severity of community-acquired pneumonia to determine
the need for hospital admission.
Reference: Lim WS et al. Thorax. 2003;58(5):377-82.
"""

from typing import Dict, Any


class Curb65Calculator:
    """Calculator for CURB-65 Score"""
    
    def __init__(self):
        # Mortality risks by score
        self.mortality_risk = {
            0: 1.5,
            1: 1.5,
            2: 9.2,
            3: 22.0,
            4: 22.0,
            5: 22.0
        }
    
    def calculate(self, confusion: bool, urea: float, respiratory_rate: int,
                 systolic_bp: int, diastolic_bp: int, age: int) -> Dict[str, Any]:
        """
        Calculates the CURB-65 score
        
        Args:
            confusion: Recent onset mental confusion
            urea: Serum urea in mg/dL
            respiratory_rate: Respiratory rate (breaths/min)
            systolic_bp: Systolic blood pressure (mmHg)
            diastolic_bp: Diastolic blood pressure (mmHg)
            age: Age in years
            
        Returns:
            Dict with result, interpretation, and mortality risk
        """
        
        # Validations
        self._validate_inputs(confusion, urea, respiratory_rate, systolic_bp, diastolic_bp, age)
        
        # Calculate score
        score = 0
        
        # C - Confusion (1 point if present)
        if confusion:
            score += 1
        
        # U - Urea > 19 mg/dL (1 point)
        if urea > 19.0:
            score += 1
        
        # R - Respiratory rate ≥ 30/min (1 point)
        if respiratory_rate >= 30:
            score += 1
        
        # B - Blood pressure: SBP < 90 mmHg OR DBP ≤ 60 mmHg (1 point)
        if systolic_bp < 90 or diastolic_bp <= 60:
            score += 1
        
        # 65 - Age ≥ 65 years (1 point)
        if age >= 65:
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        mortality_risk = self.mortality_risk.get(score, 22.0)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "mortality_risk": f"{mortality_risk}%",
            "components": {
                "confusion": 1 if confusion else 0,
                "urea": 1 if urea > 19.0 else 0,
                "respiratory_rate": 1 if respiratory_rate >= 30 else 0,
                "blood_pressure": 1 if (systolic_bp < 90 or diastolic_bp <= 60) else 0,
                "age": 1 if age >= 65 else 0
            }
        }
    
    def _validate_inputs(self, confusion: bool, urea: float, respiratory_rate: int,
                        systolic_bp: int, diastolic_bp: int, age: int):
        """Validates input parameters"""
        
        if not isinstance(confusion, bool):
            raise ValueError("Confusion must be a boolean value (True/False)")
        
        if not isinstance(urea, (int, float)) or urea < 0 or urea > 200:
            raise ValueError("Urea must be a number between 0 and 200 mg/dL")
        
        if not isinstance(respiratory_rate, int) or respiratory_rate < 0 or respiratory_rate > 60:
            raise ValueError("Respiratory rate must be an integer between 0 and 60")
        
        if not isinstance(systolic_bp, int) or systolic_bp < 0 or systolic_bp > 300:
            raise ValueError("Systolic pressure must be an integer between 0 and 300 mmHg")
        
        if not isinstance(diastolic_bp, int) or diastolic_bp < 0 or diastolic_bp > 200:
            raise ValueError("Diastolic pressure must be an integer between 0 and 200 mmHg")
        
        if not isinstance(age, int) or age < 0 or age > 120:
            raise ValueError("Age must be an integer between 0 and 120 years")
        
        # Additional logical validation
        if systolic_bp < diastolic_bp:
            raise ValueError("Systolic pressure cannot be less than diastolic pressure")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score: Calculated CURB-65 score
            
        Returns:
            Dict with clinical interpretation
        """
        
        if score <= 1:
            return {
                "stage": "Low Risk",
                "description": "Mortality: 1.5%",
                "interpretation": "Outpatient treatment. Consider oral antibiotic therapy and follow-up in 48-72 hours."
            }
        
        elif score == 2:
            return {
                "stage": "Intermediate Risk",
                "description": "Mortality: 9.2%",
                "interpretation": "Consider hospital admission vs. observation. Individually assess social factors, comorbidities, and response to initial treatment."
            }
        
        else:  # score >= 3
            return {
                "stage": "High Risk",
                "description": "Mortality: 22%",
                "interpretation": "Mandatory hospital admission. Consider ICU admission, especially if CURB-65 ≥ 4. Start intravenous antibiotic therapy immediately."
            }


def calculate_curb_65(confusion: bool, urea: float, respiratory_rate: int,
                     systolic_bp: int, diastolic_bp: int, age: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_curb_65 pattern
    """
    calculator = Curb65Calculator()
    return calculator.calculate(confusion, urea, respiratory_rate,
                               systolic_bp, diastolic_bp, age)
