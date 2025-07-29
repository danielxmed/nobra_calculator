"""
BAP-65 Score Calculator

Predicts mortality in acute COPD exacerbation using BUN, Altered mental status, 
Pulse rate, and age ≥65 years.

References (Vancouver style):
1. Tabak YP, Sun X, Johannes RS, Gupta V, Shorr AF. Mortality and need for mechanical 
   ventilation in acute exacerbations of chronic obstructive pulmonary disease: 
   development and validation of a simple risk score. Arch Intern Med. 2009 Sep 
   28;169(17):1595-602. doi: 10.1001/archinternmed.2009.270. PMID: 19786679.
2. Shorr AF, Sun X, Johannes RS, Yaitanes A, Tabak YP. Validation of a novel risk 
   score for severity of illness in acute exacerbations of COPD. Chest. 2011 
   Nov;140(5):1177-1183. doi: 10.1378/chest.10-3035. Epub 2011 Apr 28. PMID: 21527510.
"""

from typing import Dict, Any


class Bap65Calculator:
    """Calculator for BAP-65 Score"""
    
    def __init__(self):
        # Score components
        self.AGE_CUTOFF = 65
        self.PULSE_CUTOFF = 109
        self.BUN_CUTOFF = 25.0  # mg/dL
        
    def calculate(self, bun: str, altered_mental_status: str, 
                  pulse: str, age: int) -> Dict[str, Any]:
        """
        Calculates the BAP-65 score for acute COPD exacerbation
        
        Args:
            bun (str): BUN ≥25 mg/dL ('yes' or 'no')
            altered_mental_status (str): Altered mental status ('yes' or 'no')
            pulse (str): Pulse ≥109 bpm ('yes' or 'no')
            age (int): Patient age in years
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(bun, altered_mental_status, pulse, age)
        
        # Calculate score
        score = 0
        
        # BUN ≥25 mg/dL (1 point)
        if bun.lower() == "yes":
            score += 1
            
        # Altered mental status (1 point)
        if altered_mental_status.lower() == "yes":
            score += 1
            
        # Pulse ≥109 bpm (1 point)
        if pulse.lower() == "yes":
            score += 1
            
        # Age ≥65 years (1 point)
        if age >= self.AGE_CUTOFF:
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score, age)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, bun: str, altered_mental_status: str, 
                        pulse: str, age: int):
        """Validates input parameters"""
        
        # Validate yes/no parameters
        valid_options = ["yes", "no"]
        
        if bun.lower() not in valid_options:
            raise ValueError("BUN must be 'yes' or 'no'")
            
        if altered_mental_status.lower() not in valid_options:
            raise ValueError("Altered mental status must be 'yes' or 'no'")
            
        if pulse.lower() not in valid_options:
            raise ValueError("Pulse must be 'yes' or 'no'")
        
        # Validate age
        if not isinstance(age, int):
            raise ValueError("Age must be an integer")
            
        if age < 41:
            raise ValueError("BAP-65 score is only validated for patients >40 years old")
            
        if age > 120:
            raise ValueError("Age must be ≤120 years")
    
    def _get_interpretation(self, score: int, age: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the score and age
        
        Args:
            score (int): Calculated BAP-65 score (0-3)
            age (int): Patient age in years
            
        Returns:
            Dict with interpretation details
        """
        
        # Class I: 0 points, age <65 years
        if score == 0 and age < 65:
            return {
                "stage": "Class I",
                "description": "0 points, age <65 years",
                "interpretation": "0.3% in-hospital mortality risk. Low risk patient. Consider outpatient management if clinically appropriate."
            }
        
        # Class II: 0 points, age ≥65 years
        elif score == 0 and age >= 65:
            return {
                "stage": "Class II",
                "description": "0 points, age ≥65 years",
                "interpretation": "1.0% in-hospital mortality risk. Low risk patient, but age ≥65 years increases risk. Consider observation or admission based on clinical judgment."
            }
        
        # Class III: 1 point, any age
        elif score == 1:
            return {
                "stage": "Class III",
                "description": "1 point, any age",
                "interpretation": "2.2% in-hospital mortality risk. Intermediate risk patient. Hospital admission recommended for observation and treatment."
            }
        
        # Class IV: 2 points, any age
        elif score == 2:
            return {
                "stage": "Class IV",
                "description": "2 points, any age",
                "interpretation": "6.4% in-hospital mortality risk. High risk patient. Hospital admission required. Consider early aggressive treatment and close monitoring."
            }
        
        # Class V: 3 points, any age
        elif score == 3:
            return {
                "stage": "Class V",
                "description": "3 points, any age",
                "interpretation": "14.1% in-hospital mortality risk. Very high risk patient. Intensive care unit admission should be considered. Aggressive treatment and close monitoring required."
            }
        
        else:
            # This should never happen with valid inputs
            raise ValueError(f"Invalid score: {score}")


def calculate_bap_65(bun: str, altered_mental_status: str, 
                    pulse: str, age: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Bap65Calculator()
    return calculator.calculate(bun, altered_mental_status, pulse, age)