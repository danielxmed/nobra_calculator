"""
4AT (4 A's Test) for Delirium Screening Calculator

Rapid clinical test for delirium detection in elderly patients.
Developed by Bellelli et al. (2014).
"""

from typing import Dict, Any


class FourAtCalculator:
    """Calculator for 4AT (4 A's Test) for Delirium Screening"""
    
    def calculate(self, alertness: str, amt4_errors: int, attention_months: str, 
                 acute_change: str) -> Dict[str, Any]:
        """
        Calculates the 4AT score for delirium detection
        
        Args:
            alertness: Alertness level ("normal", "altered")
            amt4_errors: Number of errors in AMT4 (0-4)
            attention_months: Performance on attention test 
                            ("7_or_more", "starts_less_than_7", "refuses_untestable")
            acute_change: Acute change or fluctuating course ("absent", "present")
            
        Returns:
            Dict with result and interpretation
        """
        
        # Validations
        self._validate_inputs(alertness, amt4_errors, attention_months, acute_change)
        
        # Calculate score for each component
        alertness_score = self._score_alertness(alertness)
        amt4_score = self._score_amt4(amt4_errors)
        attention_score = self._score_attention(attention_months)
        acute_change_score = self._score_acute_change(acute_change)
        
        # Sum total
        total_score = alertness_score + amt4_score + attention_score + acute_change_score
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, alertness: str, amt4_errors: int, attention_months: str, 
                        acute_change: str):
        """Validates input parameters"""
        
        valid_alertness = ["normal", "altered"]
        if alertness not in valid_alertness:
            raise ValueError(f"Alertness must be: {', '.join(valid_alertness)}")
        
        if not isinstance(amt4_errors, int) or amt4_errors < 0 or amt4_errors > 4:
            raise ValueError("AMT4 errors must be an integer between 0 and 4")
        
        valid_attention = ["7_or_more", "starts_less_than_7", "refuses_untestable"]
        if attention_months not in valid_attention:
            raise ValueError(f"Attention must be: {', '.join(valid_attention)}")
        
        valid_acute_change = ["absent", "present"]
        if acute_change not in valid_acute_change:
            raise ValueError(f"Acute change must be: {', '.join(valid_acute_change)}")
    
    def _score_alertness(self, alertness: str) -> int:
        """Scores alertness level"""
        if alertness == "normal":
            return 0
        elif alertness == "altered":
            return 4
        
    def _score_amt4(self, errors: int) -> int:
        """Scores errors in AMT4"""
        if errors == 0:
            return 0
        elif errors == 1:
            return 1
        elif errors >= 2:
            return 2
    
    def _score_attention(self, attention_months: str) -> int:
        """Scores attention test (months in reverse order)"""
        if attention_months == "7_or_more":
            return 0
        elif attention_months == "starts_less_than_7":
            return 1
        elif attention_months == "refuses_untestable":
            return 2
    
    def _score_acute_change(self, acute_change: str) -> int:
        """Scores acute change or fluctuating course"""
        if acute_change == "absent":
            return 0
        elif acute_change == "present":
            return 4
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            score: Total score (0-12)
            
        Returns:
            Dict with interpretation
        """
        
        if score == 0:
            return {
                "stage": "Negative",
                "description": "No delirium or moderate-severe cognitive impairment",
                "interpretation": "Result suggests absence of delirium and absence of moderate to severe cognitive impairment. Continue clinical monitoring as indicated."
            }
        elif 1 <= score <= 3:
            return {
                "stage": "Cognitive Impairment",
                "description": "Possible cognitive impairment, but not delirium",
                "interpretation": "Result suggests cognitive impairment but not delirium. Evaluate causes of cognitive impairment and consider more detailed neuropsychological assessment."
            }
        elif score >= 4:
            return {
                "stage": "Possible Delirium",
                "description": "Result suggests delirium",
                "interpretation": "Score ≥4 suggests possible delirium. This result is not diagnostic - the final diagnosis must be based on clinical judgment. Comprehensive mental assessment and investigation of reversible causes are recommended."
            }


def calculate_four_at(alertness: str, amt4_errors: int, attention_months: str, 
                     acute_change: str) -> Dict[str, Any]:
    """Convenience function for the dynamic loading system"""
    calculator = FourAtCalculator()
    return calculator.calculate(alertness, amt4_errors, attention_months, acute_change)
