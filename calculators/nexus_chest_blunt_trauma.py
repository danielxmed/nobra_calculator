"""
NEXUS Chest Decision Instrument for Blunt Chest Trauma Calculator

Determines need for chest imaging in blunt trauma patients using 7 criteria.
The score is 99% sensitive for clinically significant thoracic injury.

References:
1. Rodriguez RM, et al. J Trauma. 2011;71(3):549-53.
2. Rodriguez RM, et al. JAMA Surg. 2013;148(10):940-6.
"""

from typing import Dict, Any


class NexusChestBluntTraumaCalculator:
    """Calculator for NEXUS Chest Decision Instrument for Blunt Chest Trauma"""
    
    def __init__(self):
        # Each criterion is worth 1 point
        self.POINT_VALUE = 1
    
    def calculate(self, age_over_60: str, rapid_deceleration: str, chest_pain: str,
                  intoxication: str, altered_mental_status: str, distracting_injury: str,
                  chest_wall_tenderness: str) -> Dict[str, Any]:
        """
        Calculates the NEXUS Chest score using the provided parameters
        
        Args:
            age_over_60: Is patient older than 60 years? (yes/no)
            rapid_deceleration: Fall >20ft or MVC >40mph? (yes/no)
            chest_pain: Does patient have chest pain? (yes/no)
            intoxication: Is patient intoxicated? (yes/no)
            altered_mental_status: Does patient have altered mental status? (yes/no)
            distracting_injury: Does patient have distracting painful injury? (yes/no)
            chest_wall_tenderness: Does patient have chest wall tenderness? (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(age_over_60, rapid_deceleration, chest_pain,
                            intoxication, altered_mental_status, distracting_injury,
                            chest_wall_tenderness)
        
        # Calculate score
        score = 0
        
        # Count positive criteria
        criteria = [
            age_over_60,
            rapid_deceleration,
            chest_pain,
            intoxication,
            altered_mental_status,
            distracting_injury,
            chest_wall_tenderness
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
    
    def _validate_inputs(self, age_over_60: str, rapid_deceleration: str, chest_pain: str,
                        intoxication: str, altered_mental_status: str, distracting_injury: str,
                        chest_wall_tenderness: str):
        """Validates input parameters"""
        
        # List all parameters for validation
        params = {
            "age_over_60": age_over_60,
            "rapid_deceleration": rapid_deceleration,
            "chest_pain": chest_pain,
            "intoxication": intoxication,
            "altered_mental_status": altered_mental_status,
            "distracting_injury": distracting_injury,
            "chest_wall_tenderness": chest_wall_tenderness
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
            score (int): Calculated NEXUS Chest score
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Very low risk",
                "description": "Consider no imaging",
                "interpretation": "No NEXUS Chest criteria are present. This patient is at very low risk for thoracic injury. Chest imaging can potentially be avoided. The negative predictive value is 98.5% for thoracic injury and 99.9% for clinically major injury."
            }
        else:  # score >= 1
            return {
                "stage": "Not low risk",
                "description": "Consider chest imaging",
                "interpretation": "One or more NEXUS Chest criteria are present. Cannot rule out thoracic injury. In well-appearing patients, consider chest x-ray only. In ill-appearing patients or those with multi-organ injury, consider chest CT. The score is 99% sensitive for clinically significant thoracic injury."
            }


def calculate_nexus_chest_blunt_trauma(age_over_60: str, rapid_deceleration: str, chest_pain: str,
                                      intoxication: str, altered_mental_status: str, distracting_injury: str,
                                      chest_wall_tenderness: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NexusChestBluntTraumaCalculator()
    return calculator.calculate(age_over_60, rapid_deceleration, chest_pain,
                              intoxication, altered_mental_status, distracting_injury,
                              chest_wall_tenderness)