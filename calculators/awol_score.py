"""
AWOL Score for Delirium Calculator

Predicts risk of delirium during hospitalization based on age, cognitive function,
orientation, and illness severity.

Reference:
Douglas VC, et al. The AWOL tool: derivation and validation of a delirium prediction rule.
J Hosp Med. 2013 Sep;8(9):493-9.
"""

from typing import Dict, Any


class AwolScoreCalculator:
    """Calculator for AWOL Score for Delirium"""
    
    def __init__(self):
        # Risk percentages based on score
        self.RISK_PERCENTAGES = {
            0: 2,
            1: 4,
            2: 14,
            3: 20,
            4: 64
        }
    
    def calculate(self, age: str, spelling_world_backward: str, 
                  orientation: str, illness_severity: str) -> Dict[str, Any]:
        """
        Calculates the AWOL score and delirium risk
        
        Args:
            age (str): "under_80" or "80_or_over"
            spelling_world_backward (str): "yes" or "no" - ability to spell 'world' backward
            orientation (str): "yes" or "no" - oriented to place
            illness_severity (str): nursing assessment of illness severity
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age, spelling_world_backward, orientation, illness_severity)
        
        # Calculate score
        score = 0
        
        # Age ≥80 years: 1 point
        if age == "80_or_over":
            score += 1
        
        # Unable to spell "world" backward: 1 point
        if spelling_world_backward == "no":
            score += 1
        
        # Disoriented to place: 1 point
        if orientation == "no":
            score += 1
        
        # Illness severity moderate or higher: 1 point
        if illness_severity in ["moderately_ill", "severely_ill", "moribund"]:
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, spelling_world_backward: str, 
                        orientation: str, illness_severity: str):
        """Validates input parameters"""
        
        if age not in ["under_80", "80_or_over"]:
            raise ValueError("Age must be 'under_80' or '80_or_over'")
        
        if spelling_world_backward not in ["yes", "no"]:
            raise ValueError("Spelling world backward must be 'yes' or 'no'")
        
        if orientation not in ["yes", "no"]:
            raise ValueError("Orientation must be 'yes' or 'no'")
        
        valid_severities = ["not_ill", "mildly_ill", "moderately_ill", "severely_ill", "moribund"]
        if illness_severity not in valid_severities:
            raise ValueError(f"Illness severity must be one of: {', '.join(valid_severities)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated AWOL score (0-4)
            
        Returns:
            Dict with interpretation
        """
        
        risk_percentage = self.RISK_PERCENTAGES[score]
        
        if score == 0:
            return {
                "stage": "Very Low Risk",
                "description": "0 points",
                "interpretation": f"{risk_percentage}% risk of delirium during hospitalization. Low risk patient - routine monitoring appropriate."
            }
        elif score == 1:
            return {
                "stage": "Low Risk",
                "description": "1 point",
                "interpretation": f"{risk_percentage}% risk of delirium during hospitalization. Low risk patient - routine monitoring appropriate."
            }
        elif score == 2:
            return {
                "stage": "Moderate Risk",
                "description": "2 points",
                "interpretation": f"{risk_percentage}% risk of delirium during hospitalization. Consider delirium prevention strategies (early mobilization, reorientation, sleep hygiene)."
            }
        elif score == 3:
            return {
                "stage": "High Risk",
                "description": "3 points",
                "interpretation": f"{risk_percentage}% risk of delirium during hospitalization. Implement delirium prevention protocol and consider specialist consultation."
            }
        else:  # score == 4
            return {
                "stage": "Very High Risk",
                "description": "4 points",
                "interpretation": f"{risk_percentage}% risk of delirium during hospitalization. High priority for delirium prevention measures, close monitoring, and specialist involvement."
            }


def calculate_awol_score(age: str, spelling_world_backward: str, 
                        orientation: str, illness_severity: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AwolScoreCalculator()
    return calculator.calculate(age, spelling_world_backward, orientation, illness_severity)