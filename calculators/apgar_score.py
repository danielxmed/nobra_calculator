"""
APGAR Score Calculator

Assesses neonatal vitality at 1 and 5 minutes after birth using 5 clinical criteria:
Activity/muscle tone, Pulse, Grimace reflex, Appearance/color, and Respirations.

References:
1. Apgar V. A proposal for a new method of evaluation of the newborn infant. 
   Curr Res Anesth Analg. 1953;32(4):260-267.
2. Apgar V, Holaday DA, James LS, Weisbrot IM, Berrien C. Evaluation of the 
   newborn infant; second report. J Am Med Assoc. 1958;168(15):1985-1988.
3. American College of Obstetricians and Gynecologists Committee on Obstetric Practice. 
   The Apgar Score. Committee Opinion No. 644. Obstet Gynecol. 2015;126:e52-55.

Created by Dr. Virginia Apgar in 1952 at Columbia University.
"""

from typing import Dict, Any


class ApgarScoreCalculator:
    """Calculator for APGAR Score"""
    
    def __init__(self):
        # Scoring system for each component
        self.ACTIVITY_SCORES = {
            "active": 2,
            "some_flexion": 1, 
            "limp": 0
        }
        
        self.PULSE_SCORES = {
            ">=100_bpm": 2,
            "<100_bpm": 1,
            "absent": 0
        }
        
        self.GRIMACE_SCORES = {
            "sneeze_cough": 2,
            "grimace": 1,
            "none": 0
        }
        
        self.APPEARANCE_SCORES = {
            "all_pink": 2,
            "blue_extremities": 1,
            "blue_pale": 0
        }
        
        self.RESPIRATIONS_SCORES = {
            "good_crying": 2,
            "irregular_slow": 1,
            "absent": 0
        }

    def calculate(self, activity_muscle_tone: str, pulse: str, grimace_reflex: str, 
                 appearance_color: str, respirations: str) -> Dict[str, Any]:
        """
        Calculates the APGAR score using the provided parameters
        
        Args:
            activity_muscle_tone (str): Assessment of muscle tone and activity
            pulse (str): Heart rate assessment
            grimace_reflex (str): Reflex irritability/grimace response to stimulation
            appearance_color (str): Skin color assessment
            respirations (str): Respiratory effort assessment
            
        Returns:
            Dict with the result and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(activity_muscle_tone, pulse, grimace_reflex, 
                            appearance_color, respirations)
        
        # Calculate score for each component
        activity_score = self.ACTIVITY_SCORES[activity_muscle_tone]
        pulse_score = self.PULSE_SCORES[pulse]
        grimace_score = self.GRIMACE_SCORES[grimace_reflex]
        appearance_score = self.APPEARANCE_SCORES[appearance_color]
        respirations_score = self.RESPIRATIONS_SCORES[respirations]
        
        # Calculate total score
        total_score = (activity_score + pulse_score + grimace_score + 
                      appearance_score + respirations_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, activity_muscle_tone: str, pulse: str, grimace_reflex: str,
                        appearance_color: str, respirations: str):
        """Validates input parameters"""
        
        # Validate activity/muscle tone
        if activity_muscle_tone not in self.ACTIVITY_SCORES:
            raise ValueError(f"Invalid activity_muscle_tone: {activity_muscle_tone}. Must be one of: {list(self.ACTIVITY_SCORES.keys())}")
        
        # Validate pulse
        if pulse not in self.PULSE_SCORES:
            raise ValueError(f"Invalid pulse: {pulse}. Must be one of: {list(self.PULSE_SCORES.keys())}")
        
        # Validate grimace reflex
        if grimace_reflex not in self.GRIMACE_SCORES:
            raise ValueError(f"Invalid grimace_reflex: {grimace_reflex}. Must be one of: {list(self.GRIMACE_SCORES.keys())}")
        
        # Validate appearance/color
        if appearance_color not in self.APPEARANCE_SCORES:
            raise ValueError(f"Invalid appearance_color: {appearance_color}. Must be one of: {list(self.APPEARANCE_SCORES.keys())}")
        
        # Validate respirations
        if respirations not in self.RESPIRATIONS_SCORES:
            raise ValueError(f"Invalid respirations: {respirations}. Must be one of: {list(self.RESPIRATIONS_SCORES.keys())}")
    
    def _get_interpretation(self, total_score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the total score
        
        Args:
            total_score (int): Calculated APGAR score (0-10)
            
        Returns:
            Dict with interpretation details
        """
        
        if total_score >= 7:
            return {
                "stage": "Normal",
                "description": "Normal condition - reassuring",
                "interpretation": "Score 7-10 indicates good condition. The neonate is adapting well to extrauterine life. Scores of 8-9 are most common, as most newborns lose 1 point for blue extremities which is normal."
            }
        elif total_score >= 4:
            return {
                "stage": "Moderate Distress",
                "description": "Moderate distress - may need assistance",
                "interpretation": "Score 4-6 indicates moderate distress. The neonate may require some assistance with breathing or circulatory support. Close monitoring and possible intervention are warranted."
            }
        else:  # 0-3
            return {
                "stage": "Severe Distress",
                "description": "Severe distress - immediate medical attention required",
                "interpretation": "Score 0-3 indicates severe distress. The neonate requires immediate resuscitation and intensive medical intervention. This suggests significant compromise in the transition to extrauterine life."
            }


def calculate_apgar_score(activity_muscle_tone: str, pulse: str, grimace_reflex: str,
                         appearance_color: str, respirations: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_apgar_score pattern
    """
    calculator = ApgarScoreCalculator()
    return calculator.calculate(activity_muscle_tone, pulse, grimace_reflex, 
                               appearance_color, respirations)
