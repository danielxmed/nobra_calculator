"""
ABC Score for Massive Transfusion Calculator

Assessment of Blood Consumption (ABC) Score for predicting the necessity
for massive transfusion in trauma patients. Developed by Nunez et al.
"""

from typing import Dict, Any


class AbcScoreCalculator:
    """Calculator for ABC Score for Massive Transfusion"""
    
    def __init__(self):
        # Score constants
        self.POINTS_PER_CRITERION = 1
        self.MIN_SCORE = 0
        self.MAX_SCORE = 4
        self.HIGH_RISK_THRESHOLD = 2
    
    def calculate(self, penetrating_mechanism: str, systolic_bp_90_or_less: str, 
                  heart_rate_120_or_more: str, positive_fast: str) -> Dict[str, Any]:
        """
        Calculates the ABC Score using the provided parameters
        
        Args:
            penetrating_mechanism (str): Presence of penetrating mechanism ("yes" or "no")
            systolic_bp_90_or_less (str): Systolic BP ≤90 mmHg in ED ("yes" or "no")
            heart_rate_120_or_more (str): Heart rate ≥120 bpm in ED ("yes" or "no")
            positive_fast (str): Positive FAST ultrasound ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(penetrating_mechanism, systolic_bp_90_or_less, 
                             heart_rate_120_or_more, positive_fast)
        
        # Calculate score
        result = self._calculate_score(penetrating_mechanism, systolic_bp_90_or_less,
                                     heart_rate_120_or_more, positive_fast)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, penetrating_mechanism: str, systolic_bp_90_or_less: str,
                        heart_rate_120_or_more: str, positive_fast: str):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        if not isinstance(penetrating_mechanism, str) or penetrating_mechanism not in valid_responses:
            raise ValueError("Penetrating mechanism must be 'yes' or 'no'")
        
        if not isinstance(systolic_bp_90_or_less, str) or systolic_bp_90_or_less not in valid_responses:
            raise ValueError("Systolic BP ≤90 mmHg must be 'yes' or 'no'")
        
        if not isinstance(heart_rate_120_or_more, str) or heart_rate_120_or_more not in valid_responses:
            raise ValueError("Heart rate ≥120 bpm must be 'yes' or 'no'")
        
        if not isinstance(positive_fast, str) or positive_fast not in valid_responses:
            raise ValueError("Positive FAST must be 'yes' or 'no'")
    
    def _calculate_score(self, penetrating_mechanism: str, systolic_bp_90_or_less: str,
                        heart_rate_120_or_more: str, positive_fast: str) -> int:
        """Calculates the ABC Score by summing positive criteria"""
        
        score = 0
        
        # Add 1 point for each positive criterion
        if penetrating_mechanism == "yes":
            score += self.POINTS_PER_CRITERION
        
        if systolic_bp_90_or_less == "yes":
            score += self.POINTS_PER_CRITERION
            
        if heart_rate_120_or_more == "yes":
            score += self.POINTS_PER_CRITERION
            
        if positive_fast == "yes":
            score += self.POINTS_PER_CRITERION
        
        return score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ABC Score
        
        Args:
            result (int): Calculated ABC Score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if result < self.HIGH_RISK_THRESHOLD:
            return {
                "stage": "Low Risk",
                "description": "Less likely to require massive transfusion",
                "interpretation": "Patient is less likely to require massive transfusion, defined as ≥10 units of packed red blood cells in the first 24 hours of resuscitation. Standard trauma resuscitation protocols should be followed."
            }
        else:
            return {
                "stage": "High Risk", 
                "description": "Likely to require massive transfusion",
                "interpretation": "Patient is likely to require massive transfusion, defined as ≥10 units of packed red blood cells in the first 24 hours of resuscitation. Immediate activation of massive transfusion protocol (MTP) is recommended."
            }


def calculate_abc_score(penetrating_mechanism: str, systolic_bp_90_or_less: str,
                       heart_rate_120_or_more: str, positive_fast: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_abc_score pattern
    """
    calculator = AbcScoreCalculator()
    return calculator.calculate(penetrating_mechanism, systolic_bp_90_or_less,
                               heart_rate_120_or_more, positive_fast)