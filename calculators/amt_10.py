"""
Abbreviated Mental Test (AMT-10) Calculator

Assesses mental impairment in elderly patients through 10 questions evaluating 
various aspects of cognitive function including memory, attention, and orientation.

Reference: Hodkinson HM. Evaluation of a mental test score for assessment of mental 
impairment in the elderly. Age Ageing. 1972;1(4):233-238.
"""

from typing import Dict, Any


class Amt10Calculator:
    """Calculator for Abbreviated Mental Test (AMT-10)"""
    
    def __init__(self):
        self.TOTAL_QUESTIONS = 10
    
    def calculate(self, age_correct: str, time_correct: str, year_correct: str,
                  address_correct: str, recognition_correct: str, dob_correct: str,
                  wwi_correct: str, leader_correct: str, counting_correct: str,
                  recall_correct: str) -> Dict[str, Any]:
        """
        Calculates the AMT-10 score based on the 10 assessment questions
        
        Args:
            age_correct (str): Patient correctly states their age
            time_correct (str): Patient correctly states the time to nearest hour
            year_correct (str): Patient correctly states the current year
            address_correct (str): Patient correctly states their address/location
            recognition_correct (str): Patient correctly recognizes two people
            dob_correct (str): Patient correctly states their date of birth
            wwi_correct (str): Patient correctly states when WWI started
            leader_correct (str): Patient correctly names current leader
            counting_correct (str): Patient correctly counts backwards from 20 to 1
            recall_correct (str): Patient correctly recalls given address
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            age_correct, time_correct, year_correct, address_correct,
            recognition_correct, dob_correct, wwi_correct, leader_correct,
            counting_correct, recall_correct
        )
        
        # Calculate score
        score = self._calculate_score(
            age_correct, time_correct, year_correct, address_correct,
            recognition_correct, dob_correct, wwi_correct, leader_correct,
            counting_correct, recall_correct
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(score)
        
        return {
            "result": score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, *args):
        """Validates input parameters"""
        
        valid_values = ["correct", "incorrect"]
        
        for i, arg in enumerate(args, 1):
            if not isinstance(arg, str):
                raise ValueError(f"Question {i} response must be a string")
            
            if arg not in valid_values:
                raise ValueError(f"Question {i} response must be 'correct' or 'incorrect'")
    
    def _calculate_score(self, *responses) -> int:
        """Calculates the AMT-10 score by counting correct responses"""
        
        score = sum(1 for response in responses if response == "correct")
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the AMT-10 score
        
        Args:
            score (int): AMT-10 score (0-10)
            
        Returns:
            Dict with interpretation details
        """
        
        if score >= 8:
            return {
                "stage": "Normal",
                "description": "No cognitive impairment",
                "interpretation": "Score of 8-10 points indicates normal cognitive function. No significant cognitive impairment detected."
            }
        elif score >= 6:
            return {
                "stage": "Mild impairment",
                "description": "Mild cognitive impairment",
                "interpretation": "Score of 6-7 points suggests mild cognitive impairment. Further assessment may be warranted to determine underlying causes."
            }
        else:
            return {
                "stage": "Significant impairment",
                "description": "Significant cognitive impairment",
                "interpretation": "Score of 5 or less suggests significant cognitive impairment, including possible delirium or dementia. Further comprehensive assessment and workup are recommended."
            }


def calculate_amt_10(age_correct: str, time_correct: str, year_correct: str,
                     address_correct: str, recognition_correct: str, dob_correct: str,
                     wwi_correct: str, leader_correct: str, counting_correct: str,
                     recall_correct: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = Amt10Calculator()
    return calculator.calculate(
        age_correct, time_correct, year_correct, address_correct,
        recognition_correct, dob_correct, wwi_correct, leader_correct,
        counting_correct, recall_correct
    )