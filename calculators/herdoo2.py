"""
HERDOO2 Rule for Discontinuing Anticoagulation in Unprovoked VTE Calculator

Identifies low-risk women who can safely discontinue anticoagulation after 
completing treatment for unprovoked venous thromboembolism.

References:
- Rodger MA, et al. CMAJ. 2008;179(5):417-26.
- Rodger MA, et al. BMJ. 2017;356:j1065.
"""

from typing import Dict, Any


class Herdoo2Calculator:
    """Calculator for HERDOO2 Rule"""
    
    def __init__(self):
        # Scoring points
        self.POST_THROMBOTIC_SIGNS_POINTS = 1
        self.D_DIMER_ELEVATED_POINTS = 1
        self.BMI_HIGH_POINTS = 1
        self.AGE_HIGH_POINTS = 1
        
        # Risk thresholds
        self.LOW_RISK_MAX = 1
    
    def calculate(self, post_thrombotic_signs: str, d_dimer_level: str, 
                  bmi: str, age: str) -> Dict[str, Any]:
        """
        Calculates the HERDOO2 score
        
        Args:
            post_thrombotic_signs (str): "yes" or "no" - Hyperpigmentation, edema, or redness
            d_dimer_level (str): "normal" or "elevated" - D-dimer ≥250 μg/L
            bmi (str): "under_30" or "30_or_over" - Body Mass Index
            age (str): "under_65" or "65_or_over" - Patient age
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(post_thrombotic_signs, d_dimer_level, bmi, age)
        
        # Calculate score
        score = 0
        
        # Post-thrombotic signs (1 point if present)
        if post_thrombotic_signs == "yes":
            score += self.POST_THROMBOTIC_SIGNS_POINTS
        
        # D-dimer level (1 point if elevated)
        if d_dimer_level == "elevated":
            score += self.D_DIMER_ELEVATED_POINTS
        
        # BMI (1 point if ≥30)
        if bmi == "30_or_over":
            score += self.BMI_HIGH_POINTS
        
        # Age (1 point if ≥65)
        if age == "65_or_over":
            score += self.AGE_HIGH_POINTS
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, post_thrombotic_signs: str, d_dimer_level: str, 
                        bmi: str, age: str):
        """Validates input parameters"""
        
        valid_yes_no = ["yes", "no"]
        valid_d_dimer = ["normal", "elevated"]
        valid_bmi = ["under_30", "30_or_over"]
        valid_age = ["under_65", "65_or_over"]
        
        if post_thrombotic_signs not in valid_yes_no:
            raise ValueError(f"Post-thrombotic signs must be one of {valid_yes_no}")
        
        if d_dimer_level not in valid_d_dimer:
            raise ValueError(f"D-dimer level must be one of {valid_d_dimer}")
        
        if bmi not in valid_bmi:
            raise ValueError(f"BMI must be one of {valid_bmi}")
        
        if age not in valid_age:
            raise ValueError(f"Age must be one of {valid_age}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): HERDOO2 score
            
        Returns:
            Dict with interpretation
        """
        
        if score <= self.LOW_RISK_MAX:
            return {
                "stage": "Low Risk",
                "description": "Can discontinue anticoagulation",
                "interpretation": "Low risk of VTE recurrence (3.0% annual risk). "
                                "Anticoagulation can be safely discontinued after "
                                "completing initial treatment period."
            }
        else:
            return {
                "stage": "Not Low Risk",
                "description": "Continue anticoagulation",
                "interpretation": "Not low risk for VTE recurrence (7.4% annual risk). "
                                "Continued anticoagulation is recommended as the risk "
                                "of recurrence outweighs the bleeding risk."
            }


def calculate_herdoo2(post_thrombotic_signs: str, d_dimer_level: str, 
                      bmi: str, age: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Herdoo2Calculator()
    return calculator.calculate(post_thrombotic_signs, d_dimer_level, bmi, age)