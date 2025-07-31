"""
NEXUS Chest CT Decision Instrument Calculator

Identifies blunt trauma patients with clinically significant chest injuries
requiring CT chest imaging.

References:
1. Rodriguez RM, et al. PLoS Med. 2015;12(10):e1001883.
2. Rodriguez RM, et al. J Trauma. 2011;71(3):549-53.
"""

from typing import Dict, Any


class NexusChestCtCalculator:
    """Calculator for NEXUS Chest CT Decision Instrument"""
    
    def __init__(self):
        # Each criterion present counts as 1
        self.POINT_VALUE = 1
    
    def calculate(self, abnormal_chest_xray: str, distracting_injury: str,
                  chest_wall_tenderness: str, sternal_tenderness: str,
                  thoracic_spine_tenderness: str, scapular_tenderness: str,
                  rapid_deceleration: str) -> Dict[str, Any]:
        """
        Calculates the NEXUS Chest CT score using the provided parameters
        
        Args:
            abnormal_chest_xray: Abnormal CXR with injury or widened mediastinum? (yes/no)
            distracting_injury: Distracting painful injury present? (yes/no)
            chest_wall_tenderness: Chest wall tenderness on palpation? (yes/no)
            sternal_tenderness: Sternal tenderness on palpation? (yes/no)
            thoracic_spine_tenderness: Thoracic spine tenderness? (yes/no)
            scapular_tenderness: Scapular tenderness on palpation? (yes/no)
            rapid_deceleration: Fall >20ft or MVA >40mph? (yes/no)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(abnormal_chest_xray, distracting_injury,
                            chest_wall_tenderness, sternal_tenderness,
                            thoracic_spine_tenderness, scapular_tenderness,
                            rapid_deceleration)
        
        # Calculate score
        score = 0
        
        # Count positive criteria
        criteria = [
            abnormal_chest_xray,
            distracting_injury,
            chest_wall_tenderness,
            sternal_tenderness,
            thoracic_spine_tenderness,
            scapular_tenderness,
            rapid_deceleration
        ]
        
        for criterion in criteria:
            if criterion.lower() == "yes":
                score += self.POINT_VALUE
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "criteria present",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, abnormal_chest_xray: str, distracting_injury: str,
                        chest_wall_tenderness: str, sternal_tenderness: str,
                        thoracic_spine_tenderness: str, scapular_tenderness: str,
                        rapid_deceleration: str):
        """Validates input parameters"""
        
        # List all parameters for validation
        params = {
            "abnormal_chest_xray": abnormal_chest_xray,
            "distracting_injury": distracting_injury,
            "chest_wall_tenderness": chest_wall_tenderness,
            "sternal_tenderness": sternal_tenderness,
            "thoracic_spine_tenderness": thoracic_spine_tenderness,
            "scapular_tenderness": scapular_tenderness,
            "rapid_deceleration": rapid_deceleration
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
            score (int): Number of positive NEXUS Chest CT criteria
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Low risk",
                "description": "CT chest not indicated",
                "interpretation": "No NEXUS Chest CT criteria are present. Major or minor thoracic injury can be excluded without CT chest imaging. The negative predictive value is 98.7% for all thoracic injuries."
            }
        else:  # score >= 1
            return {
                "stage": "CT indicated",
                "description": "Consider CT chest",
                "interpretation": "One or more NEXUS Chest CT criteria are present. Major or minor thoracic injury cannot be excluded. Further workup is indicated, potentially including CT chest. This rule is 99.0% sensitive for all thoracic injuries and 100% sensitive for aortic and great vessel injuries."
            }


def calculate_nexus_chest_ct(abnormal_chest_xray: str, distracting_injury: str,
                           chest_wall_tenderness: str, sternal_tenderness: str,
                           thoracic_spine_tenderness: str, scapular_tenderness: str,
                           rapid_deceleration: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NexusChestCtCalculator()
    return calculator.calculate(abnormal_chest_xray, distracting_injury,
                              chest_wall_tenderness, sternal_tenderness,
                              thoracic_spine_tenderness, scapular_tenderness,
                              rapid_deceleration)