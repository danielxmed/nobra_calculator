"""
Osteoporosis Self Assessment Tool (OST) Calculator

Predicts risk of osteoporosis based on age and body weight.
Different risk thresholds apply for men and women.

References:
1. Koh LK, et al. Osteoporos Int. 2001;12(8):699-705.
2. Adler RA, et al. Mayo Clin Proc. 2003;78(6):723-7.
3. Richy F, et al. QJM. 2004;97(1):39-46.
4. Richards JS, et al. J Clin Densitom. 2014;17(1):32-7.
"""

import math
from typing import Dict, Any


class OstCalculator:
    """Calculator for Osteoporosis Self Assessment Tool"""
    
    def __init__(self):
        # Risk thresholds for women
        self.FEMALE_LOW_RISK = 2  # > 1
        self.FEMALE_HIGH_RISK = -3  # < -3
        
        # Risk thresholds for men
        self.MALE_LOW_RISK = 4  # > 3
        self.MALE_HIGH_RISK = -1  # < -1
    
    def calculate(self, age: int, weight: float, sex: str) -> Dict[str, Any]:
        """
        Calculates the OST score using the provided parameters
        
        Args:
            age (int): Patient age in years
            weight (float): Body weight in kilograms
            sex (str): Patient biological sex (female or male)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, weight, sex)
        
        # Calculate score
        result = self._calculate_score(age, weight)
        
        # Get interpretation based on sex
        interpretation = self._get_interpretation(result, sex)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, weight: float, sex: str):
        """Validates input parameters"""
        
        if not isinstance(age, (int, float)):
            raise ValueError("Age must be a number")
        
        if age < 40 or age > 120:
            raise ValueError("Age must be between 40 and 120 years")
        
        if not isinstance(weight, (int, float)):
            raise ValueError("Weight must be a number")
        
        if weight < 20 or weight > 200:
            raise ValueError("Weight must be between 20 and 200 kg")
        
        if sex not in ["female", "male"]:
            raise ValueError("Sex must be either 'female' or 'male'")
    
    def _calculate_score(self, age: int, weight: float) -> int:
        """Calculates the OST score"""
        
        # Formula: (weight in kg - age in years) × 0.2
        score = (weight - age) * 0.2
        
        # Truncate to integer (towards zero)
        return int(score)
    
    def _get_interpretation(self, result: int, sex: str) -> Dict[str, str]:
        """
        Determines the interpretation based on the result and sex
        
        Args:
            result (int): Calculated OST score
            sex (str): Patient biological sex
            
        Returns:
            Dict with interpretation
        """
        
        if sex == "female":
            if result > 1:
                return {
                    "stage": "Low risk",
                    "description": "Low risk of osteoporosis",
                    "interpretation": "This patient scores above 1 on the OST scale for women, indicating low risk of osteoporosis. Routine screening may be appropriate based on other risk factors and clinical guidelines."
                }
            elif result >= -3:
                return {
                    "stage": "Intermediate risk",
                    "description": "Intermediate risk of osteoporosis",
                    "interpretation": "This patient scores between -3 and 1 on the OST scale for women, indicating intermediate risk of osteoporosis. Consider bone density testing (DXA scan) based on clinical judgment and other risk factors."
                }
            else:
                return {
                    "stage": "High risk",
                    "description": "High risk of osteoporosis",
                    "interpretation": "This patient scores below -3 on the OST scale for women, indicating high risk of osteoporosis. Bone density testing (DXA scan) is strongly recommended. The original validation study showed 91% sensitivity and 45% specificity for identifying osteoporosis."
                }
        else:  # male
            if result > 3:
                return {
                    "stage": "Low risk",
                    "description": "Low risk of osteoporosis",
                    "interpretation": "This patient scores above 3 on the OST scale for men, indicating low risk of osteoporosis. Routine screening may be appropriate based on other risk factors and clinical guidelines."
                }
            elif result >= -1:
                return {
                    "stage": "Intermediate risk",
                    "description": "Intermediate risk of osteoporosis",
                    "interpretation": "This patient scores between -1 and 3 on the OST scale for men, indicating intermediate risk of osteoporosis. Consider bone density testing (DXA scan) based on clinical judgment and other risk factors."
                }
            else:
                return {
                    "stage": "High risk",
                    "description": "High risk of osteoporosis",
                    "interpretation": "This patient scores below -1 on the OST scale for men, indicating high risk of osteoporosis. Bone density testing (DXA scan) is strongly recommended. The validation study showed 93% sensitivity and 66% specificity for identifying osteoporosis in men."
                }


def calculate_ost(age: int, weight: float, sex: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = OstCalculator()
    return calculator.calculate(age, weight, sex)