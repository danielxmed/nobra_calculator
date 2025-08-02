"""
HARK (Humiliation, Afraid, Rape, Kick) Calculator

Detects domestic abuse (intimate partner violence) in women in primary care settings 
using four simple yes/no questions about different types of IPV in the past year.

References:
- Sohal H, Eldridge S, Feder G. The sensitivity and specificity of four questions (HARK) 
  to identify intimate partner violence: a diagnostic accuracy study in general practice. 
  BMC Fam Pract. 2007 Oct 15;8:49.
"""

from typing import Dict, Any


class HarkCalculator:
    """Calculator for HARK (Humiliation, Afraid, Rape, Kick) screening tool"""
    
    def __init__(self):
        # Point values for each question (1 point for "yes", 0 for "no")
        self.question_points = {
            "yes": 1,
            "no": 0
        }
    
    def calculate(self, humiliation: str, afraid: str, rape: str, kick: str) -> Dict[str, Any]:
        """
        Calculates HARK score for intimate partner violence screening
        
        Args:
            humiliation (str): Humiliation or emotional abuse by partner ("yes" or "no")
            afraid (str): Being afraid of partner ("yes" or "no")
            rape (str): Rape or forced sexual activity by partner ("yes" or "no")
            kick (str): Physical violence by partner ("yes" or "no")
            
        Returns:
            Dict with HARK score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(humiliation, afraid, rape, kick)
        
        # Calculate total score (sum of "yes" responses)
        score = (
            self.question_points[humiliation] +
            self.question_points[afraid] +
            self.question_points[rape] +
            self.question_points[kick]
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        # Identify specific types of abuse reported
        abuse_types = self._identify_abuse_types(humiliation, afraid, rape, kick)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"],
            "abuse_types_identified": abuse_types,
            "requires_safety_assessment": score >= 1
        }
    
    def _validate_inputs(self, humiliation: str, afraid: str, rape: str, kick: str):
        """Validates input parameters"""
        
        valid_responses = ["yes", "no"]
        
        if humiliation not in valid_responses:
            raise ValueError(f"Humiliation response must be one of: {valid_responses}")
        
        if afraid not in valid_responses:
            raise ValueError(f"Afraid response must be one of: {valid_responses}")
        
        if rape not in valid_responses:
            raise ValueError(f"Rape response must be one of: {valid_responses}")
        
        if kick not in valid_responses:
            raise ValueError(f"Kick response must be one of: {valid_responses}")
    
    def _identify_abuse_types(self, humiliation: str, afraid: str, rape: str, kick: str) -> list:
        """
        Identifies specific types of abuse based on positive responses
        
        Args:
            humiliation, afraid, rape, kick: Response strings
            
        Returns:
            List of identified abuse types
        """
        
        abuse_types = []
        
        if humiliation == "yes":
            abuse_types.append("Emotional/Psychological Abuse")
        
        if afraid == "yes":
            abuse_types.append("Intimidation/Fear")
        
        if rape == "yes":
            abuse_types.append("Sexual Violence")
        
        if kick == "yes":
            abuse_types.append("Physical Violence")
        
        return abuse_types
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on HARK score
        
        Args:
            score (int): HARK score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "Negative Screen",
                "description": "Score 0",
                "interpretation": "Negative screen for intimate partner violence. No indication of IPV based on current screening. Continue to provide supportive care and maintain awareness for signs of abuse."
            }
        else:
            return {
                "stage": "Positive Screen",
                "description": "Score ≥1",
                "interpretation": "Positive screen for intimate partner violence. Patient has disclosed at least one form of IPV in the past year. Requires immediate safety assessment, documentation, resource provision, and follow-up care planning in accordance with institutional protocols."
            }


def calculate_hark(humiliation: str, afraid: str, rape: str, kick: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HarkCalculator()
    return calculator.calculate(humiliation, afraid, rape, kick)