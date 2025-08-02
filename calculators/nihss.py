"""
NIH Stroke Scale/Score (NIHSS) Calculator

Quantifies stroke severity based on weighted evaluation findings.

References:
1. Brott T, Adams HP Jr, Olinger CP, Marler JR, Barsan WG, Biller J, et al. 
   Measurements of acute cerebral infarction: a clinical examination scale. 
   Stroke. 1989 Jul;20(7):864-70. doi: 10.1161/01.str.20.7.864.
2. Lyden P, Brott T, Tilley B, Welch KM, Mascha EJ, Levine S, et al. 
   Improved reliability of the NIH Stroke Scale using video training. 
   NINDS TPA Stroke Study Group. Stroke. 1994 Nov;25(11):2220-6. 
   doi: 10.1161/01.str.25.11.2220.
"""

from typing import Dict, Any


class NihssCalculator:
    """Calculator for NIH Stroke Scale/Score (NIHSS)"""
    
    def __init__(self):
        # Score ranges for interpretation
        self.score_ranges = [
            (0, 0, "No stroke symptoms", "No stroke symptoms present"),
            (1, 4, "Minor stroke", "Minor stroke symptoms that typically do not require urgent treatment but should be monitored closely"),
            (5, 15, "Moderate stroke", "Moderate stroke requiring urgent evaluation and treatment. May be eligible for thrombolytic therapy if within time window"),
            (16, 20, "Moderate to severe stroke", "Moderate to severe stroke requiring immediate intensive treatment and monitoring"),
            (21, 42, "Severe stroke", "Severe stroke with significant neurological impairment. Requires immediate intensive care and may have poor prognosis")
        ]
    
    def calculate(self, loc_responsiveness: int, loc_questions: int, loc_commands: int,
                  best_gaze: int, visual_fields: int, facial_palsy: int,
                  motor_arm_left: int, motor_arm_right: int,
                  motor_leg_left: int, motor_leg_right: int,
                  limb_ataxia: int, sensory: int, best_language: int,
                  dysarthria: int, extinction_inattention: int) -> Dict[str, Any]:
        """
        Calculates the NIH Stroke Scale score
        
        Args:
            loc_responsiveness (int): Level of consciousness (0-3)
            loc_questions (int): LOC questions - month and age (0-2)
            loc_commands (int): LOC commands - close eyes, make fist (0-2)
            best_gaze (int): Horizontal eye movement (0-2)
            visual_fields (int): Visual field testing (0-3)
            facial_palsy (int): Facial movement (0-3)
            motor_arm_left (int): Left arm motor drift (0-4)
            motor_arm_right (int): Right arm motor drift (0-4)
            motor_leg_left (int): Left leg motor drift (0-4)
            motor_leg_right (int): Right leg motor drift (0-4)
            limb_ataxia (int): Limb ataxia (0-2)
            sensory (int): Sensation (0-2)
            best_language (int): Language/aphasia (0-3)
            dysarthria (int): Speech clarity (0-2)
            extinction_inattention (int): Extinction and inattention/neglect (0-2)
            
        Returns:
            Dict with the NIHSS score and interpretation
        """
        
        # Validate inputs
        self._validate_inputs(
            loc_responsiveness, loc_questions, loc_commands,
            best_gaze, visual_fields, facial_palsy,
            motor_arm_left, motor_arm_right,
            motor_leg_left, motor_leg_right,
            limb_ataxia, sensory, best_language,
            dysarthria, extinction_inattention
        )
        
        # Calculate total NIHSS score
        total_score = (
            loc_responsiveness + loc_questions + loc_commands +
            best_gaze + visual_fields + facial_palsy +
            motor_arm_left + motor_arm_right +
            motor_leg_left + motor_leg_right +
            limb_ataxia + sensory + best_language +
            dysarthria + extinction_inattention
        )
        
        # Get interpretation
        interpretation = self._get_interpretation(total_score)
        
        return {
            "result": total_score,
            "unit": "points",
            "interpretation": interpretation["interpretation"],
            "stage": interpretation["stage"],
            "stage_description": interpretation["description"]
        }
    
    def _validate_inputs(self, loc_responsiveness: int, loc_questions: int, 
                        loc_commands: int, best_gaze: int, visual_fields: int, 
                        facial_palsy: int, motor_arm_left: int, motor_arm_right: int,
                        motor_leg_left: int, motor_leg_right: int,
                        limb_ataxia: int, sensory: int, best_language: int,
                        dysarthria: int, extinction_inattention: int):
        """Validates input parameters"""
        
        # Validate ranges for each parameter
        if not 0 <= loc_responsiveness <= 3:
            raise ValueError("Level of consciousness must be between 0 and 3")
            
        if not 0 <= loc_questions <= 2:
            raise ValueError("LOC questions must be between 0 and 2")
            
        if not 0 <= loc_commands <= 2:
            raise ValueError("LOC commands must be between 0 and 2")
            
        if not 0 <= best_gaze <= 2:
            raise ValueError("Best gaze must be between 0 and 2")
            
        if not 0 <= visual_fields <= 3:
            raise ValueError("Visual fields must be between 0 and 3")
            
        if not 0 <= facial_palsy <= 3:
            raise ValueError("Facial palsy must be between 0 and 3")
            
        if not 0 <= motor_arm_left <= 4:
            raise ValueError("Motor arm left must be between 0 and 4")
            
        if not 0 <= motor_arm_right <= 4:
            raise ValueError("Motor arm right must be between 0 and 4")
            
        if not 0 <= motor_leg_left <= 4:
            raise ValueError("Motor leg left must be between 0 and 4")
            
        if not 0 <= motor_leg_right <= 4:
            raise ValueError("Motor leg right must be between 0 and 4")
            
        if not 0 <= limb_ataxia <= 2:
            raise ValueError("Limb ataxia must be between 0 and 2")
            
        if not 0 <= sensory <= 2:
            raise ValueError("Sensory must be between 0 and 2")
            
        if not 0 <= best_language <= 3:
            raise ValueError("Best language must be between 0 and 3")
            
        if not 0 <= dysarthria <= 2:
            raise ValueError("Dysarthria must be between 0 and 2")
            
        if not 0 <= extinction_inattention <= 2:
            raise ValueError("Extinction and inattention must be between 0 and 2")
    
    def _get_interpretation(self, score: int) -> Dict[str, str]:
        """
        Determines the interpretation based on the NIHSS score
        
        Args:
            score (int): Total NIHSS score
            
        Returns:
            Dict with interpretation details
        """
        
        for min_score, max_score, stage, interpretation in self.score_ranges:
            if min_score <= score <= max_score:
                return {
                    "stage": stage,
                    "description": stage,
                    "interpretation": interpretation
                }
        
        # This should never happen with valid inputs
        return {
            "stage": "Unknown",
            "description": "Unknown severity",
            "interpretation": "Unable to classify stroke severity"
        }


def calculate_nihss(loc_responsiveness: int, loc_questions: int, loc_commands: int,
                   best_gaze: int, visual_fields: int, facial_palsy: int,
                   motor_arm_left: int, motor_arm_right: int,
                   motor_leg_left: int, motor_leg_right: int,
                   limb_ataxia: int, sensory: int, best_language: int,
                   dysarthria: int, extinction_inattention: int) -> Dict[str, Any]:
    """
    Convenience function for the dynamic loading system
    
    IMPORTANT: This function must follow the calculate_{score_id} pattern
    """
    calculator = NihssCalculator()
    return calculator.calculate(
        loc_responsiveness, loc_questions, loc_commands,
        best_gaze, visual_fields, facial_palsy,
        motor_arm_left, motor_arm_right,
        motor_leg_left, motor_leg_right,
        limb_ataxia, sensory, best_language,
        dysarthria, extinction_inattention
    )