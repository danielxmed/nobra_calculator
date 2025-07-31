"""
Disease Steps for Multiple Sclerosis Calculator

Assesses MS disease progression based on patient's ambulatory ability.

References:
1. Hohol MJ, Orav EJ, Weiner HL. Disease steps in multiple sclerosis: a simple approach 
   to evaluate disease progression. Neurology. 1995 Feb;45(2):251-5.
2. Learmonth YC, Motl RW, Sandroff BM, Pula JH, Cadavid D. Validation of patient 
   determined disease steps (PDDS) scale scores in persons with multiple sclerosis. 
   BMC Neurol. 2013 Apr 25;13:37.
"""

from typing import Dict, Any, Union


class DiseaseStepsMsCalculator:
    """Calculator for Disease Steps for Multiple Sclerosis"""
    
    def __init__(self):
        # Disease Steps mapping
        self.DISEASE_STEPS = {
            "normal": {
                "score": 0,
                "stage": "Normal",
                "description": "Normal function",
                "interpretation": "Normal neurologic function with no activity limitations. Patient functions normally in all activities of daily living."
            },
            "mild_disability": {
                "score": 1,
                "stage": "Mild disability",
                "description": "Mild symptoms or signs",
                "interpretation": "Mild disability with minimal symptoms or neurologic signs. Patient may have minor complaints but maintains normal function in most activities."
            },
            "moderate_disability": {
                "score": 2,
                "stage": "Moderate disability",
                "description": "Visible abnormality of gait",
                "interpretation": "Moderate disability with visibly abnormal gait. Patient has noticeable walking difficulties but remains ambulatory without assistance."
            },
            "early_cane": {
                "score": 3,
                "stage": "Early cane",
                "description": "Intermittent unilateral support",
                "interpretation": "Early cane use with intermittent need for unilateral support. Patient requires walking aid occasionally but not continuously."
            },
            "late_cane": {
                "score": 4,
                "stage": "Late cane",
                "description": "Dependent on unilateral support",
                "interpretation": "Late cane stage with continuous dependence on unilateral support. Patient requires walking aid for most or all ambulation."
            },
            "bilateral_support": {
                "score": 5,
                "stage": "Bilateral support",
                "description": "Requires bilateral support",
                "interpretation": "Bilateral support required with need for two canes, crutches, or walker. Patient has significant mobility impairment but remains ambulatory."
            },
            "wheelchair": {
                "score": 6,
                "stage": "Wheelchair",
                "description": "Confined to wheelchair",
                "interpretation": "Wheelchair dependent with severely limited mobility. Patient requires wheelchair for most activities and has minimal ambulatory function."
            },
            "unclassifiable": {
                "score": "U",
                "stage": "Unclassifiable",
                "description": "Does not fit other categories",
                "interpretation": "Unclassifiable patient who does not fit into standard Disease Steps categories. Individual clinical assessment required."
            }
        }
    
    def calculate(self, disease_step: str) -> Dict[str, Any]:
        """
        Determines the Disease Steps score and interpretation
        
        Args:
            disease_step (str): Patient's disease step category
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(disease_step)
        
        # Get disease step information
        step_info = self.DISEASE_STEPS[disease_step]
        
        return {
            "result": step_info["score"],
            "unit": "step",
            "interpretation": step_info["interpretation"],
            "stage": step_info["stage"],
            "stage_description": step_info["description"]
        }
    
    def _validate_inputs(self, disease_step: str):
        """Validates input parameters"""
        
        if not isinstance(disease_step, str):
            raise ValueError("disease_step must be a string")
        
        if disease_step not in self.DISEASE_STEPS:
            valid_steps = list(self.DISEASE_STEPS.keys())
            raise ValueError(f"disease_step must be one of: {valid_steps}")


def calculate_disease_steps_ms(disease_step: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = DiseaseStepsMsCalculator()
    return calculator.calculate(disease_step)