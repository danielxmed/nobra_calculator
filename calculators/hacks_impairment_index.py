"""
Hack's Impairment Index (HII) Calculator

Provides a quantitative assessment of alcohol-induced impairment in emergency department patients.

References:
- Hack JB, et al. Am J Drug Alcohol Abuse. 2014;40(2):111-7.
- Goldlust EJ, et al. Acad Emerg Med. 2017;24(10):1193-1203.
"""

from typing import Dict, Any


class HacksImpairmentIndexCalculator:
    """Calculator for Hack's Impairment Index (HII)"""
    
    def __init__(self):
        # Task parameters
        self.MIN_SCORE = 0
        self.MAX_SCORE_PER_TASK = 4
        self.TIME_TO_RESOLUTION_FACTOR = 0.0616
    
    def calculate(self, speech_mentation: int, gross_motor: int, eye_movement: int,
                  coordination: int, fine_motor: int, tasks_completed: int) -> Dict[str, Any]:
        """
        Calculates the HII score
        
        Args:
            speech_mentation: Speech quality and mentation score (0-4)
            gross_motor: Gross motor skills score (0-4)
            eye_movement: Eye movement score (0-4)
            coordination: Coordination with target pursuit score (0-4)
            fine_motor: Fine motor skills score (0-4)
            tasks_completed: Number of tasks completed (1-5)
            
        Returns:
            Dict with the score, interpretation, and estimated time to resolution
        """
        
        # Validate inputs
        self._validate_inputs(speech_mentation, gross_motor, eye_movement,
                            coordination, fine_motor, tasks_completed)
        
        # Calculate HII score
        result = self._calculate_hii(speech_mentation, gross_motor, eye_movement,
                                   coordination, fine_motor, tasks_completed)
        
        # Calculate estimated time to resolution
        time_to_resolution = self._calculate_time_to_resolution(result)
        
        # Get interpretation
        interpretation = self._get_interpretation(result)
        
        response = {
            "result": result,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
        
        # Add time to resolution if calculable
        if time_to_resolution is not None:
            response["estimated_time_to_resolution_hours"] = time_to_resolution
        
        return response
    
    def _validate_inputs(self, speech_mentation: int, gross_motor: int, eye_movement: int,
                        coordination: int, fine_motor: int, tasks_completed: int):
        """Validates input parameters"""
        
        # Validate each task score
        task_scores = {
            "speech_mentation": speech_mentation,
            "gross_motor": gross_motor,
            "eye_movement": eye_movement,
            "coordination": coordination,
            "fine_motor": fine_motor
        }
        
        for task_name, score in task_scores.items():
            if not isinstance(score, int):
                raise ValueError(f"{task_name} must be an integer")
            if score < self.MIN_SCORE or score > self.MAX_SCORE_PER_TASK:
                raise ValueError(f"{task_name} must be between {self.MIN_SCORE} and {self.MAX_SCORE_PER_TASK}")
        
        # Validate tasks completed
        if not isinstance(tasks_completed, int):
            raise ValueError("tasks_completed must be an integer")
        if tasks_completed < 1 or tasks_completed > 5:
            raise ValueError("tasks_completed must be between 1 and 5")
    
    def _calculate_hii(self, speech_mentation: int, gross_motor: int, eye_movement: int,
                      coordination: int, fine_motor: int, tasks_completed: int) -> float:
        """Calculates the HII score"""
        
        # Sum all subscores
        total_score = speech_mentation + gross_motor + eye_movement + coordination + fine_motor
        
        # Calculate maximum possible score based on tasks completed
        max_possible_score = tasks_completed * self.MAX_SCORE_PER_TASK
        
        # Calculate HII score
        hii_score = (total_score / max_possible_score) * max_possible_score
        
        # Round to 2 decimal places
        return round(hii_score, 2)
    
    def _calculate_time_to_resolution(self, hii_score: float) -> float:
        """
        Calculates estimated time to resolution in hours
        
        Args:
            hii_score: The calculated HII score
            
        Returns:
            Estimated time in hours or None if not calculable
        """
        
        if hii_score == 0:
            return 0.0
        
        # Formula: Time to resolution = HII Score / 0.0616
        time_hours = hii_score / self.TIME_TO_RESOLUTION_FACTOR
        
        # Round to 1 decimal place
        return round(time_hours, 1)
    
    def _get_interpretation(self, score: float) -> Dict[str, str]:
        """
        Determines the interpretation based on the score
        
        Args:
            score (float): HII score (0-15)
            
        Returns:
            Dict with interpretation
        """
        
        if score <= 2:
            return {
                "stage": "Minimal Impairment",
                "description": "Minimal to no clinically significant impairment",
                "interpretation": "Patient shows minimal signs of alcohol-induced impairment. Consider evaluation for discharge if other clinical criteria are met."
            }
        elif score <= 4:
            return {
                "stage": "Mild Impairment",
                "description": "Mild alcohol-induced impairment",
                "interpretation": "Patient shows mild impairment. Continue monitoring and reassess in 2 hours. Consider evaluation for potential alcohol withdrawal."
            }
        elif score <= 8:
            return {
                "stage": "Moderate Impairment",
                "description": "Moderate alcohol-induced impairment",
                "interpretation": "Patient shows moderate impairment. Not safe for discharge. Continue supportive care and reassess every 2 hours."
            }
        elif score <= 12:
            return {
                "stage": "Severe Impairment",
                "description": "Severe alcohol-induced impairment",
                "interpretation": "Patient shows severe impairment. Requires close monitoring and supportive care. Reassess frequently."
            }
        else:
            return {
                "stage": "Profound Impairment",
                "description": "Profound alcohol-induced impairment",
                "interpretation": "Patient shows profound impairment. May require intensive monitoring and airway protection. Consider ICU level care."
            }


def calculate_hacks_impairment_index(speech_mentation, gross_motor, eye_movement,
                                    coordination, fine_motor, tasks_completed) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = HacksImpairmentIndexCalculator()
    return calculator.calculate(speech_mentation, gross_motor, eye_movement,
                              coordination, fine_motor, tasks_completed)