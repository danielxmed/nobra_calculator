"""
Migraine Disability Assessment (MIDAS) Calculator

Quantifies headache-related disability over a 3-month period.

References:
1. Stewart WF, et al. Cephalalgia. 1999;19(2):107-14.
2. Stewart WF, et al. Neurology. 2001;56(6 Suppl 1):S20-8.
3. Stewart WF, et al. Pain. 2000;88(1):41-52.
"""

from typing import Dict, Any


class MidasCalculator:
    """Calculator for Migraine Disability Assessment (MIDAS)"""
    
    def __init__(self):
        # Grade thresholds
        self.GRADES = {
            "I": {"min": 0, "max": 5, "description": "Little or no disability"},
            "II": {"min": 6, "max": 10, "description": "Mild disability"},
            "III": {"min": 11, "max": 20, "description": "Moderate disability"},
            "IV": {"min": 21, "max": float('inf'), "description": "Severe disability"}
        }
    
    def calculate(self, missed_work_school: int, reduced_work_school: int,
                  missed_household: int, reduced_household: int,
                  missed_social: int) -> Dict[str, Any]:
        """
        Calculates the MIDAS score
        
        Args:
            missed_work_school (int): Days missed work/school (0-90)
            reduced_work_school (int): Days work/school productivity reduced ≥50% (0-90)
            missed_household (int): Days missed household work (0-90)
            reduced_household (int): Days household productivity reduced ≥50% (0-90)
            missed_social (int): Days missed social/leisure activities (0-90)
            
        Returns:
            Dict with MIDAS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(missed_work_school, reduced_work_school,
                            missed_household, reduced_household, missed_social)
        
        # Calculate total score
        total_score = (missed_work_school + reduced_work_school +
                      missed_household + reduced_household + missed_social)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, missed_work_school: int, reduced_work_school: int,
                        missed_household: int, reduced_household: int,
                        missed_social: int):
        """Validates input parameters"""
        
        # Check all parameters are integers
        params = {
            "missed_work_school": missed_work_school,
            "reduced_work_school": reduced_work_school,
            "missed_household": missed_household,
            "reduced_household": reduced_household,
            "missed_social": missed_social
        }
        
        for param_name, value in params.items():
            if not isinstance(value, (int, float)):
                raise ValueError(f"{param_name} must be a number, got '{type(value).__name__}'")
            
            # Convert to int if float
            if isinstance(value, float):
                if value != int(value):
                    raise ValueError(f"{param_name} must be a whole number, got {value}")
                value = int(value)
            
            # Check range (0-90 days in 3 months)
            if value < 0 or value > 90:
                raise ValueError(f"{param_name} must be between 0 and 90 days, got {value}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the MIDAS grade and interpretation based on score
        
        Args:
            score (int): Calculated MIDAS score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score <= 5:
            return {
                "stage": "Grade I",
                "description": "Little or no disability",
                "interpretation": "Patient has little or no headache-related disability. Consider simple analgesics and lifestyle modifications. Prophylactic treatment typically not required."
            }
        elif score <= 10:
            return {
                "stage": "Grade II",
                "description": "Mild disability",
                "interpretation": "Patient has mild headache-related disability. Consider migraine-specific acute treatments. Discuss prophylaxis if attacks are frequent or disabling."
            }
        elif score <= 20:
            return {
                "stage": "Grade III",
                "description": "Moderate disability",
                "interpretation": "Patient has moderate headache-related disability. Recommend migraine-specific acute treatments and strongly consider prophylactic treatment to reduce frequency and severity."
            }
        else:  # score >= 21
            return {
                "stage": "Grade IV",
                "description": "Severe disability",
                "interpretation": "Patient has severe headache-related disability. Urgent need for effective acute treatment and prophylaxis. Consider referral to headache specialist if not already under specialist care."
            }


def calculate_midas(missed_work_school: int, reduced_work_school: int,
                   missed_household: int, reduced_household: int,
                   missed_social: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = MidasCalculator()
    return calculator.calculate(missed_work_school, reduced_work_school,
                              missed_household, reduced_household, missed_social)