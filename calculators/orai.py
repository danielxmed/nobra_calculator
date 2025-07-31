"""
Osteoporosis Risk Assessment Instrument (ORAI) Calculator

Identifies women at risk for osteoporosis and recommends bone densitometry
based on age, weight, and current estrogen use.

References:
1. Cadarette SM, et al. CMAJ. 2000;162(9):1289-94.
2. El Maghraoui A, et al. Arch Osteoporos. 2006;1(1-2):35-42.
3. Rubin KH, et al. Bone. 2013;56(1):16-22.
"""

from typing import Dict, Any


class OraiCalculator:
    """Calculator for Osteoporosis Risk Assessment Instrument"""
    
    def __init__(self):
        # Score mappings
        self.AGE_SCORES = {
            "45-54": 0,
            "55-64": 5,
            "65-74": 9,
            "75_or_older": 15
        }
        
        self.WEIGHT_SCORES = {
            "over_69kg": 0,
            "60-69kg": 3,
            "under_60kg": 9
        }
        
        self.ESTROGEN_SCORES = {
            "yes": 0,
            "no": 2
        }
    
    def calculate(self, age: str, weight: str, current_estrogen_use: str) -> Dict[str, Any]:
        """
        Calculates the ORAI score using the provided parameters
        
        Args:
            age (str): Age range of the patient
            weight (str): Weight category of the patient
            current_estrogen_use (str): Current estrogen use status
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, weight, current_estrogen_use)
        
        # Calculate score
        result = self._calculate_score(age, weight, current_estrogen_use)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, weight: str, current_estrogen_use: str):
        """Validates input parameters"""
        
        if age not in self.AGE_SCORES:
            raise ValueError(f"Age must be one of: {', '.join(self.AGE_SCORES.keys())}")
        
        if weight not in self.WEIGHT_SCORES:
            raise ValueError(f"Weight must be one of: {', '.join(self.WEIGHT_SCORES.keys())}")
        
        if current_estrogen_use not in self.ESTROGEN_SCORES:
            raise ValueError(f"Current estrogen use must be one of: {', '.join(self.ESTROGEN_SCORES.keys())}")
    
    def _calculate_score(self, age: str, weight: str, current_estrogen_use: str) -> int:
        """Calculates the ORAI score"""
        
        age_points = self.AGE_SCORES[age]
        weight_points = self.WEIGHT_SCORES[weight]
        estrogen_points = self.ESTROGEN_SCORES[current_estrogen_use]
        
        total = age_points + weight_points + estrogen_points
        
        return total
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the result
        
        Args:
            result (int): Calculated ORAI score
            
        Returns:
            Dict with interpretation
        """
        
        if result < 9:
            return {
                "stage": "Low risk",
                "description": "Bone densitometry may not be needed",
                "interpretation": "This patient scores less than 9 points on the ORAI scale. Bone densitometry may not be needed at this time. However, clinical judgment should be used, especially if other risk factors for osteoporosis are present."
            }
        else:
            return {
                "stage": "High risk",
                "description": "Consider bone densitometry",
                "interpretation": "This patient scores 9 or more points on the ORAI scale. Bone densitometry should be considered for this patient. The ORAI has a sensitivity of 93.3% and specificity of 46.4% for identifying women with low bone mineral density."
            }


def calculate_orai(age: str, weight: str, current_estrogen_use: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OraiCalculator()
    return calculator.calculate(age, weight, current_estrogen_use)