"""
ASTRAL Score for Ischemic Stroke Calculator

Predicts 90-day poor outcome (mRS >2) in patients with acute ischemic stroke.
The ASTRAL score combines age, NIHSS, timing, visual defects, glucose levels, 
and consciousness to stratify prognosis.

References:
- Ntaios G, Faouzi M, Ferrari J, et al. An integer-based score to predict 
  functional outcome in acute ischemic stroke: the ASTRAL score. 
  Neurology. 2012;78(24):1916-22.
"""

from typing import Dict, Any


class AstralScoreCalculator:
    """Calculator for ASTRAL Score for Ischemic Stroke"""
    
    def __init__(self):
        # Score interpretation thresholds
        self.LOW_RISK_MAX = 15
        self.MODERATE_RISK_MAX = 25
        
    def calculate(self, age: int, nihss_score: int, onset_to_admission_over_3h: str,
                  visual_field_defect: str, abnormal_glucose: str, 
                  impaired_consciousness: str) -> Dict[str, Any]:
        """
        Calculates the ASTRAL score for predicting 90-day poor outcome in ischemic stroke
        
        Args:
            age (int): Patient age in years
            nihss_score (int): National Institutes of Health Stroke Scale score (0-42)
            onset_to_admission_over_3h (str): More than 3 hours from symptom onset to admission ("yes" or "no")
            visual_field_defect (str): Presence of any new visual field defect ("yes" or "no")
            abnormal_glucose (str): Admission glucose >131 mg/dL or <66 mg/dL ("yes" or "no")
            impaired_consciousness (str): Impaired consciousness at admission ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, nihss_score, onset_to_admission_over_3h,
                             visual_field_defect, abnormal_glucose, impaired_consciousness)
        
        # Calculate score
        score = self._calculate_score(age, nihss_score, onset_to_admission_over_3h,
                                     visual_field_defect, abnormal_glucose, impaired_consciousness)
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: int, nihss_score: int, onset_to_admission_over_3h: str,
                        visual_field_defect: str, abnormal_glucose: str, 
                        impaired_consciousness: str):
        """Validates input parameters"""
        
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
        
        if age < 0 or age > 120:
            raise ValueError("Age must be between 0 and 120 years")
        
        if not isinstance(nihss_score, int):
            raise ValueError("NIHSS score must be an integer")
        
        if nihss_score < 0 or nihss_score > 42:
            raise ValueError("NIHSS score must be between 0 and 42 points")
        
        valid_yes_no = ["yes", "no"]
        
        if onset_to_admission_over_3h not in valid_yes_no:
            raise ValueError("Onset to admission >3h must be 'yes' or 'no'")
        
        if visual_field_defect not in valid_yes_no:
            raise ValueError("Visual field defect must be 'yes' or 'no'")
        
        if abnormal_glucose not in valid_yes_no:
            raise ValueError("Abnormal glucose must be 'yes' or 'no'")
        
        if impaired_consciousness not in valid_yes_no:
            raise ValueError("Impaired consciousness must be 'yes' or 'no'")
    
    def _calculate_score(self, age: int, nihss_score: int, onset_to_admission_over_3h: str,
                        visual_field_defect: str, abnormal_glucose: str, 
                        impaired_consciousness: str) -> int:
        """Implements the ASTRAL score calculation"""
        
        # Base score = Age + NIHSS
        score = age + nihss_score
        
        # Add points for risk factors
        if onset_to_admission_over_3h == "yes":
            score += 2
        
        if visual_field_defect == "yes":
            score += 2
        
        if abnormal_glucose == "yes":
            score += 1
        
        if impaired_consciousness == "yes":
            score += 3
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (int): Calculated ASTRAL score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= self.LOW_RISK_MAX:
            return {
                "stage": "Low Risk",
                "description": "Lower probability of poor outcome",
                "interpretation": "Scores 0-15 points indicate lower probability of poor outcome (mRS >2) at 90 days. Patients in this range have better prognosis for functional independence."
            }
        elif score <= self.MODERATE_RISK_MAX:
            return {
                "stage": "Moderate Risk",
                "description": "Moderate probability of poor outcome",
                "interpretation": "Scores 16-25 points indicate moderate probability of poor outcome (mRS >2) at 90 days. These patients require careful monitoring and intensive rehabilitation planning."
            }
        else:
            return {
                "stage": "High Risk",
                "description": "High probability of poor outcome",
                "interpretation": "Scores ≥26 points indicate high probability of poor outcome (mRS >2) at 90 days. These patients are at high risk for significant disability or death and may benefit from palliative care discussions."
            }


def calculate_astral_score(age: int, nihss_score: int, onset_to_admission_over_3h: str,
                          visual_field_defect: str, abnormal_glucose: str, 
                          impaired_consciousness: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_astral_score pattern
    """
    calculator = AstralScoreCalculator()
    return calculator.calculate(age, nihss_score, onset_to_admission_over_3h,
                               visual_field_defect, abnormal_glucose, impaired_consciousness)
