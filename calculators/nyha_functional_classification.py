"""
New York Heart Association (NYHA) Functional Classification for Heart Failure Calculator

Stratifies severity of heart failure by symptoms based on physical activity limitations.

References:
1. Dolgin M, et al. Nomenclature and criteria for diagnosis of diseases of the heart 
   and great vessels. 9th ed. Lippincott Williams and Wilkins; 1994.
2. Goldman L, et al. Comparative reproducibility and validity of systems for assessing 
   cardiovascular functional class. Circulation. 1981;64(6):1227-34.
3. Raphael C, et al. Limitations of the New York Heart Association functional 
   classification system and self-reported walking distances in chronic heart failure. 
   Heart. 2007;93(4):476-82.
"""

from typing import Dict, Any


class NyhaFunctionalClassificationCalculator:
    """Calculator for NYHA Functional Classification for Heart Failure"""
    
    def __init__(self):
        # NYHA classification definitions
        self.classifications = {
            "Class I - No limitation of physical activity": {
                "class": "Class I",
                "description": "No limitation of physical activity",
                "interpretation": "Ordinary physical activity does not cause undue fatigue, palpitation, or dyspnea. Patients can perform activities requiring ≥7 METs.",
                "met_capacity": "≥7 METs"
            },
            "Class II - Slight limitation of physical activity": {
                "class": "Class II", 
                "description": "Slight limitation of physical activity",
                "interpretation": "Comfortable at rest. Ordinary physical activity results in fatigue, palpitation, or dyspnea. Patients can perform activities requiring ≥5 METs but <7 METs.",
                "met_capacity": "≥5 to <7 METs"
            },
            "Class III - Marked limitation of physical activity": {
                "class": "Class III",
                "description": "Marked limitation of physical activity", 
                "interpretation": "Comfortable at rest. Less than ordinary activity causes fatigue, palpitation, or dyspnea. Patients can perform activities requiring ≥2 METs but <5 METs.",
                "met_capacity": "≥2 to <5 METs"
            },
            "Class IV - Unable to carry on any physical activity without discomfort": {
                "class": "Class IV",
                "description": "Unable to carry on any physical activity without discomfort",
                "interpretation": "Symptoms of heart failure at rest. If any physical activity is undertaken, discomfort increases. Patients cannot or should not perform activities requiring >2 METs.",
                "met_capacity": "<2 METs"
            }
        }
    
    def calculate(self, physical_ability: str) -> Dict[str, Any]:
        """
        Determines NYHA functional classification based on physical ability
        
        Args:
            physical_ability (str): Patient's physical ability selection
            
        Returns:
            Dict with NYHA classification and interpretation
        """
        
        # Validate input
        self._validate_input(physical_ability)
        
        # Get classification details
        classification = self.classifications[physical_ability]
        
        return {
            "result": classification["class"],
            "unit": "",
            "interpretation": classification["interpretation"],
            "stage": classification["class"],
            "stage_description": classification["description"],
            "met_capacity": classification["met_capacity"]
        }
    
    def _validate_input(self, physical_ability: str):
        """Validates input parameter"""
        
        if physical_ability not in self.classifications:
            valid_options = list(self.classifications.keys())
            raise ValueError(
                f"Invalid physical_ability value. Must be one of: {', '.join(valid_options)}"
            )


def calculate_nyha_functional_classification(physical_ability: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NyhaFunctionalClassificationCalculator()
    return calculator.calculate(physical_ability)