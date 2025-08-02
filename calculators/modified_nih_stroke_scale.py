"""
Modified NIH Stroke Scale (mNIHSS) Calculator

Shortened, validated version of NIH Stroke Scale for quantifying stroke severity 
with improved interrater reliability. Removes redundant and poorly reliable items 
from the original NIHSS while maintaining validity.

References:
1. Meyer BC, et al. Stroke. 2002;33(2):328-33.
2. Meyer BC, Lyden PD. Int J Stroke. 2009;4(4):267-73.
3. Lyden P, et al. Stroke. 1994;25(11):2220-6.
"""

from typing import Dict, Any


class ModifiedNihStrokeScaleCalculator:
    """Calculator for Modified NIH Stroke Scale (mNIHSS)"""
    
    def __init__(self):
        # Scoring mappings for each parameter
        self.ORIENTATION_SCORES = {
            "both_correct": 0,
            "one_correct": 1,
            "zero_correct": 2
        }
        
        self.COMMAND_SCORES = {
            "both_correct": 0,
            "one_correct": 1,
            "zero_correct": 2
        }
        
        self.EYE_MOVEMENT_SCORES = {
            "normal": 0,
            "partial_gaze_palsy": 1,
            "total_gaze_palsy": 2
        }
        
        self.VISUAL_FIELD_SCORES = {
            "no_visual_loss": 0,
            "partial_hemianopia": 1,
            "complete_hemianopia": 2,
            "bilateral_hemianopia": 3
        }
        
        self.MOTOR_SCORES = {
            "no_drift": 0,
            "drift_before_10_seconds": 1,
            "falls_before_10_seconds": 2,
            "no_effort_against_gravity": 3,
            "no_movement": 4
        }
        
        self.SENSATION_SCORES = {
            "normal_no_sensory_loss": 0,
            "abnormal_sensory_loss": 1
        }
        
        self.LANGUAGE_SCORES = {
            "normal_no_aphasia": 0,
            "mild_aphasia": 1,
            "severe_aphasia": 2,
            "mute_global_aphasia": 3
        }
        
        self.EXTINCTION_SCORES = {
            "normal": 0,
            "mild": 1,
            "severe": 2
        }
    
    def calculate(self, orientation_questions: str, commands: str, 
                  horizontal_eye_movements: str, visual_fields: str,
                  left_arm_motor: str, right_arm_motor: str,
                  left_leg_motor: str, right_leg_motor: str,
                  sensation: str, language_aphasia: str,
                  extinction_neglect: str) -> Dict[str, Any]:
        """
        Calculates the Modified NIH Stroke Scale score
        
        Args:
            orientation_questions (str): Level of consciousness - orientation
            commands (str): Level of consciousness - commands
            horizontal_eye_movements (str): Horizontal extraocular movements
            visual_fields (str): Visual field testing
            left_arm_motor (str): Left arm motor assessment
            right_arm_motor (str): Right arm motor assessment
            left_leg_motor (str): Left leg motor assessment
            right_leg_motor (str): Right leg motor assessment
            sensation (str): Sensory function
            language_aphasia (str): Language and aphasia
            extinction_neglect (str): Extinction, inattention, neglect
            
        Returns:
            Dict with mNIHSS score and clinical interpretation
        """
        
        # Validate inputs
        self._validate_inputs(orientation_questions, commands, horizontal_eye_movements,
                             visual_fields, left_arm_motor, right_arm_motor,
                             left_leg_motor, right_leg_motor, sensation,
                             language_aphasia, extinction_neglect)
        
        # Calculate scores for each parameter
        orientation_score = self.ORIENTATION_SCORES[orientation_questions]
        command_score = self.COMMAND_SCORES[commands]
        eye_movement_score = self.EYE_MOVEMENT_SCORES[horizontal_eye_movements]
        visual_field_score = self.VISUAL_FIELD_SCORES[visual_fields]
        left_arm_score = self.MOTOR_SCORES[left_arm_motor]
        right_arm_score = self.MOTOR_SCORES[right_arm_motor]
        left_leg_score = self.MOTOR_SCORES[left_leg_motor]
        right_leg_score = self.MOTOR_SCORES[right_leg_motor]
        sensation_score = self.SENSATION_SCORES[sensation]
        language_score = self.LANGUAGE_SCORES[language_aphasia]
        extinction_score = self.EXTINCTION_SCORES[extinction_neglect]
        
        # Calculate total score
        total_score = (orientation_score + command_score + eye_movement_score +
                      visual_field_score + left_arm_score + right_arm_score +
                      left_leg_score + right_leg_score + sensation_score +
                      language_score + extinction_score)
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, orientation_questions: str, commands: str,
                        horizontal_eye_movements: str, visual_fields: str,
                        left_arm_motor: str, right_arm_motor: str,
                        left_leg_motor: str, right_leg_motor: str,
                        sensation: str, language_aphasia: str,
                        extinction_neglect: str):
        """Validates input parameters"""
        
        # Validate each parameter against valid options
        valid_orientation = list(self.ORIENTATION_SCORES.keys())
        if orientation_questions not in valid_orientation:
            raise ValueError(f"Orientation questions must be one of: {', '.join(valid_orientation)}")
        
        valid_commands = list(self.COMMAND_SCORES.keys())
        if commands not in valid_commands:
            raise ValueError(f"Commands must be one of: {', '.join(valid_commands)}")
        
        valid_eye_movements = list(self.EYE_MOVEMENT_SCORES.keys())
        if horizontal_eye_movements not in valid_eye_movements:
            raise ValueError(f"Horizontal eye movements must be one of: {', '.join(valid_eye_movements)}")
        
        valid_visual_fields = list(self.VISUAL_FIELD_SCORES.keys())
        if visual_fields not in valid_visual_fields:
            raise ValueError(f"Visual fields must be one of: {', '.join(valid_visual_fields)}")
        
        valid_motor = list(self.MOTOR_SCORES.keys())
        for limb, motor_value in [("Left arm", left_arm_motor), ("Right arm", right_arm_motor),
                                  ("Left leg", left_leg_motor), ("Right leg", right_leg_motor)]:
            if motor_value not in valid_motor:
                raise ValueError(f"{limb} motor must be one of: {', '.join(valid_motor)}")
        
        valid_sensation = list(self.SENSATION_SCORES.keys())
        if sensation not in valid_sensation:
            raise ValueError(f"Sensation must be one of: {', '.join(valid_sensation)}")
        
        valid_language = list(self.LANGUAGE_SCORES.keys())
        if language_aphasia not in valid_language:
            raise ValueError(f"Language/aphasia must be one of: {', '.join(valid_language)}")
        
        valid_extinction = list(self.EXTINCTION_SCORES.keys())
        if extinction_neglect not in valid_extinction:
            raise ValueError(f"Extinction/neglect must be one of: {', '.join(valid_extinction)}")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Provides clinical interpretation based on mNIHSS score
        
        Args:
            score (int): Total mNIHSS score
            
        Returns:
            Dict with interpretation details
        """
        
        if score <= 4:
            return {
                "stage": "Minor Stroke",
                "description": "Minimal neurological deficit",
                "interpretation": (f"mNIHSS Score {score}: Minor stroke with minimal neurological "
                                f"impairment. The patient demonstrates minor deficits that are unlikely "
                                f"to significantly impact daily activities. Good functional outcome is "
                                f"likely with appropriate medical management. Consider standard stroke "
                                f"protocols and monitor for potential improvement. Early mobilization "
                                f"and rehabilitation may accelerate recovery.")
            }
        elif score <= 15:
            return {
                "stage": "Moderate Stroke",
                "description": "Moderate neurological deficit",
                "interpretation": (f"mNIHSS Score {score}: Moderate stroke severity with noticeable "
                                f"neurological deficits that may impact daily functioning. Functional "
                                f"outcomes are variable and depend on specific deficits, patient factors, "
                                f"and quality of rehabilitation. Comprehensive stroke evaluation is "
                                f"indicated, including assessment for thrombolytic therapy if within "
                                f"time window. Multidisciplinary rehabilitation planning should be "
                                f"initiated early to optimize recovery potential.")
            }
        elif score <= 20:
            return {
                "stage": "Moderate-Severe Stroke",
                "description": "Moderate to severe neurological deficit",
                "interpretation": (f"mNIHSS Score {score}: Moderate to severe stroke with significant "
                                f"neurological impairment affecting multiple domains of function. "
                                f"Substantial rehabilitation will likely be needed to optimize functional "
                                f"outcomes. Consider intensive monitoring and aggressive stroke management. "
                                f"Early assessment by rehabilitation specialists is recommended. Patient "
                                f"and family education about expected recovery trajectory and long-term "
                                f"care needs should be provided.")
            }
        else:  # score > 20
            return {
                "stage": "Severe Stroke",
                "description": "Severe neurological deficit",
                "interpretation": (f"mNIHSS Score {score}: Severe stroke with major neurological deficits "
                                f"across multiple domains. Poor functional outcome is likely without "
                                f"intensive intervention and comprehensive rehabilitation. Consideration "
                                f"for advanced stroke therapies may be warranted if within treatment "
                                f"windows. Intensive monitoring for complications is essential. Early "
                                f"palliative care consultation may be appropriate to address goals of "
                                f"care and quality of life issues alongside aggressive medical management.")
            }


def calculate_modified_nih_stroke_scale(orientation_questions: str, commands: str,
                                       horizontal_eye_movements: str, visual_fields: str,
                                       left_arm_motor: str, right_arm_motor: str,
                                       left_leg_motor: str, right_leg_motor: str,
                                       sensation: str, language_aphasia: str,
                                       extinction_neglect: str) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = ModifiedNihStrokeScaleCalculator()
    return calculator.calculate(orientation_questions, commands, horizontal_eye_movements,
                               visual_fields, left_arm_motor, right_arm_motor,
                               left_leg_motor, right_leg_motor, sensation,
                               language_aphasia, extinction_neglect)