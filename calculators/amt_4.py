"""
Abbreviated Mental Test 4 (AMT-4) Calculator

A shortened version of the Abbreviated Mental Test for rapid cognitive screening 
in elderly patients. Developed by Dr. David G. Swain.
"""

from typing import Dict, Any


class Amt4Calculator:
    """Calculator for Abbreviated Mental Test 4 (AMT-4)"""
    
    def __init__(self):
        # Score constants
        self.CORRECT_POINTS = 1
        self.INCORRECT_POINTS = 0
        self.MAX_SCORE = 4
        self.MIN_SCORE = 0
    
    def calculate(self, age: str, date_of_birth: str, place: str, year: str) -> Dict[str, Any]:
        """
        Calculates the AMT-4 score using the provided parameters
        
        Args:
            age (str): Whether patient correctly states their age ("correct" or "incorrect")
            date_of_birth (str): Whether patient correctly states their date of birth ("correct" or "incorrect") 
            place (str): Whether patient correctly identifies current place ("correct" or "incorrect")
            year (str): Whether patient correctly states current year ("correct" or "incorrect")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validations
        self._validate_inputs(age, date_of_birth, place, year)
        
        # Calculate score
        result = self._calculate_score(age, date_of_birth, place, year)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        return {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, age: str, date_of_birth: str, place: str, year: str):
        """Validates input parameters"""
        
        valid_responses = ["correct", "incorrect"]
        
        if not isinstance(age, str) or age not in valid_responses:
            raise ValueError("Age must be 'correct' or 'incorrect'")
        
        if not isinstance(date_of_birth, str) or date_of_birth not in valid_responses:
            raise ValueError("Date of birth must be 'correct' or 'incorrect'")
        
        if not isinstance(place, str) or place not in valid_responses:
            raise ValueError("Place must be 'correct' or 'incorrect'")
        
        if not isinstance(year, str) or year not in valid_responses:
            raise ValueError("Year must be 'correct' or 'incorrect'")
    
    def _calculate_score(self, age: str, date_of_birth: str, place: str, year: str) -> int:
        """Calculates the AMT-4 score by summing correct responses"""
        
        score = 0
        
        # Add 1 point for each correct response
        if age == "correct":
            score += self.CORRECT_POINTS
        
        if date_of_birth == "correct":
            score += self.CORRECT_POINTS
            
        if place == "correct":
            score += self.CORRECT_POINTS
            
        if year == "correct":
            score += self.CORRECT_POINTS
        
        return score
    
    def _get_interpretation(self, result: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the AMT-4 score
        
        Args:
            result (int): Calculated AMT-4 score (0-4)
            
        Returns:
            Dict with interpretation details
        """
        
        if result == 4:
            return {
                "stage": "Normal Cognition",
                "description": "Normal cognitive function",
                "interpretation": "Score of 4/4 suggests normal cognitive function. No cognitive impairment detected on this brief screening test."
            }
        else:
            return {
                "stage": "Cognitive Impairment",
                "description": "Significant cognitive impairment likely",
                "interpretation": "Score <4 suggests significant cognitive impairment. Further detailed cognitive assessment recommended. Consider underlying causes such as delirium, dementia, or depression."
            }


def calculate_amt_4(age: str, date_of_birth: str, place: str, year: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_amt_4 pattern
    """
    calculator = Amt4Calculator()
    return calculator.calculate(age, date_of_birth, place, year)