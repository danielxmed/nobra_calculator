"""
Newsom Score for Non-traumatic Chest Pain Calculator

Rules out need for chest X-ray in patients with non-traumatic chest pain.
The score uses 12 clinical criteria to identify low-risk patients.

References:
1. Rothrock SG, et al. J Emerg Med. 2002;23(2):117-24.
2. Newsom C, et al. Acad Emerg Med. 2018;25(6):650-656.
"""

from typing import Dict, Any


class NewsomScoreCalculator:
    """Calculator for Newsom Score for Non-traumatic Chest Pain"""
    
    def __init__(self):
        # Each criterion is worth 1 point
        self.POINT_VALUE = 1
    
    def calculate(self, age_60_or_more: str, chf_history: str, smoking_history: str,
                  hemoptysis: str, tuberculosis_history: str, thromboembolic_history: str,
                  alcohol_abuse: str, fever: str, oxygen_saturation_low: str,
                  respiratory_rate_high: str, diminished_breath_sounds: str, 
                  rales: str) -> Dict[str, Any]:
        """
        Calculates the Newsom Score using the provided parameters
        
        Args:
            age_60_or_more: Is patient ≥60 years old? (yes/no)
            chf_history: History of congestive heart failure? (yes/no)
            smoking_history: Current or former smoking history? (yes/no)
            hemoptysis: Coughing up blood? (yes/no)
            tuberculosis_history: History of tuberculosis? (yes/no)
            thromboembolic_history: History of PE or DVT? (yes/no)
            alcohol_abuse: Prior or current alcohol abuse? (yes/no)
            fever: Temperature ≥100.4°F (38°C)? (yes/no)
            oxygen_saturation_low: O2 saturation <90%? (yes/no)
            respiratory_rate_high: Respiratory rate >24? (yes/no)
            diminished_breath_sounds: Diminished breath sounds? (yes/no)
            rales: Rales/crackles on auscultation? (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_60_or_more, chf_history, smoking_history,
                            hemoptysis, tuberculosis_history, thromboembolic_history,
                            alcohol_abuse, fever, oxygen_saturation_low,
                            respiratory_rate_high, diminished_breath_sounds, rales)
        
        # Calculate score
        score = 0
        
        # Count positive criteria
        criteria = [
            age_60_or_more,
            chf_history,
            smoking_history,
            hemoptysis,
            tuberculosis_history,
            thromboembolic_history,
            alcohol_abuse,
            fever,
            oxygen_saturation_low,
            respiratory_rate_high,
            diminished_breath_sounds,
            rales
        ]
        
        for criterion in criteria:
            if criterion.lower() == "yes":
                score += self.POINT_VALUE
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age_60_or_more: str, chf_history: str, smoking_history: str,
                        hemoptysis: str, tuberculosis_history: str, thromboembolic_history: str,
                        alcohol_abuse: str, fever: str, oxygen_saturation_low: str,
                        respiratory_rate_high: str, diminished_breath_sounds: str, 
                        rales: str):
        """Validates input parameters"""
        
        # List all parameters for validation
        params = {
            "age_60_or_more": age_60_or_more,
            "chf_history": chf_history,
            "smoking_history": smoking_history,
            "hemoptysis": hemoptysis,
            "tuberculosis_history": tuberculosis_history,
            "thromboembolic_history": thromboembolic_history,
            "alcohol_abuse": alcohol_abuse,
            "fever": fever,
            "oxygen_saturation_low": oxygen_saturation_low,
            "respiratory_rate_high": respiratory_rate_high,
            "diminished_breath_sounds": diminished_breath_sounds,
            "rales": rales
        }
        
        # Validate each parameter
        for param_name, param_value in params.items():
            if not isinstance(param_value, str):
                raise ValueError(f"{param_name} must be a string")
            
            if param_value.lower() not in ["yes", "no"]:
                raise ValueError(f"{param_name} must be 'yes' or 'no'")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated Newsom Score
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low risk",
                "description": "Chest x-ray not needed",
                "interpretation": "This patient has no risk factors present and is considered low risk. Chest x-ray is not needed based on the Newsom Score criteria. The negative predictive value is 98.4%, making it highly unlikely that a clinically significant finding would be missed."
            }
        else:  # score >= 1
            return {
                "stage": "Not low risk",
                "description": "Consider chest x-ray",
                "interpretation": "This patient has one or more risk factors present. Consider obtaining a chest x-ray as clinically significant findings may be present. The score has 92.9% sensitivity for detecting abnormal chest x-ray findings such as pneumonia, congestive heart failure, or pleural effusion."
            }


def calculate_newsom_score(age_60_or_more: str, chf_history: str, smoking_history: str,
                          hemoptysis: str, tuberculosis_history: str, thromboembolic_history: str,
                          alcohol_abuse: str, fever: str, oxygen_saturation_low: str,
                          respiratory_rate_high: str, diminished_breath_sounds: str, 
                          rales: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NewsomScoreCalculator()
    return calculator.calculate(age_60_or_more, chf_history, smoking_history,
                              hemoptysis, tuberculosis_history, thromboembolic_history,
                              alcohol_abuse, fever, oxygen_saturation_low,
                              respiratory_rate_high, diminished_breath_sounds, rales)