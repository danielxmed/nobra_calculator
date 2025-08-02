"""
Migraine Treatment Optimization Questionnaire-4 (mTOQ-4) Calculator

Determines effectiveness of current migraine treatment plan.

References:
1. Lipton RB, et al. Cephalalgia. 2009;29(7):751-9.
2. Lipton RB, et al. Neurology. 2015;84(7):688-95.
"""

from typing import Dict, Any


class Mtoq4Calculator:
    """Calculator for Migraine Treatment Optimization Questionnaire-4 (mTOQ-4)"""
    
    def __init__(self):
        # Scoring values for each response
        self.RESPONSE_SCORES = {
            "never_rarely": 0,
            "less_than_half": 1,
            "half_or_more": 2
        }
    
    def calculate(self, pain_free_2_hours: str, relief_24_hours: str,
                  able_to_plan: str, feel_in_control: str) -> Dict[str, Any]:
        """
        Calculates the mTOQ-4 score
        
        Args:
            pain_free_2_hours (str): Response for 2-hour pain freedom question
            relief_24_hours (str): Response for 24-hour relief question
            able_to_plan (str): Response for ability to plan activities question
            feel_in_control (str): Response for feeling in control question
            
        Returns:
            Dict with mTOQ-4 score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(pain_free_2_hours, relief_24_hours,
                            able_to_plan, feel_in_control)
        
        # Calculate total score
        total_score = (
            self.RESPONSE_SCORES[pain_free_2_hours] +
            self.RESPONSE_SCORES[relief_24_hours] +
            self.RESPONSE_SCORES[able_to_plan] +
            self.RESPONSE_SCORES[feel_in_control]
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, pain_free_2_hours: str, relief_24_hours: str,
                        able_to_plan: str, feel_in_control: str):
        """Validates input parameters"""
        
        valid_responses = list(self.RESPONSE_SCORES.keys())
        
        # Check each parameter
        params = {
            "pain_free_2_hours": pain_free_2_hours,
            "relief_24_hours": relief_24_hours,
            "able_to_plan": able_to_plan,
            "feel_in_control": feel_in_control
        }
        
        for param_name, value in params.items():
            if value not in valid_responses:
                raise ValueError(
                    f"{param_name} must be one of {valid_responses}, got '{value}'"
                )
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the treatment efficacy category and interpretation
        
        Args:
            score (int): Calculated mTOQ-4 score
            
        Returns:
            Dict with stage, description, and interpretation
        """
        
        if score == 0:
            return {
                "stage": "Very Poor",
                "description": "Very poor treatment efficacy",
                "interpretation": "Current migraine treatment is ineffective. Strong recommendation to modify acute treatment strategy. Patient has 6.8% risk of progression to chronic migraine. Consider preventive therapy if not already prescribed."
            }
        elif score <= 5:
            return {
                "stage": "Poor",
                "description": "Poor treatment efficacy",
                "interpretation": "Current migraine treatment shows limited effectiveness. Recommend modifying acute treatment medication or dosing strategy. Patient has 4.4% risk of progression to chronic migraine. Consider preventive therapy."
            }
        elif score <= 7:
            return {
                "stage": "Moderate",
                "description": "Moderate treatment efficacy",
                "interpretation": "Current migraine treatment is moderately effective. May benefit from treatment optimization. Patient has 2.7% risk of progression to chronic migraine. Assess if further improvements are needed."
            }
        else:  # score == 8
            return {
                "stage": "Maximum",
                "description": "Maximum treatment efficacy",
                "interpretation": "Current migraine treatment is highly effective. Continue current treatment plan. Patient has only 1.9% risk of progression to chronic migraine. No changes recommended unless new issues arise."
            }


def calculate_mtoq_4(pain_free_2_hours: str, relief_24_hours: str,
                     able_to_plan: str, feel_in_control: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Mtoq4Calculator()
    return calculator.calculate(pain_free_2_hours, relief_24_hours,
                              able_to_plan, feel_in_control)