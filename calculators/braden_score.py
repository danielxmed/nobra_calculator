"""
Braden Score for Pressure Ulcers Calculator

Identifies patients at risk for pressure ulcers by assessing six key factors.

References:
1. Braden BJ, Bergstrom N. Clinical utility of the Braden scale for Predicting 
   Pressure Sore Risk. Decubitus. 1989;2(3):44-6, 50-1.
2. Bergstrom N, Braden BJ, Laguzza A, Holman V. The Braden Scale for Predicting 
   Pressure Sore Risk. Nurs Res. 1987;36(4):205-10.
"""

from typing import Dict, Any


class BradenScoreCalculator:
    """Calculator for Braden Score for Pressure Ulcers"""
    
    def __init__(self):
        # Risk thresholds
        self.NO_RISK_MIN = 19
        self.MILD_RISK_MIN = 15
        self.MODERATE_RISK_MIN = 13
        self.HIGH_RISK_MIN = 10
        
    def calculate(self, sensory_perception: int, moisture: int, activity: int,
                  mobility: int, nutrition: int, friction_shear: int) -> Dict[str, Any]:
        """
        Calculates the Braden score for pressure ulcer risk
        
        Args:
            sensory_perception (int): 1-4 points (ability to respond to pressure discomfort)
            moisture (int): 1-4 points (degree of skin moisture exposure)
            activity (int): 1-4 points (degree of physical activity)
            mobility (int): 1-4 points (ability to change body position)
            nutrition (int): 1-4 points (usual food intake pattern)
            friction_shear (int): 1-3 points (friction and shear when moving)
            
        Returns:
            Dict with score, unit, risk stage, and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(sensory_perception, moisture, activity,
                            mobility, nutrition, friction_shear)
        
        # Calculate total score
        total_score = (sensory_perception + moisture + activity + 
                      mobility + nutrition + friction_shear)
        
        # Get risk interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, sensory_perception: int, moisture: int, activity: int,
                        mobility: int, nutrition: int, friction_shear: int):
        """Validates input parameters"""
        
        # Validate each parameter is an integer
        params = {
            "sensory_perception": sensory_perception,
            "moisture": moisture,
            "activity": activity,
            "mobility": mobility,
            "nutrition": nutrition,
            "friction_shear": friction_shear
        }
        
        for param_name, param_value in params.items():
            if not isinstance(param_value, int):
                raise ValueError(f"{param_name} must be an integer")
        
        # Validate ranges for 1-4 parameters
        for param_name in ["sensory_perception", "moisture", "activity", "mobility", "nutrition"]:
            param_value = params[param_name]
            if param_value < 1 or param_value > 4:
                raise ValueError(f"{param_name} must be between 1 and 4")
        
        # Validate friction_shear (1-3)
        if friction_shear < 1 or friction_shear > 3:
            raise ValueError("friction_shear must be between 1 and 3")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines risk level and interpretation based on total score
        
        Args:
            score (int): Total Braden score (6-23)
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score >= self.NO_RISK_MIN:
            return {
                "stage": "No Risk",
                "description": "No risk for pressure ulcers",
                "interpretation": "Patient is not at risk for developing pressure ulcers. Continue routine skin care and monitoring. Reassess if patient condition changes."
            }
        elif score >= self.MILD_RISK_MIN:
            return {
                "stage": "Mild Risk",
                "description": "Mild risk for pressure ulcers",
                "interpretation": "Patient is at mild risk for developing pressure ulcers. Implement basic preventive measures including turning schedule every 2-3 hours, skin moisturization, and nutritional support."
            }
        elif score >= self.MODERATE_RISK_MIN:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate risk for pressure ulcers",
                "interpretation": "Patient is at moderate risk for developing pressure ulcers. Implement turning schedule every 2 hours, use pressure-reducing surfaces, optimize nutrition and hydration, and perform daily comprehensive skin assessments."
            }
        elif score >= self.HIGH_RISK_MIN:
            return {
                "stage": "High Risk",
                "description": "High risk for pressure ulcers",
                "interpretation": "Patient is at high risk for developing pressure ulcers. Implement aggressive prevention protocol: turning every 1-2 hours, specialized support surfaces, nutritional consultation, moisture management, and twice-daily skin assessments."
            }
        else:
            return {
                "stage": "Very High Risk",
                "description": "Very high risk for pressure ulcers",
                "interpretation": "Patient is at very high risk for developing pressure ulcers. Implement maximum prevention measures: hourly repositioning, advanced pressure redistribution surfaces, intensive nutritional support, barrier creams, and frequent comprehensive skin assessments. Consider wound care specialist consultation."
            }


def calculate_braden_score(sensory_perception: int, moisture: int, activity: int,
                          mobility: int, nutrition: int, friction_shear: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BradenScoreCalculator()
    return calculator.calculate(sensory_perception, moisture, activity,
                              mobility, nutrition, friction_shear)