"""
FeverPAIN Score for Strep Pharyngitis Calculator

Predicts likelihood of streptococcal pharyngitis and guides antibiotic 
prescribing decisions.

References:
- Little P, et al. Incidence and clinical variables associated with streptococcal 
  throat infections. Br J Gen Pract. 2012;62(604):e787-94.
"""

import math
from typing import Dict, Any


class FeverpainScoreCalculator:
    """Calculator for FeverPAIN Score for Strep Pharyngitis"""
    
    def __init__(self):
        # No constants needed for this calculator
        pass
    
    def calculate(self, fever_24h: str, absence_cough_coryza: str, 
                 symptom_onset_3days: str, purulent_tonsils: str, 
                 severe_tonsil_inflammation: str) -> Dict[str, Any]:
        """
        Calculates the FeverPAIN score using the provided parameters
        
        Args:
            fever_24h (str): Fever in past 24 hours ("yes" or "no")
            absence_cough_coryza (str): Absence of cough or coryza ("yes" or "no")
            symptom_onset_3days (str): Symptom onset ≤3 days ("yes" or "no")
            purulent_tonsils (str): Purulent tonsils ("yes" or "no")
            severe_tonsil_inflammation (str): Severe tonsil inflammation ("yes" or "no")
            
        Returns:
            Dict with the FeverPAIN score and interpretation
        """
        
        # Validations
        self._validate_inputs(fever_24h, absence_cough_coryza, symptom_onset_3days,
                           purulent_tonsils, severe_tonsil_inflammation)
        
        # Calculate score
        result = self._calculate_feverpain(fever_24h, absence_cough_coryza, 
                                         symptom_onset_3days, purulent_tonsils,
                                         severe_tonsil_inflammation)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation.get("stage", ""),
            "stage_description": interpretation.get("description", "")
        }
    
    def _validate_inputs(self, fever_24h, absence_cough_coryza, symptom_onset_3days,
                        purulent_tonsils, severe_tonsil_inflammation):
        """Validates input parameters"""
        
        valid_values = ["yes", "no"]
        
        if fever_24h not in valid_values:
            raise ValueError("Fever in past 24 hours must be 'yes' or 'no'")
        
        if absence_cough_coryza not in valid_values:
            raise ValueError("Absence of cough or coryza must be 'yes' or 'no'")
        
        if symptom_onset_3days not in valid_values:
            raise ValueError("Symptom onset ≤3 days must be 'yes' or 'no'")
        
        if purulent_tonsils not in valid_values:
            raise ValueError("Purulent tonsils must be 'yes' or 'no'")
        
        if severe_tonsil_inflammation not in valid_values:
            raise ValueError("Severe tonsil inflammation must be 'yes' or 'no'")
    
    def _calculate_feverpain(self, fever_24h, absence_cough_coryza, symptom_onset_3days,
                           purulent_tonsils, severe_tonsil_inflammation):
        """Calculates the FeverPAIN score"""
        
        score = 0
        
        # Each "yes" answer adds 1 point
        if fever_24h == "yes":
            score += 1
        
        if absence_cough_coryza == "yes":
            score += 1
        
        if symptom_onset_3days == "yes":
            score += 1
        
        if purulent_tonsils == "yes":
            score += 1
        
        if severe_tonsil_inflammation == "yes":
            score += 1
        
        return score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the FeverPAIN score
        
        Args:
            result (int): FeverPAIN score (0-5)
            
        Returns:
            Dict with interpretation
        """
        
        if result <= 1:
            return {
                "stage": "Low Risk",
                "description": "13-18% strep isolation",
                "interpretation": "13-18% likelihood of streptococcus isolation. No antibiotics recommended. Consider supportive care and symptom management."
            }
        elif result == 2:
            return {
                "stage": "Moderate Risk",
                "description": "30-35% strep isolation",
                "interpretation": "30-35% likelihood of streptococcus isolation. Delayed antibiotic prescription may be appropriate. Consider 3-day delayed prescribing strategy."
            }
        elif result == 3:
            return {
                "stage": "Moderate-High Risk",
                "description": "39-48% strep isolation",
                "interpretation": "39-48% likelihood of streptococcus isolation. Delayed antibiotic prescription may be appropriate. Consider 3-day delayed prescribing strategy."
            }
        else:  # result >= 4
            return {
                "stage": "High Risk",
                "description": "62-65% strep isolation",
                "interpretation": "62-65% likelihood of streptococcus isolation. Consider antibiotics if symptoms are severe or patient is systemically unwell. Short delayed prescribing strategy (48 hours) may be appropriate."
            }


def calculate_feverpain_score(fever_24h, absence_cough_coryza, symptom_onset_3days,
                             purulent_tonsils, severe_tonsil_inflammation) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = FeverpainScoreCalculator()
    return calculator.calculate(fever_24h, absence_cough_coryza, symptom_onset_3days,
                              purulent_tonsils, severe_tonsil_inflammation)