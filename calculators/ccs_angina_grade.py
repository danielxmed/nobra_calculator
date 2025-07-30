"""
Canadian Cardiovascular Society (CCS) Angina Grade Calculator

Classifies the severity of exertional angina based on the degree of effort 
necessary to induce angina symptoms.

References:
1. Campeau L. Letter: Grading of angina pectoris. Circulation. 1976;54(3):522-3.
2. Campeau L. The Canadian Cardiovascular Society grading of angina pectoris 
   revisited 30 years later. Can J Cardiol. 2002;18(4):371-9.
"""

from typing import Dict, Any


class CcsAnginaGradeCalculator:
    """Calculator for Canadian Cardiovascular Society (CCS) Angina Grade"""
    
    def __init__(self):
        # Define the grading system
        self.grades = {
            "strenuous_exertion_only": {
                "grade": "Grade I",
                "description": "Angina only with strenuous exertion",
                "interpretation": "Ordinary physical activity (such as walking and climbing stairs) does not cause angina. Angina occurs with strenuous, rapid, or prolonged exertion at work or recreation. No limitation of ordinary activity."
            },
            "moderate_exertion_limitation": {
                "grade": "Grade II",
                "description": "Slight limitation of ordinary activity",
                "interpretation": "Angina occurs on walking or climbing stairs rapidly, walking uphill, walking or stair climbing after meals, in cold, in wind, under emotional stress, or only during the few hours after awakening. Angina on walking more than 2 blocks on the level and climbing more than 1 flight of ordinary stairs at normal pace and in normal conditions."
            },
            "marked_limitation": {
                "grade": "Grade III",
                "description": "Marked limitation of ordinary physical activity",
                "interpretation": "Angina occurs on walking 1 to 2 blocks on the level and climbing 1 flight of stairs at normal pace in normal conditions. Marked limitation of ordinary physical activity."
            },
            "symptoms_at_rest": {
                "grade": "Grade IV",
                "description": "Inability to carry out any physical activity without discomfort",
                "interpretation": "Angina may be present at rest. Unable to perform any physical activity without discomfort. Anginal symptoms may occur at rest."
            }
        }
    
    def calculate(self, angina_symptoms: str) -> Dict[str, Any]:
        """
        Calculates the CCS Angina Grade based on symptom pattern
        
        Args:
            angina_symptoms: Level of physical activity that triggers angina
                - "strenuous_exertion_only": Only with strenuous exertion
                - "moderate_exertion_limitation": Slight limitation of ordinary activity
                - "marked_limitation": Marked limitation of ordinary activity  
                - "symptoms_at_rest": Symptoms at rest or any activity
            
        Returns:
            Dict with CCS grade and interpretation
        """
        
        # Validate input
        self._validate_inputs(angina_symptoms)
        
        # Get the grade information
        grade_info = self.grades[angina_symptoms]
        
        return {
            "result": grade_info["grade"],
            "unit": "grade",
            "interpretation": grade_info["interpretation"],
            "stage": grade_info["grade"],
            "stage_description": grade_info["description"]
        }
    
    def _validate_inputs(self, angina_symptoms: str):
        """Validates input parameters"""
        
        valid_options = ["strenuous_exertion_only", "moderate_exertion_limitation", 
                        "marked_limitation", "symptoms_at_rest"]
        
        if angina_symptoms not in valid_options:
            raise ValueError(
                f"angina_symptoms must be one of: {', '.join(valid_options)}"
            )


def calculate_ccs_angina_grade(angina_symptoms: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = CcsAnginaGradeCalculator()
    return calculator.calculate(angina_symptoms=angina_symptoms)