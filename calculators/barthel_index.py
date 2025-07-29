"""
Barthel Index for Activities of Daily Living (ADL) Calculator

Assesses functional independence in activities of daily living.

References:
1. Mahoney FI, Barthel DW. Functional evaluation: the Barthel Index. 
   Md State Med J. 1965 Feb;14:61-5.
"""

from typing import Dict, Any


class BarthelIndexCalculator:
    """Calculator for Barthel Index for Activities of Daily Living"""
    
    def __init__(self):
        # Define scoring for each activity
        self.scoring = {
            "feeding": {
                "independent": 10,
                "needs_help": 5,
                "unable": 0
            },
            "bathing": {
                "independent": 5,
                "unable": 0
            },
            "grooming": {
                "independent": 5,
                "unable": 0
            },
            "dressing": {
                "independent": 10,
                "needs_help": 5,
                "unable": 0
            },
            "bowel_control": {
                "continent": 10,
                "occasional_accident": 5,
                "incontinent": 0
            },
            "bladder_control": {
                "continent": 10,
                "occasional_accident": 5,
                "incontinent": 0
            },
            "toilet_use": {
                "independent": 10,
                "needs_help": 5,
                "unable": 0
            },
            "transfers": {
                "independent": 15,
                "needs_minor_help": 10,
                "needs_major_help": 5,
                "unable": 0
            },
            "mobility": {
                "independent": 15,
                "walks_with_help": 10,
                "wheelchair_independent": 5,
                "immobile": 0
            },
            "stairs": {
                "independent": 10,
                "needs_help": 5,
                "unable": 0
            }
        }
    
    def calculate(self, feeding: str, bathing: str, grooming: str, dressing: str,
                  bowel_control: str, bladder_control: str, toilet_use: str,
                  transfers: str, mobility: str, stairs: str) -> Dict[str, Any]:
        """
        Calculates Barthel Index score based on 10 activities of daily living
        
        Args:
            feeding (str): Feeding ability level
            bathing (str): Bathing ability level
            grooming (str): Grooming ability level
            dressing (str): Dressing ability level
            bowel_control (str): Bowel control level
            bladder_control (str): Bladder control level
            toilet_use (str): Toilet use ability level
            transfers (str): Transfer ability level
            mobility (str): Mobility level
            stairs (str): Stair climbing ability level
            
        Returns:
            Dict with Barthel Index score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(feeding, bathing, grooming, dressing,
                            bowel_control, bladder_control, toilet_use,
                            transfers, mobility, stairs)
        
        # Calculate total score
        total_score = 0
        
        total_score += self.scoring["feeding"][feeding]
        total_score += self.scoring["bathing"][bathing]
        total_score += self.scoring["grooming"][grooming]
        total_score += self.scoring["dressing"][dressing]
        total_score += self.scoring["bowel_control"][bowel_control]
        total_score += self.scoring["bladder_control"][bladder_control]
        total_score += self.scoring["toilet_use"][toilet_use]
        total_score += self.scoring["transfers"][transfers]
        total_score += self.scoring["mobility"][mobility]
        total_score += self.scoring["stairs"][stairs]
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, feeding: str, bathing: str, grooming: str, dressing: str,
                        bowel_control: str, bladder_control: str, toilet_use: str,
                        transfers: str, mobility: str, stairs: str):
        """Validates input parameters"""
        
        validations = {
            "feeding": ["independent", "needs_help", "unable"],
            "bathing": ["independent", "unable"],
            "grooming": ["independent", "unable"],
            "dressing": ["independent", "needs_help", "unable"],
            "bowel_control": ["continent", "occasional_accident", "incontinent"],
            "bladder_control": ["continent", "occasional_accident", "incontinent"],
            "toilet_use": ["independent", "needs_help", "unable"],
            "transfers": ["independent", "needs_minor_help", "needs_major_help", "unable"],
            "mobility": ["independent", "walks_with_help", "wheelchair_independent", "immobile"],
            "stairs": ["independent", "needs_help", "unable"]
        }
        
        inputs = {
            "feeding": feeding,
            "bathing": bathing,
            "grooming": grooming,
            "dressing": dressing,
            "bowel_control": bowel_control,
            "bladder_control": bladder_control,
            "toilet_use": toilet_use,
            "transfers": transfers,
            "mobility": mobility,
            "stairs": stairs
        }
        
        for activity, value in inputs.items():
            if value not in validations[activity]:
                raise ValueError(f"{activity} must be one of: {', '.join(validations[activity])}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines functional independence level based on Barthel score
        
        Args:
            score (int): Total Barthel Index score (0-100)
            
        Returns:
            Dict with interpretation details
        """
        
        if score >= 80:
            return {
                "stage": "Independent",
                "description": "Independent in daily activities",
                "interpretation": "Patient is functionally independent in activities of daily living. " +
                                "May require minimal assistance or supervision for complex tasks."
            }
        elif score >= 60:
            return {
                "stage": "Minimally Dependent",
                "description": "Minimal dependency",
                "interpretation": "Patient requires minimal assistance with daily activities. " +
                                "Generally able to live independently with some support."
            }
        elif score >= 40:
            return {
                "stage": "Partially Dependent",
                "description": "Partial dependency",
                "interpretation": "Patient requires moderate assistance with daily activities. " +
                                "May need regular caregiver support or assisted living arrangement."
            }
        elif score >= 20:
            return {
                "stage": "Very Dependent",
                "description": "Very dependent",
                "interpretation": "Patient requires substantial assistance with most daily activities. " +
                                "Likely needs full-time caregiver or institutional care."
            }
        else:
            return {
                "stage": "Totally Dependent",
                "description": "Total dependency",
                "interpretation": "Patient is totally dependent for all activities of daily living. " +
                                "Requires complete care and continuous supervision."
            }


def calculate_barthel_index(feeding: str, bathing: str, grooming: str, dressing: str,
                           bowel_control: str, bladder_control: str, toilet_use: str,
                           transfers: str, mobility: str, stairs: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = BarthelIndexCalculator()
    return calculator.calculate(feeding, bathing, grooming, dressing,
                              bowel_control, bladder_control, toilet_use,
                              transfers, mobility, stairs)