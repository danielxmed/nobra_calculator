"""
Abnormal Involuntary Movement Scale (AIMS) Calculator

Measures involuntary movements of tardive dyskinesia (TD) in patients
receiving neuroleptic medications.
"""

from typing import Dict, Any


class AimsCalculator:
    """Calculator for Abnormal Involuntary Movement Scale (AIMS)"""
    
    def calculate(self, facial_muscles: int, lips_perioral: int, jaw: int, tongue: int,
                 upper_extremities: int, lower_extremities: int, trunk_movements: int,
                 global_severity: int, incapacitation: int, patient_awareness: int,
                 current_problems_teeth: str, dental_problems_interfere: str) -> Dict[str, Any]:
        """
        Calculates the AIMS Score
        
        Args:
            facial_muscles (int): Facial muscles and facial expression (0-4)
            lips_perioral (int): Lips and perioral area (0-4)
            jaw (int): Jaw (0-4)
            tongue (int): Tongue (0-4)
            upper_extremities (int): Upper extremities (0-4)
            lower_extremities (int): Lower extremities (0-4)
            trunk_movements (int): Trunk movements (0-4)
            global_severity (int): Global severity (0-4)
            incapacitation (int): Incapacitation (0-4)
            patient_awareness (int): Patient awareness (0-4)
            current_problems_teeth (str): "yes" or "no"
            dental_problems_interfere (str): "yes" or "no"
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(
            facial_muscles, lips_perioral, jaw, tongue, upper_extremities,
            lower_extremities, trunk_movements, global_severity, incapacitation,
            patient_awareness, current_problems_teeth, dental_problems_interfere
        )
        
        # Calculate total score (sum of items 1-7)
        total_score = (
            facial_muscles + lips_perioral + jaw + tongue +
            upper_extremities + lower_extremities + trunk_movements
        )
        
        # Detect presence of tardive dyskinesia (any item ≥2)
        movement_items = [
            facial_muscles, lips_perioral, jaw, tongue,
            upper_extremities, lower_extremities, trunk_movements
        ]
        
        has_tardive_dyskinesia = any(item >= 2 for item in movement_items)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score, has_tardive_dyskinesia)
        
        # Prepare full result
        result = {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "has_tardive_dyskinesia": has_tardive_dyskinesia,
            "additional_scores": {
                "global_severity": global_severity,
                "incapacitation": incapacitation,
                "patient_awareness": patient_awareness,
                "dental_problems": current_problems_teeth == "yes",
                "dental_interference": dental_problems_interfere == "yes"
            }
        }
        
        return result
    
    def _validate_inputs(self, facial_muscles, lips_perioral, jaw, tongue,
                        upper_extremities, lower_extremities, trunk_movements,
                        global_severity, incapacitation, patient_awareness,
                        current_problems_teeth, dental_problems_interfere):
        """Validates input parameters"""
        
        # Validate movement items (0-4)
        movement_items = [
            ("facial_muscles", facial_muscles),
            ("lips_perioral", lips_perioral),
            ("jaw", jaw),
            ("tongue", tongue),
            ("upper_extremities", upper_extremities),
            ("lower_extremities", lower_extremities),
            ("trunk_movements", trunk_movements),
            ("global_severity", global_severity),
            ("incapacitation", incapacitation),
            ("patient_awareness", patient_awareness)
        ]
        
        for name, value in movement_items:
            if not isinstance(value, int) or value < 0 or value > 4:
                raise ValueError(f"{name} must be an integer between 0 and 4")
        
        # Validate dental questions
        valid_dental = ["yes", "no"]
        if current_problems_teeth not in valid_dental:
            raise ValueError(f"current_problems_teeth must be: {', '.join(valid_dental)}")
        
        if dental_problems_interfere not in valid_dental:
            raise ValueError(f"dental_problems_interfere must be: {', '.join(valid_dental)}")
    
    def _get_interpretation(self, total_score: int, has_tardive_dyskinesia: bool) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score and presence of TD
        
        Args:
            total_score (int): Sum of items 1-7
            has_tardive_dyskinesia (bool): If any item ≥2
            
        Returns:
            Dict with clinical interpretation
        """
        
        if total_score <= 1 and not has_tardive_dyskinesia:
            return {
                "stage": "No Dyskinesia",
                "description": "Absent or questionable movements",
                "interpretation": "No evidence of tardive dyskinesia. Continue regular monitoring."
            }
        elif total_score <= 13 or (has_tardive_dyskinesia and total_score < 14):
            return {
                "stage": "Mild to Moderate Dyskinesia",
                "description": "Presence of tardive dyskinesia",
                "interpretation": "Evidence of tardive dyskinesia. Re-evaluate need for neuroleptic medication, consider dose reduction or medication change."
            }
        else:  # total_score >= 14
            return {
                "stage": "Severe Dyskinesia",
                "description": "Significant tardive dyskinesia",
                "interpretation": "Severe tardive dyskinesia. Consider discontinuation of neuroleptics if clinically possible, or use of specific medications for TD."
            }


def calculate_aims(facial_muscles: int, lips_perioral: int, jaw: int, tongue: int,
                  upper_extremities: int, lower_extremities: int, trunk_movements: int,
                  global_severity: int, incapacitation: int, patient_awareness: int,
                  current_problems_teeth: str, dental_problems_interfere: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = AimsCalculator()
    return calculator.calculate(
        facial_muscles, lips_perioral, jaw, tongue, upper_extremities,
        lower_extremities, trunk_movements, global_severity, incapacitation,
        patient_awareness, current_problems_teeth, dental_problems_interfere
    )
