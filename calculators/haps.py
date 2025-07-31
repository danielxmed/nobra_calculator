"""
Harmless Acute Pancreatitis Score (HAPS) Calculator

Identifies patients who do not require intensive care for their first episode of acute pancreatitis.
The HAPS enables identification, within approximately 30 minutes after admission, of patients with 
acute pancreatitis whose disease will run a mild course.

References:
1. Lankisch PG, et al. Clin Gastroenterol Hepatol. 2009;7(6):702-5.
2. Oskarsson V, et al. Pancreatology. 2011;11(5):464-8.
"""

from typing import Dict, Any


class HapsCalculator:
    """Calculator for Harmless Acute Pancreatitis Score (HAPS)"""
    
    def __init__(self):
        # No constants needed for this simple scoring system
        pass
    
    def calculate(self, peritonitis: str, creatinine_elevated: str, 
                  hematocrit_elevated: str) -> Dict[str, Any]:
        """
        Calculates the HAPS score using the provided parameters
        
        Args:
            peritonitis (str): "absent" or "present" - rebound tenderness or guarding
            creatinine_elevated (str): "no" or "yes" - creatinine ≥2 mg/dL
            hematocrit_elevated (str): "no" or "yes" - hematocrit ≥43% (male) or ≥39.6% (female)
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(peritonitis, creatinine_elevated, hematocrit_elevated)
        
        # Calculate HAPS score
        score = 0
        
        # Peritonitis present = 1 point
        if peritonitis == "present":
            score += 1
            
        # Creatinine ≥2 mg/dL = 1 point
        if creatinine_elevated == "yes":
            score += 1
            
        # Hematocrit elevated = 1 point
        if hematocrit_elevated == "yes":
            score += 1
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, peritonitis: str, creatinine_elevated: str, 
                        hematocrit_elevated: str):
        """Validates input parameters"""
        
        valid_peritonitis = ["absent", "present"]
        valid_yes_no = ["yes", "no"]
        
        if peritonitis not in valid_peritonitis:
            raise ValueError(f"Peritonitis must be one of: {', '.join(valid_peritonitis)}")
            
        if creatinine_elevated not in valid_yes_no:
            raise ValueError(f"Creatinine elevated must be one of: {', '.join(valid_yes_no)}")
            
        if hematocrit_elevated not in valid_yes_no:
            raise ValueError(f"Hematocrit elevated must be one of: {', '.join(valid_yes_no)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the HAPS score
        
        Args:
            score (int): Calculated HAPS score
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Harmless",
                "description": "Low risk for severe pancreatitis",
                "interpretation": (
                    "Patient has a harmless acute pancreatitis. Absence of pancreatic necrosis, "
                    "need for dialysis, artificial ventilation, or fatal outcome with 97% specificity "
                    "and 98% positive predictive value. Patient may not require ICU admission and could "
                    "potentially be managed on a general ward or even at home after short observation."
                )
            }
        else:  # score >= 1
            return {
                "stage": "Not Harmless",
                "description": "Cannot rule out severe pancreatitis",
                "interpretation": (
                    "Patient does not meet criteria for harmless acute pancreatitis. Cannot exclude "
                    "severe disease course. Continue standard acute pancreatitis management and monitoring. "
                    "Consider ICU admission based on clinical assessment and other severity scores."
                )
            }


def calculate_haps(peritonitis: str, creatinine_elevated: str, 
                   hematocrit_elevated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HapsCalculator()
    return calculator.calculate(peritonitis, creatinine_elevated, hematocrit_elevated)