"""
Mentzer Index Calculator

Differentiates beta thalassemia trait from iron deficiency anemia using MCV and RBC count.
A simple but effective screening tool for microcytic anemia evaluation.

References:
1. Mentzer WC Jr. Lancet. 1973;1(7808):882.
2. Vehapoglu A, et al. Anemia. 2014;2014:576738.
3. Zaghloul A, et al. Hematology. 2016;21(6):351-8.
"""

from typing import Dict, Any


class MentzerIndexCalculator:
    """Calculator for Mentzer Index to differentiate beta thalassemia from iron deficiency anemia"""
    
    def __init__(self):
        # Interpretation thresholds
        self.BETA_THALASSEMIA_THRESHOLD = 13
        self.IRON_DEFICIENCY_THRESHOLD = 13
        
        # Normal ranges for reference
        self.NORMAL_MCV_MIN = 80
        self.NORMAL_MCV_MAX = 100
        self.NORMAL_RBC_MIN = 4.0
        self.NORMAL_RBC_MAX = 6.0
    
    def calculate(self, mcv: float, rbc_count: float) -> Dict[str, Any]:
        """
        Calculates the Mentzer Index to help differentiate between beta thalassemia trait
        and iron deficiency anemia
        
        Args:
            mcv (float): Mean Corpuscular Volume in femtoliters (fL)
            rbc_count (float): Red Blood Cell count in millions per microliter (10⁶/µL)
            
        Returns:
            Dict with the Mentzer Index value and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(mcv, rbc_count)
        
        # Calculate Mentzer Index
        mentzer_index = mcv / rbc_count
        
        # Round to 1 decimal place for clinical use
        mentzer_index = round(mentzer_index, 1)
        
        # Get interpretation
        interpretation = self._get_interpretation(mentzer_index)
        
        return {
            "result": mentzer_index,
            "unit": "",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, mcv: float, rbc_count: float):
        """Validates input parameters"""
        
        # Validate MCV
        if not isinstance(mcv, (int, float)):
            raise ValueError("MCV must be a number")
        
        if mcv <= 0 or mcv > 200:
            raise ValueError(f"MCV must be between 0 and 200 fL, got {mcv}")
        
        # Validate RBC count
        if not isinstance(rbc_count, (int, float)):
            raise ValueError("RBC count must be a number")
        
        if rbc_count < 0.001 or rbc_count > 15:
            raise ValueError(f"RBC count must be between 0.001 and 15 × 10⁶/µL, got {rbc_count}")
    
    def _get_interpretation(self, mentzer_index: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the Mentzer Index value
        
        Args:
            mentzer_index (float): Calculated Mentzer Index
            
        Returns:
            Dict with stage, description, and clinical interpretation
        """
        
        if mentzer_index < self.BETA_THALASSEMIA_THRESHOLD:
            return {
                "stage": "Beta Thalassemia Trait Likely",
                "description": "Index < 13",
                "interpretation": (
                    "Beta thalassemia trait is more likely. In thalassemia, RBC production "
                    "is normal but cells are smaller and more fragile, resulting in normal "
                    "RBC count with low MCV. Consider hemoglobin electrophoresis for confirmation."
                )
            }
        elif mentzer_index == self.IRON_DEFICIENCY_THRESHOLD:
            return {
                "stage": "Indeterminate",
                "description": "Index = 13",
                "interpretation": (
                    "Results are inconclusive. Both beta thalassemia trait and iron deficiency "
                    "anemia are possible. Further testing with iron studies and hemoglobin "
                    "electrophoresis is recommended."
                )
            }
        else:  # mentzer_index > 13
            return {
                "stage": "Iron Deficiency Anemia Likely",
                "description": "Index > 13",
                "interpretation": (
                    "Iron deficiency anemia is more likely. In iron deficiency, the marrow "
                    "cannot produce as many RBCs and they are small, resulting in both low "
                    "RBC count and low MCV. Consider iron studies for confirmation."
                )
            }


def calculate_mentzer_index(mcv: float, rbc_count: float) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MentzerIndexCalculator()
    return calculator.calculate(mcv, rbc_count)