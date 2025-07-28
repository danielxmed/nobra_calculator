"""
Adverse Childhood Experiences (ACE) Score Calculator

Screens for adverse childhood experiences to assess risk of health problems in adulthood.

Based on the seminal CDC-Kaiser Permanente Adverse Childhood Experiences Study (1995-1997).
The ACE Score is a simple count of 10 types of adverse childhood experiences that occurred
before age 18, including abuse, neglect, and household dysfunction.

References:
- Felitti VJ, Anda RF, Nordenberg D, et al. Relationship of childhood abuse and household 
  dysfunction to many of the leading causes of death in adults. The Adverse Childhood 
  Experiences (ACE) Study. Am J Prev Med. 1998;14(4):245-58.
"""

from typing import Dict, Any


class AceScoreCalculator:
    """Calculator for Adverse Childhood Experiences (ACE) Score"""
    
    def __init__(self):
        # ACE categories for validation
        self.ace_categories = [
            'emotional_abuse',
            'physical_abuse', 
            'sexual_abuse',
            'emotional_neglect',
            'physical_neglect',
            'parental_separation',
            'mother_treated_violently',
            'household_substance_abuse',
            'household_mental_illness',
            'household_member_incarcerated'
        ]
    
    def calculate(self, emotional_abuse: str, physical_abuse: str, sexual_abuse: str,
                 emotional_neglect: str, physical_neglect: str, parental_separation: str,
                 mother_treated_violently: str, household_substance_abuse: str,
                 household_mental_illness: str, household_member_incarcerated: str) -> Dict[str, Any]:
        """
        Calculates the ACE Score using the provided parameters
        
        Args:
            emotional_abuse (str): Emotional abuse during childhood ("yes" or "no")
            physical_abuse (str): Physical abuse during childhood ("yes" or "no")
            sexual_abuse (str): Sexual abuse during childhood ("yes" or "no")
            emotional_neglect (str): Emotional neglect during childhood ("yes" or "no")
            physical_neglect (str): Physical neglect during childhood ("yes" or "no")
            parental_separation (str): Parental separation or divorce ("yes" or "no")
            mother_treated_violently (str): Mother treated violently ("yes" or "no")
            household_substance_abuse (str): Household substance abuse ("yes" or "no")
            household_mental_illness (str): Household mental illness ("yes" or "no")
            household_member_incarcerated (str): Household member incarcerated ("yes" or "no")
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Collect all parameters
        parameters = {
            'emotional_abuse': emotional_abuse,
            'physical_abuse': physical_abuse,
            'sexual_abuse': sexual_abuse,
            'emotional_neglect': emotional_neglect,
            'physical_neglect': physical_neglect,
            'parental_separation': parental_separation,
            'mother_treated_violently': mother_treated_violently,
            'household_substance_abuse': household_substance_abuse,
            'household_mental_illness': household_mental_illness,
            'household_member_incarcerated': household_member_incarcerated
        }
        
        # Validate inputs
        self._validate_inputs(parameters)
        
        # Calculate ACE score
        ace_score = self._calculate_score(parameters)
        
        # Get interpretation
        interpretation = self._get_interpretation(ace_score)
        
        return {
            "result": ace_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, parameters: Dict[str, str]):
        """Validates input parameters"""
        
        # Check that all required parameters are present
        for category in self.ace_categories:
            if category not in parameters:
                raise ValueError(f"Missing required parameter: {category}")
            
            value = parameters[category]
            
            # Check parameter type
            if not isinstance(value, str):
                raise ValueError(f"Parameter {category} must be a string ('yes' or 'no')")
            
            # Check parameter value
            if value.lower() not in ['yes', 'no']:
                raise ValueError(f"Parameter {category} must be 'yes' or 'no', got: {value}")
    
    def _calculate_score(self, parameters: Dict[str, str]) -> int:
        """Calculates the ACE score by counting 'yes' responses"""
        
        score = 0
        for category in self.ace_categories:
            if parameters[category].lower() == 'yes':
                score += 1
        
        return score
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the ACE score
        
        Args:
            score (int): ACE score (0-10)
            
        Returns:
            Dict with interpretation details
        """
        
        if score == 0:
            return {
                "stage": "No ACEs",
                "description": "No adverse childhood experiences",
                "interpretation": "Low risk for health problems related to childhood trauma. This represents the lowest risk category, though it doesn't guarantee absence of all health risks."
            }
        elif 1 <= score <= 3:
            return {
                "stage": "Low to Moderate",
                "description": "1-3 adverse childhood experiences",
                "interpretation": "Moderate risk for health problems. While some increased risk exists, many people with scores in this range lead healthy lives. Protective factors and resilience can significantly mitigate risks."
            }
        elif 4 <= score <= 5:
            return {
                "stage": "High",
                "description": "4-5 adverse childhood experiences",
                "interpretation": "High risk for health problems including depression, substance abuse, and chronic diseases. Early intervention and trauma-informed care can be beneficial. Consider screening for mental health issues and providing appropriate support."
            }
        else:  # score >= 6
            return {
                "stage": "Very High",
                "description": "6 or more adverse childhood experiences",
                "interpretation": "Very high risk for serious health problems including mental illness, substance abuse, chronic diseases, and early death. Strong recommendation for trauma-informed care, mental health screening, and comprehensive support services. However, with appropriate interventions and support, positive outcomes are still possible."
            }


def calculate_ace_score(emotional_abuse: str, physical_abuse: str, sexual_abuse: str,
                       emotional_neglect: str, physical_neglect: str, parental_separation: str,
                       mother_treated_violently: str, household_substance_abuse: str,
                       household_mental_illness: str, household_member_incarcerated: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_ace_score pattern
    """
    calculator = AceScoreCalculator()
    return calculator.calculate(
        emotional_abuse=emotional_abuse,
        physical_abuse=physical_abuse,
        sexual_abuse=sexual_abuse,
        emotional_neglect=emotional_neglect,
        physical_neglect=physical_neglect,
        parental_separation=parental_separation,
        mother_treated_violently=mother_treated_violently,
        household_substance_abuse=household_substance_abuse,
        household_mental_illness=household_mental_illness,
        household_member_incarcerated=household_member_incarcerated
    )